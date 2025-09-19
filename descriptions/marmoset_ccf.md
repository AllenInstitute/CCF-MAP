## Marmoset

This atlas uses the marmoset RIKEN25 template, which is an averaged template from 25 *C. jacchus* individual brains resampled to 70 um<sup>3</sup> voxel resolution. This template is overlaid with basal ganglia **annotations** as defined by the [HOMBA](../docs/HOMBA_ontology_v1.md) **terminology**.  

###### [View marmoset CCF neuroglancer visualization](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/marmoset/HMBA-10X-Multiome-BG-MarmosetSlabROI/20250630/viewer_states/marmoset_roi_pins_ccf.json)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| RIKEN25 template                | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/hmba-adult-marmoset-mri-template/2025/template_70.nii.gz      |
| Annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-marmoset-homba-annotation/2025/annotations_compressed_70.nii.gz                               |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks