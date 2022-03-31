import os
import sys
# import ipdb

from sipbuild import Option, Project




class FBXSDKPyProject(Project):
    """ A project that adds an additional configuration options to specify
    the locations of the fib header file and library.
    """

    def get_options(self):
        """ Return the sequence of configurable options. """

        # Get the standard options.
        options = super().get_options()

        # Add our new options.
        win_libs_option = Option('win_libraries',
                help="a list of libraries needed on the windows platform for Python >=3.7", option_type=list, metavar="LIST")
        options.append(win_libs_option)

        win_py36_libs_option = Option('win_py36_libraries',
                help="a list of libraries needed on the windows platform for Python <=3.6", option_type=list, metavar="LIST")
        options.append(win_py36_libs_option)

        linux_libs_option = Option('linux_libraries',
                help="a list of libraries needed on the linuxdows platform", option_type=list, metavar="LIST")
        options.append(linux_libs_option)

        linux_static_libs_option = Option('linux_static_libraries',
                help="a list of libraries needed on the linuxdows platform", option_type=list, metavar="LIST")
        options.append(linux_static_libs_option)

        return options

    def update(self, tool):
        """ Update the project configuration. """

        # Get the fib bindings object.
        fbx_bindings = self.bindings['fbx_module']

        libraries = []
        if sys.platform == "win32":
            if sys.version_info.major == 3 and sys.version_info.minor < 7:
                libraries = self.win_py36_libraries
            else:
                libraries = self.win_libraries
        elif sys.platform == "linux":
            libraries = self.linux_libraries
        else:
            raise Exception("Your platform "+sys.platform+" is not supported")

        fbx_bindings.libraries.extend(libraries)

    def setup(self, pyproject, tool, tool_description):
        self.verbose = True
        # don't download Autodesk's stuff when making sdist
        if tool != "sdist":
            if sys.platform == "win32":
                super().run_command(["call pull_reqs.bat"],fatal=True)
            elif sys.platform == "linux":
                super().run_command(["./pull_reqs.sh"],fatal=True)
            else:
                raise Exception("Your platform "+sys.platform+" is not supported")
        super().setup(pyproject, tool, tool_description)

