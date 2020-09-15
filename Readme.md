# FBXSDK Python Bindings

This repository contains scripts to build the FBXSDK Python Bindings for various platforms    
**Pre-built binaries are available on the [Releases page](https://gitlab.inria.fr/radili/fbxsdk_python/-/release://gitlab.inria.fr/radili/fbxsdk_python/-/releases)**

## Install

1. Download from the [Release Page](https://gitlab.inria.fr/radili/fbxsdk_python/-/releases) the archive `fbxsdkpy-cpPYTHONVERSION-PLATFORM` corresponding to your `PYTHONVERSION` and `PLATFORM`. `PYTHONVERSION` 35 corresponds to any 3.5 version of Python for example. The version of Python can be found with `python --version`
2. Extract it
3. Move the content of the extracted directory (not the directory itself) in either the `sites-package` directory or directly in your project directory. The path of the `sites-package` directory is generally present in the Python path, which can be obtained using `python -c "import sys; print(sys.path)"`

## Build 

The scripts can build the Python Bindings for Python versions >=3.5 on Windows and GNU/Linux and will only produce x64 binaries    
Don't hesitate to ask me if you need support of other versions, platforms or architectures     

### GNU/Linux

1. Install dependencies (for example with apt):
```
sudo apt install make gcc python3-dev zlib1g-dev libxml2-dev
```
2. Run the build script
```
./build.sh
```
3. Binaries are outputed to the `fbxsdkpy-cpPYTHONVERSION-gnu_linux_x64` directory. You can follow the Install instructions from step 3 with the files in this directory

### Windows

1. Execute the `build.bat` file, or run it as Administrator with "Right-Click > Run as Administrator" to skip the authorizations requests. Windows might prevent the execution of the script with a message "Windows protected your PC", to bypass it click "More Info", and then "Run Anyway"


2. Binaries are outputed to the `fbxsdkpy-cpPYTHONVERSION-win_x64` directory. You can follow the Install instructions from step 3 with the files in this directory


There is no dependencies, installing Visual Studio is not necessary, the script will download and install the needed building tools and remove them once it's done
