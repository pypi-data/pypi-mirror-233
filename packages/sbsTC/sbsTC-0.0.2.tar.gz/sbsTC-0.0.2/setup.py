import setuptools

_VERSION = '0.0.2'
_PROJECT_NAME = 'sbsTC'

with open('README.md','r') as fh:
    long_description = fh.read()
    
setuptools.setup(
    name=_PROJECT_NAME,
    version=_VERSION,
    packages=setuptools.find_packages(),
    url='https://github.com/cdeazambuja/sbsTC',
    license='GNU General Public License v3.0',
    author='Cesar De Azambuja',
    author_email='cdeazambuja@gmail.com',
    description='Get the official exchange rate of the SBS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.10',
    install_requires=[
        'pandas',
        'numpy',
        'lxml'
    ],
    # PyPI package information.
    classifiers=sorted([
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]),
)