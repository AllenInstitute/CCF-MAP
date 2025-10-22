## Marmoset

The HOMBA Adult Marmoset Basal Ganglia Atlas is a three-dimensional brain reference atlas based on the RIKEN25v1 MRI-derived template, based on an average of 25 C. jacchus brains resampled to 70 um<sup>3</sup> voxel resolution. It provides detailed parcellations of the basal ganglia and associated subcortical structures, annotated using the [Harmonized Ontology of Mammalian Brain Anatomy (HOMBA)](../docs/HOMBA_ontology_v1.md) 
unified ontology that enables cross-species alignment and interpretation. The atlas also includes selected published subcortical parcellations to aid in comparing across parcellation schemes. As a foundational reference resource for the BICAN consortium, this atlas facilitates registration, integration, and comparative analysis of multimodal datasets across marmoset, macaque, and human brains. It is designed to be updated and refined with new datasets, ensuring its continued relevance for exploring structural homologies and functional relationships across species.

###### [View marmoset CCF neuroglancer visualization](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/marmoset/HMBA-10X-Multiome-BG-MarmosetSlabROI/20250630/viewer_states/marmoset_ccf.json)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| RIKEN25 template                | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/hmba-adult-marmoset-mri-template/2025/template_70.nii.gz      |
| Annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-marmoset-homba-annotation/2025/annotations_compressed_70.nii.gz                               |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks