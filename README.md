# mri_dicom_checker
A simple command‑line tool to extract ZIP or CAB archives, sanitize DICOM filenames, test each file’s integrity with `dcmftest`, and output CSVs of valid and corrupt files.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [How It Works](#how-it-works)
6. [Function Reference](#function-reference)
7. [Example](#example)
8. [Cleanup & Temp Files](#cleanup--temp-files)
9. [Contributing](#contributing)
10. [License](#license)

---

## Features

* Unpacks `.zip` or `.cab` archives
* Recursively finds `.dcm` (DICOM) files
* Removes spaces and `#` characters from filenames and directories
* Runs `dcmftest` on each DICOM file to check for corruption
* Produces two CSV reports: valid and corrupt file lists
* Cleans up temporary extraction directory automatically

## Prerequisites

* Python 3.6+ installed
* `dcmftest` available in your PATH (part of the DCMTK toolkit)
* `cabextract` available in your PATH (for CAB support)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-org/dicom-validator.git
   cd dicom-validator
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install any Python dependencies (standard library only for this script):

   ```bash
   pip install --upgrade pip
   # No extra packages needed
   ```

## Usage

```bash
python validate_archives.py <path/to/archive.zip>
```

* Replace `<path/to/archive.zip>` with your `.zip` or `.cab` file.
* Two CSVs will be created in the `output/` folder, named:

  * `<archive_name>_valid_file.csv`
  * `<archive_name>_corrupt_file.csv`

## How It Works

1. **Argument parsing**: Expects exactly one argument (the archive path).
2. **Extraction**: Uses Python’s `zipfile` or external `cabextract` to unpack to a temp folder.
3. **Sanitization**: Walks the extracted tree, renames files/dirs to strip spaces and `#`.
4. **Discovery**: Finds every file ending in `.dcm` (case‑insensitive).
5. **Validation**: Calls `dcmftest <file>` for each DICOM, categorizes based on output prefix (`yes:` vs `no:`).
6. **Reporting**: Writes two CSVs listing absolute paths of valid vs corrupt files.
7. **Cleanup**: Deletes the temporary extraction directory.

## Function Reference

* `unzip_file(zip_path, extract_to)`: Extracts a ZIP archive.
* `extract_archive(archive_path, extract_to)`: Chooses ZIP or CAB extraction.
* `sanitize_filenames(directory)`: Removes spaces and `#` in all files and directories.
* `find_dcm_files(directory) -> List[str]`: Returns full paths of `.dcm` files.
* `check_dcmftest(dcm_file) -> bool`: Runs `dcmftest`, returns True if valid.
* `write_csv(file_list, csv_path)`: Writes a list of file paths to a CSV.
* `main()`: Orchestrates argument parsing, extraction, validation, reporting, and cleanup.

## Example

```bash
# Given archive: scans.zip
python validate_archives.py scans.zip

# Output files created:
# output/scans_valid_file.csv
# output/scans_corrupt_file.csv
```

Open the CSVs in Excel or your favorite spreadsheet to review which DICOMs passed or failed the sanity check.

## Cleanup & Temp Files

The script uses a random temp directory (via Python’s `tempfile`) that is automatically removed after processing. Any failures during cleanup will be warned but won’t stop the script.

## Contributing

1. Fork the repo and create a feature branch.
2. Write tests (if adding features).
3. Submit a pull request with a clear description.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

