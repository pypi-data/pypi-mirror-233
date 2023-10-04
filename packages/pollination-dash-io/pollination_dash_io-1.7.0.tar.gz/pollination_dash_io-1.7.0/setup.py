import json
from setuptools import setup


with open('package.json') as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

def _clean_version():
    """
    This function was required because scm was generating developer versions on
    GitHub Action.
    """
    def get_version(version):
        return str(version.tag)
    def empty(version):
        return ''

    return {'local_scheme': get_version, 'version_scheme': empty, 'root': '../' }

setup(
    name=package_name,
    # version=package["version"],
    use_scm_version=_clean_version,
    setup_requires=['setuptools_scm'],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=['dash>=2.5.1'],
    classifiers=[
        'Framework :: Dash',
    ],
    author_email="info@ladybug.tools",
    long_description=package.get('description', package_name),
    url="https://github.com/pollination/pollination-dash-io",
    python_requires=">=3.7",
)
