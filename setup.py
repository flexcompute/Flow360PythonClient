from setuptools import setup

version = '20.4.1.0';
setup(
    name='flow360client',
    version=version,
    description='A Python API for Flow360 CFD solver',
    author='FlexCompute, Inc.',
    author_email='john@simulation.cloud',
    packages=['flow360client'],
    install_requires=['requests>=2.13.0', 'aws-requests-auth', 'bcrypt', 'boto3'],
    dependency_links=['http://github.com/flexcompute/warrant/tarball/master#egg=warrant-0.6.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
