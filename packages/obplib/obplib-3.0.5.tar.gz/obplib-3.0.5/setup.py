# SPDX-FileCopyrightText: 2019,2020 Freemelt AB
#
# SPDX-License-Identifier: Apache-2.0

# Built-in
import sys

# PyPI
import setuptools

from setuptools.command.build_py import build_py
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

import pkg_resources

with open("README.md", "r") as fh:
    description = fh.read()

sys.path.append("obplib")
from _version import __version__

sys.path.remove("obplib")


class Protoc(setuptools.Command):
    """Use protoc to generate OBP_pb2.py and OBP_pb2_grpc.py"""

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.protoc

        # Explicitly include the built-in proto files from grpc_tools
        # because OBP.proto uses google.protobuf.Any. Seems to be
        # necessary on Windows only.
        proto_include = pkg_resources.resource_filename("grpc_tools", "_proto")
        command = [
            "grpc_tools.protoc",
            "-I=.",
            f"-I={proto_include}",
            "--python_out=.",
            "--grpc_python_out=.",
            "obplib/OBP.proto",
        ]
        code = grpc_tools.protoc.main(command)
        command_str = " ".join(command)
        assert code == 0, f"Command {command_str!r} failed with exit code {code}"


# python3 setup.py build
class BuildCommand(build_py):
    def run(self):
        self.run_command("protoc")
        super().run()


# python3 setup.py bdist_wheel
# pip will call "python3 setup.py bdist_wheel" if 'wheel' is installed,
# otherwise it will fallback to "python setup.py install".
try:
    from wheel.bdist_wheel import bdist_wheel

    class WheelCommand(bdist_wheel):
        def run(self):
            self.run_command("protoc")
            super().run()


except ModuleNotFoundError:
    WheelCommand = None


# python3 setup.py install
class InstallCommand(install):
    def run(self):
        self.run_command("protoc")
        super().run()


# python3 setup.py develop
class DevelopCommand(develop):
    def run(self):
        self.run_command("protoc")
        super().run()


setuptools.setup(
    name="obplib",
    version=__version__,
    license="apache-2.0",
    author="Freemelt AB",
    author_email="opensource@freemelt.com",
    description="A library for the creation of beam paths",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/freemelt/openmelt/obplib-python",
    download_url="https://gitlab.com/freemelt/openmelt/obplib-python/-/archive/0.3.0/obplib-python-0.3.0.tar.gz",
    keywords="obp openbeampath freemelt",
    packages=setuptools.find_packages(exclude=["tests"]),
    entry_points={
        "console_scripts": [
            "obpc=obplib.compiler.__main__:OBPC",
            "obpviewer=obplib.viewer.obpviewer:main",
        ]
    },
    setup_requires=[
        "grpcio-tools",
    ],
    install_requires=[
        "protobuf",
        "grpcio",
        "svg.path==3.0",
        "click",
    ],
    cmdclass={
        "build_py": BuildCommand,
        "install": InstallCommand,
        "develop": DevelopCommand,
        # "egg_info": EggInfoCommand,
        "bdist_wheel": WheelCommand,
        "protoc": Protoc,
    },
    package_data={"obplib": ["OBP.proto"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
