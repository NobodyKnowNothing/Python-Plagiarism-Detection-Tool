import os
import requests
import tkinter as tk
from tkinter import filedialog
import zipfile
import shutil
import copy


def downloadgithub(query, max_results, download_dir): # downloads github repositories by a query and the number to download
    repos = []
    # create download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # API search endpoint
    search_endpoint = "https://api.github.com/search/repositories"

    # search query
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results
    }

    # api request
    response = requests.get(search_endpoint, params=params)
    if response.status_code == 200:
        results = response.json()["items"]
        for index, result in enumerate(results, 1):
            repo_name = result["full_name"]
            repos.append(repo_name)
            download_url = result["html_url"] + "/archive/master.zip"
            download_path = os.path.join(
                download_dir, f"{repo_name.split('/')[-1]}_{index}.zip")
            print(f"Downloading {repo_name}...") # download the repository zip file
            download_response = requests.get(download_url)
            if download_response.status_code == 200:
                with open(download_path, "wb") as f:
                    f.write(download_response.content)
                print(f"Downloaded {repo_name} to {download_path}")
            else:
                print(f"Failed to download {repo_name}. Status code: {
                      download_response.status_code}")
    else:
        print("Failed to fetch GitHub search results.")
    return repos

class sortlines: # table class for organizing lines
    def __init__(self):
        self.storage = {}

    def insert(self, lst):
        # idea: iterate until duplicate key, if found stop, make list of similar lines, when done delete stored lines and start from duplicate key line

        key = str(lst[0])  # Using the list as key without space count
        if key in self.storage:
            self.storage[key].append(lst)
        else:
            self.storage[key] = [lst]
        return self.storage

    def get(self, key):
        res = False
        x = self.storage.get(key, [])
        if x != []:
            res = True
        return x, res

# [1, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], def main():\n


def linevec(line, count): # Defines line keys (vec cuz a list of nums is a vector) and returns a list of the key, the line and its line number
    linevec = [  
        [
            line.count(" "),
            line.count("(") + line.count(")"),
            line.count("[") + line.count("] ") + line.count("],"),
            line.count("{") + line.count("}"),
            line.count("="),
            line.count(":"),
            line.count("."),
            line.count(","),
            line.count("#"),
            line.count("'") + line.count('"'),
            line.count("')") + line.count('")'),
            line.count("('") + line.count('("'),
            line.count(" in "),
            line.count("if "),
            line.count("elif "),
            line.count("else:"),
            line.count("while "),
            line.count("def "),
            line.count("range("),
            line.count("for "),
            line.count("try:"),
            line.count("except:"),
            line.count("with "),
            line.count("return"),
            line.count(" True"),
            line.count(" False"),
            line.count("not "),
            line.count("is "),
            line.count(" as "),
            line.count("):\n"),
            line.count(")\n"),
            line.count("():\n"),
            line.count("()"),
            line.count("()\n"),
            line.count("]["),
            line.count(")["),
            line.count("))"),
            line.count("])"),
            line.count("))"),
            line.count("]."),
            line.count('f"'),
            line.count("f'"),
            line.count("+"),
            line.count("-"),
            line.count("*"),
            line.count("/"),
            line.count("%")],
        line,
        count
    ]
    return linevec


def orglines(file): # organizes lines into a list of lines with their keys 
    linesvec = []
    with open(file, "r") as file:
        for linnum, line in enumerate(file, start=1):
            if (line.count(" ") + 2) < len(line):
                linevec1 = linevec(line, linnum)
                linesvec.append(linevec1)

    return linesvec

def removeassign(suspect, empty): # iterates through the suspect file and removes all identical empty lines  
    emplines = sortlines()
    matches = []
    with open(empty, 'r') as file:
        for line in file: # stores empty file as a table
            line1 = [line]
            emplines.insert(line1)
    with open(suspect, 'r') as file1: # finds identical lines
        suslines = file1.readlines().copy()
        count = 0
        for y in suslines:
            x = emplines.get(str(y))
            if x[1]:
                matches.append(count)
            count += 1
    
    for num in matches:
        suslines[num] = "\n" # replaces the matching lines with 
    
    with open(suspect, 'w') as file2:
        file2.writelines(suslines)
            
    return matches

def matching(original, suspect): # matches plagiarised lines by storing original file lines as a table where the key is based on the control structures and python code (not variables or function names)
    file1, file2 = sortlines(), sortlines()
    similar, matches = [], []
    for vec in orglines(original):  # make original lines into keys
        file1.insert(vec)  # insert lines into table organized by keys
    with open(suspect, "r") as file:  # Organize suspect file into keys for original
        count = 0
        for line in file:
            count += 1
            if (line.count(" ") + 2) < len(line):  # Checks if the line is empty
                linevec1 = linevec(line, count)
                x2 = file1.get(str(linevec1[0]))
                if x2[1]:
                    similar.append([linevec1, x2[0]])

    similar = sorted(similar, key=lambda y: y[0][2])
    i = 0
    while i < len(similar) - 2:
        y = 0
        while y+i < len(similar) - 2:
            if similar[i][0][2] != ((similar[i+y][0][2] - y)):
                y -= 1
                break
            y += 1

        if (y >= 2) and (len(similar) >= i+y): # if there are 2 or more consecutive lines found within the originals table, look for correct specific lines within their slot on the table
            z, z1 = 0, 0
            # Multiple lines can be stored in the same spot in the table so this is to fix
            gap = similar[i+y][0][2] - similar[i][0][2]
            loop = True
            # Iterates through the table slots until it finds 2 original lines with a gap between them that is the same as the gap between the first and last suspect 
            for sim in similar[i+y][1]:
                z1 = 0
                for sim1 in similar[i][1]:
                    if sim[2] - sim1[2] == gap:
                        loop = False
                        break
                    z1 +=1
                if loop == False:
                    break
                z += 1
            try: # tries to append lines that are assumed to be correctly aligned
                matches.append([[similar[i][1][z1][1], similar[i][1][z1][2],
                                 similar[i+y][1][z][1], similar[i+y][1][z][2]], [similar[i][0][1], similar[i][0][2], similar[i+y][0][1], similar[i+y][0][2]]])
                similar[i][1][0+z1][2] = -100
                similar[i+y][1][0+z][2] = -100
                i += y
            except: # if it returns an error then the match was wrong and the alignment would never have worked
                if similar[i][1][z1-1][2] == -100:
                    print("Line alignment failure, disregard.")

        i += 1
    return matches

def filematch(zipfile1, zipfile2, num_matching_chars, writesus, search): # matches files within a zip file by a common string or set of last characters and extracts them
    # only extracts matched files from suspect if writesus is true
    matching_files = []

    # Extract folder names from zip file names (removing the extension)
    base_folder1 = os.path.splitext(os.path.basename(zipfile1))[0]
    base_folder2 = os.path.splitext(os.path.basename(zipfile2))[0]

    # Create base subfolders if they do not exist
    base_path1 = os.path.join('original', base_folder1)
    base_path2 = os.path.join('suspect', base_folder2)
    os.makedirs(base_path1, exist_ok=True)
    os.makedirs(base_path2, exist_ok=True)

    try:
        with zipfile.ZipFile(zipfile1, 'r') as zip1, zipfile.ZipFile(zipfile2, 'r') as zip2:
            file1_list = [file for file in zip1.namelist() if file.endswith('.py')]
            file2_list = [file for file in zip2.namelist() if file.endswith('.py')]
            
            for file1 in file1_list:
                for file2 in file2_list:
                    # following checks if the found python files have the search in their filepath and if the specified num of characters match counting from the end
                    if os.path.basename(file1)[:num_matching_chars] == os.path.basename(file2)[:num_matching_chars] and search.lower() in os.path.join(base_folder1, file1).lower() and search.lower() in os.path.join(base_folder2, file2).lower():
                        response = input(f"Are {os.path.join(base_folder1, file1)} and {os.path.join(base_folder2, file2)} correct matches? (yes/no/end): ")
                        if response.lower() == 'end':
                            return matching_files
                        elif "y" in response.lower():
                            # Constructing full paths including internal zip structure in order to make it easy to see where the file came from
                            original_path = os.path.join(base_path1, file1)
                            suspect_path = os.path.join(base_path2, file2)
                            
                            # Ensure subdirectories exist
                            os.makedirs(os.path.dirname(original_path), exist_ok=True)
                            os.makedirs(os.path.dirname(suspect_path), exist_ok=True)
                            
                            # Write files to their respective paths
                            with open(original_path, 'wb') as original_file:
                                original_file.write(zip1.read(file1))
                            if writesus: # Checks if it should overwrite the suspect file
                                with open(suspect_path, 'wb') as suspect_file:
                                    suspect_file.write(zip2.read(file2))
                            matching_files.append((original_path, suspect_path))
                            file2_list.remove(file2)  # Remove matched file to avoid duplicate matches
                            break
        if matching_files == []:
            print("No matching files found with given criteria")
    except FileNotFoundError:
        print("One or both zip files not found.")

    return matching_files

def listzips(folder_path): # lists zip files in given folder
    zip_files = []
    count = 0
    for file in os.listdir(folder_path):
        if file.endswith('.zip'):
            zip_files.append([file, count]) # makes into list
            count += 1
    return zip_files

def delete_folder(path): # deletes folder contents
    # check if the directory exists
    if not os.path.exists(path):
        os.makedirs(path)

    # Remove all contents of a directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)  # Remove directories
        else:
            os.remove(item_path)  # Remove files
            
def askreset(Force): # function to wipe temp files with bool to ask user or not
    check = False
    if not Force:
        if "y" in input("Would you like to delete all temporary files and wipe the save? (yes/no): ").lower():
            check = True
    if Force or check:
        try:
            delete_folder("./suspect")
            delete_folder("./original")
            delete_folder("./github_downloads")
            if os.path.exists("./save.txt"):
                os.remove("./save.txt")
            if check:
                print("'suspect', 'original' and 'github_downloads' folders are now cleared.")
        except:
            if check:
                print("Failure to clear temporary files, disregard.")

def end(): # Exit program menu
    if "y" in input("Would you like to use the tool again? (yes/no): ").lower():
        main()
    else:
        askreset(False)
        print('------------Goodbye-----------')
        exit()
    
def main():
    gutsuspect = False
    saved = False
    selectsus = False
    download = False
    repos = []
    downloadloc = "./github_downloads"
    root = tk.Tk()
    root.withdraw()
    print("-----")
    print("Welcome to the python plagiarism detection tool.\n")
    print("This tool looks for sections of code with similar formatting and control structures between 2 zipped python projects.")
    print("It ignores variables and function names in order to avoid the trap of comparing easily changed names.")
    print("Note: this tool should be expected to make some rare mistakes, punish only without a reasonable doubt.")
    print("Tip: you can say anything with y for yes and anything else for no.")
    print("-----")
    
    try: # Checks if save file exists via try/except
        with open('./save.txt', 'r') as save:
            if "y" in input("A previous save was found, would you like to use it? (yes/no): ").lower():
                # Loads save file if they want to load it
                saved = True
                saves = []
                for line in save: # Turns save file into list
                    try: # It doesnt like evaluating file paths so this is to catch it
                        saves.append(eval(line))
                    except:
                        saves.append(line)
                repos = saves[0] # Turn save file list into variables
                gutsuspect = saves[1]
                zip2 = saves[2][:-1]
                empty = saves[3]
                zip1 = saves[4][:-1]
            else:
                askreset(False) # Ask if they want to erase the save file
    except: # If save not found tells the user and sets saved to false
        print("No save was found or error reading save") 
        saved = False
        askreset(True)
    charmatch = 0
    if saved: # Checks if a save was loaded and asks if you want to select a new file
        if "y" in input("Would you like to use a new plagiarism suspect file? (yes/no): "):
            selectsus = True
    if not saved or selectsus: # Checks if you saved or if you wanted to overwrite it
        print("-----")
        print("The window specifies the suspect zip file.")
        print("-----")
        
        root.deiconify() # Makes file select window visible
        zip2 = filedialog.askopenfilename(title="Select the plagiarised zip") # Selecting plagiarised file
        while ".zip" not in zip2: # Checking for correct format
            print("You did not select a zip file, please select the zip of the plagiarised assignment")
            zip2 = filedialog.askopenfilename(title="Select the plagiarised zip")
        empty = "./test1.zip" # Testing
        root.withdraw() # Makes file select window invisible
    else:
        print("Suspect file retrieved from save")
    
    down = ""
    if saved: # if saved asks if you want to use the saved files or not
        if "y" in input("Would you like to download new original files from github? (yes/no): "):
            download = True
    if not saved or download:
        delete_folder("./github_downloads") # Clears downloads for new files
        if not saved: # if not saved, asks if they want to download github files
            down = input("To compare against the suspected file, would you like to download files from github? (yes/no): ")
        if "y" in down or download:
            download = True 
            resnum = input("How many search results would you like to compare against?: ") # Asks for the amount of repos to get from github
            while not resnum.isdigit(): # Makes sure input is int
                print("Input was not a number.")
                resnum = input("How many search results would you like to compare against?: ")
            repos = downloadgithub(input("Github query (Class code, assignment names can be to specific): "), int(resnum), downloadloc) # Downloads github files and returns the repo names
        else: # asks for a original file to compare suspect against for plagiarism
            # runs if they have no save and they dont want to download github files
            root.deiconify() # makes file window visible
            print("-----")
            print("The window specifies the original zip file to compare suspect to.")
            print("-----")
            zip1 = filedialog.askopenfilename(title="Select the original zip file (not suspect)") # asks for original zio file
            while ".zip" not in zip1: # checks if the selected file is a zip
                print("You did not select a zip file, please select the zip of an original file to compare suspect to")
                zip1 = filedialog.askopenfilename(title="Select the original zip file (not suspect)")
            root.withdraw() # makes file window invisible
    
    # Given an empty version of the suspected assignment, the following removes redundant assignment code from the suspected file to avoid false positives
    if saved: # Tells the user they can skip suspect trimming if they have already saved trimmed files
        print("If, during the last save, you already gave an empty assignment, and selected suspect files, that you intend to check now for plagiarism, you can say no to skip.")
    if "y" in input("Would you like to give a blank assignment (not an empty python file) to decrease potential false positives? (yes/no): ").lower():
        gutsuspect = True # bool representing if the files have been trimmed
        print("-----")
        print("The window specifies zip file to compare in order to remove redundant code from suspect.")
        print("-----")
        root.deiconify()
        empty = filedialog.askopenfilename(title="Select the empty assignment zip") # asks for the empty assignment file
        while ".zip" not in empty:
            print("You did not select a zip file, please select the zip of an empty assignment")
            zip2 = filedialog.askopenfilename(title="Select the empty assignment zip")
        root.withdraw()
        search = ""
        searchbool = input("Would you like to look at a specific assignment (folder or python file) within the zip files? (yes/no): ") # asks if they want to specify what potential files to compare
        if "y" in searchbool.lower():
            search = input("What string will always be in the name of the assignment? (a string that is in both assignments names in both zip files): ")
        gutfiles = filematch(empty, zip2, charmatch, True, search) # matches empty assignment files to suspect assignment and asks user if they are correct
        for gfile1, gfile2 in gutfiles:
                removeassign(gfile2, gfile1)  # removes lines from suspect that are exactly the same as empty assignment
        print("Removing redundant assignment code complete.")
    root.destroy() # Destroys tkinter window because its no longer used
        
    print("-----")
    print("The following specifies what files you want to compare for plagiarism.")
    print("-----")
    
    search = ""
    searchbool = input("Would you like to look at a specific assignment (folder or python file) within the zip files? (yes/no): ")
    if "y" in searchbool.lower():
        search = input("What string will always be in the name of the assignment? (a string that is in both assignments names in both zip files): ")
    if download: # if files were downloaded from github, make a list of them to iterate through
        zips = listzips(downloadloc)
    else: # if files were not downloaded, use the selected zip instead
        zips = [[zip1, 0]] 
    for zip_1, i in zips: # Iterates through downloaded zips
        print("-----")
        files = filematch(zip_1, zip2, charmatch, (not gutsuspect), search) # Matches original assignment files to suspect assignment and asks user if they are correct
        for file1, file2 in files: # Iterates through matched files
            origin = ""
            if download: 
                origin = f"from {repos[i]} on github\n" # if origin is from github, tell the user what repo
            else:
                origin = " " # if local origin then dont tell the user
            print(f"Now showing {file1} and {file2} {origin}") # Announces each file iteration to the user
            for i in matching(file1, file2): # finds similar lines between files based on python control structures and methods (not on specific characters between line
                print(f"-----\nMatch found at: {i[0][1]} to {i[0][3]} original lines, {i[1][1]} to {i[1][3]} plagiarised lines.\n") # Prints matched files to users
                print(f"Original border lines:\n{i[0][0]}{i[0][2]}\nPlagiarised border lines:\n{i[1][0]}{i[1][2]}")
    print("-----------Complete-----------")
    
    if "y" in input("Would you like to save? (yes/no): ").lower(): # Save file
        with open("./save.txt", 'w') as original_file: # Writes saved info
            original_file.write(f"{repos}\n{gutsuspect}\n{zip2}\n{empty}\n{zip1}") # Saves downloaded repo names, if suspect files redundant code removed, suspect zip location, and empty zip location 
    end()

if __name__ == "__main__":
    try:
        main()
    except:
        print("Error, please restart.")
    # save filessorted.storage in a text file so you dont have to keep updating it
    # could also use a similar storage function to store empty assignment and then remove all identical lines in repos
    # (Done) sort similar lines by count, any consecutive series of 4 or more lines is returned
