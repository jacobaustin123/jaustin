import setuptools
import json

def get_version_info(path):
    with open(path, "r") as f:
        config = json.load(f)

    major, minor, patch = config['version'].split('.')
    version = major + "." + minor + "." + str(int(patch) + 1)
    config['version'] = version

    with open(path, "w") as f:
        json.dump(config, f)
    
    print(f"current version is {version}.")

    return version

version = get_version_info("config.json")

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="jaustin", 
    version=version,
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


