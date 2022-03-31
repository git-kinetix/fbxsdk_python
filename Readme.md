# FBXSDK Python Bindings

The Source Distribution (sdist) repository for the FBXSDK Python Bindings     
**A source packages can be built and installed with pip (see Install)**    

## Install

```
pip --verbose install fbxsdkpy --extra-index-url https://gitlab.inria.fr/api/v4/projects/18692/packages/pypi/simple
```
This will download the sources from Autodesk website, build them, and install the built package

## Manual Build

Alternatively, the bindings can be built and installed by cloning this repository and running `pip --verbose install .`

## Troubleshooting

- `--verbose` is recommended to get the output of the compiler in case of an error. Also, as compilation can take several minutes, `pip` might otherwise seem unresponsive  
- On outdated Windows versions, curl is not available, in this case install it from [https://curl.se/](https://curl.se/)
- On Windows, Build Tools are required for compiling, and C++ Redistributables for runtime, they are available individually on Microsoft's website, or with Visual Studio
- On Windows, the installers from Autodesk trigger Permission Requests, if left unanswered they will timeout, the installation will continue without the required files and quietly fail. A solution to run the installation unattended is to do it from an Administrator command line
- For more on runtime errors, see [PyNimation documentation](https://lhoyet.gitlabpages.inria.fr/pynimation/static/overview/troubleshooting.html#importerror-dll-load-failed-while-importing-fbx)
