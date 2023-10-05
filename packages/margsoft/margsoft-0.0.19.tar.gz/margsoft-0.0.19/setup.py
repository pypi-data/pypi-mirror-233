import setuptools
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "datacollection"
AUTHOR_USER_NAME = "Codebugged-Research"
SRC_REPO = "src"


setuptools.setup(
    name="margsoft",
    version="0.0.19",
    author=AUTHOR_USER_NAME,
    description="data collection package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="thecodebugged@gmail.com",
    package_dir={'': "src"},
    python_requires=">=3.6",
    packages=setuptools.find_packages(where="src"),
    license="MIT",
    install_requires=['opencv-python',
                   'numpy',],
        classifiers=[
        'Intended Audience :: Developers', 'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3.6', 'Topic :: Utilities',
        'Programming Language :: Python :: 3.7', 'Topic :: Utilities',
        'Programming Language :: Python :: 3.8', 'Topic :: Utilities'
    ], )
