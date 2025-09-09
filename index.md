# Common Coordinate Framework and Multi-Species Atlas Primer

The Human and Mammalian Brain Atlas (HMBA) consortium has developed a standardized set of mouse, marmoset, macaque, and human atlases. Each atlas is composed of a 3D template, a template space, regional segmentations of that template, and a set of taxonomic terms used to name the segmentations. Together, these define a **common coordinate framework (CCF)** that can be used as a 3D reference for mapping volumetric and spatial data. This repository contains examples for using the template for downstream applications. 

CCF data assets are hosted on a public S3 bucket on Amazon Web Services (AWS). All data assets described in this repository are available publicly with no account or login required for access. 

### Data releases

#### 2025 data release

The 2025 data release includes dorsal and ventral striatum, subthalamic nucleus, substantia nigra, and ventral tegmental area parcellations from the **[Harmonized Ontology of Mammalian Brain Anatomy (HOMBA)](docs/HOMBA_ontology_v1.md)**

- **[Human](descriptions/human_ccf.md)**
- **[Macaque](descriptions/macaque_ccf.md)**
- **[Marmoset](descriptions/marmoset_ccf.md)**

The data release also includes visualizations of each atlas as a neuroglancer instance. 

### Documentation and notebooks

- **[Getting started](notebooks/getting_started.ipynb)**: Introduction to atlas assets and data organization
- **[Navigating neuroglancer](docs/neuroglancer_primer.md)**: Brief introduction to navigating neuroglancer's interface for visualizing atlases
- **[Working with annotatation volumes](notebooks/working_with_annotation_volume.ipynb)**: Primer on using CCFs for querying voxels and accessing region masks

