import setuptools


setup_args = dict(
    name='scalyca',
    version='0.0.1',
    description='Simple Console Application with Logging, Yaml Configuration and Argparse',
    long_description='A framework for creating simple non-interactive console applications '
        'that require basic logging and parsing command argument with optional peristent configuration',
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
