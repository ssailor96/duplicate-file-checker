# Duplicate File Checker

This application checks for duplicate files. It can compare two provided files or compare all files in a provided directory. The program creates a json file listing all duplicates as well as a json file containing metadata for the user to review.

## Prerequisites

- Python 3
- humanize package

## Using the Application

When the program is run, it outputs the system, release, and version of the platform being used to the console. It then prompts the user to provide either the path to a file or a path to a directory. If a path to a file is provided, the program prompts the user to provide the path to a second file.

To check if two files are the same, enter a path to a file. To check for duplicates in an entire directory, enter a path to a directory.

The application takes all files provided and gets their metadata as well as their hashes. The metadata, file paths, and hashes are saved to a file titled "metadata_*currentdatetime*.json".

The application checks for duplicates by comparing the hashes of each file. The user is notified through the console whether or not a duplicate has been found. If any duplicates are found, the metadata, hashes, and list of duplicates for each duplicate file are saved to a file titled "duplicates_*currentdatetime*.json".

## Outputs

- metadata_*currentdatetime*.json
- duplicates_*currentdatetime*.json

## Notes

- Make sure to use correct input (a path to a file or directory). If incorrect input is used, the program will exit and need to be run again.

## License

This application is licensed under an MIT License. See the [License](https://github.com/ssailor96/duplicate-file-checker/blob/main/LICENSE) file for details.