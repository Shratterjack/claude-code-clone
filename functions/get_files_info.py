import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    working_directory_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_path, directory))
    # Will be True or False
    valid_target_dir = (
        os.path.commonpath([working_directory_path, target_dir])
        == working_directory_path
    )
    if valid_target_dir is False:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    is_directory = os.path.isdir(target_dir)
    if is_directory is False:
        return f'Error: "{directory}" is not a directory'

    entries = os.listdir(target_dir)
    info = "Result for current directory:"

    for entry in entries:
        file_path = f"{target_dir}/{entry}"
        file_size = os.path.getsize(file_path)
        is_content_dir = os.path.isdir(file_path)
        content_info = (
            f"- {entry}: file_size={file_size} bytes, is_dir={is_content_dir}"
        )
        info = "\n".join([info, content_info])
    return info
