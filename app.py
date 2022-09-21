
import os
import hashlib
from datetime import datetime
import json
import platform
import humanize

# class for modeling file data


class FileData:
    def __init__(self, absPath, sha256Hash, fileSize, modTime, createTime, isDuplicate, duplicateOf):
        self.absPath = absPath
        self.sha256Hash = sha256Hash
        self.fileSize = fileSize
        self.modTime = modTime
        self.createTime = createTime
        self.isDuplicate = isDuplicate
        self.duplicateOf = duplicateOf

    def __repr__(self):
        return f'Absolute path: {self.absPath} \nFile hash: {self.sha256Hash} \nFile size: {self.fileSize} \nFile modified at: {self.modTime} \nFile created at: {self.createTime} \nDuplicate file: {self.isDuplicate} \nDuplicate of: {self.duplicateOf}'


# hashing function


def hashing(pathToFile):

    # buffer size variable
    BUF_SIZE = 66536
    # initialize  sha method
    sha256 = hashlib.sha256()

    # open the file with the given file path
    with open(pathToFile, 'rb') as file:
        while True:
            fileContents = file.read(BUF_SIZE)

            # end when end of file is reached
            if not fileContents:
                break

            # pass the file contents to the hash function, outputs hash object
            sha256.update(fileContents)

    # return hash as a string in hexidecimal format
    return sha256.hexdigest()


# comparison function for finding duplicates between hashes
def dupeFinder(fileList):
    dupeList = []
    # check each object in list exactly once
    for i, x in enumerate(fileList):
        for y in fileList[i + 1:]:
            if x.sha256Hash == y.sha256Hash:

                # update duplicate info
                x.isDuplicate = True
                x.duplicateOf.append(y.absPath)
                y.isDuplicate = True
                y.duplicateOf.append(x.absPath)

                # append duplicates to dupeList
                if x not in dupeList:
                    dupeList.append(x)
                if y not in dupeList:
                    dupeList.append(y)

    # check if dupeList is empty
    if not dupeList:
        print("*********************No duplicate files found!*********************")
    else:
        # create file name with current datetime
        outputFileName = "duplicates_" + str(datetime.now()) + ".json"

        # convert objects to json string
        json_string = json.dumps([x.__dict__ for x in dupeList], indent=4)
        # write the json string to json file
        with open(outputFileName, "w") as outfile:
            outfile.write(json_string)
        outfile.close()
        print("*********************Duplicates found! Duplicates written to json file*********************")
    return dupeList


def main():
    fileList = []
    # find out which system, release, and version is being used
    print("System: " + str(platform.system()))
    print("Release: " + str(platform.release()))
    print("Version: " + str(platform.version()))

    userInput = input("Please provide a path or folder: ")
    if os.path.isdir(userInput):
        print("*********************User provided directory*********************")
        # create list for containing file objects
        for (root, dirs, files) in os.walk(userInput, topdown=True):

            for file in files:
                # get absolute path using user input
                absPath = os.path.join(root, file)

                # call hashing function on each file
                sha256Hash = hashing(absPath)

                # get metadata
                # get file size and make it human readable
                fileSize = humanize.naturalsize(os.path.getsize(absPath))

                # get modification time and creation time for the current file
                modTimeStamp = os.path.getmtime(absPath)
                modTime = datetime.fromtimestamp(
                    modTimeStamp).strftime('%Y-%m-%d--%H-%M-%S')
                createTimeStamp = os.path.getctime(absPath)
                createTime = datetime.fromtimestamp(
                    createTimeStamp).strftime('%Y-%m-%d--%H-%M-%S')

                isDuplicate = False
                duplicateOf = []
                # instantiate model object and add data
                fd = FileData(absPath, sha256Hash, fileSize, modTime,
                              createTime, isDuplicate, duplicateOf)

                # append the object to the list
                fileList.append(fd)
        dupeFinder(fileList)

        # write metadata to file
        mdFileName = "metadata_" + str(datetime.now()) + ".json"

        # convert objects to json string
        json_string = json.dumps([x.__dict__ for x in fileList], indent=4)
        # write the json string to json file
        with open(mdFileName, "w") as outfile:
            outfile.write(json_string)
        outfile.close()
        for x in fileList:
            print(repr(x))

    elif os.path.isfile(userInput):
        print("*********************User provided file*********************")
        # if a path to a file is provided, prompt for a second path
        userInput2 = input("Please provide a second path: ")
        if os.path.isfile(userInput2):
            # get hashes for both files
            sha256Hash1 = hashing(userInput)
            sha256Hash2 = hashing(userInput2)

            # get metadata
            fileSize1 = humanize.naturalsize(os.path.getsize(userInput))
            fileSize2 = humanize.naturalsize(os.path.getsize(userInput2))

            modTime1 = os.path.getmtime(userInput)
            modTime2 = os.path.getmtime(userInput2)

            # get modification and creation time for file 1
            modTimeStamp1 = os.path.getmtime(userInput)
            modTime1 = datetime.fromtimestamp(
                modTimeStamp1).strftime('%Y-%m-%d--%H-%M-%S')
            createTimeStamp1 = os.path.getctime(userInput)
            createTime1 = datetime.fromtimestamp(
                createTimeStamp1).strftime('%Y-%m-%d--%H-%M-%S')

            # get modification and creation time for file 2
            modTimeStamp2 = os.path.getmtime(userInput2)
            modTime2 = datetime.fromtimestamp(
                modTimeStamp2).strftime('%Y-%m-%d--%H-%M-%S')
            createTimeStamp2 = os.path.getctime(userInput2)
            createTime2 = datetime.fromtimestamp(
                createTimeStamp2).strftime('%Y-%m-%d--%H-%M-%S')

            isDuplicate = False
            duplicateOf = []
            # instantiate objects and append to list
            fd = FileData(userInput, sha256Hash1, fileSize1, modTime1,
                          createTime1, isDuplicate, duplicateOf)
            fileList.append(fd)
            fd = FileData(userInput2, sha256Hash2, fileSize2, modTime2,
                          createTime2, isDuplicate, duplicateOf)
            fileList.append(fd)

            # call comparison function
            dupeFinder(fileList)
            # write metadata to file
            mdFileName = "metadata_" + str(datetime.now()) + ".json"

            # convert objects to json string
            json_string = json.dumps([x.__dict__ for x in fileList], indent=4)
            # write the json string to json file
            with open(mdFileName, "w") as outfile:
                outfile.write(json_string)
            outfile.close()

        else:
            print("*********************Not a file or a directory*********************")

    else:
        print("*********************Not a file or a directory*********************")


if __name__ == "__main__":
    main()
