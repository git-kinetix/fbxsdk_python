SET "CURRENTDIR=%cd%"
SET "BUILDDIR=%CURRENTDIR%\build"
SET "BUILDTOOLSDIR=%BUILDDIR%\buildtools"
SET "VCVARSBAT=%BUILDTOOLSDIR%\VC\Auxiliary\Build\vcvars64.bat"
SET "SIPDIR=%BUILDDIR%\sip-4.19.3"
SET "SIPINSTALLDIR=%BUILDDIR%\sipinstall"
SET "vs_buildtoolsexe=%TEMP%\vs_buildtools.exe"
SET "FBXSDKDIR=%BUILDDIR%\fbxsdk"
SET "FBXSDKPYTHONDIR=%BUILDDIR%\fbxsdkpy"
mkdir "%BUILDDIR%"
mkdir "%BUILDTOOLSDIR%"
mkdir "%SIPINSTALLDIR%"
mkdir "%FBXSDKDIR%"
mkdir "%FBXSDKPYTHONDIR%"

echo "Download and install Visual Studio Build Tools (nmake, MSVC, link, etc.)"

::Invoke-WebRequest https://aka.ms/vs/16/release/vs_buildtools.exe -OutFile %vs_buildtoolsexe%
::curl -o %vs_buildtoolsexe% https://aka.ms/vs/16/release/vs_buildtools.exe

::%vs_buildtoolsexe% --quiet --wait --norestart --nocache --installPath "%BUILDTOOLSDIR%" --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 --remove Microsoft.VisualStudio.Component.Windows81SDK --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows10SDK || IF "%ERRORLEVEL%"=="3010" EXIT 0


echo "Load environment variables to use Build Tools from this script"
call %VCVARSBAT%

for /F "tokens=1,2 delims=;" %%i in (reqs_win.txt) do (
	SET "INSTALLEXE=%BUILDDIR%\%%i.exe"
	SET "INSTALLDIR=%BUILDDIR%\%%i"
	echo "%INSTALLEXE%"
	echo "%INSTALLDIR%"
	echo "Downloading %%j to %%i"
	::curl -L -o "%INSTALLEXE%" %%j
	::%INSTALLEXE% /S /D=%INSTALLDIR%
)


::tar xvf sip-4.19.3.tar.gz -C "%BUILDDIR%"
::cd "%BUILDDIR%"\sip-*
::python  "configure.py" -b "%SIPINSTALLDIR%" -d "%SIPINSTALLDIR%" -e "%SIPINSTALLDIR%" --pyidir="%SIPINSTALLDIR%"
::nmake
::nmake install
::cd %CURRENTDIR%


