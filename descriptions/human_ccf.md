## Human

The HOMBA Adult Human Basal Ganglia Atlas is a three-dimensional (3D) common coordinate framework (CCF) and reference atlas that defines the spatial organization 
of the basal ganglia of the adult human brain. This atlas uses the [HCP template](https://www.humanconnectome.org/study/hcp-young-adult/document/hcp-young-adult-2025-release) from the August 2025 release, which is an averaged template from 1071 young adult brains scanned at 3T, coregistered with the MNI152 nonlinear space, and resampled to 700 um<sup>3</sup> voxel resolution. This atlas includes annotations for basal ganglia including CaH, CaB, CaT, NACc, NACs, OT, GPe, GPi, VeP, PuR, PuM, PuC, PuCv, SN, VTA and STH. This atlas incorporates a unified ontology developed for cross-species comparisons, the [Harmonized Ontology of the Mammalian Brain Anatomy (HOMBA)](../docs/HOMBA_ontology_v1.md) and serves as a reference framework for aligning multimodal datasets, including transcriptomics and connectomics. The resource supports data registration, integration, and interpretation across individuals, laboratories, and species, and is designed to be iteratively refined with new data to capture individual variability and emerging anatomical detail as part of the BRAIN Initiative Cell Atlas Network.

###### [View human CCF neuroglancer visualization](https://neuroglancer-demo.appspot.com/#!s3://allen-hmba-releases/neuroglancer/human/HMBA-10X-Multiome-BG-HumanSlabROI/20250630/viewer_state/human_roi_pins_ccf.json)

| Data asset                      | S3 location                                                                                                                                            |
|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| HCP template                    | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/templates/hmba-adult-human-mri-template/2025/template_700.nii.gz      |
| Annotation                      | https://allen-atlas-assets.s3.us-west-2.amazonaws.com/annotation-sets/hmba-adult-human-homba-annotation/2025/annotations_compressed_700.nii.gz                               |

#### Related notebooks

- [Getting started](../notebooks/getting_started.ipynb) - Overview of atlases and file organization
- [Working with annotation volume](../notebooks/working_with_annotation_volume.ipynb) - Tutorial on using annotation volumes to query voxels and get region masks