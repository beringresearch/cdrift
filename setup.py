from setuptools import find_packages, setup

def readme():
    with open("README.md") as f:
        return f.read()

# read version file
exec(open("cdrift/version.py").read())

setup(
    name="cdrift",
    author="Bering Limited",
    author_email="info@beringresearch.com",
    version=__version__, 
    description="Algorithms for concept drift detection.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/beringresearch/cdrift",
    license="Apache 2.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    
    install_requires=[
        "numpy>=1.16.2, <2.0.0",
        "scikit-learn>=0.20.2",
    ],
    test_suite="tests",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering",
    ],
)