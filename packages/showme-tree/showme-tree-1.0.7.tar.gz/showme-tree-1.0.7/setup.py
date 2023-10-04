from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="showme-tree",
    version="1.0.7",
    author="Sophia Shovkovy",
    packages=find_packages(),
    url="https://github.com/sshovkov/showme-folder-structure",
    entry_points={
        "console_scripts": [
            "showme-tree = showme_tree.main:main",
        ],
    },
    install_requires=[
        "gitignore-parser",
    ],
    description="A command-line tool that prints the folder and file structure of your VSCode project, excluding nested items of content in .gitignore.",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
