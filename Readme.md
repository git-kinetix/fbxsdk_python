# FBXSDK Python Bindings

The Source Distribution (sdist) repository for the FBXSDK Python Bindings     
**Pre-compiled packages are available in PyNimation's package registry, they can be installed with pip (see PyNimation documentation)**    

## Build and install from source

```
pip --verbose install fbxsdkpy --extra-index-url https://gitlab.inria.fr/api/v4/projects/18692/packages/pypi/simple
```
This will download the sources from Autodesk website, build them, and install the built package

Alternatively, the bindings can be built and installed by cloning this repository and running `pip --verbose install .`

## Build Wheels

Wheels are Python package files, intended to be put in a Python package index (registry in GitLab) and installed with pip. When they include binaries like for this package, they need to be built for every combination of platform and Python version that is supported    
This package is supported on Windows and Linux and on Python versions >= 3.6    

### Linux

On linux, wheels are built inside the [manylinux](https://github.com/pypa/manylinux) environment, that ensures compatibility with the widest range of distributions    
To do so, a Dockerfile is available. All that is needed is to clone the repo, build an docker image and run it    

```
git clone https://gitlab.inria.fr/radili/fbxsdk_python
cd fbxsdk_python
docker build -t fbxsdkpy .
docker run -v $(pwd):/build fbxsdkpy
```

This will create wheels in the current directory as well as a `wheelhouse` directory    
**Only the wheels in wheelhouse are valid, the ones in the current directory are not yet patched with required libraries**

### Windows

Automation is more difficult on Windows. A virtual environment has to be created for every supported major version of Python (3.7, 3.8, etc.). Different Python versions can be obtained on the same machine using [miniconda](https://conda.io/miniconda.html) or [pyenv-win](https://github.com/pyenv-win/pyenv-win)    
First, clone the repo

```
git clone https://gitlab.inria.fr/radili/fbxsdk_python
cd fbxsdk_python
```

Then in every environment, build the wheel    

```
# ensure python version is the right one
python --version

python -m pip wheel --verbose .
```

This will create a wheel for this python version

## Create sdist

The sdist (or source distribution) is the package file used to build wheels from source, it is used by pip to build a package when no wheels are found matching the platform and Python version. It should be uploaded to the Python package index as well    
To create a sdist for this package, sip is needed

```
git clone https://gitlab.inria.fr/radili/fbxsdk_python
cd fbxsdk_python

pip install sip
sip-sdist
```

This will create a tar archive with the source distribution that can be upload the same way as wheels

## Upload wheels and sdist to GitLab

In GitLab, a package registry can be enabled for every repo, to hold Python packages    
To upload wheels and sdist to it, use twine like so:

on Linux

```
TWINE_PASSWORD=<YOUR_GITLAB_TOKEN> TWINE_USERNAME=__token__ python -m twine upload --repository-url https://gitlab.inria.fr/api/v4/projects/<project_id>/packages/pypi *.whl
```

or on Windows

```
set TWINE_PASSWORD=<YOUR_GITLAB_TOKEN>
set TWINE_USERNAME=__token__
python -m twine upload --repository-url https://gitlab.inria.fr/api/v4/projects/<project_id>/packages/pypi *.whl
```

Replacing `<YOUR_GITLAB_TOKEN>` with your global gitlab token, `<project_id>` with the id of the project you want to upload a package to, and `*.whl` with wheels or sdist files you want to upload
More documentation [here](https://gitlab.inria.fr/help/user/packages/pypi_repository/index)

## Troubleshooting

- `--verbose` is recommended to get the output of the compiler in case of an error. Also, as compilation can take several minutes, `pip` might otherwise seem unresponsive  
- The latest version of pip is always a plus: `pip install --upgrade pip`
- On outdated Windows versions, cURL is not available, in this case install it from [https://curl.se/](https://curl.se/)
- On Windows, Build Tools are required for compiling, and C++ Redistributables for runtime, they are available individually on Microsoft's website at these links: [build tools](https://aka.ms/vs/16/release/vs_buildtools.exe), [redistributables](https://aka.ms/vs/16/release/vc_redist.x64.exe), or with Visual Studio
- On Windows, the installers from Autodesk trigger Permission Requests, if left unanswered they will timeout, the installation will continue without the required files and quietly fail. A solution to run the installation unattended is to do it from an Administrator command line
- For more on runtime errors, see [PyNimation documentation](https://lhoyet.gitlabpages.inria.fr/pynimation/static/overview/troubleshooting.html#importerror-dll-load-failed-while-importing-fbx)

## Detailed Build Process

- `pip install .` or `pip wheel .` reads `pyproject.toml` and installs build dependencies in `[build-system]` `requires`
- `project.py` is run to create a new build project
- This script runs `pull_reqs.sh` on Linux or `pull_reqs.bat` on Windows, which will
  - create a `build` directory with subdirectories for different installations
  - read the urls for the fbxsdk and fbxpy installation executables for Linux in `reqs.txt` and for Windows in `reqs_win.txt`
  - download the installation executables with cURL
  - run them, saying they should install their files in `build`
  - patch the sip bindings in `build/fbxpy/sip` with the `patch` file, to fix compilation errors, and add needed functions that are not initially present
- `builder.py` will be run to create a new Builder, with the compile options given in `pyproject.toml`
- Sip generates the python extension cpp files from sip files
- They are compiled and linked with the static libfbxsdk
- Everything is put into a wheel
- auditwheel patches in the required libraries when in manylinux
