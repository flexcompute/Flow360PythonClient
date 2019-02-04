from setuptools import setup
version = 0.1
setup(
    name='flow360client',
    version=version,
    description='A Python API for Flow360 CFD solver',
    author='FlexCompute, Inc.',
    author_email='john@simulation.cloud',
    packages=['flow360client'],
    install_requires=['requests', 'warrant',
                      'aws-requests-auth', 'bcrypt', 'boto3']
)
