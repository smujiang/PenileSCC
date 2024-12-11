import os
import shutil

def encode_parent_folders(file_paths):
    """
    Extracts the parent folder names of each file in the list and encodes them with integer numbers.

    Parameters:
    file_paths (list): A list of file paths.

    Returns:
    dict: A dictionary mapping each unique parent folder name to an integer encoding.
    list: A list of encoded parent folder names corresponding to the file paths.
    """

    # Extract parent folder names
    parent_folders = [os.path.basename(os.path.dirname(file_path)) for file_path in file_paths]

    # Create a mapping from folder names to integers
    folder_to_int = {folder: idx for idx, folder in enumerate(sorted(set(parent_folders)))}

    # Encode the parent folders
    encoded_folders = [folder_to_int[folder] for folder in parent_folders]

    return folder_to_int, encoded_folders

    # # Example usage:
    # file_paths = [
    #     "/path/to/folder1/file1.txt",
    #     "/path/to/folder2/file2.txt",
    #     "/path/to/folder1/file3.txt",
    #     "/path/to/folder3/file4.txt"
    # ]
    #
    # folder_to_int, encoded_folders = encode_parent_folders(file_paths)
    # print("Folder to Integer Mapping:", folder_to_int)
    # print("Encoded Parent Folders:", encoded_folders)


def copy_files_to_target(source_files, target_directory):
    """
    Copies a list of files to a target directory.

    Parameters:
    source_files (list): A list of file paths to be copied.
    target_directory (str): The path to the target directory.
    """

    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Copy each file to the target directory
    for file in source_files:
        try:
            if os.path.isfile(file):
                shutil.copy(file, target_directory)
                print(f"Copied {file} to {target_directory}")
            else:
                print(f"Skipping {file}: Not a valid file")
        except Exception as e:
            print(f"Failed to copy {file}: {e}")

# Example usage:
# source_files = ['file1.txt', 'file2.txt', 'file3.txt']
# target_directory = '/path/to/target/directory'
# copy_files_to_target(source_files, target_directory)


def encode_integers_to_colors(int_list):
    # Define a list of colors to map to the integers
    color_map = [
        "red", "green", "blue", "yellow", "purple",
        "orange", "cyan", "magenta", "lime", "pink"
    ]

    # Map integers to colors
    encoded_colors = []
    for num in int_list:
        # Use modulo operation to cycle through colors if the integer is larger than the color_map size
        color = color_map[num % len(color_map)]
        encoded_colors.append(color)

    return encoded_colors
#
# # Example usage
# integers = [1, 2, 5, 8, 10, 15, 20, 30, 40, 50]
# encoded_colors = encode_integers_to_colors(integers)
# print(encoded_colors)




