import os
from setuptools import setup, find_packages

version_ns = {}
with open(os.path.join("blt_venv_mgr", "version.py")) as f:
    exec(f.read(), version_ns)
version = version_ns['VERSION']

install_requires = ["virtualenv"]

setup(
    name='blt_venv_mgr',
    version=version,
    packages=find_packages(),
    description='BLT Virtualenv Manager',
    install_requires=install_requires,
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering"
    ],
    keywords=[
        "virtualenv"
    ],
    entry_points={'console_scripts':
                  ['venv_man=blt_venv_mgr.venv_man:parse_args']
    },
    author='Ben Glick',
    author_email='glick@glick.cloud',
    license="Apache License, Version 2.0",
    url="https://github.com/benhg/blt-venv-mgr"
)