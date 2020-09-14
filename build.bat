pushd %~dp0
SET "CURRENTDIR=%cd%"
SET "BUILDDIR=%CURRENTDIR%\build"
SET "BUILDTOOLSDIR=%BUILDDIR%\buildtools"
SET "VCVARSBAT=%BUILDTOOLSDIR%\VC\Auxiliary\Build\vcvars64.bat"
SET "SIPDIR=%BUILDDIR%\sip-4.19.3"
SET "SIPINSTALLDIR=%BUILDDIR%\sipinstall"
SET "vs_buildtoolsexe=%BUILDDIR%\vs_buildtools.exe"
SET "FBXSDKDIR=%BUILDDIR%\fbxsdk"
SET "FBXSDKPYTHONDIR=%BUILDDIR%\fbxsdkpy"
SET "FBXDIR=%CURRENTDIR%\fbx"
mkdir "%BUILDDIR%"
mkdir "%BUILDTOOLSDIR%"
mkdir "%SIPINSTALLDIR%"
mkdir "%FBXSDKDIR%"
mkdir "%FBXSDKPYTHONDIR%"
mkdir "%FBXDIR%"

echo "Download and install Visual Studio Build Tools (nmake, MSVC, link, etc.)"

curl -L -o %vs_buildtoolsexe% https://aka.ms/vs/16/release/vs_buildtools.exe

%vs_buildtoolsexe% --quiet --wait --norestart --nocache --installPath "%BUILDTOOLSDIR%" --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 --remove Microsoft.VisualStudio.Component.Windows81SDK --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows10SDK|| IF "%ERRORLEVEL%"=="3010" EXIT 0


echo "Load environment variables to use Build Tools from this script"
call %VCVARSBAT%

for /F "tokens=1,2 delims=;" %%i in (reqs_win.txt) do (
        curl -L -o "%BUILDDIR%\%%i.exe" %%j
        "%BUILDDIR%\%%i.exe" /S /D=%BUILDDIR%\%%i
)

::curl -L -O "https://gitlab.inria.fr/radili/fbxsdk_python/uploads/12002ae82d20e4d6b60107dacb5abe4b/sip-4.19.3.tar.gz"

tar xvf sip-4.19.3.tar.gz -C "%BUILDDIR%"
cd "%BUILDDIR%"\sip-*
python  "configure.py" -b "%SIPINSTALLDIR%" -d "%SIPINSTALLDIR%" -e "%SIPINSTALLDIR%" --pyidir="%SIPINSTALLDIR%" --sip-module="fbxsip"
nmake
nmake install
cd %CURRENTDIR%

copy "PythonBindings.py" "%FBXSDKPYTHONDIR%/PythonBindings.py"
SET "FBXSDK_ROOT=%FBXSDKDIR%"
SET "SIP_ROOT=%SIPDIR%"
python "%FBXSDKPYTHONDIR%"/PythonBindings.py Python3_x64
copy "%FBXSDKPYTHONDIR%\build\Distrib\site-packages\fbx\*" "%FBXDIR%"
copy "%SIPINSTALLDIR%\sip.pyd" "%FBXDIR%"

%vs_buildtoolsexe% uninstall --quiet --wait --norestart --nocache --installPath "%BUILDTOOLSDIR%" --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 --remove Microsoft.VisualStudio.Component.Windows81SDK --remove Microsoft.VisualStudio.Workload.VCTools --remove Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --remove Microsoft.VisualStudio.Component.Windows10SDK || IF "%ERRORLEVEL%"=="3010" EXIT 0
popd
pause
