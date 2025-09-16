# Common Coordinate Framework and Multi-Species Atlas Primer (CCF-MAP)

This repository contains notebooks for accessing and using common coordinate frameworks (CCF) for mouse, marmoset, macaque, and human data.

### CCF-MAP reference and tutorials

[JupyterBook references and tutorials](https://alleninstitute.github.io/CCF-MAP/intro.html) for downloading volumes, using CCFs in research, and for visualization. 

### Setup and installation

A clean conda environment is recommended for installation. For instructions on setting up conda, see [conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-python)

To install tools for interacting with atlas assets, run

```
pip install -e .
```

For all dependencies associated with notebooks, run 

```
pip install "ccf_map[notebooks] @ git+https://github.com/alleninstitute/CCF-MAP.git"
```

## How to contribute 
[JupyterBook Contribution Guide](docs/jupyterbook/README.md)

Note: for scientific questions regarding the data this repository is accessing, please use the [Allen Institute's community forum](https://community.brain-map.org/).

If you are having an issue with the code or notebooks not running properly, please open an issue on this Github repository. However, please see below.

### Level of support

We are not currently supporting this code, but simply releasing it to the community **AS IS** but are not able to provide any guarantees of support. The community is welcome to submit issues, but you should not expect an active response. 
