from setuptools import setup
import codecs
import os


VERSION = '0.1.0'
DESCRIPTION = 'Unofficial Facebook Graph API Handler'
LONG_DESCRIPTION = 'A Facebook Graph API Handler to ease the use of Meta Graph APIs.'

setup(
    name="GraphHandler",
    version=VERSION,
    author="Ambar Rizvi",
    author_email="<brannstrom9911@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    py_modules=["GraphHandler"],
    package_dir={'' : 'src'},
    install_requires=['requests==2.31.0', 'typing==3.7.4.3'],
    keywords=['python', 'facebook', 'graph api', 'social media', 'instagram', 'meta', 'meta api'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
