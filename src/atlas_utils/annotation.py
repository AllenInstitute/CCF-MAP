# Utilities for reading and writing nifti image volumes

import SimpleITK as sitk
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple, Union, List
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
        """Precompute terminology dfs with value and acronym indices"""
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

    def _coordinate_to_index(
        self,
        coordinate: Union[List, Tuple],
        *,
        physical_coordinate: bool,
        neuroglancer_coordinate: bool,
    ) -> Tuple[int, int, int]:
        """Convert an input coordinate to an image index (x, y, z)."""
        if physical_coordinate:
            point = [float(c) for c in coordinate]
            if neuroglancer_coordinate:
                query = [point[0], -point[2], -point[1]]
                import numpy as np
                continuous = np.array(self.img.TransformPhysicalPointToIndex(tuple(query)))
                continuous += np.array([0,6,-5])
                continuous[1] = -continuous[1]
            else:
                continuous = self.img.TransformPhysicalPointToContinuousIndex(point)
        else:
            continuous = [float(c) for c in coordinate]
        return tuple(int(round(c)) for c in continuous)

    def get_atlas_label(
        self,
        coordinate: List,
        physical_coordinate: bool = False,
        neuroglancer_coordinate: bool = False,
    ) -> Tuple[str, str]:
        """Return the atlas label (acronym, name) at a coordinate.

        Args:
            coordinate: Either voxel index (x, y, z) or physical (x, y, z) in image space.
            physical_coordinate: If True, interpret `coordinate` as a physical point
                and convert to an index using the image's transform.

        Returns:
            tuple[str, str]: (label_acronym, label_name) for the voxel's annotation value.
        """
        index = self._coordinate_to_index(
            coordinate,
            physical_coordinate=physical_coordinate,
            neuroglancer_coordinate=neuroglancer_coordinate,
        )
        size_x, size_y, size_z = self.img.GetSize()
        x, y, z = index
        if not (0 <= x < size_x and 0 <= y < size_y and 0 <= z < size_z):
            raise IndexError("Coordinate out of bounds for annotation volume")

        annotation_value = int(self.npy[z, y, x])
        row = self._by_value.loc[annotation_value]

        return str(row["abbreviation"]), str(row["name"])

    def label_csv(
        self,
        input_data: pd.DataFrame,
        physical_coordinate: bool = False,
        neuroglancer_coordinate: bool = False,
    ) -> pd.DataFrame:
        """Label input csv with labels from annotation.

        Args:
            input_data: DataFrame containing (x,y,z) coordinates for labeling.
        Returns:
            output_data: DataFrame with acronym and full name labels annotated for each coordinate.
        """
        required = {"x", "y", "z"}
        if not required.issubset(input_data.columns):
            missing = required - set(input_data.columns)
            raise ValueError(f"Missing required coordinate columns: {sorted(missing)}")

        coords = input_data[["x", "y", "z"]].to_numpy()
        indices = np.array(
            [
                self._coordinate_to_index(
                    coord,
                    physical_coordinate=physical_coordinate,
                    neuroglancer_coordinate=neuroglancer_coordinate,
                )
                for coord in coords
            ],
            dtype=np.int64,
        ).reshape(len(coords), 3)

        size_x, size_y, size_z = self.img.GetSize()
        in_bounds = (
            (indices[:, 0] >= 0)
            & (indices[:, 0] < size_x)
            & (indices[:, 1] >= 0)
            & (indices[:, 1] < size_y)
            & (indices[:, 2] >= 0)
            & (indices[:, 2] < size_z)
        )

        values = np.full(len(coords), -1, dtype=np.int64)
        if in_bounds.any():
            xs = indices[in_bounds, 0]
            ys = indices[in_bounds, 1]
            zs = indices[in_bounds, 2]
            values[in_bounds] = self.npy[zs, ys, xs]

        acronym = self._by_value["abbreviation"].reindex(values).fillna("").to_numpy()
        name = self._by_value["name"].reindex(values).fillna("").to_numpy()

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
            region_acronym: Abbreviation of the target region (e.g., 'DS', 'Ca').
            terminology_df: DataFrame indexed by 'abbreviation' with columns
                'annotation_value' and 'descendant_annotation_values'.
            save_filename: Output filename where the mask will be written.

        Returns:
            None. Writes the mask image to `save_filename`.
        """
        row = self._by_abbrev.loc[region_acronym]

        descendants = row["descendant_annotation_values"]
        if isinstance(descendants, str): 
            try:
                descendants = ast.literal_eval(descendants)
            except Exception:
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


def sitk_to_npy(image) -> np.ndarray:
    """Convert a SimpleITK image to a NumPy array with z, y, x axis order"""

    return sitk.GetArrayFromImage(image)

def npy_to_sitk(image_npy: np.ndarray):
    """Convert a NumPy array (z, y, x) to a SimpleITK image (x, y, z)."""

    return sitk.GetImageFromArray(image_npy)

def write_volume_to_file(volume: np.ndarray,
                         ref_img: sitk.Image,
                         output_filename: Union[str, Path]) -> None:
    """Write a NumPy volume (z, y, x) to disk via SimpleITK"""

    img = npy_to_sitk(volume)
    img.CopyInformation(ref_img)
    sitk.WriteImage(img, str(output_filename))
