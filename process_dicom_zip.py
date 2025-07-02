import os
import zipfile
import shutil
import subprocess
import csv
import tempfile

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def find_dcm_files(directory):
    dcm_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.dcm'):
                dcm_files.append(os.path.join(root, file))
    return dcm_files

def sanitize_filenames(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            old_path = os.path.join(root, name)
            new_name = name.replace('#', '').replace(' ', '')
            new_path = os.path.join(root, new_name)
            if old_path != new_path:
                os.rename(old_path, new_path)
        for name in dirs:
            old_path = os.path.join(root, name)
            new_name = name.replace('#', '').replace(' ', '')
            new_path = os.path.join(root, new_name)
            if old_path != new_path:
                os.rename(old_path, new_path)

def check_dcmftest(dcm_file):
    try:
        result = subprocess.run(['dcmftest', dcm_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        if output.startswith(f"yes: "):
            return True
        elif output.startswith(f"no: "):
            return False
        else:
            return False
    except Exception:
        return False

def write_csv(file_list, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['file_path'])
        for f in file_list:
            writer.writerow([f])

def extract_archive(archive_path, extract_to):
    if archive_path.lower().endswith('.zip'):
        unzip_file(archive_path, extract_to)
    elif archive_path.lower().endswith('.cab'):
        result = subprocess.run(['cabextract', '-d', extract_to, archive_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Error extracting CAB file: {archive_path}\n{result.stderr.decode()}")
            raise RuntimeError(f"Failed to extract CAB file: {archive_path}")
    else:
        raise ValueError(f"Unsupported archive type: {archive_path}")

def main():
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <zip_or_cab_file_path>")
        sys.exit(1)
    archive_path = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(archive_path))[0]
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    valid_csv = os.path.join(output_dir, f"{base_name}_valid_file.csv")
    corrupt_csv = os.path.join(output_dir, f"{base_name}_corrupt_file.csv")
    tmpdir = tempfile.mkdtemp()
    try:
        extract_archive(archive_path, tmpdir)
        sanitize_filenames(tmpdir)
        dcm_files = find_dcm_files(tmpdir)
        valid_files = []
        corrupt_files = []
        for dcm in dcm_files:
            if check_dcmftest(dcm):
                valid_files.append(dcm)
            else:
                corrupt_files.append(dcm)
        write_csv(valid_files, valid_csv)
        write_csv(corrupt_files, corrupt_csv)
    finally:
        try:
            shutil.rmtree(tmpdir)
        except Exception as e:
            print(f"Warning: Failed to delete temporary directory {tmpdir}: {e}")

if __name__ == '__main__':
    main()
