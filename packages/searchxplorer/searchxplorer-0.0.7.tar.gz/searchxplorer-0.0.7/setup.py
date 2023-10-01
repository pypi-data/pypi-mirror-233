from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.7'
DESCRIPTION = 'searchxplorer is a Python library that empowers developers with powerful search algorithms for efficient data exploration and retrieval.'
LONG_DESCRIPTION = 'searchxplorer is a versatile Python library designed to simplify data exploration and retrieval tasks. Leveraging a set of robust search algorithms, including linear and binary search, SearchXplorer empowers developers to efficiently locate and retrieve information within their datasets, be it searching for specific values in unsorted lists or quickly finding elements in sorted arrays.'

# Setting up
setup(
    name="searchxplorer",
    version=VERSION,
    author="HD7(Harshit)",
    author_email="<mail@HD7.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['search', 'exploration', 'Python library', 'data retrieval', 'search algorithms', 'linear search', 'binary search', 'data exploration', 'data navigation', 'data analysis', 'data retrieval', 'data search', 'search utility', 'data exploration library', 'efficient search', 'Python development', 'Python programming', 'developer tools', 'open-source', 'code library'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)