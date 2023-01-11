# Duplicate File Checker

This application checks for duplicate files. It can compare two provided files or compare all files in a provided directory. The program generates a log file as well as a json file listing metadata and hashes for each file and states whether or not those files are duplicates. It also deletes any duplicate files the user chooses.

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

Before the program is run, the user may add a config.json file to the directory the application files are in. This file may be used to set a desired location for output files, choose a hash algorithm, and set the path for an existing log file the user wants the program to write to. If no config file is provided or if any of the settings are invalid, default settings will be used. Hash algorithm choices include SHA256, MD5, and BLAKE2b. The default hash algorithm is SHA256, and the default location for output files and the log file is the directory that contains the application files. This is an example config file:

```
{
    "output location": "/Users/bobsmith/folder",
    "hash algorithm": "blake2b",
    "log file location": "/Users/bobsmith/folder2/std.log"
}
```

As soon as the program starts, it creates an array for storing logging information since the log file is not yet created. It configures settings as chosen by the user or sets them to defaults. Once settings are established, the log file is created and previously logged information is added to it. The program now starts logging in real time.

It then prompts the user to provide either the path to a file or a path to a directory. If a path to a file is provided, the program prompts the user to provide the path to a second file. If a directory is provided, the application will examine all files not only in the directory itself but also in all its subfolders.

To check if two files are the same, enter a path to a file. To check for duplicates in an entire directory, enter a path to a directory. The application takes all files provided and gets their metadata as well as their hashes. It checks for duplicates by comparing the hashes of each file. 

If no duplicates are found, the user will be informed via the console:

`********************* No duplicate files found *********************`

If duplicates are found, the paths for files that are duplicates of each other are printed to the console in the format shown below. The user will be prompted to either enter 0 to keep all the listed files, or enter the number of each one they want deleted, separated by spaces:

```
The following files are duplicates of each other: 
(1) sampleFile.txt
(2) sampleFile2.txt
(3) sampleFile3.txt
Enter '0' to keep all files. Otherwise, enter the numbers listed next to each file you would like to delete, separated by spaces.
```

If the user wanted to delete sampleFile.txt and sampleFile3.txt, for example, they would enter the following:
```
1 3
```

The program will move through each set of duplicates until they have all been chosen to be kept or deleted. Any remaining duplicate files the user chose to keep will have their paths printed to the console as well as the number of duplicate files remaining. 

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
    "deleteFlag": false
}
```
Deleted files will not have their information recorded.

## Log File

The program generates a log file with two types of messages: INFO and WARNING. If a log file already exists, it will be appended to instead. 

INFO messages are for:
- Stating the start or stop of a session
- System/release/version information
- Whether or not duplicates are found
- Whether or not duplicates are kept
- Which files are deleted
- Hash report creation

WARNING messages are only used for invalid user input.


## Inputs

- config.json (optional)
- std.log (optional)


## Outputs

- hash_report-*currentdatetime*.json
- std.log

## Notes

- Make sure to use correct input (a path to a file or directory). If incorrect input is used, the program will print "Invalid input" to the console and reprompt the user for input.
- The path provided must be an absolute path.
- Because all logging done prior to the creation of the log file must be dumped into the log file all at once, those logs will all have the same time stamp.

## License

This application is licensed under an MIT License. See the [License](https://github.com/ssailor96/duplicate-file-checker/blob/main/LICENSE) file for details.