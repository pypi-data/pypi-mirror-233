from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'Universities API Wrapper'
LONG_DESCRIPTION = 'Python package for consuming universities-domains-list API'

# Setting up
setup(
        name="universities-api-wrapper",
        version=VERSION,
        author="Juha Remes",
        author_email="jremes@outlook.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        url='https://github.com/jremes-foss/universities-api-wrapper/',
        download_url='https://github.com/jremes-foss/universities-api-wrapper/archive/refs/tags/0.0.5.tar.gz',
        install_requires=['requests', 'mock'],
        keywords=['python', 'api', 'wrapper', 'education', 'universities'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
