import setuptools

with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sbsTC',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/cdeazambuja/sbsTC',
    license='GNU General Public License v3.0',
    author='Cesar De Azambuja',
    author_email='cdeazambuja@gmail.com',
    description='Get the official exchange rate of the SBS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pandas',
        'numpy',
        'lxml'
    ]
)