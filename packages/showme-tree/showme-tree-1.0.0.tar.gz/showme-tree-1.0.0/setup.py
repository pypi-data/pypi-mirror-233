from setuptools import setup, find_packages

setup(
    name="showme-tree",
    version="1.0.0",
    packages=find_packages(where="showme-folder-structure"),
    entry_points={
        "console_scripts": [
            "showme-tree = showme_tree.main:main",
        ],
    },
    install_requires=[
        "gitignore-parser",
    ],
)
