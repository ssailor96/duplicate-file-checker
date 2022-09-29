
import os
import hashlib
from datetime import datetime
import json
import platform
import humanize
import sys

# class for modeling file data


class FileData:
    def __init__(self, abs_path, sha256_hash, file_size, mod_time, create_time, is_duplicate, duplicate_of):
        self.abs_path = abs_path
        self.sha256_hash = sha256_hash
        self.file_size = file_size
        self.mod_time = mod_time
        self.create_time = create_time
        self.is_duplicate = is_duplicate
        self.duplicate_of = duplicate_of

    def __repr__(self):
        return f'Absolute path: {self.abs_path} \nFile hash: {self.sha256_hash} \nFile size: {self.file_size} \nFile modified at: {self.mod_time} \nFile created at: {self.create_time} \nDuplicate file: {self.is_duplicate} \nDuplicate of: {self.duplicate_of}'


# hashing function


def hashing(path_to_file):

    # buffer size variable
    BUF_SIZE = 66536
    # initialize  sha method
    sha256 = hashlib.sha256()

    # open the file with the given file path
    with open(path_to_file, 'rb') as file:
        while True:
            file_contents = file.read(BUF_SIZE)

            # end when end of file is reached
            if not file_contents:
                break

            # pass the file contents to the hash function, outputs hash object
            sha256.update(file_contents)

    # return hash as a string in hexidecimal format
    return sha256.hexdigest()

# function for getting metadata for files and instantiating the objects


def get_info(path_list, file_list):
    # get file info here given a list of paths

    for file_path in path_list:

        # call hashing function on each file
        sha256_hash = hashing(file_path)

        # get metadata
        # get file size and make it human readable
        file_size = humanize.naturalsize(os.path.getsize(file_path))

        # get modification time and creation time for the current file
        mod_time = datetime.fromtimestamp(
            os.path.getmtime(file_path)).isoformat()

        create_time = datetime.fromtimestamp(
            os.path.getctime(file_path)).isoformat()

        is_duplicate = False
        duplicate_of = []
        # instantiate model object and add data
        fd = FileData(file_path, sha256_hash, file_size, mod_time,
                      create_time, is_duplicate, duplicate_of)

        # append the object to the list
        file_list.append(fd)
    return file_list


# comparison function for finding duplicates between hashes
def dupe_finder(file_list):
    dupe_list = []
    # check each object in list exactly once
    for i, x in enumerate(file_list):
        for y in file_list[i + 1:]:
            if x.sha256_hash == y.sha256_hash:

                # update duplicate info
                x.is_duplicate = True
                x.duplicate_of.append(y.abs_path)
                y.is_duplicate = True
                y.duplicate_of.append(x.abs_path)

                # append duplicates to dupe_list
                if x not in dupe_list:
                    dupe_list.append(x)
                if y not in dupe_list:
                    dupe_list.append(y)

    # get current datetime and format as string
    current_time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    # create file name with current datetime
    output_file_name = "hash_report-" + current_time + ".json"

    # convert objects to json string
    json_string = json.dumps([x.__dict__ for x in file_list], indent=4)
    # write the json string to json file
    with open(output_file_name, "w") as outfile:
        outfile.write(json_string)
    outfile.close()

    # check if dupe_list is empty
    if not dupe_list:
        print("********************* No duplicate files found *********************")
    else:
        print("********************* Duplicate files found! Duplicates listed below *********************")
        # print all duplicates to console along with the number of duplicates
        num_duplicates = 0
        for x in file_list:
            if x.is_duplicate == True:
                num_duplicates = num_duplicates + 1
                print(x.abs_path)
        print("Number of duplicate files found: " + str(num_duplicates))
        print("********************* See hash report file for more information *********************")
    return dupe_list


def main():
    file_list = []
    path_list = []
    # find out which system, release, and version is being used
    print("System: " + str(platform.system()))
    print("Release: " + str(platform.release()))
    print("Version: " + str(platform.version()))

    user_input = input("Please provide a path or folder: ")
    if os.path.isdir(user_input):
        print("********************* User provided directory path *********************")
        # create list for containing file objects
        for (root, dirs, files) in os.walk(user_input, topdown=True):

            for file in files:
                # get absolute path using user input
                abs_path = os.path.join(root, file)
                path_list.append(abs_path)

    # if a file path is provided by user, get a second file path
    elif os.path.isfile(user_input):
        print("********************* User provided file path *********************")
        # save both file paths to path_list
        path_list.append(user_input)
        user_input2 = input("Please provide a second file path: ")
        if os.path.isfile(user_input2):
            path_list.append(user_input2)

        else:
            print("********************* Not a file or a directory *********************")
            sys.exit()

    else:
        print("********************* Not a file or a directory *********************")
        sys.exit()

    # calls get_info to get metadata for files and use that information to create model objects
    get_info(path_list, file_list)

    # calls dupe_finder to search for duplicate files and save duplicates to a file
    dupe_finder(file_list)


if __name__ == "__main__":
    main()
