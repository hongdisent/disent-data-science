import zipfile

def compress_files(file_list, output_path):
    """
    Compress multiple files into a ZIP archive.
    
    :param file_list: List of file paths to be compressed.
    :param output_path: Path to the output ZIP file.

    # Example
    # if __name__ == "__main__":
    #     file_list = [r"S:\TheNewDisent\UX Assets\world\Getting Started\Data_nerd\Common_utility\File_Handling\text1.txt"]
    #     output_zip = "compressed_files.zip"
    #     compress_files(file_list, output_zip)

    """

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in file_list:
            zipf.write(file, arcname=file.split('/')[-1])
    
    print(f"Files compressed successfully into {output_path}")


