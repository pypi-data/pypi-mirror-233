import os

# Multiple class folders merging (useful for ML data preprocessing)
def mergeClassFolders(parentClassPath, mergeDestination, removeOriginal = False):
	#iterate through each folder in the parentClassPath:
	for folder in parentClassPath:
		# Get the path of the folder:
		folder_path = os.path.join(parentClassPath, folder)
		#Iterate through each file in the folder:
		for file in folder:
			#Join the path of the destination to join all files together with the name of the file.
			if removeOriginal == False:
				copyFile(os.path.join(folder_path, file), mergeDestination)
			else:
				moveFile(os.path.join(folder_path, file), mergeDestination)
			
			


Injected Text