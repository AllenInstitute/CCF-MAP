## Human CCF

This atlas uses the [HCP template](https://www.humanconnectome.org/study/hcp-young-adult/document/hcp-young-adult-2025-release) from the August 2025 release, which is an averaged template from 1071 young adult brains scanned at 3T. This template has been resampled to 700 um<sup>3</sup> voxel resolution. This template is overlaid with basal ganglia **annotations** as defined by the [HOMBA](../docs/HOMBA_ontology_v1.md) **terminology**. 

#### [View human CCF](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/human/HMBA-10X-Multiome-BG-HumanSlabROI/20250630/viewer_state/human_roi_pins_ccf.json)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| HCP template                    | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/hmba-adult-human-mri-template/2025/template_700.nii.gz      |
| Annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-human-homba-annotation/20250829/annotations_compressed_700.nii.gz                               |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks