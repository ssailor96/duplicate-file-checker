# Duplicate File Checker

This application checks for duplicate files. It can compare two provided files or compare all files in a provided directory. The program creates a json file listing metadata and hashes for each file and states whether or not those files are duplicates.

## Getting Started
### Prerequisites

- Python 3
- humanize package

### Installation

1. Clone the repository to your machine
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install the requirements: `pip install -r requirements.txt`


## Using the Application

When the program is run, it outputs the system, release, and version of the platform being used to the console. It then prompts the user to provide either the path to a file or a path to a directory. If a path to a file is provided, the program prompts the user to provide the path to a second file. If a directory is provided, the application will examine all files not only in the directory itself but also in all its subfolders.

To check if two files are the same, enter a path to a file. To check for duplicates in an entire directory, enter a path to a directory.

The application takes all files provided and gets their metadata as well as their hashes. It checks for duplicates by comparing the hashes of each file. If a duplicate is found, the paths for duplicate files and the number of duplicates are printed to the console in the following format:

```
********************* Duplicate files found! Duplicates listed below *********************
sampleFile.txt
sampleFile2.txt
sampleFile3.txt
Number of duplicate files found: 3
```
If no duplicates are found, the user will be informed via the console:

`********************* No duplicate files found *********************`

The metadata, hashes, and list of duplicates for each duplicate file are saved to a file titled "hash_report-*currentdatetime*.json" in the following format:

```
{
    "absPath": "sampleFile.txt",
    "sha256Hash": "SAMPLE FILE HASH",
    "fileSize": "SAMPLE FILE SIZE",
    "modTime": "SAMPLE FILE MODIFICATION TIME",
    "createTime": "SAMPLE FILE CREATION TIME",
    "isDuplicate": true,
    "duplicateOf": [
        "sampleFile2.txt",
        "sampleFile3.txt"
    ]
}
```



## Outputs

- hash_report-*currentdatetime*.json

## Notes

- Make sure to use correct input (a path to a file or directory). If incorrect input is used, the program will exit and need to be run again.
- The path provided must be an absolute path.

## License

This application is licensed under an MIT License. See the [License](https://github.com/ssailor96/duplicate-file-checker/blob/main/LICENSE) file for details.