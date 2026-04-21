## HMBA Adult Cynomolgus Macaque Brain Atlas

This three-dimensional brain reference atlas for macaque basal ganglia was created based on the Mac25Cyno template, an averaged MRI template from 25 cynomolgus macaque (*M. cynomolgus*) individual brains resampled to 160 um<sup>3</sup> voxel resolution. Brain regions were annotated on a 2D histology series using the terms set from the Harmonized Ontology of Mammalian Brain Anatomy (HOMBA), a unified cross-species ontology. 2D labeled histology sections were registered to the Mac25Cyno template and labels were transferred to 3D space. This atlas enables mapping of samples and integration of multimodal data within and across species. This reference atlas is a foundational element for coordinated studies of basal ganglia in the BICAN consortium. 

###### [View cynomolgus macaque CCF neuroglancer visualization](https://allen.neuroglass.io/glances/069d98a0-ada9-753f-8000-5e20a520b335)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Mac25 Cyno template           | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/hmba-adult-cynomolgousmacaque-mri-template/2026/template_160.nii.gz      |
| HOMBA BG Annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-cynomolgousmacaque-homba-annotation/2026/annotations_compressed_160.nii.gz                               |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks