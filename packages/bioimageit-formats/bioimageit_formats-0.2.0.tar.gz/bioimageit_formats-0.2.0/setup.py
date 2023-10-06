import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bioimageit_formats",
    version="0.2.0",
    author="Sylvain Prigent and BioImageIT team",
    author_email="bioimageit@gmail.com",
    description="Manage data formats for BioImageIT project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bioimageit/bioimageit_formats",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "numpy",
        "pandas",
        "scikit-image>=0.18.3",
        "zarr>=2.12.0"
    ],
)
