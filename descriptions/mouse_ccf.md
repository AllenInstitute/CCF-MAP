## Mouse

Allen Mouse Brain Common Coordinate Framework (CCFv3, Wang et al, 2020) is a 3D reference space is an average brain at 10 um voxel resolution created from serial two-photon tomography images of 1,675 young adult C57Bl6/J mice. Using multimodal reference data, the entire brain parcellated directly in 3D, labeling every voxel with a brain structure spanning 43 isocortical areas and their layers, 314 subcortical gray matter structures, 81 fiber tracts, and 8 ventricular structures. The 2020 version (1) adds new annotations for layers of the Ammon’s horn (CA), main olfactory bulb (MOB) and minor modification of surrounding fiber tracts and (2) sets the atlas origin at the anterior commissure to align with HMBA atlases. 

###### [View CCFv3 neuroglancer visualization](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/mouse/mouse_CCFv3_viewer_state.json)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| CCFv3 template                  | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/allen-adult-mouse-stpt-template/2020/template_10.nii.gz      |
| Annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/allen-adult-mouse-stereotaxic-annotation/2020/annotations_compressed_10.nii.gz                              |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks
