# FBXSDK Python Bindings

This repository contains scripts to create a Source Distribution (sdist) for the FBXSDK Python Bindings and build wheels (package with binaries) for various platforms and versions from it    
**Packages for the Source Distribution and wheels can be installed with pip (see Install)**

## Install

1. Obtain a [Gitlab Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token) to authenticate to the project pypi repository   
2. Run the following command, with `<Gitlab Token>` replaced with your personal token :
```
pip install --extra-index-url https://__token__:<Gitlab Token>@gitlab.inria.fr/api/v4/projects/18034/packages/pypi/simple fbxsdkpy
```
If there is no wheel available for your platform, pip will attempt to build from source using the Source Distribution

## Create a Source Distribution

The Source distribution is obtained by downloading the FBXSDK libraries and Python Bindings for Linux and Windows from Autodesk, then patching them to work with sip5    

## Build wheels for package distribution

### GNU/Linux

Wheels need to be built inside a manylinux2014 environment, a Docker image is used for that purpose     

1. `docker run -t -v .:/fbxsdkpy`

### Windows

1. `build.bat`

