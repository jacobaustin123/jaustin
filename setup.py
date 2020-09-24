import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jaustin", 
    version="0.0.1",
    author="Jacob Austin",
    url="https://github.com/jacobaustin123/jaustin",
    author_email="jacob.austin@columbia.edu",
    description="A set of core Python utilities for machine learning and general programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


