from cx_Freeze import setup, Executable

setup(
    name="LargeFileManager",
    version="0.1",
    description="A tool to split, compress, and restore large files.",
    executables=[Executable("split_and_zip.py")]  # replace 'file_chunker.py' with the name you chose for the script
)
