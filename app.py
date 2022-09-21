
import os
import hashlib
from datetime import datetime
import json
import platform
import humanize
import sys

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

# function for getting metadata for files and instantiating the objects


def getInfo(pathList, fileList):
    # get file info here given a list of paths

    for filePath in pathList:

        # call hashing function on each file
        sha256Hash = hashing(filePath)

        # get metadata
        # get file size and make it human readable
        fileSize = humanize.naturalsize(os.path.getsize(filePath))

        # get modification time and creation time for the current file
        modTimeStamp = os.path.getmtime(filePath)
        modTime = datetime.fromtimestamp(
            modTimeStamp).strftime('%Y-%m-%d--%H-%M-%S')
        createTimeStamp = os.path.getctime(filePath)
        createTime = datetime.fromtimestamp(
            createTimeStamp).strftime('%Y-%m-%d--%H-%M-%S')

        isDuplicate = False
        duplicateOf = []
        # instantiate model object and add data
        fd = FileData(filePath, sha256Hash, fileSize, modTime,
                      createTime, isDuplicate, duplicateOf)

        # append the object to the list
        fileList.append(fd)
    return fileList


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
        print("********************* No duplicate files found *********************")
    else:
        # create file name with current datetime
        outputFileName = "duplicates_" + str(datetime.now()) + ".json"

        # convert objects to json string
        json_string = json.dumps([x.__dict__ for x in dupeList], indent=4)
        # write the json string to json file
        with open(outputFileName, "w") as outfile:
            outfile.write(json_string)
        outfile.close()
        print("********************* Duplicates found. Duplicates written to json file *********************")
    return dupeList


# writes metadata to a json file
def writeMetadata(fileList):
    # write metadata to file
    mdFileName = "metadata_" + str(datetime.now()) + ".json"

    # convert objects to json string
    json_string = json.dumps([x.__dict__ for x in fileList], indent=4)
    # write the json string to json file
    with open(mdFileName, "w") as outfile:
        outfile.write(json_string)
    outfile.close()


def main():
    fileList = []
    pathList = []
    # find out which system, release, and version is being used
    print("System: " + str(platform.system()))
    print("Release: " + str(platform.release()))
    print("Version: " + str(platform.version()))

    userInput = input("Please provide a path or folder: ")
    if os.path.isdir(userInput):
        print("********************* User provided directory path *********************")
        # create list for containing file objects
        for (root, dirs, files) in os.walk(userInput, topdown=True):

            for file in files:
                # get absolute path using user input
                absPath = os.path.join(root, file)
                pathList.append(absPath)

    # if a file path is provided by user, get a second file path
    elif os.path.isfile(userInput):
        print("********************* User provided file path *********************")
        # save both file paths to pathList
        pathList.append(userInput)
        userInput2 = input("Please provide a second file path: ")
        if os.path.isfile(userInput2):
            pathList.append(userInput2)

        else:
            print("********************* Not a file or a directory *********************")
            sys.exit()

    else:
        print("********************* Not a file or a directory *********************")
        sys.exit()

    # calls getInfo to get metadata for files and use that information to create model objects
    getInfo(pathList, fileList)

    # calls dupeFinder to search for duplicate files and save duplicates to a file
    dupeFinder(fileList)

    # calls writeMetadata to output file metadata to a json file
    writeMetadata(fileList)


if __name__ == "__main__":
    main()
