## Macaque

This three-dimensional brain reference atlas for macaque basal ganglia was created based on the annotation of BG structures on the Mac25Rhesus template, an 
averaged MRI template from 25 M. mulatta individual brains resampled to 160 um<sup>3</sup> voxel resolution. Brain regions were annotated using the terms set from the 
Harmonized Ontology of Mammalian Brain Anatomy (HOMBA), a unified cross-species ontology. The atlas also includes selected published subcortical parcellations to aid in 
comparing across parcellation schemes. This atlas enables mapping of samples and integration of multimodal data within and across species. This reference atlas is a 
foundational element for coordinated studies of basal ganglia in the BICAN consortium

###### [View macaque CCF neuroglancer visualization](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/macaque/HMBA-10X-Multiome-BG-MacaqueSlabROI/20250630/viewer_state/macaque_ccf.json)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Mac25 Rhesus template           | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/hmba-adult-macaque-mri-template/2025/template_160.nii.gz      |
| Annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-macaque-homba-annotation/2025/annotations_compressed_160.nii.gz                               |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks