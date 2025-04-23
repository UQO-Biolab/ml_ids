import shutil
import gzip
import os

def decompress_gz_files(log_path, output_directory):
    # Check if the output directory exists, otherwise create it
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all files in the input directory
    for filename in os.listdir(log_path):
        # Checks if the file is a .gz file
        if filename.endswith('.gz'):
            # Full path to the .gz file
            file_path = os.path.join(log_path, filename)

            # Name of the unzipped file
            decompressed_filename = filename[:-3]  # Remove .gz extension
            decompressed_file_path = os.path.join(output_directory, decompressed_filename)

            # Unzip file
            with gzip.open(file_path, 'rb') as f_in:
                with open(decompressed_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            print(f"Unzipped file: {filename} -> {decompressed_filename}")