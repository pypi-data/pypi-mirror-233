# showme-tree

`showme-tree` is a command-line tool that prints the folder and file structure of your VSCode project, excluding files and folders specified in `.gitignore`.

## Installation

You can install `showme-tree` using pip:

```bash
pip install showme-tree
```

## Usage

Simply run the following command in your terminal to display the folder and file structure of your VSCode project:

```bash
showme-tree
```

Example Output:

```
|---showme-folder-structure/
    |---LICENSE
    |---dist/
    |---showme-tree/
        |---__init__.py
        |---main.py
    |---README.md
    |---setup.py
    |---.gitignore
    |---myenv/
    |---.git/
```
