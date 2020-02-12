import os, sys, shutil,re,time
import platform
import multiprocessing
import subprocess
import FbxUtils

WINDOWS_PLATFORM = (platform.system() == 'Windows' or platform.system() == "Microsoft")

# Python module extension
SIP_MODULE_EXT     = '.pyd' if WINDOWS_PLATFORM else '.so'
SIP_MODULE_NAME    = 'fbxsip' # make sure we use a fully qualified private sip module
SIP_PRIVATE_MODULE = []       # if using Sip >= 4.19.9 must add -n <name> at the call of sip.exe

EXTRA_INCLUDE_DIRS     = []
EXTRA_INCLUDE_DIRS_MAC = []
EXTRA_LIBS_DIR         = []
EXTRA_STATIC_LIBS      = []
EXTRA_LIBS             = []

# link with FBX SDK library built with VisualStudio 2015 by default
vcCompiler = "vc140"
vsCompiler = "vs2015"

# default supported python modules.
# The script is decomposing the module to figure out what it needs to build. If more (or different modules) are
# desired, make sure to change gModules, gPlatformTag and gUCSCompatible.
gModules   = ["Python2_x86","Python2_ucs4_x86",
              "Python2_x64","Python2_ucs4_x64",
              "Python3_x86","Python3_x64",
              "Python2_ub", "Python3_ub"]
gPlatformTag = {
    'Python2_x86'     :'FBX_X86',
    'Python2_ucs4_x86':'FBX_X86',
    'Python2_x64'     :'FBX_X64',
    'Python2_ucs4_x64':'FBX_X64',
    'Python3_x86'     :'FBX_X86',
    'Python3_x64'     :'FBX_X64',
    'Python2_ub'      :'FBX_X86_X64',
    'Python3_ub'      :'FBX_X86_X64'
}
gUCScompatible = {
    'Python2_x86'     : 65535,
    'Python2_ucs4_x86': 1114111,
    'Python2_x64'     : 65535, 
    'Python2_ucs4_x64': 1114111,
    'Python3_x86'     : 1114111,
    'Python3_x64'     : 1114111,
    'Python2_ub'      : 65535,
    'Python3_ub'      : 1114111
}

rootPath        = os.path.dirname(os.path.abspath(sys.argv[0]))
buildPath       = os.path.join(rootPath, 'build')
distribPath     = os.path.join(buildPath, 'Distrib', 'site-packages')
inclDstFolder   = False
libBaseDir      = 'fbx'
docBaseDir      = os.path.join('fbx', 'doc')
cmdLineDescr    = "PythonBindings.py module module [buildsip]"

def PrintError(txt):
    print ("\n================================================================================================\n")
    FbxUtils.Log(2, "ERROR: " + txt)
    print ("\n================================================================================================\n")
    exit(1)

    
def log(txt):
    msg = "=> " + txt + "\n"
    FbxUtils.Log(1, msg)


def test_python_fbx_examples(fbx_wrapper_dir, build_dir, sdk_lib_dir):
    log("")
    log("-=[ Testing the samples ]=-")
    log("")

    shutil.copyfile(os.path.join(fbx_wrapper_dir, 'common/FbxCommon.py'), os.path.join(sdk_lib_dir, 'FbxCommon.py'))
    src_samples_dir = os.path.join(fbx_wrapper_dir, 'samples')
    dst_samples_dir = os.path.join(build_dir, 'samples')
    try:
        FbxUtils.DirCopy(src_samples_dir, dst_samples_dir)
    except:
        PrintError("Failed to copy samples directories")
        exit(1)
    
    example_dirs = (
        os.path.join(dst_samples_dir, 'Audio'),
        os.path.join(dst_samples_dir, 'ExportScene01'),
        os.path.join(dst_samples_dir, 'ExportScene02'),
        os.path.join(dst_samples_dir, 'ExportScene03'),
        os.path.join(dst_samples_dir, 'ExportScene04'),
        os.path.join(dst_samples_dir, 'Layers'),
        os.path.join(dst_samples_dir, 'SplitMeshPerMaterial'),
    )
    example_scripts = (
        'Audio.py',
        'ExportScene01.py', 
        'ExportScene02.py', 
        'ExportScene03.py',
        'ExportScene04.py', 
        'Layers.py', 
        'SplitMeshPerMaterial.py multiplematerials.FBX',        
    )

    os.environ['PYTHONPATH'] = sdk_lib_dir
    for index in range(len(example_dirs)):
        os.chdir(example_dirs[index])
        command = " ".join(['"' + sys.executable + '"', example_scripts[index]])
        log("  RUN COMMAND       : %s" % command)
        result = os.system(command)
    
    os.chdir(os.path.join(dst_samples_dir, 'ImportScene'))
    files = (
        '../Audio/Audio.fbx',
        '../ExportScene01/ExportScene01.fbx',
        '../ExportScene02/ExportScene02.fbx',
        '../ExportScene03/ExportScene03.fbx',
        '../ExportScene04/ExportScene04.fbx',
        '../Layers/Layers.fbx'
    )

    dump_output = '' if WINDOWS_PLATFORM else '> /dev/null'
    for index in range(len(files)):
        command = " ".join(['"' + sys.executable + '"', 'ImportScene.py', files[index], dump_output])
        log("  RUN COMMAND       : %s" % command)
        result = os.system(command)


def generate_python_fbx_documentation(python_dir, api_doc_dir):
    if WINDOWS_PLATFORM:
        # documentation can only be generated on Windows
        log("")
        log("-=[ Generating documentation ]=-")
        log("")

        pydocInstallPath = os.path.dirname(sys.executable) + "/Lib"

        os.chdir(python_dir)
        log("%s" % pydocInstallPath)
        command = sys.executable + " " + pydocInstallPath + "/pydoc.py -w fbx"
        log("%s" % command)
        os.system(command)

        if not os.path.exists(api_doc_dir):
            os.mkdir(api_doc_dir)

        # The generation with pydoc can take a while so wait until file exists before copying
        timeout = 0
        while ((not os.path.exists(os.path.join(python_dir, "fbx.html"))) and (timeout < 60)):
            time.sleep(1)
            timeout += 1

        shutil.copyfile(os.path.join(python_dir, "fbx.html"), os.path.join(api_doc_dir, "fbx.html"))


def ResetDirectory(build_dir):
    timeout = 100
    while timeout:
        try:
            FbxUtils.DirDelete(build_dir)
            timeout = 0
        except:
            timeout -= 1
            time.sleep(0.01)
    try:

        FbxUtils.DirCreate(build_dir)
    except:
        PrintError("Cannot reset build directory: %s" % build_dir)


def Clean(python_dir):
    # Clear the generated sip files by last build
    if os.path.exists(os.path.join(python_dir, SIP_MODULE_NAME + SIP_MODULE_EXT)):
        os.remove(os.path.join(python_dir, SIP_MODULE_NAME + SIP_MODULE_EXT))

    if os.path.exists(os.path.join(python_dir, 'sipconfig.py')):
        os.remove(os.path.join(python_dir, 'sipconfig.py'))
    if os.path.exists(os.path.join(python_dir, 'sipdistutils.py')):
        os.remove(os.path.join(python_dir, 'sipdistutils.py'))

    sipconfig = os.path.join(python_dir, 'sipconfig.pyc')
    if os.path.exists(sipconfig):
        os.remove(sipconfig)

    # with python3.2 the sipconfig compiled file goes inside the __pycache__
    sipconfig = os.path.join(python_dir,"__pycache__")
    if os.path.exists(sipconfig):
        shutil.rmtree(sipconfig)

    # Residual files 
    if WINDOWS_PLATFORM:
        if os.path.exists(os.path.join(python_dir, 'sip.exe')):
            os.remove(os.path.join(python_dir, 'sip.exe'))
        if os.path.exists(os.path.join(python_dir, 'sip.h')):
            os.remove(os.path.join(python_dir, 'sip.h'))
        if os.path.exists(os.path.join(python_dir, 'fbx.html')):
            os.remove(os.path.join(python_dir, 'fbx.html'))


def vcvars(platform_tag):
    prefix = vcCompiler.replace('vc', 'VS')
    vc_common_tool_dir = os.path.expandvars('$'+prefix+'COMNTOOLS')
    if platform_tag == 'FBX_X64':
        result = os.path.normpath(os.path.join(vc_common_tool_dir, '../../VC/bin/amd64/vcvars64.bat'))
    else:
        result = os.path.normpath(os.path.join(vc_common_tool_dir, '../../VC/bin/vcvars32.bat'))
    return result


def osarch(platform_tag):
    result = ''
    if platform.system() == 'Darwin':
        if platform_tag == 'FBX_X86_X64':
            result = ' --arch=i386 --arch=x86_64'
        elif platform_tag == 'FBX_X64':
            result = ' --arch=x86_64'
        elif platform_tag == 'FBX_X86':
            result = ' --arch=i386'
    return result


def tag(platform_tag):
    if platform_tag == 'FBX_X64':
        return '-t FBX_X64 '
    elif platform_tag == 'FBX_X86':
        return '-t FBX_X86 '
    else:
        return '-t FBX_X64 '


def FindSipconfig():
    # look into the registered sites for sipconfig.py
    import site
    sites = site.getsitepackages()
    sites.append(site.getusersitepackages())
    print(sites)
    for s in sites:
        sipconfigpy = os.path.join(s, 'sipconfig.py')
        try:
            if FbxUtils.FileExist(sipconfigpy):
                return s
        except:
            pass
    return ''


def GetSipVersionFromFile(file):
    f = open(file, 'r')
    content = f.read()
    f.close();

    version = [0, 0, 0]
    v = re.search('sip_version_str = "[0-9]+.[0-9]+.[0-9]+"', content)
    if v:
        tmp = v.group().replace('sip_version_str = ', '').replace('"', "")
        tmp = tmp.split('.')
        if len(tmp):
            version = []
            version.append(int(tmp[0]))
            version.append(int(tmp[1]) if len(tmp) >= 2 else 0)
            version.append(int(tmp[2]) if len(tmp) >= 3 else 0)

    return version

def GetSipVersionFromConfig(sipconfig):
    sip_version_str = sipconfig._pkg_config.get('sip_version_str')
    sipVer = sip_version_str.split('.')

    version = [0, 0, 0]
    if len(sipVer):
        version = []
        version.append(int(sipVer[0]))
        version.append(int(sipVer[1]) if len(sipVer) >= 2 else 0)
        version.append(int(sipVer[2]) if len(sipVer) >= 3 else 0)

    return version


def BuildSipModule(python_dir, build_dir, platform_tag, define_sip_module):
    # --------------------------------------
    # compile sip
    # --------------------------------------
    sip_dir = os.environ["SIP_ROOT"]
    log("SIP              : %s\n" % sip_dir)
    log("")
    log("-=[ Build SIP Module ]=-")
    log("")
      
    sip_module_name = ''
    if define_sip_module:
        sip_module_name = ' --sip-module='+SIP_MODULE_NAME

    # Clear the generated sip files by last build (if this script is launched manually residues may exist in the folder)
    Clean(python_dir)

    os.chdir(sip_dir)
    log("CURRENT DIR      : %s" % sip_dir)
    command = '"' + sys.executable + '"' + ' configure.py ' + sip_module_name + \
              ' -b ' + build_dir + ' -d ' + python_dir + \
              ' ' + osarch(platform_tag) + ' -e ' + build_dir

    log("RUN COMMAND      : %s" % command)
    os.system(command)

    if WINDOWS_PLATFORM:
        bat_file = open('compile.bat', 'w')
        bat_file.write('@echo off\n')
        bat_file.write('call "' + vcvars(platform_tag) + '"\n')
        bat_file.write('set CL=/MP\n')
        bat_file.write('nmake clean\n')
        bat_file.write('nmake\n')
        bat_file.write('nmake install\n')
        bat_file.close()
        log("RUN BATCH        : %s" % command)
        log("RUN BATCH        : %s" % 'nmake clean')
        log("RUN BATCH        : %s" % 'nmake')
        log("RUN BATCH        : %s" % 'nmake install')
        subprocess.call('compile.bat', shell=True)
    else:
        log("RUN COMMAND    : %s" % 'make clean')
        subprocess.call('make clean', shell=True)
        log("RUN COMMAND    : %s" % 'make')
        subprocess.call('make', shell=True)
        log("RUN COMMAND    : %s" % 'make install')
        subprocess.call('make install', shell=True)

    os.chdir(python_dir)
    log("CURRENT DIR      : %s" % python_dir)


def main(args):

    # Display help if wrong number arguments
    nbArgs = len(args)
    if nbArgs < 2 or nbArgs > 5:
        mods = " | ".join(gModules)
        print ("Syntax: " + cmdLineDescr + " [test] [doc]\n")
        print ("        modules = " + mods)
        exit(1)

    # get and validate arguments
    moduleFound = False
    inputModule = args[1]
    for module in gModules:
        if inputModule.lower() == module.lower():
            inputModule = module
            moduleFound = True
            break

    if not moduleFound:
        PrintError("No module name match for: "+ inputModule)

    # Asking this scrip to build Sip, will requires the sources of Riverbanks Sip code version 4.19.3
    # more recent versions have not been tested. Important: this step generates an fbxsip.pyd module to
    # avoid any conflicts with other existing sip modules. For code more recent than 4.19.3, you must be sure that
    # an fbxsip.pyd module is created (at the time this comment has been written, the latest Sip sources are
    # version 4.19.13 but it looks like these sources hardcode the target to sip.py instead of using the --sip-module
    # name defined in the configuration.
    buildSip = False
    test = False
    doc = False

    for i in range(2,nbArgs):
        if args[i].lower() == 'buildsip': buildSip = True;
        if args[i].lower() == 'test': test = True;
        if args[i].lower() == 'doc': doc = True;
        
    # make sure the python interpreter running this script is the correct version with
    # the specified module
    pyVer = sys.version.split(' ')[0].replace('.','')[:2]
    v = inputModule.replace('Python', '')[:2]
    if v[0] != pyVer[0]:
        PrintError("The interpreter running this script mismatch the requested target version: " + inputModule)

    # make sure the python interpreter running this script is UCS compatible with the
    # specified module
    if not (gUCScompatible[inputModule] == sys.maxunicode):        
        PrintError("The interpreter running this script is not UCS compliant with target: " + inputModule)

    # setup build environment    
    fbx_wrapper_dir   = rootPath

    dst_folder        = re.sub(r'Python[0-9]+_', 'Python'+pyVer+'_', inputModule)
    build_dir         = os.path.join(buildPath, dst_folder)
    python_dir        = os.path.dirname(os.path.abspath(sys.argv[0]))

    sip_subfolder     = 'sip'
    sbf_filename      = 'fbx_module.sbf'

    sipRootPath = os.path.normpath(os.environ["SIP_ROOT"])
    sys.path.append(sipRootPath)

    # FBX_X64 or FBX_X86
    platform_tag      = gPlatformTag[inputModule]
    os.environ["ENV_PLATEFORM_TAG"] = platform_tag # python2.7 is more strict. tools/sip/config.py needs it!
    os.environ["ENV_DISTRIB_DIR"] = distribPath

    # Set the extra folders
    if not "FBXSDK_ROOT" in os.environ:
        PrintError("Missing definition of environment variable FBXSDK_ROOT")
        
    fbxsdkRootPath = os.path.normpath(os.environ["FBXSDK_ROOT"])
    platform_tag = os.environ["ENV_PLATEFORM_TAG"]

    global EXTRA_INCLUDE_DIRS
    global EXTRA_INCLUDE_DIRS_MAC
    global EXTRA_LIBS_DIR
    global EXTRA_STATIC_LIBS
    global EXTRA_LIBS
    
    if WINDOWS_PLATFORM:
        EXTRA_LIBS = ["libfbxsdk-md", "zlib-md", "libxml2-md", "Advapi32", "Wininet"]
        EXTRA_LIBS_DIR = [os.path.join(fbxsdkRootPath, 'lib', vsCompiler, 'x86', 'Release')]
        if 'FBXSDK_LIBS_32_FOLDER' in os.environ:
            EXTRA_LIBS_DIR = [os.environ['FBXSDK_LIBS_32_FOLDER']]

        if platform_tag == "FBX_X64":
            EXTRA_LIBS_DIR = [os.path.join(fbxsdkRootPath, 'lib', vsCompiler, 'x64', 'Release')]
            if 'FBXSDK_LIBS_64_FOLDER' in os.environ:
                EXTRA_LIBS_DIR = [os.environ['FBXSDK_LIBS_64_FOLDER']]

    elif platform.system()=="Linux":
        libPath = os.path.join(fbxsdkRootPath, 'lib', 'gcc', 'x86', 'release')
        if 'FBXSDK_LIBS_32_FOLDER' in os.environ:
            libPath = os.environ['FBXSDK_LIBS_32_FOLDER']
            
        if platform_tag == "FBX_X64":
            libPath = os.path.join(fbxsdkRootPath, 'lib', 'gcc', 'x64', 'release')
            if 'FBXSDK_LIBS_64_FOLDER' in os.environ:
                libPath = os.environ['FBXSDK_LIBS_64_FOLDER']

        EXTRA_LIBS_DIR = [libPath]
        EXTRA_LIBS = ["z", "xml2"]
        EXTRA_STATIC_LIBS = [os.path.join(libPath, "libfbxsdk.a")]
                
    elif platform.system()=="Darwin":
        libPath = os.path.join(fbxsdkRootPath, 'lib', 'clang', 'release')
        if 'FBXSDK_LIBS_64_FOLDER' in os.environ:
            libPath = os.environ['FBXSDK_LIBS_64_FOLDER']
            
        EXTRA_LIBS_DIR = [libPath]
        EXTRA_LIBS = ["z", "xml2", "iconv"]
        EXTRA_STATIC_LIBS = ['"' + os.path.join(libPath, "libfbxsdk.a") + '"']

    # Extra required folders
    EXTRA_INCLUDE_DIRS = [os.path.join(fbxsdkRootPath,"include")]
    EXTRA_INCLUDE_DIRS_MAC = [os.path.join(fbxsdkRootPath,"include"),
                              "/usr/include",
                              "/usr/lib/gcc/i686-apple-darwin10/4.0.1/include",
                              "/usr/include/c++/4.0.0",
                              os.path.join(sipRootPath,"sipgen")]


    log("SRC PYTHON       : %s" % fbx_wrapper_dir)
    log("SCRIPT PATH      : %s" % python_dir)
    log("BUILD PATH       : %s" % build_dir)      
    log("SDK Headers      : %s" % EXTRA_INCLUDE_DIRS)
    log("Machine Type     : %s" % platform.machine())
    log("LIB PATH         : %s" % EXTRA_LIBS_DIR)
    log("PLATFORM TAG     : %s" % platform_tag)

    # make sure 'build_dir' exists and is empty
    ResetDirectory(build_dir)

   # sipRootPath = FindSipconfig()

    if buildSip:
        # Check if we have the Riverbanks Sip sources properly installed. This is mandatory.
        # We assume that we have a valid installation if the folder exists and contains the
        # file 'configure.py'
        if not "SIP_ROOT" in os.environ:
            PrintError("Missing definition of environment variable SIP_ROOT")

        sipRootPath = os.path.normpath(os.environ["SIP_ROOT"])
        configpy = os.path.join(sipRootPath, 'configure.py')
        if not os.path.exists(sipRootPath) or not FbxUtils.FileExist(configpy):
            PrintError("Unable to locate sip sources in %s. Install them before running the script" % (sipRootPath))

        sip_ver = GetSipVersionFromFile(configpy)
        sip_module_define = True
        if sip_ver[0] >= 4 and sip_ver[1] >= 19 and sip_ver[2] >= 9:
            sip_module_define = False

        # Force building the sip module with our local version.
        # pre-installed sip may not play nice
        BuildSipModule(build_dir, build_dir, platform_tag, sip_module_define)
        sipRootPath = build_dir
        sys.path.insert(0, build_dir)

    try:
        sipconfigpy = os.path.join(sipRootPath, 'sipconfig.py')
        if not os.path.exists(sipRootPath) or not FbxUtils.FileExist(sipconfigpy):
            PrintError("Unable to automatically locate sipconfig.py. Make sure Sip is installed in one of the\n" +
                       "       standard sites before running the script. Or install sources from RiverBank site\n" +
                       "       and use the 'buildsip' option.")

        log("Sipconfig Path   : %s" % sipRootPath)
        os.chdir(sipRootPath)
        import sipconfig
        os.chdir(python_dir)
    except ImportError:
        PrintError("Unable to import sipconfig module.")

    # get Sip version
    global SIP_PRIVATE_MODULE
    global SIP_MODULE_NAME
    
    sip_ver = GetSipVersionFromConfig(sipconfig)
    if buildSip:
        if sip_module_define:
            if sip_ver[2] >= 9: SIP_PRIVATE_MODULE = ['-n', SIP_MODULE_NAME+SIP_MODULE_EXT]
            if sip_ver[0] >= 4 and sip_ver[1] >= 19 and sip_ver[2] > 3:
                sip_version_str = '.'.join(map(str,sip_ver))
                # we are building sip locally but the version we are using cannot generate fbxsip.x
                log("")
                log("WARNING: Using Sip version %s may not be able to compile '%s'" %
                    (sip_version_str, SIP_MODULE_NAME+SIP_MODULE_EXT))
        else:
            SIP_MODULE_NAME = 'sip'

    # --------------------------------------
    # compile fbx python binding
    # --------------------------------------
    log("\n")
    log("-=[ Build FBX Module ]=-")
    log("")
    config = sipconfig.Configuration()
    build_macros = config.build_macros()

    build_macros['CXXFLAGS_WARN_ON'] = ''
    if platform.system() == 'Linux':
        config.platform = 'linux-g++'
        build_macros['CXXFLAGS'] += ' -std=c++11 -Wno-unused-variable -Wno-sign-compare -Wno-strict-aliasing' 
    elif WINDOWS_PLATFORM:
        build_macros['CXXFLAGS'] += ' /EHsc'
        config.platform = 'win32-msvc2008'
    elif platform.system() == 'Darwin':
        config.platform = 'macx-univ-g++'
        build_macros['CXXFLAGS'] += ' -std=c++11'

    config.set_build_macros(build_macros)
    
    """
    http://www.riverbankcomputing.co.uk/static/Docs/sip4/command_line.html
    -t <TAG>
        The SIP version tag (declared using a %Timeline directive) or the SIP platform tag (declared using the 
        %Platforms directive) to generate code for. This option may be given any number of times so long as the tags
        do not conflict.
    -c <DIR>
        The name of the directory (which must exist) into which all of the generated C or C++ code is placed. 
        By default no code is generated.
    -b <FILE>
        The name of the build file to generate. This file contains the information about the module needed by the 
        SIP build system to generate a platform and compiler specific Makefile for the module. By default the file
        is not generated.
    -I <DIR>
        The directory is added to the list of directories searched when looking for a specification file given in 
        an %Include or %Import directive. This option may be given any number of times.
    """
    sbf_fn = os.path.join(build_dir, sbf_filename)
    includes = os.path.join(fbx_wrapper_dir, sip_subfolder)
    module_sip = os.path.join(fbx_wrapper_dir, sip_subfolder, "fbx_module.sip")
    sip_bin=sipRootPath+"/sipgen/sip"
    if len(SIP_PRIVATE_MODULE):
        command = " ".join(['"' + sip_bin + '"',
                            SIP_PRIVATE_MODULE[0], SIP_PRIVATE_MODULE[1],
                            "-o", tag(platform_tag), "-c", build_dir, "-b", sbf_fn,
                            "-I", includes, "-I", os.path.join(sipRootPath,"sipgen"), module_sip])
    else:
        command = " ".join(['"' + sip_bin + '"',
                        "-o", tag(platform_tag), "-c", build_dir, "-b", sbf_fn,
                        "-I", includes, "-I", os.path.join(sipRootPath,"sipgen"),
                       module_sip])
    log("  RUN COMMAND       : %s" % command)
    result = os.system(command)

    if result == 1:
        sys.exit(1)
    if platform.system() == 'Darwin':
        config.qt_framework = None  # Hack to avoid sip bug under Mac
    makefile = sipconfig.SIPModuleMakefile(config, sbf_filename, dir = build_dir)
    if platform.system() == 'Darwin':
        makefile.extra_include_dirs = EXTRA_INCLUDE_DIRS_MAC
        makefile.extra_lflags = ['-framework', 'Carbon', '-arch i386', '-arch x86_64']
    else:
        makefile.extra_include_dirs = EXTRA_INCLUDE_DIRS

    if(platform.system() == 'Linux' and platform_tag == 'FBX_X86'):
        makefile.extra_cflags = ['-m32']
        makefile.extra_cxxflags = ['-m32']
        makefile.extra_lflags = ['-m32']

    makefile.extra_lib_dirs = EXTRA_LIBS_DIR
    makefile.extra_libs = EXTRA_LIBS  
    if len(EXTRA_STATIC_LIBS):
        makefile.LIBS.set(EXTRA_STATIC_LIBS)
    makefile.generate()    

    # build with MAKEFILE
    os.chdir(build_dir)
    log("CURRENT DIR         : %s" % build_dir)
    
    if WINDOWS_PLATFORM:
        bat_file = open('compile.bat', 'w')
        bat_file.write('@echo off\n')
        bat_file.write('call "' + vcvars(platform_tag) + '"\n')
        bat_file.write('set CL=/MP\n')
        bat_file.write('nmake\n')
        bat_file.close()
        subprocess.call('compile.bat', shell=True)
    else:
        os.system('make -j '+str(multiprocessing.cpu_count()))

    sdk_lib_dir = os.path.join(os.environ["ENV_DISTRIB_DIR"],libBaseDir)
    if inclDstFolder:
        sdk_lib_dir = os.path.join(os.environ["ENV_DISTRIB_DIR"],libBaseDir, dst_folder)
        
    api_doc_dir = os.path.join(os.environ["ENV_DISTRIB_DIR"],docBaseDir)
    log("Copy the results to the folder:" + sdk_lib_dir)
    if not os.path.exists(sdk_lib_dir):
        os.makedirs(sdk_lib_dir)

    if buildSip:
        try:
            file = SIP_MODULE_NAME + SIP_MODULE_EXT
            shutil.copyfile(os.path.join(build_dir, file), os.path.join(sdk_lib_dir,file))
        except:
            if len(SIP_PRIVATE_MODULE):
                log("WARNING: Unable to copy private sip file (%s)" % os.path.join(build_dir, file))

    shutil.copyfile(os.path.join(build_dir, 'fbx' + SIP_MODULE_EXT), os.path.join(sdk_lib_dir, 'fbx' + SIP_MODULE_EXT))
    shutil.copyfile(os.path.join(fbx_wrapper_dir,"common/FbxCommon.py"), os.path.join(sdk_lib_dir, "FbxCommon.py"))

    os.chdir(python_dir)

    if test:
        test_python_fbx_examples(fbx_wrapper_dir, build_dir, sdk_lib_dir)

    if doc:
        generate_python_fbx_documentation(python_dir, api_doc_dir)

    # --------------------------------------
    # Clean
    # --------------------------------------
    if buildSip:
        Clean(build_dir)

    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
