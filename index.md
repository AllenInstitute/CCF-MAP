# Atlas Primer

Digital 3D spatial atlases provide a framework for mapping large-scale multimodal datasets to a common reference space for visualization and analysis. Each atlas is comprised of an anatomical template, a coordinate space, regional parcellations of that template, and a set of taxonomic terms used to name the segmentations. Together, this set defines an **atlas** that can be used as a 3D reference for mapping volumetric and point cloud data. 

This resource provides example notebooks for programmatic access to the Allen Institute's atlases and their components for quantification, visualization, and other spatial applications. 

CCF data assets are hosted on a public S3 bucket on Amazon Web Services (AWS). All data assets described in this repository are available publicly with no account or login required for access. 

### Data releases

#### 2025 data release

The [Human and Mammalian Brain Atlas (HMBA) consortium](https://brain-map.org/consortia/hmba) has developed a standardized set of marmoset, macaque, and human atlases. The 2025 data release includes dorsal and ventral striatum, subthalamic nucleus, substantia nigra, and ventral tegmental area annotations from the **[Harmonized Ontology of Mammalian Brain Anatomy (HOMBA)](docs/HOMBA_ontology_v1.md)**. Note that the ontology spans the brain and spinal cord, but this data release only contains the basal ganglia and associated structure annotations. 

This release also contains the Allen Institute's mouse CCFv3 atlas (Wang et al. 2020) in which the whole brain has been parcellated into 1327 structures and named using the CCFv3 ontology.  

- **[Human](descriptions/human_ccf.md)**
- **[Macaque](descriptions/macaque_ccf.md)**
- **[Marmoset](descriptions/marmoset_ccf.md)**
- **[Mouse](descriptions/mouse_ccf.md)**

Each atlas also includes Neuroglancer instances for interactive visualization. 

**Note**: Future releases will be accessible through the [BrainGlobe Atlas API](https://brainglobe.info/documentation/brainglobe-atlasapi/index.html).

### Documentation and notebooks

- **[Getting started](notebooks/getting_started.ipynb)**: Introduction to atlas assets and data organization
- **[Navigating neuroglancer](docs/neuroglancer_primer.md)**: Brief introduction to navigating neuroglancer's interface for visualizing atlases
- **[Working with annotatation volumes](notebooks/working_with_annotation_volume.ipynb)**: Primer on using CCFs for querying voxels and accessing region masks

