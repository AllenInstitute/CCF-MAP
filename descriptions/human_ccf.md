## Developing Human Brain Atlas, version 2 (DHBAv2)

The Developing Human Brain Atlas version 2 (DHBAv2) is a three-dimensional (3D) common coordinate framework (CCF) and reference atlas that defines the spatial organization 
of cortical and subcortical structures in the adult human brain. This atlas modifies and expands the [Allen Human Reference atlas (2020)](https://community.brain-map.org/t/allen-human-reference-atlas-3d-2020-new/405). This atlas parcellates the [MNI152 ICBM2009b symmetric template](https://nist.mni.mcgill.ca/icbm-152-nonlinear-atlases-2009/), an averaged template from 152 young adult brains (mean age: 25.02 years, range: 18-44 years, 86 male, 66 female). The template has been sampled to 500 um<sup>3</sup> voxel resolution and symmetrized along the right-left axis. 

This atlas includes annotations for all subcortical and cortical structures using a unified ontology developed for cross-species comparisons, the [Harmonized Ontology of the Mammalian Brain Anatomy (HOMBA)](../docs/HOMBA_ontology_v1.md). HOMBA serves as a reference framework for aligning multimodal datasets, including transcriptomics and connectomics. The resource supports data registration, integration, and interpretation across individuals, laboratories, and species, and is designed to be iteratively refined with new data to capture individual variability and emerging anatomical detail as part of the BRAIN Initiative Cell Atlas Network.

The DHBAv2 whole brain atlas is split into two sets, gyral and Brodmann. The annotation sets share the same subcortical parcellations, but the cerebral cortex is parcellated into a gyral annotation set and a modified Brodmann area set using criteria and boundaries derived from [Ding et al. 2016](https://doi.org/10.1002/cne.24080)

###### [View human CCF neuroglancer visualization](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/human/HMBA-10X-Multiome-BG-HumanSlabROI/20250630/viewer_state/human_ccf_whole_brain.json)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| MNI ICBM2009b template                    | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/hmba-adult-human-icbm2009b-template/2025/template_500.nii.gz      |
| Gyral annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-human-hombagyral-annotation/2025/annotations_compressed_500.nii.gz                               |
| Brodmann annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-human-hombabrodmann-annotation/2025/annotations_compressed_500.nii.gz                               |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks