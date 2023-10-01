from setuptools import setup, find_packages

# Package metadata
NAME = 'MyPocket'
DESCRIPTION = 'Collect some interesting computation tools'
VERSION = '0.1.0'
AUTHOR = 'Molin Yue'
EMAIL = 'yuemolin@umich.edu'
URL = 'https://github.com/yuemolin/ToolBox'
LICENSE = 'MIT'

# Package dependencies
INSTALL_REQUIRES = [
    # List your dependencies here, e.g., 'numpy>=1.0'
]

# Additional package files (e.g., non-Python files)
# PACKAGE_DATA = {
#     'your_package_name': ['data/*.txt', 'data/*.csv'],
# }

# Package classifiers (https://pypi.org/classifiers/)
# CLASSIFIERS = [
#     'Development Status :: 3 - Alpha',
#     'Intended Audience :: Developers',
#     'License :: OSI Approved :: MIT License',
#     'Programming Language :: Python :: 3',
#     'Programming Language :: Python :: 3.x',
#     'Programming Language :: Python :: 3.y',
# ]

# Create the package
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=INSTALL_REQUIRES,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #package_data=PACKAGE_DATA,
    #classifiers=CLASSIFIERS,
)
