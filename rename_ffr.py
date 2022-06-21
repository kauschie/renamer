import os


# takes a dictionary of file names and makes a new dictionary with the full file path
# needed to wait until just before renaming so that there werent accidents with other  
# subdirectories. Returns the new dictionary.
def make_file_paths(dictionary, directory):
    new_dictionary = {}
    keys_to_del = []
    for key, value in dictionary.items():
        new_key = directory+"\\"+key
        new_value = directory+"\\"+value
        new_dictionary[new_key] = new_value
    del dictionary
    return new_dictionary


# function to cull the list of possibles down to ones
# with only the valid file extension passed as a string
# returns a list of matching file names back to main()
def getWorkingSet(originals, extension_list):
    # if the extension list is empty, return the original list as
    # the working list
    if len(extension_list) == 0:
        return originals
    list_of_matches = []
    for file in originals:
        extension = getExtension(file) # gets file extension and checks against
        if extension in extension_list: # extension_list and appends file to
            list_of_matches.append(file) # list of matches if it's ext is in.
    return list_of_matches


# function takes old file name and takes out identifier
def howToRenameFiles(list_of_files, directory):
    # dictionary for renaming files.
    # {key:} is the string of the current file name,
    # {:value} is the string to set the new name of the file
    renameDict = {}
    filePathDict = {}
    print("How do you want to rename the files?")
    print("Enter '1' to shorten the names at a configurable delimiter")
    while True:
        response = input('Enter your response here: ')
        if response == '1':
            renameDict = rn_shorten(list_of_files)
            filePathDict = make_file_paths(renameDict, directory)
            rename(filePathDict)
            print('Done.')
            break
        else:
            print(f"I didn't understand {response}")
            print("You need to enter a valid response.")


# takes a renaming dictionary as input
# {key:} is the current file name; {:value} is the new file name
def rename(rename_dictionary):
    for key in rename_dictionary:
        if os.path.isfile(rename_dictionary[key]) == True:
            newValue = addOne(rename_dictionary[key])
            os.rename(key,newValue)
        else:
            os.rename(key,rename_dictionary[key])


def addOne(filepath):
    newpath = ''
    i = 0
    substrings = filepath.split('.')
    for strg in substrings:
        newpath += strg
        if i == (len(substrings)-2):
            newpath += '(1).'
        i += 1
    return newpath


# creates a dictionary for renaming the files based on shortening behavior.
# {key:} is the string of the current file name,
# {:value} is the string to set the new name of the file
def rn_shorten(list_of_files):
    renameDict = {}
    delimiter = set_delimiter()
    newFileName = ''
    for file in list_of_files:
        substrings = []
        # splits string into multiple segements at the delimiter
        # there should be 2 substrings otherwise warnings are issued
        substrings = file.split(delimiter)
        if len(substrings) <= 1:
            print("**************** WARNING ********************************")
            print(f"'{delimiter}' was not found in file\n{file}\n so it will"
                  f" not be renamed")
        if len(substrings) > 2:
            print(f"***WARNING*** your delimiter '{delimiter}' was found <!>"
            f"{len(substrings)-1}<!> times on file:\n{file}\n Choosing to "
            "continue will cut the filename closest to the end of the "
            "string. Do you wish to continue?:")
            response = yes_no_Q()
            if response == True:
                newFileName = makeFileName(substrings)
                renameDict[file] = newFileName
        if len(substrings) == 2:
            newFileName = makeFileName(substrings)
            renameDict[file] = newFileName
    return renameDict

def yes_no_Q():
    while True:
        response = input("'yes' or 'no': ").lower()
        if response == 'yes':
            return True
        elif response == 'no':
            return False
        else:
            print(f"I didn't understand '{response}'")

def makeFileName(list_of_substrings):
    newFileName = ''
    extension = getExtension(list_of_substrings[len(list_of_substrings)-1])
    list_of_substrings[len(list_of_substrings)-1] = '.'
    list_of_substrings.append(extension)
    for substring in list_of_substrings:
        newFileName += substring
    return newFileName


def getExtension(string):
    extPosition = string.rfind(".")
    return string[extPosition+1:]


#
def set_delimiter():
    while True:
        delimiter = input("Enter the case sensitive 'id' string: ")
        print(f"Confirming '{delimiter}' is correct?")
        answer = yes_no_Q()
        if answer == True:
            return delimiter
        else:
            print("It's OK mistakes happen.")


# prompts user to confirm if list is accurate
# returns True or False back to getFileExtList
def confirmList(list_to_confirm):
    print("Here is the current list:\n")
    print(list_to_confirm)
    print('Is this correct?')
    while True:
        response = yes_no_Q()
        if response == True:
            return True
        elif response == False:
            return False


# prompts the user for a list of file extensions
# calls confirmList to confirm the list with the user
# returns the list to setFileExtension
def getFileExtList():
    fileExtList = []
    print("Enter file extensions that are to be included")
    print("One entry at a time")
    print("return 'done' when you are finished")
    while True:
        entry = input("Enter your response here: ").lower()
        if entry == 'done':
            confirmation = confirmList(fileExtList)
            if confirmation == True:
                return fileExtList
            if confirmation == False:
                fileExtList = []
        else:
            fileExtList.append(entry)


# Asks the user to specify file types to be used for renaming
# returns the list of file type extensions or an empty list
def setFileExtension():
    fileExtList = []
    print('Do you want want to:\n'
          '1) Work on ALL files\n'
          ' -------- or -------- \n'
          '2) Work on a specific file type')
    while True:
        response = input('Enter your answer here: ')
        if response == '1':
            return fileExtList
        elif response == '2':
            fileExtList = getFileExtList()
            return fileExtList
        else:
            print("I didn't understand that")


# Removes directories from the working list
# Returns the list culled of the directories
def cullDirectories(directory, original_list):
    files = []
    for item in original_list:
        temp = directory + "\\" + item
        if os.path.isfile(temp) == True:
            files.append(item)
    return files


# checks to see if the currently set directory is correct
# returns True or False
def correctDirectory(filepath):
    print("The current directory that is set to be sorted is:\n")
    print(f"({filepath})")
    while True:
        print('Do you wish to use this as the working directory?')
        response = input("'yes' or 'no': ").lower()
        if response == 'yes':
            return True
        elif response == 'no':
            return False
        else:
            print("I didn't understand what you meant.")


# Sets and returns the correct file path
def fixDirectory():
    while True:
        workingDir = input("Enter the correct file path: ")
        while True:
            print(f"You entered ({workingDir})")
            response = input("Is this correct? 'yes' or 'no' ").lower()
            if response == 'yes':
                if os.path.isdir(workingDir) == True:
                    return workingDir
                else:
                    print('I could not locate that directory, try again')
                    break
            else:
                break


# Sets the working directory to
def getDirectory():
    workingDir = os.getcwd()
    if correctDirectory(workingDir) == True:
        return workingDir
    else:
        workingDir = fixDirectory()
        return workingDir


def introduction():
    print("This program will rename files in a directory.")


def rename_ffr():
    introduction()
    directory = getDirectory()  # Prompts user to set working directory
    originals = os.listdir(directory)  # Gets a list of everything in directory
    files = cullDirectories(directory, originals)
    extension = setFileExtension()
    working_set = getWorkingSet(files, extension)
    howToRenameFiles(working_set, directory)

rename_ffr()


