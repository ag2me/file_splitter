import os
import zipfile
import json
from datetime import datetime

def process_and_compress_chunk(file, chunk_size, output_folder, base_filename, filename_prefix=None):
    idx = 0
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break

        effective_filename = filename_prefix if filename_prefix else base_filename

        zip_filename = os.path.join(output_folder, f"{effective_filename}_part_{idx+1}.zip")
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.writestr(f"{effective_filename}_part_{idx+1}", chunk)
        
        print(f"Processed and compressed chunk {idx+1}")
        idx += 1

def main():
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return
    except FileNotFoundError:
        print("config.json not found.")
        return

    source_dir_backup = config.get("source_dir_backup")
    allowed_extensions = config.get("allowed_extensions", [])
    chunk_size = config.get("chunk_size", 10 * 1024 * 1024)
    filename_prefix = config.get("filename_prefix", "")
    folder_name = config.get("folder_name", "")
    use_current_date_as_folder = config.get("use_current_date_as_folder", False)

    if not source_dir_backup:
        print("Source directory not specified in config.json.")
        return
    elif not os.path.exists(source_dir_backup):
        print(f"Source directory '{source_dir_backup}' does not exist.")
        return

    destination_dir_backup = config.get("destination_dir_backup", ".")
    current_date = datetime.now().strftime('%Y-%m-%d') if use_current_date_as_folder else ""

    found_allowed_extension = False

    for root, dirs, files in os.walk(source_dir_backup):
        for file in files:
            _, extension = os.path.splitext(file)
            if allowed_extensions and extension not in allowed_extensions:
                continue

            found_allowed_extension = True

            file_path = os.path.join(root, file)
            base_filename_no_ext = os.path.splitext(os.path.basename(file_path))[0]
            
            folder_name_to_use = folder_name if folder_name else base_filename_no_ext
            destination_folder = os.path.join(destination_dir_backup, folder_name_to_use, current_date) if current_date else os.path.join(destination_dir_backup, folder_name_to_use)
            
            os.makedirs(destination_folder, exist_ok=True)
            base_filename = os.path.basename(file_path)

            print(f"Starting to process and compress: {base_filename}")

            try:
                with open(file_path, 'rb') as f:
                    process_and_compress_chunk(f, chunk_size, destination_folder, base_filename, filename_prefix)
            except Exception as e:
                print(f"An error occurred while processing {file}: {e}")

    if not found_allowed_extension:
        print("No files with the allowed extensions were found.")

    print("Process completed!")

if __name__ == "__main__":
    main()
