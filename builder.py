from distutils.command.build_ext import build_ext
from distutils.dist import Distribution
from distutils.extension import Extension
from distutils.log import ERROR, INFO, set_threshold

import os
import sys

from sipbuild.buildable import BuildableModule
from sipbuild.distutils_builder import DistutilsBuilder, ExtensionCommand
from sipbuild.exceptions import UserException
from sipbuild.installable import Installable


class FBXSDKBuilder(DistutilsBuilder):
    """ Custom Builder for FBX SDK"""

    def _build_extension_module(self, buildable):

        project = self.project

        set_threshold(INFO if project.verbose else ERROR)

        distribution = Distribution()

        module_builder = ExtensionCommand(distribution, buildable)
        module_builder.build_lib = buildable.build_dir
        module_builder.debug = buildable.debug

        module_builder.ensure_finalized()

        define_macros = []
        for macro in buildable.define_macros:
            parts = macro.split("=", maxsplit=1)
            name = parts[0]
            try:
                value = parts[1]
            except IndexError:
                value = None

            define_macros.append((name, value))

        buildable.make_names_relative()

        if sys.platform == "linux":
            linux_static_libs = [
                os.path.abspath(a) for a in project.linux_static_libraries
            ]
            extra_compile_args = ["-std=c++11"]
        else:
            linux_static_libs = []
            extra_compile_args = []

        module_builder.extensions = [
            Extension(
                buildable.fq_name,
                buildable.sources,
                define_macros=define_macros,
                include_dirs=buildable.include_dirs,
                libraries=buildable.libraries,
                library_dirs=buildable.library_dirs,
                extra_link_args=linux_static_libs,
                extra_compile_args=extra_compile_args,
            )
        ]

        project.progress(
            "Compiling the '{0}' module".format(buildable.fq_name)
        )

        saved_cwd = os.getcwd()
        os.chdir(buildable.build_dir)

        try:
            module_builder.run()
        except Exception as e:
            raise UserException(
                "Unable to compile the '{0}' module".format(buildable.fq_name),
                detail=str(e),
            )

        installable = Installable(
            "module", target_subdir=buildable.get_install_subdir()
        )
        installable.files.append(
            module_builder.get_ext_fullpath(buildable.fq_name)
        )
        buildable.installables.append(installable)

        os.chdir(saved_cwd)
