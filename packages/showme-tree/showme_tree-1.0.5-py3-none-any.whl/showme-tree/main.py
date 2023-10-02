import os
from gitignore_parser import parse_gitignore


def main():
    # Find the root directory
    project_path = find_project_root()

    if os.path.exists(project_path):
        display_project_structure(project_path)
    else:
        print("No indicators of a version-controlled project root found.")
        project_path = input("Please enter the path of the VSCode project: ")

        if os.path.exists(project_path):
            display_project_structure(project_path)
        else:
            print("Invalid project path. Please enter a valid path.")


def find_project_root():
    current_directory = os.getcwd()

    # Iterate upwards in the directory hierarchy until a .git directory is found
    while not os.path.exists(os.path.join(current_directory, ".git")):
        if current_directory == os.path.dirname(current_directory):
            return None
        current_directory = os.path.dirname(current_directory)
    return current_directory


def display_project_structure(project_path):
    # Get .gitignore path
    gitignore_path = os.path.join(project_path, ".gitignore")

    if os.path.exists(gitignore_path):
        matches = parse_gitignore(gitignore_path)
    else:
        # If there is no .gitignore file, set matches to a function that always returns False
        matches = lambda path: False

    print(f"VSCode Project Structure for: {project_path}\n")
    print_folder_structure(project_path, matches)


def print_folder_structure(folder_path, matches, indent=0):
    # Get the folder name with a trailing '/' if it's a directory
    folder_name = (
        os.path.basename(folder_path) + "/"
        if os.path.isdir(folder_path)
        else os.path.basename(folder_path)
    )
    # Print the current folder with appropriate indentation
    print("    " * indent + "|---" + folder_name)

    # If the current folder is in .gitignore or is the .git folder, return without printing its contents
    if matches(folder_path) or os.path.basename(folder_path) == ".git":
        return

    # List all files and subdirectories in the current folder
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        # If the item is a directory, recursively print its structure
        if os.path.isdir(item_path):
            print_folder_structure(item_path, matches, indent + 1)
        else:
            # If it's a file, print its name with proper indentation
            print("    " * (indent + 1) + "|---" + item)


if __name__ == "__main__":
    main()
