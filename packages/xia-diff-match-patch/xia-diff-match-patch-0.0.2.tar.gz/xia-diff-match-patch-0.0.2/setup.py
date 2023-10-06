import codecs
import sys
import os.path
import glob
import setuptools


with open("README.rst", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            return line.split('"')[1]
    else:
        raise RuntimeError("Unable to find version string.")


project_name = os.path.basename(os.getcwd())
package_name = project_name.replace("-", "_")
version_name = get_version(os.path.join(package_name, "__init__.py"))


# Get a list of all files in the templates directory
templates_files = glob.glob(f"{package_name}/templates/**/*", recursive=True)
templates_files += glob.glob(f"{package_name}/templates/**/.*", recursive=True)
templates_files = [f for f in templates_files if os.path.isfile(f)]
package_data_files = [os.path.relpath(f, f"{package_name}") for f in templates_files]


def get_short_description(full_description: str):
    old_line = ""
    for line in full_description.splitlines():
        if old_line.startswith("==="):
            return line.strip()
        old_line = line
    return project_name  # By default, short description is package name


# Generate manifest file to including packages
with open("MANIFEST.in", "w") as f:
    f.write(f"recursive-include {package_name}/templates *")


short_description = get_short_description(long_description)
requirements = [line.strip() for line in read("requirements.txt").splitlines() if line.strip()]
requirements_xia = [line.strip() for line in read("requirements-xia.txt").splitlines() if line.strip()]


setuptools.setup(
    name=project_name,
    version=version_name,
    author="X-I-A",
    author_email="admin@x-i-a.com",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://develop.x-i-a.com/docs/" + project_name + "/" + version_name + "/index.html",
    packages=setuptools.find_packages(),
    license_files=('LICENSE.txt',),
    package_data={
        package_name:
            ["*.pyd" if "win_amd64" in sys.argv else "*.so"] +
            ["**/*.pyd" if "win_amd64" in sys.argv else "**/*.so"] +
            package_data_files,
    },
    install_requires=requirements+requirements_xia,
    python_requires='>=3.9',
)
