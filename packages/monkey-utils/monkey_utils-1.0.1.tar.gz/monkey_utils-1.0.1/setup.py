import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "monkey_utils",
    version = "1.0.1",
    author = "Trung.HM",
    author_email = "trung.hoang@monkey.edu.vn",
    description = "Common function for project Monkey",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://pypi.org/project/monkey-utils/",
    project_urls = {
        "Bug Tracker": "https://github.com/eduhub123/monkey_utils",
    },
    install_requires=["boto3", "python-dotenv", "tqdm", "requests"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)