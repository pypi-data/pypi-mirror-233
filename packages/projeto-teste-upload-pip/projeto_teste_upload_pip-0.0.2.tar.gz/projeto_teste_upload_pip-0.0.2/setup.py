from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Projeto para a faculdade.'
LONG_DESCRIPTION = 'Projeto realizado para a matéria de laboratório de programação avançada.'

setup(
    name="projeto_teste_upload_pip",
    version=VERSION,
    author="Bruno Kalel",
    author_email="brunokalel@icluoud.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
