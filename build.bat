powershell -Command "Invoke-WebRequest https://aka.ms/vs/16/release/vs_buildtools.exe -OutFile C:\TEMP\vs_buildtools.exe"
SET "CURRENTDIR=%cd%"
SET "BUILDDIR=%CURRENTDIR%\build"
SET "BUILDTOOLSDIR=%BUILDDIR%\buildtools"
SET "SIPINSTALLDIR=%BUILDDIR%\sipinstall"
mkdir "%BUILDDIR%"
mkdir "%BUILDTOOLSDIR%"
mkdir "%SIPINSTALLDIR%"
C:\TEMP\vs_buildtools.exe --quiet --wait --norestart --nocache --installPath "%BUILDTOOLSDIR%" --add Microsoft.VisualStudio.Workload.AzureBuildTools --remove Microsoft.VisualStudio.Component.Windows10SDK.10240 --remove Microsoft.VisualStudio.Component.Windows10SDK.10586 --remove Microsoft.VisualStudio.Component.Windows10SDK.14393 --remove Microsoft.VisualStudio.Component.Windows81SDK --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 || IF "%ERRORLEVEL%"=="3010" EXIT 0
"$BUILDTOOLSDIR"\
tar xvf sip-4.19.3.tar.gz -C "$BUILDDIR"
cd "$BUILDDIR"\sip-*
python  "configure.py" -b "$SIPINSTALLDIR" -d "$SIPINSTALLDIR" -e "$SIPINSTALLDIR" --pyidir="$SIPINSTALLDIR"
nmake
