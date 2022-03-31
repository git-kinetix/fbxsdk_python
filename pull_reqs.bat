pushd %~dp0
SET "CURRENTDIR=%cd%"
SET "BUILDDIR=%CURRENTDIR%\build"
SET "FBXSDKDIR=%BUILDDIR%\fbxsdk"
SET "FBXSDKPYTHONDIR=%BUILDDIR%\fbxpy"
mkdir "%BUILDDIR%"
mkdir "%FBXSDKDIR%"
mkdir "%FBXSDKPYTHONDIR%"

for /F "tokens=1,2 delims=;" %%i in (reqs_win.txt) do (
        curl.exe -C - -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0" -L -o "%BUILDDIR%\%%i.exe" %%j
        "%BUILDDIR%\%%i.exe" /S /D=%BUILDDIR%\%%i
)

curl.exe -C - -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0" -L -o "%BUILDDIR%\patch.py" "https://raw.githubusercontent.com/techtonik/python-patch/master/patch.py"
python "%BUILDDIR%\patch.py" --verbose --directory "%CURRENTDIR%" --debug patch 
move "%BUILDDIR%\fbxsdk\lib\vs2017" "%BUILDDIR%\fbxsdk\lib\all"
popd
