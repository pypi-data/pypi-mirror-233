import os
import setuptools


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="bbpp",
    version="0.0.1",
    author="Sergio Pena",
    author_email="isergiopena@gmail.com",
    description=("Monitor bitbucket pipelines and notify on macos any status change"),
    license="BSD",
    keywords="bitbucket monitor macos notify",
    url="https://www.github.com/sergiopena/bbpp",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'bbpp = bbpp:main'
        ]
    },
    install_requires=[
        'httpx==0.24.1'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
