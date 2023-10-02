import os
import FinderZ
import shutil
import time
from FinderZ import GatherInfo as g
from FinderZ import fileOperands as f
from FinderZ import Synchronize as S
import hashlib
# This is the new update for FinderZ 2.0.7

# Remember to remove/add class calls such as f and g when copying into the library!

#New functions (fileOperands):

# Multiple class folders merging (useful for ML data preprocessing)
def mergeClassFolders(parentClassPath, mergeDestination, removeOriginal = False):
	# Get the dirs:
	dirs = g.readDir(parentClassPath, returnFiles = False)
	# Iterate through each folder in the parentClassPath:
	for folder in dirs:
		# Get the path of the folder:
		folder_path = os.path.join(parentClassPath, folder)
		# Get the files:
		files = g.readDir(folder_path, returnDirectories = False)
		#Iterate through each file in the folder:
		for file in files:
			if removeOriginal == False:
				f.copyFile(os.path.join(folder_path, file), mergeDestination)
			else:
				try:
					f.moveFile(os.path.join(folder_path, file), mergeDestination)
				except shutil.Error:
					print(f"File \"{os.path.join(mergeDestination, file)}\" already existed before moving file.")


	
# New functions (GatherInfo):
def wordCount(string): return len(string.split())
	
def charCount(string): return len(string)
	
def byteCount(filePath): return os.path.getsize(filePath)

def getFileStats(filePath):
	try:
		f = open(filePath)
		stringed_contents = f.read()
	except:
		raise Exception("ERR: The file could not be opened/decoded.")
	
	stats = {'Word Count': 0, 'Char Count': 0, 'Byte Count': 0, 'Line Count': 0}
	
	#word count:
	stats["Word Count"] = (wordCount(stringed_contents))
	
	#char count:
	stats["Char Count"] = (charCount(stringed_contents))
	
	#byte count:
	stats["Byte Count"] = (byteCount(filePath))
	
	#line count:
	stats["Line Count"]= (g.getFileLineAmount(filePath))
	
	return stats

stats = getFileStats("/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/Finderz/tests/file_tests/2.0.7.py")
print(f"{stats}\n")



#example usage:
#mergeClassFolders("/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/Finderz/tests/file_tests/sub/", "/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/Finderz/tests/file_tests/merge/", removeOriginal = True)

#Bug fixes in functions:

#Fixed len bug, fixed that files did not count as "empty":
def isEmptyDir(dir):
		directories, files = g.readDir(dir)
		if len(directories) == 0 and len(files) == 0:
			return True
		else:
			return False

# Change name from getAmountofFilesinDir ---> getAmountofComponentsinDir. Switch parameter name from mainDir ---> dir. Added other options.
def getAmountofComponentsinDir(dir, returnAmountFiles = True, returnAmountDirectories = True):
	directories, files = g.readDir(dir)
	
	#Get each amount:
	amount_dirs = len(directories)
	amount_files = len(files)
	if returnAmountFiles == False:
		return amount_dirs
	elif returnAmountDirectories == False:
		return amount_files
	else:
		return amount_dirs, amount_files


# Added option to return the value has a string (via f.read()) rather than a list (via f.readlines()). Add a try except to notify of errors (e.g. UnicodeDecodeError, FileExistsError)
def getFileLineContents(filePath, returnStringType = False):
	try:
		f = open(filePath, 'r')
	except:
		raise Exception("ERR: The file could not be opened/decoded.")
	if returnStringType == False:
		lines = f.readlines()
	else:
		lines = f.read()
	return lines


# Fixed firstFileStartsAtOne boolean inversion issue:
def createFiles(createAmount, keyWord, extensionType, path, firstFileStartsAtOne = False):
	originalDir = os.getcwd()
	os.chdir(path)
	numExtension = 1
	for i in range(createAmount):
		
		if numExtension == 1 and firstFileStartsAtOne == False:
			numExtension = str(numExtension)
			f = open(keyWord + extensionType, 'w')
		else:
			numExtension = str(numExtension)
			f = open(keyWord + numExtension + extensionType, 'w')
		f.close()
		numExtension = int(numExtension)
		numExtension += 1
	# Return into original directory once complete:
	os.chdir(originalDir)



# Now, time to test/fix/optimize the Synchronize and Backup classes. All of the below functions are modified in order to 

def computeHash(path):
		h = hashlib.sha1()
		#Add try except block (to avoid duplicate directory errors in Synchronize class
		try:
			file = open(path, 'rb')

			file_size = os.path.getsize(path)
			# If the file is not empty, compute the hash:
			if file_size > 0:
				print(file_size)
				chunk = 0
				while chunk != b'':
						chunk = file.read(1024)
						h.update(chunk)	
				return h.hexdigest()
			else:
				#Return false if the file is empty. In other words, skip the file:
				return False
		except:
			#Return False if unhashable
			return False

#The main logging class (Used in Synchronize and Backup classes)
class Logging:
	#Here, the announcement is simply something to announce/thecurrent/main activity or in this case print. dir is the parameter that takes in dir. dirAction consists of things like removing, adding, or copying, renaming, etc.
	def Log(loggingBool, logList, announcement = '', dir1 = '', dir2 = '', dir1Action = '', dir2Action = '', logTag = 'NC', log_non_critical = True):
		#'NC' = Not Critical, 'C' is Critical, for the logTag
		#Check if the boolean loggingBool is True, to determine whether or not the User actually wants to log or not:
		
		if loggingBool == True:
			newLogList = []
			
			#The main log list (which are really the lines that will be passed on to the writeLogsToFile function). This will be returned at the end:

			currentTime = time.ctime()
			
			def printAnnouncement(announcement, currentTime):

				if announcement != '':
					log = f"\n\n[{logTag}] CURRENT/MAIN ACTIVITY:\n{currentTime}: {announcement}\n"
					print(log)
					newLogList.append(log)
			def logDirectories(logList, dir1, dir2, dir1Action, dir2Action, currentTime):
				#First, print the announcement if there is one:
				newLogList = logList
				#Second, print the dir actions:

				#If dir1 is not empty but dir2 is, only print the dir2Action and the dir1:
				if dir1 != '' and dir2 == '':
					log = f"\n	{currentTime}: SUBPROCESS: {dir1Action} {dir1}"
					print(log)
					newLogList.append(log)
				#Vice Versa:
				elif dir1 == '' and dir2 != '':
					log = f"\n	{currentTime}: SUBPROCESS: {dir2Action} {dir2}"
					print(log)
					newLogList.append(log)
				#If they are both included (Something like "Copying files from" = dir1Action, "/path/to/dir1" = dir1, "and putting them into" = dir2Action, "path/to/dir2/" = dir2)
				elif (dir1 and dir2) != '':
					log = f"\n	{currentTime}: SUBPROCESS: {dir1Action} {dir1} {dir2Action} {dir2}" 
					print(log)
					newLogList.append(log)
				
				return newLogList

			#Apply non-critical filter:
			if log_non_critical == False:
				if logTag != 'NC':

					printAnnouncement(announcement, currentTime)
					
					newLogList = logDirectories(newLogList, dir1, dir2, dir1Action, dir2Action, currentTime)
			else:
				printAnnouncement(announcement, currentTime)
					
				newLogList = logDirectories(newLogList, dir1, dir2, dir1Action, dir2Action, currentTime)
		else:
			return logList

		#This logList will be passed by throughout the whole process, and will then be written out to a file after everything is done.
		return newLogList
		

	#The main function to write to the file:
	def writeLogsToFile(creationPath, fileLines, mode):
		#Get the current date:
		currentTime = time.ctime()
		logFileName = f"LogRun({mode})__{currentTime}.txt"
		
		file = os.path.join(creationPath, logFileName)
		#Create and open the log file:
		f = open(file, 'a')
		
		#Write the lines:
		f.writelines(fileLines)
		
		f.close()

#Main Synchronize class:
class Synchronize:
	def backUpToSyncFolder(filePath, syncBackUpFolderName, maindir, syncdir):
		
		#This function returns a path, with an ending including the syncBackUpFolderName:
		def getSyncBackUpFolderPath(maindir, syncdir, syncBackUpFolderName):
			
			#Join the two paths:
			syncBackUpFolderPathMain = os.path.join(maindir, f"{syncBackUpFolderName}")
			
			syncBackUpFolderPathSync = os.path.join(syncdir, f"{syncBackUpFolderName}")
			return syncBackUpFolderPathMain, syncBackUpFolderPathSync
		
		#Check whether or not the filePath is in the syncBackUpFolder. If it is, dont execute it:
		if syncBackUpFolderName in filePath:
			return False
		#Step 1: retreive the syncBackUpFolderPath
		syncBackUpFolderPathMain, syncBackUpFolderPathSync = getSyncBackUpFolderPath(maindir, syncdir, syncBackUpFolderName)
		
		#Once we have the syncBackUpFolderPath, we can then, copy the file or directory within the parametric filePath variable, and move it to the syncBackUpFolderPath.
		singleComponent = os.path.split(filePath)[1]
		
		isExistingInSyncBackUpFolderDirectory_Main = os.path.join(syncBackUpFolderPathMain, singleComponent)
		isExistingInSyncBackUpFolderDirectory_Sync = os.path.join(syncBackUpFolderPathSync, singleComponent)
		
		#If the path leads to a file:
		if os.path.isfile(filePath):
			#Here, check whether or not the file already exists within the syncBackUpFolderPath:
			
			#Main Path:
			if os.path.exists(isExistingInSyncBackUpFolderDirectory_Main) == True:
				os.remove(isExistingInSyncBackUpFolderDirectory_Main)
				
			f.copyFile(filePath, syncBackUpFolderPathMain)
			
			#Sync Path:
			if os.path.exists(isExistingInSyncBackUpFolderDirectory_Sync) == True:
				os.remove(isExistingInSyncBackUpFolderDirectory_Sync)
				
			f.copyFile(filePath, syncBackUpFolderPathSync)
			
		#If the path leads to a directory:
		if os.path.isdir(filePath):
			#Here, check whether or not the directory already exists within the syncBackUpFolderPath:
			
			#Main path:
			if os.path.exists(isExistingInSyncBackUpFolderDirectory_Main) == True:
				shutil.rmtree(isExistingInSyncBackUpFolderDirectory_Main)
			f.copyDir(filePath, syncBackUpFolderPathMain)
			
			#Sync path:
			if os.path.exists(isExistingInSyncBackUpFolderDirectory_Sync) == True:
				shutil.rmtree(isExistingInSyncBackUpFolderDirectory_Sync)
			f.copyDir(filePath, syncBackUpFolderPathSync)
			
	#IMPORTANT: Important files flag is used to never delete certain files that start with a specific character (default = _ ). The importantFilesFlag is important as it may prevent deletion of files/dirs!
	def synchronizeComponents(dir1, dir2, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool, maindir, syncdir, log_non_critical = True):
		
		logList = []
		#Checks whether or not the directory or file is important by checking the first character of the string:
		def isImportantFile(dir, importantFilesFlag):
			
			dir = os.path.basename(os.path.normpath(dir))
			#Get first character and check if it equals importFilesFlag:
			if dir[0] == importantFilesFlag:
				return True
			else:
				return False
			
			
		#The two very important functions: merge
		def mergeDirectories(parentdir, parentdir2, parentdirs, parent2dirs):
			#For parentdir:
			parentdirHashes = [] 
			
			#For parentdir2:
			parentdir2Hashes = []
			
			#First, iterate through parentdir files:
			if len(parentdirs) != 0:
				for dir in parentdirs:
					fullpath = os.path.join(parentdir, dir)
					for folder, dirs, files in os.walk(fullpath):
						os.chdir(folder)
						if len(files) != 0:
							for file in files:
								Hash = computeHash(file)
								if Hash == False:
									pass
								else:
									parentdirHashes.append(Hash)
									
			#Second, iterate through parentdir2 files:
			if len(parent2dirs) != 0:
				for dir in parent2dirs:
					fullpath = os.path.join(parentdir2, dir)
					for folder, dirs, files in os.walk(fullpath):
						os.chdir(folder)
						if len(files) != 0:
							for file in files:
								Hash = computeHash(file)
								if Hash == False:
									pass
								else:
									parentdir2Hashes.append(Hash)
			matchBoolean = g.isOneInCommon(parentdirHashes, parentdir2Hashes)
			
			return matchBoolean
		
		#The main merge function: Merges the important files and directories together in order to avoid loss of files. Worst case scenario, the deleted files will end up in the syncBackups folder:
		def mergeFiles(parentdir, parentdir2, parentfiles, parent2files):
			#For parentdir:
			parentdirHashes = [] 
			
			#For parentdir2:
			parentdir2Hashes = []
			
			#First, iterate through parentdir files:
			if len(parentfiles) != 0:
				for file in parentfiles:
					fullpath = os.path.join(parentdir, file)
					Hash = computeHash(fullpath)
					if Hash == False:
						pass
					else:
						parentdirHashes.append(Hash)
						
			#Second, iterate through parentdir2 files:
			if len(parent2files) != 0:
				for file in parent2files:
					fullpath = os.path.join(parentdir2, file)
					Hash = computeHash(fullpath) #Problem lies here:
					if Hash == False:
						pass
					else:
						parentdir2Hashes.append(Hash)
						
			#Now, for the comparison:
			matchBoolean = g.isOneInCommon(parentdirHashes, parentdir2Hashes)
			
			return matchBoolean
			#Take in both the parentfiles lists to get the files in each directory. For each of those, create a list with the computed hashes. IF any of those hashes matches any other hash from the other files listed... else...
			#We can return a boolean. True = mathing. False = not matching. Based on this boolean, we can then execute either deleting or merging.
		
		#Main class that takes in dir1, dir2, separates the files and dirs, makes the comparisons, and adds/removes the files, or even renames directories.
		def main(parentdir, parentdir2, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool, maindir, syncdir, log_non_critical = log_non_critical):
			
			logList = []
			#Get the source components of the parentdir and parentdir2:
			parentdirs, parentfiles = g.readDir(parentdir)
			parent2dirs, parent2files = g.readDir(parentdir2)
			
			
			
			#First, do the basic operations:
			
			#To add files:
			for dir in parentdirs:
				if dir not in parent2dirs:
					
					newLogList = Logging.Log(loggingBool, logList, announcement = f"Adding directories that exist in mainpath but not in syncpath (missing/extra).", dir1 = f"'{dir}'", dir2 = parentdir2, dir1Action = 'Found directory', dir2Action = f'in {parentdir}, but not in', logTag = "C", log_non_critical = log_non_critical)
					logList.extend(newLogList)
					#If the directory is not in the folder to sync to, then it adds it:
					path = os.path.join(parentdir2, dir)
					os.mkdir(path)
			for file in parentfiles:
				#If the file is not in the folder to sync to, then it adds it
				if file not in parent2files:
					originalpath = os.path.join(parentdir, file)
					
					newLogList = Logging.Log(loggingBool, logList, announcement = f"Adding files that exist in mainpath but not in syncpath (missing/extra).", dir1 = f"'{file}'", dir2 = parentdir2, dir1Action = 'Found file', dir2Action = f'in {parentdir}, but not in', logTag = 'C', log_non_critical = log_non_critical)
					logList.extend(newLogList)
					f.copyFile(originalpath, parentdir2)
					
			#Second, do the hard operations (Merging, replacing with newer versions, important files/dirs)
			

			# CHANGE in 2.1: The directory of the syncbackup folder is no longer popped. This is because the theory of not popping causing the infinite sync backup folder error is no longer true, that was not because of this.
			if syncBackUpFolderExists:
				if syncBackUpFolderName in parentdirs:
					parentdirs.pop(parentdirs.index(syncBackUpFolderName))
				if syncBackUpFolderName in parent2dirs:
					parent2dirs.pop(parent2dirs.index(syncBackUpFolderName))
					
			#To deal with removing files:
			for file in parent2files:
				if file not in parentfiles:
					
					#Log it:
					newLogList = Logging.Log(loggingBool, logList, announcement = f"Removing additional files:", dir1 = os.path.join(parentdir2, file), dir2 = f'Removing file from {parentdir}', dir1Action = 'File found at ', dir2Action = f'but not found in {parentdir}', logTag = 'C', log_non_critical = log_non_critical)
					logList.extend(newLogList)
					isMatching = mergeFiles(parentdir, parentdir2, parentfiles, parent2files)
					
					directory = os.path.join(parentdir2, file)
					
					if isMatching == True or len(parentfiles) < 1:
						
						newLogList = Logging.Log(loggingBool, logList, announcement = "Skipping file and directory merging as some files/dirs are matching.", logTag = 'C', log_non_critical = log_non_critical)
						logList.extend(newLogList)
						#Check if the files are important files. If they are, do not remove them, but rather copy them to the parent dir:
						if isImportantFile(directory, importantFilesFlag) == True:
							#Log it:
							newLogList = Logging.Log(loggingBool, logList, announcement = f"'{directory}' is an important file, as the first character matches the importantFilesFlag. Restoring...", logTag = 'C', log_non_critical = log_non_critical)
							logList.extend(newLogList)
							
							f.copyFile(directory, os.path.join(parentdir))
						else:
							
							#If the directory is not in the main directory but is in the sync directory, remove the directory from the sync directory:
							checkDir = os.path.split(directory)[0]
							if os.path.basename(os.path.normpath(checkDir)) == syncBackUpFolderName:
								pass
							else:
								#Check if the user wants a backup folder or not:
								if syncBackUpFolderExists:
									Synchronize.backUpToSyncFolder(directory, syncBackUpFolderName, maindir, syncdir)
									
								#Log it:
								newLogList = Logging.Log(loggingBool, logList, announcement = f"Removing {file} from {parentdir2}, as it doesn't exist in {parentdir}", logTag = 'C', log_non_critical = log_non_critical)
								logList.extend(newLogList)
								os.remove(directory)
					elif isMatching == False:
						#Log it:
						
						#Merge the directories as well:
						for dir in parent2dirs:
							if dir not in parentdirs:
								#Log it:
								newLogList = Logging.Log(loggingBool, logList, announcement = "Merging files and dirs, as no files/dirs are matching.", dir1 = dir, dir2 = f"'{parentdir}'. Merging directories...", dir1Action = "Directory '", dir2Action = f"' exists in {parentdir2}, but not in", logTag = 'C', log_non_critical = log_non_critical)
								logList.extend(newLogList)
								dirDirectory = os.path.join(parentdir2, dir)
								
								dirDirectoryParent = os.path.join(parentdir, dir)
								
								#Copy the files and the directories:
								if os.path.exists(dirDirectoryParent) == False:
									f.copyDir(dirDirectory, os.path.join(parentdir))
									
						#Log list:
						newLogList = Logging.Log(loggingBool, logList, announcement = f"Merging missing file: {file} into {parentdir}", logTag = 'C', log_non_critical = log_non_critical)
						logList.extend(newLogList)
						f.copyFile(directory, os.path.join(parentdir))
			#To deal with directories: (remove from folder to sync to:)
			for dir in parent2dirs:
				if dir not in parentdirs:
					
					#If the directory is not in the main directory but is in the sync directory, remove the directory from the sync directory:
					
					
					isMatching = mergeDirectories(parentdir, parentdir2, parentdirs, parent2dirs)
					
					directory = os.path.join(parentdir2, dir)
					
					if isMatching == True or len(parentdirs) < 1:
						#Log it: CONTINUE HERE
						newLogList = Logging.Log(loggingBool, logList, announcement = "Skipping file and directory merging as some files/dirs are matching.", log_non_critical = log_non_critical)
						logList.extend(newLogList)
						
						#Check if it is important directory:
						if isImportantFile(directory, importantFilesFlag) == True:
							#Log it:
							newLogList = Logging.Log(loggingBool, logList, announcement = f"'{directory}' is an important directory, as the first character matches the importantFilesFlag. Restoring...", logTag ='C', log_non_critical = log_non_critical)
							logList.extend(newLogList)
							
							f.copyDir(directory, os.path.join(parentdir))
						else:
							#Here check if the directory name before the directory is the synBackUpFolderName. That way, the remove doesnt deal with the synBackUpsFolder:
							checkDir = os.path.split(directory)[0]
							if os.path.basename(os.path.normpath(checkDir)) == syncBackUpFolderName:
								pass
							else:
								#Backup:
								if syncBackUpFolderExists:
									Synchronize.backUpToSyncFolder(directory, syncBackUpFolderName, maindir, syncdir)
									
								#Log it:
								newLogList = Logging.Log(loggingBool, logList, announcement = f"Removing {directory} and all of its contents, as it is directory {parentdir2}, but not in {parentdir}", logTag= 'C', log_non_critical = log_non_critical)
								logList.extend(newLogList)
								
								shutil.rmtree(directory)
					else:
						
						for file in parent2files:
							if file not in parentfiles:
								fileDirectory = os.path.join(parentdir2, file)
								parentFileDirectory = os.path.join(parentdir, file)
								
								#Log it:
								newLogList = Logging.Log(loggingBool, logList, announcement = "Merging files and dirs, as no files/dirs are matching.", dir1 = file, dir2 = f"'{parentdir}'. Merging Files...", dir1Action = "File '", dir2Action = f"' exists in {parentdir2}, but not in", logTag = 'C', log_non_critical = log_non_critical)
								logList.extend(newLogList)
								
								#Copy the files and the directories:
								if os.path.exists(parentFileDirectory) == False:
									f.copyFile(fileDirectory, os.path.join(parentdir))
									
						#Add a try except block in case the function above this one already took care of the directories:
						try:
							
							newLogList = Logging.Log(loggingBool, logList, announcement = f"Copying missing dir: {dir}, into {parentdir}", logTag = 'C', log_non_critical = log_non_critical)
							logList.extend(newLogList)
							
							f.copyDir(directory, os.path.join(parentdir))
						except FileExistsError:
							pass
							
							
			#Here, create a for loop similar to those above that actually update the contents of a file by checking the time last modified, removing the old file, and copying the new one.
			for file in parentfiles:
				maindirpath = os.path.join(parentdir, file)
				dirsyncpath = os.path.join(parentdir2, file)
				
				mainfiletime = os.path.getmtime(maindirpath)
				
				dirsyncfiletime = os.path.getmtime(dirsyncpath)
				#Compute hashes (hot fix 2.0.4)
				if (computeHash(maindirpath) != computeHash(dirsyncpath)):
					if (mainfiletime > dirsyncfiletime):
						#Remove and copy the file:
						os.remove(dirsyncpath)
						f.copyFile(maindirpath, os.path.split(dirsyncpath)[0])
						newLogList = Logging.Log(loggingBool, logList, announcement = f"Updating file contents:", dir1 = maindirpath, dir2 = "Updating file.", dir1Action = 'File at path', dir2Action = f'was modified before file {dirsyncpath}.', logTag = 'C', log_non_critical = log_non_critical)
						logList.extend(newLogList)
					elif mainfiletime < dirsyncfiletime:
						os.remove(maindirpath)
						newLogList = Logging.Log(loggingBool, logList, announcement = f"Updating file contents:", dir1 = dirsyncpath, dir2 = "Updating file.", dir1Action = 'File at path', dir2Action = f'was modified before file {maindirpath}.', logTag = 'C', log_non_critical = log_non_critical)
						logList.extend(newLogList)
						f.copyFile(dirsyncpath, os.path.split(maindirpath)[0])
			return logList
		#Execute the main function:		
		newLogList = main(dir1, dir2, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool, maindir, syncdir)
		logList.extend(newLogList)
		
		return logList
	#Organize the path slashes, as os.path.join would not always work properly:
	def organizePathSlashes(path):
		if  ("/" or "\\") not in (path[-1]):
			path = path + "/" 
		return path
	
	#Function to move removed files and folders into in case of accidental deletions:
	def createSyncBackupFolder(dir1, dir2, syncBackUpFolderName):
		os.chdir(dir1)
		if os.path.exists(syncBackUpFolderName) == False:
			os.mkdir(syncBackUpFolderName)
			
		os.chdir(dir2)
		if os.path.exists(syncBackUpFolderName) == False:
			os.mkdir(syncBackUpFolderName)
			
	#For synchronizing files and dirs (The main function:)
	def synchronize(dir1, dir2, importantFilesFlag = '_', syncBackUpFolderExists = True, loggingBool = False, logCreationPath = '', log_non_critical = True):
		
		#The main logList:
		logList = []
		
		#Log it:
		#Check if the user actually wants to create a syncBackUpFolder (It is recommended in order to reduce the chances of accidental file loss!)
		newLogList = Logging.Log(loggingBool, logList, announcement = f"Running in mode SYNCHRONIZATION: importantFilesFlag = '{importantFilesFlag}', syncBackUpFolderExists = {syncBackUpFolderExists}", logTag = 'C', log_non_critical = log_non_critical)
		#Append to the logList
		logList.extend(newLogList)
		#Initialize the backup directory:
		syncBackUpFolderName = f"{importantFilesFlag}syncBackups"
		if syncBackUpFolderExists == True:
			
			#Create the backup Folder:
			Synchronize.createSyncBackupFolder(dir1, dir2, syncBackUpFolderName)
			
			
		#Organize the directory slash marks (to avoid errors)
		dir1 = Synchronize.organizePathSlashes(dir1)
		dir2 = Synchronize.organizePathSlashes(dir2)
		
		maindir = dir1
		syncdir = dir2
		#Get the time of when the folders were last modified:
		# dir1ti_m = os.path.getmtime(dir1)
		# dir2ti_m = os.path.getmtime(dir2)
		dir1ti_m = []
		dir2ti_m = []
		
		
		
		#Check the times in the dir1:
		for folder, dirs, files in os.walk(dir1):
				#Here, get everything that is after the dir1 in order to get the other directories:
			
				time = os.path.getmtime(folder)
			
				#Append the values:
				dir1ti_m.append(time)
			
				#Get the time modified for the files as well:
				if len(files) != 0:
					for i in range(len(files)):
						
						filePath = os.path.join(folder, files[i])
						
						fileTimeModified = os.path.getmtime(filePath)
						
						dir1ti_m.append(fileTimeModified)
		#Now, do the same thing, but check for dir2 for which was last modified:
		for folder, dirs, files in os.walk(dir2):
			
				#Here, get everything that is after the dir1 in order to get the other directories:
			
				timedir = os.path.getmtime(folder)
			
				#Append the values:
				dir2ti_m.append(timedir)
			
				if len(files) != 0:
					for i in range(len(files)):
						
						filePath = os.path.join(folder, files[i])
						
						fileTimeModified = os.path.getmtime(filePath)
						
						dir2ti_m.append(fileTimeModified)
						
						
						
		dir1time = max(dir1ti_m)
		dir2time = max(dir2ti_m)
		
		#Log it:
		newLogList = Logging.Log(loggingBool, logList, announcement = f"Recursively got the time last modified for each directory: {dir1time} for {dir1} and {dir2time} for {dir2}", log_non_critical = log_non_critical)
		#Append to the logList
		logList.extend(newLogList)
		
		#The greater (bigger) time indicates the folder that was edited most recently:
		if float(dir1time) > float(dir2time):
			#IMPORTANT: Here, place if statement, deciding which folder was edited last (In other words, decide which one should follow the other based on the time they were edited. The one that gets edited the most recent gets the priority)
			#When doing the above, invert the dir1 with dir2 (Because you are doing pretty much the opposite!)
			for folder, dirs, files in os.walk(dir1):
				#Here, get everything that is after the dir1 in order to get the other directories:
				
				childdir = (folder.split(dir1,1)[1])
				
				syncpath = os.path.join(dir2, childdir)
				
				newLogList = Logging.Log(loggingBool, logList, announcement = f"Iterating through main loop with {dir1} as the main dir, as {dir2} has an older modification time.", dir1 = folder, dir2 = syncpath, dir1Action = 'Entering child directory', dir2Action = "to compare files and dirs with ", log_non_critical = log_non_critical)
				#Append to the logList
				logList.extend(newLogList)
				
				#Set the newLogList equal to the log that the function returns:
				newLogList = Synchronize.synchronizeComponents(folder, syncpath, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool, maindir, syncdir, log_non_critical = log_non_critical)
				logList.extend(newLogList)
				
		elif float(dir1time) < float(dir2time):
			for folder, dirs, files in os.walk(dir2):
				#Here, get everything that is after the dir1 in order to get the other directories:
				childdir = (folder.split(dir2,1)[1])
				syncpath = os.path.join(dir1, childdir)
				
				newLogList = Logging.Log(loggingBool, logList, announcement = f"Iterating through main loop with {dir2} as the main dir, as {dir1} has an older modification time.", dir1 = folder, dir2 = syncpath, dir1Action = 'Entering child directory', dir2Action = "to compare files and dirs with ", log_non_critical = log_non_critical)
				#Append to the logList
				logList.extend(newLogList)
				
				#Set the newLogList equal to the log that the function returns:
				newLogList = Synchronize.synchronizeComponents(folder, syncpath, syncBackUpFolderName, syncBackUpFolderExists, importantFilesFlag, loggingBool, maindir, syncdir, log_non_critical = log_non_critical)
				
				
				logList.extend(newLogList)
		#At the very end, check if loggingBool is True. If it is, write the lines of the list logList to the specific directory of where the Log should be created:
		if loggingBool == True:
			#Write logs to file:
			Logging.writeLogsToFile(logCreationPath, logList, 'synchronize')

# testing the new refined Synchronize class:
Synchronize.synchronize("/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/Finderz/tests/file_tests/sub", "/Users/edwardferrari/MyPythonProjects/GitHubRepos/Active/Finderz/tests/file_tests/sub2")