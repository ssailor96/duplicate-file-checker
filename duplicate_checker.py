
import os
import hashlib
from datetime import datetime
import json
import platform
import humanize
import sys
import logging

# class for modeling file data


class FileData:
    def __init__(self, abs_path, sha256_hash, file_size, mod_time, create_time, is_duplicate, duplicate_of, delete_flag):
        self.absPath = abs_path
        self.sha256Hash = sha256_hash
        self.fileSize = file_size
        self.modTime = mod_time
        self.createTime = create_time
        self.isDuplicate = is_duplicate
        self.duplicateOf = duplicate_of
        self.deleteFlag = delete_flag

    def __repr__(self):
        return f'Absolute path: {self.absPath} \nFile hash: {self.sha256Hash} \nFile size: {self.fileSize} \nFile modified at: {self.modTime} \nFile created at: {self.createTime} \nDuplicate file: {self.isDuplicate} \nDuplicate of: {self.duplicateOf} \nDelete flag: {self.deleteFlag}'


# file deletion function
def delete_files(deletion_list, logger):
    for file in deletion_list:
        # delete all files in deletion_list and log their deletion
        os.remove(file)
        logger.info(file + " deleted!")
        print(file + " deleted!")
    return


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
            os.path.getmtime(file_path)).astimezone().isoformat()

        create_time = datetime.fromtimestamp(
            os.path.getctime(file_path)).astimezone().isoformat()

        is_duplicate = False
        duplicate_of = []
        delete_flag = None
        # instantiate model object and add data
        fd = FileData(file_path, sha256_hash, file_size, mod_time,
                      create_time, is_duplicate, duplicate_of, delete_flag)

        # append the object to the list
        file_list.append(fd)
    return file_list


# comparison function for finding duplicates between hashes
def dupe_finder(file_list, logger):
    dupe_list = []
    # check each object in list exactly once
    for i, x in enumerate(file_list):
        for y in file_list[i + 1:]:
            if x.sha256Hash == y.sha256Hash:

                # update duplicate info
                x.isDuplicate = True
                x.duplicateOf.append(y.absPath)
                y.isDuplicate = True
                y.duplicateOf.append(x.absPath)

                # append duplicates to dupe_list
                if x not in dupe_list:
                    dupe_list.append(x)
                if y not in dupe_list:
                    dupe_list.append(y)

    # go through list of file objects and determine whether to delete duplicates
    for file in file_list:
        # if the file isn't a duplicate set delete flag to False
        if file.isDuplicate == False:
            file.deleteFlag = False

        elif (file.isDuplicate == True) and (file.deleteFlag == None):
            # if the file is a duplicate and the delete flag is set to none prompt user to choose whether or not to delete files
            logger.info("Duplicate files found")
            print("The following files are duplicates of each other: ")

            # make a list of the current file and all its duplicates and print it
            output_dupes = file.duplicateOf[:]
            output_dupes.append(file.absPath)
            i = 1
            for dupe in output_dupes:
                print("(" + str(i) + ") " + dupe)
                i += 1

            # flag for determining whether output request should continue
            output_loop_flag = True
            while(output_loop_flag):
                # prompt user to choose which files to delete if any
                user_input = input(
                    "Enter '0' to keep all files. Otherwise, enter the numbers listed next to each file you would like to delete, separated by spaces.\n")

                # if input is 0, break from loop
                if user_input == "0":
                    logger.info("User chose to keep all files")
                    break
                else:
                    # clean up input
                    deletion_list = []
                    list_input = list(user_input)
                    # strip spaces from input
                    delete_selection = [z for z in list_input if z.strip()]

                    # loop through list and make sure every element is valid input
                    for selection in delete_selection:
                        if selection.isdigit() and 1 <= int(selection) <= i:
                            # need a check for reaching end of list
                            if selection == delete_selection[-1]:
                                output_loop_flag = False
                            continue
                        else:
                            logger.warning("Invalid input")
                            print("Invalid input")
                            break

            if user_input != "0":

                # make a new list using output_dupes and deletion list that contains paths
                #       with the associated delete numbers
                for file in delete_selection:
                    deletion_list.append(output_dupes[int(file)-1])

                # list of duplicates that won't be deleted
                flag_list = [x for x in output_dupes if x not in deletion_list]

                for file in file_list:
                    # if there is only one remaining in the set of duplicates, change its duplicate flag to false
                    if len(flag_list) == 1 and file.absPath == flag_list[0]:
                        file.isDuplicate = False
                    # set the delete flag to false for any duplicates that won't be deleted
                    for flagged_file in flag_list:
                        if file.absPath == flagged_file:
                            file.deleteFlag = False

                # set the delete flag to true for any file the user chooses to delete
                for file_to_delete in deletion_list:
                    for file in file_list:
                        if file_to_delete == file.absPath:
                            file.deleteFlag = True
                            # loop through all duplicateOf lists and remove any duplicates that will be deleted
                            for f in file_list:
                                for dupe in f.duplicateOf:
                                    if dupe == file.absPath:
                                        f.duplicateOf.remove(dupe)

                # call deletion function
                delete_files(deletion_list, logger)

            # set delete flags to false for all files if the user chooses to keep them
            else:
                for file_to_keep in output_dupes:
                    for file in file_list:
                        if file_to_keep == file.absPath:
                            file.deleteFlag = False

        else:
            continue

    # check if dupe_list is empty
    if not dupe_list:
        logger.info("No duplicate files")
        print("********************* No duplicate files found *********************")
    else:
        print("********************* Remaining duplicate files listed below *********************")
        # print all remaining duplicates to console along with the number of duplicates
        num_duplicates = 0
        for file in file_list:
            if file.isDuplicate == True and file.deleteFlag == False:
                num_duplicates = num_duplicates + 1
                print(file.absPath)
        print("Number of duplicate files remaining: " + str(num_duplicates))
        print("********************* See hash report file for more information *********************")

    return dupe_list


# function for generating output file
def output_data(file_list, logger):
    current_time = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    # create file name with current datetime
    output_file_name = "hash_report-" + current_time + ".json"

    # convert objects to json string
    json_string = json.dumps(
        [file.__dict__ for file in file_list if file.deleteFlag == False], indent=4)
    # write the json string to json file
    with open(output_file_name, "w") as outfile:
        outfile.write(json_string)
    logger.info("Hash report file created")
    outfile.close()
    logger.info("Session end")


def main():

    # create log file
    logging.basicConfig(filename="std.log",
                        format='%(asctime)s: %(levelname)s: %(message)s', filemode='a+')

    # create logger object and set threshold
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    logger.info("Session start")

    # find out which system, release, and version is being used
    print("System: " + str(platform.system()))
    print("Release: " + str(platform.release()))
    print("Version: " + str(platform.version()))

    # log system, release, and platform info
    logger.info("System: " + str(platform.system()))
    logger.info("Release: " + str(platform.release()))
    logger.info("Version: " + str(platform.version()))

    file_list = []
    path_list = []

    # get input from user and check if it is a path to a file or folder
    while(True):
        user_input = input("Please provide a path to a file or folder: ")
        # if input is correct, exit loop
        if os.path.isfile(user_input) or os.path.isdir(user_input):
            break
        # if input is invalid, loop again to reprompt user for correct input
        else:
            logger.warning("Invalid input")
            print("Invalid input")
            continue

    if os.path.isdir(user_input):
        print(
            "********************* User provided directory path *********************")
        # create list of file paths
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
        # prompt user for second file path and make sure input is correct
        while(True):
            user_input2 = input("Please provide a second file path: ")
            # if input is correct, exit loop
            if os.path.isfile(user_input2):
                path_list.append(user_input2)
                break
            # if input is invalid, loop again to reprompt user for correct input
            else:
                logger.warning("Invalid input")
                print("Invalid input")
                continue

    # calls get_info to get metadata for files and use that information to create model objects
    get_info(path_list, file_list)

    # calls dupe_finder to search for duplicate files and save duplicates to a file
    dupe_finder(file_list, logger)

    # calls output_data to create json output file
    output_data(file_list, logger)


if __name__ == "__main__":
    main()
