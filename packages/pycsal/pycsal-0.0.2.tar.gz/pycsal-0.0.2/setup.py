import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycsal",
    version="0.0.2",
    author="Jialu Chen",
    author_email="jialu.chen@ist.ac.at",
    description=
    "Python crystal search with active learning (pycsal)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phys-chem/pycsal/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'mendeleev', 'asap', 'pyxtal'
    ],
    python_requires='>=3.7')
