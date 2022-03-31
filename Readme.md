# FBXSDK Python Bindings

This the Source Distribution (sdist) repository for the FBXSDK Python Bindings     
**Packages for the Source Distribution and wheels (prebuilt binaries) can be installed with pip (see Install)**    

## Install

1. Obtain a [Gitlab Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#creating-a-personal-access-token) to authenticate to the project pypi repository   
2. Run the following command, with `<Gitlab Token>` replaced with your personal token :
```
pip --verbose install --extra-index-url https://__token__:<Gitlab Token>@gitlab.inria.fr/api/v4/projects/18034/packages/pypi/simple fbxsdkpy
```
If there is no wheel available for your platform, pip will attempt to build from source     
To force an install from source, pass the `--no-binary` option to pip

## Manual Build

Alternatively, the bindings can be built and installed by cloning this repository and running `pip --verbose install .`

### Remarks

Instead of the libraries and bindings from Autodesk being included in the repository, they are downloaded before building    
`--verbose` is recommended to get the output of the compiler in case of an error. Also, as compilation can take several minutes, `pip` might otherwise seem unresponsive
