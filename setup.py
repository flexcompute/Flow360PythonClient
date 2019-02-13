from setuptools import setup
version = 0.1
setup(
    name='flow360client',
    version=version,
    description='A Python API for Flow360 CFD solver',
    author='FlexCompute, Inc.',
    author_email='john@simulation.cloud',
    packages=['flow360client'],
    install_requires=['requests>=2.13.0', 'warrant==0.6.4',
                      'aws-requests-auth', 'bcrypt', 'boto3'],
    dependency_links=['http://github.com/flexcompute/warrant/tarball/master#egg=warrant-0.6.4']
)
