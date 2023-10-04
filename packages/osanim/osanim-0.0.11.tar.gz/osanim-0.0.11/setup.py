import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "osanim",
    version = "0.0.11",
    author = "Osanim Systems",
    author_email = "osanimsystems@gmail.com",
    description = "Business Utility Library",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/osanim/one_py",
    project_urls = {
        "Bug Tracker" : "https://github.com/osanim/one_py/-/issues",
        "repository" : "https://github.com/osanim/one_py"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "osanim"},
    packages = setuptools.find_packages(where="osanim"),
    python_requires = ">=3.6"
)