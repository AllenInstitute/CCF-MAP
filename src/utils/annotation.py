# Utilities for reading and writing nifti image volumes

import SimpleITK as sitk
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple, Union
import ast

@dataclass
class Annotation():
    """Container for an annotation volume in both SimpleITK and NumPy forms.

    Holds a SimpleITK image (`img`) and its NumPy representation (`npy`).
    """
    img: sitk.Image
    npy: np.ndarray 
    terminology: pd.DataFrame
    _by_value: pd.DataFrame = field(init=False, repr=False)
    _by_abbrev: pd.DataFrame = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Precompute indexed views for fast lookups."""
        self._by_value = self.terminology.set_index("annotation_value", drop=True)
        self._by_abbrev = self.terminology.set_index("abbreviation", drop=True)

    @staticmethod
    def from_file(image_volume_filename: Path,
                  terminology_filename: Path) -> "Annotation":
        """Load an annotation image from a file.

        Args:
            image_volume_filename: Path to the image volume file readable by SimpleITK.
            terminology_filename: Path to terminology lookup table

        Returns:
            Annotation: Instance with `img` as the SimpleITK image and `npy` as
            the NumPy array (axes permuted to z, y, x).
        """
        img = sitk.ReadImage(str(image_volume_filename))
        npy = sitk_to_npy(img)
        terminology = pd.read_csv(str(terminology_filename))

        return Annotation(img=img, npy=npy, terminology=terminology)
    
    def get_atlas_label(self,
                        coordinate: Tuple[Union[int, float], Union[int, float], Union[int, float]],
                        physical_coordinate: bool = False
                        ) -> Tuple[str, str]:
        """Return the atlas label (acronym, name) at a coordinate.

        Args:
            coordinate: Either voxel index (x, y, z) or physical (x, y, z) in image space.
            physical_coordinate: If True, interpret `coordinate` as a physical point
                and convert to an index using the image's transform.

        Returns:
            tuple[str, str]: (label_acronym, label_name) for the voxel's annotation value.
        """

        if physical_coordinate is True:
            coordinate_idx = self.img.TransformPhysicalPointToIndex(tuple(float(n) for n in coordinate))
            x, y, z = (int(coordinate_idx[0]), int(coordinate_idx[1]), int(coordinate_idx[2]))
        else:
            x, y, z = (int(coordinate[0]), int(coordinate[1]), int(coordinate[2]))

        # Convert to NumPy indexing order z, y, x and bounds-check
        zyx = (z, y, x)
        sz, sy, sx = self.npy.shape
        if not (0 <= zyx[0] < sz and 0 <= zyx[1] < sy and 0 <= zyx[2] < sx):
            raise IndexError("Coordinate out of bounds for annotation volume")

        annotation_value = int(self.npy[zyx])
        row = self._by_value.loc[annotation_value]

        label_name = row["name"]
        label_acronym = row["abbreviation"]

        return str(label_acronym), str(label_name)
    
    def label_csv(self,
                  input_data: pd.DataFrame,
                  physical_coordinate: bool = False) -> pd.DataFrame:

        """Label input csv with labels from annotation
        
        Args: 
            input_data: DataFrame containing (x,y,z) coordinates for labeling
        Returns:
            output_data: DataFrame with acronym and full name labels annotated for each coordinate"""

        # Validate input columns
        required = {"x", "y", "z"}
        if not required.issubset(input_data.columns):
            missing = required - set(input_data.columns)
            raise ValueError(f"Missing required coordinate columns: {sorted(missing)}")

        coords = input_data[["x", "y", "z"]].to_numpy()

        if physical_coordinate is True:
            idx = self._physical_to_index_numpy(coords)
        else:
            idx = coords.astype(np.int64, copy=False)

        # Split x,y,z and compute in-bounds mask
        x = idx[:, 0].astype(np.int64, copy=False)
        y = idx[:, 1].astype(np.int64, copy=False)
        z = idx[:, 2].astype(np.int64, copy=False)
        sz, sy, sx = self.npy.shape
        in_bounds = (z >= 0) & (y >= 0) & (x >= 0) & (z < sz) & (y < sy) & (x < sx)

        vals = np.full(len(input_data), -1, dtype=np.int64)
        if in_bounds.any():
            vals[in_bounds] = self.npy[z[in_bounds], y[in_bounds], x[in_bounds]].astype(np.int64, copy=False)

        # Get labels from _by_value df
        acronym = self._by_value["abbreviation"]
        name = self._by_value["name"]
        acronym = acronym.reindex(vals).fillna("").to_numpy()
        name = name.reindex(vals).fillna("").to_numpy()

        out = input_data.copy()
        out["abbreviation"] = acronym
        out["name"] = name
        out.loc[~in_bounds, ["abbreviation", "name"]] = ["", ""]
        return out

    def create_region_mask(self,
                           region_acronym: str,
                           save_filename: Path) -> None:
        """Create and save a binary/region mask for a region and its descendants.

        Builds a mask containing all voxels whose annotation value is either the
        region's own value or any of its descendants as provided by the terminology.
        The saved image preserves the spatial metadata of the original annotation.

        Args:
            region_acronym: Abbreviation of the target region (e.g., 'VISp').
            terminology_df: DataFrame indexed by 'abbreviation' with columns
                'annotation_value' and 'descendant_annotation_values' (iterable of ints).
            save_filename: Output filename where the mask will be written.

        Returns:
            None. Writes the mask image to `save_filename`.
        """
        row = self._by_abbrev.loc[region_acronym]

        descendants = row["descendant_annotation_values"]
        # Parse descendants if stored as a string
        if isinstance(descendants, str):
            try:
                descendants = ast.literal_eval(descendants)
            except Exception:
                # Fallback: split on common delimiters
                if "," in descendants:
                    descendants = [int(x) for x in descendants.split(",") if x.strip()]
                else:
                    descendants = [int(descendants)] if descendants.strip() else []

        descendants = np.asarray(list(descendants), dtype=self.npy.dtype)
        annotation_value = int(row["annotation_value"])

        bool_mask = np.isin(self.npy, descendants)
        region_mask = np.where(bool_mask, annotation_value, 0).astype(self.npy.dtype, copy=False)

        save_filename_str = str(Path(save_filename).resolve())
        write_volume_to_file(region_mask, self.img, save_filename_str)

    def _physical_to_index_numpy(self, points: np.ndarray) -> np.ndarray:
        """Vectorized physical (x,y,z) -> index (x,y,z) conversion.

        Args:
            points: Array of shape (N, 3) with physical coordinates.

        Returns:
            np.ndarray: Array of shape (N, 3) with integer voxel indices (x, y, z).
        """
        origin = np.asarray(self.img.GetOrigin(), dtype=np.float64)
        spacing = np.asarray(self.img.GetSpacing(), dtype=np.float64)
        direction = np.asarray(self.img.GetDirection(), dtype=np.float64).reshape(3, 3)

        # Compute inverse mapping: idx = inv(direction) @ ((pt - origin) / spacing)
        inv_dir = np.linalg.inv(direction)
        pts = np.asarray(points, dtype=np.float64)
        scaled = (pts - origin) / spacing
        idx = (inv_dir @ scaled.T).T
        return np.rint(idx).astype(np.int64, copy=False)



def sitk_to_npy(image) -> np.ndarray:
    """Convert a SimpleITK image to a NumPy array with z, y, x axis order.

    SimpleITK uses x, y, z ordering; NumPy arrays of volumes are typically z, y, x.
    This function permutes axes accordingly before conversion.

    Args:
        image: Input SimpleITK image.

    Returns:
        np.ndarray: Volume data with shape (z, y, x).
    """

    return sitk.GetArrayFromImage(image)

def npy_to_sitk(image_npy: np.ndarray):
    """Convert a NumPy array (z, y, x) to a SimpleITK image (x, y, z).

    Args:
        image_npy: NumPy array representing a volume with shape (z, y, x).

    Returns:
        sitk.Image: SimpleITK image with axes permuted back to x, y, z.
    """
    return sitk.GetImageFromArray(image_npy)

def write_volume_to_file(volume: np.ndarray,
                         ref_img: sitk.Image,
                         output_filename: Union[str, Path]) -> None:
    """Write a NumPy volume (z, y, x) to disk via SimpleITK.

    Args:
        volume: NumPy array volume with shape (z, y, x).
        ref_img: Reference image used to get orientation, direction, spacing data.
        output_filename: Destination filename accepted by SimpleITK.

    Returns:
        None. Writes the image to `output_filename`.
    """
    img = npy_to_sitk(volume)
    img.CopyInformation(ref_img)
    sitk.WriteImage(img, str(output_filename))
