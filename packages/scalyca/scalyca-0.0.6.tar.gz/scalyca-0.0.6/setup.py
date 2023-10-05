import setuptools


with open('README.md') as f:
    __readme__ = f.read()

with open('LICENSE') as f:
    __license__ = f.read()


setup_args = dict(
    name='scalyca',
    version='0.0.6',
    description='Simple Console Application with Logging, Yaml Configuration and Argparse',
    long_description=__readme__,
    license='MIT',
    packages=setuptools.find_packages(),
    author="Martin Baláž",
    author_email='martin.balaz@trojsten.sk',
    keywords=['framework', 'console'],
    url='https://github.com/sesquideus/scalyca',
    download_url='https://pypi.org/project/scalyca/',
    include_package_data=True,
)

install_requires = [
    'argparse', 'pathlib', 'pyyaml', 'colorama', 'dotmap', 'schema',
]

if __name__ == '__main__':
    setuptools.setup(**setup_args, install_requires=install_requires)
