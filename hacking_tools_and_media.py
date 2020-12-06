import subprocess, os, time, sys, json, grp, pwd

############ Delete All Hacking Tools
def purgeHackingTools():
	hacking_tools = ["zenmap", "nmap", "telnet", "hydra", "john", "nitko", "freeciv", "ophcrack", "kismet", "minetest", "netcat", "vsftpd", "metasploit", "ncat", "wesnoth"]

	response = input("Would you like to remove all the hacking tools? y or n")
	if response is 'y' or response is 'Y':
		for hacking_tool in hacking_tools:
			print("Removing ", hacking_tool)
			subprocess.call(["sudo", "apt-get", "purge", hacking_tool + "*", "-y"])


############ Final All Media Files and Delete
def purgeMediaFiles():
	media_file_extensions = ["mp3", "mov", "mp4", "png", "pdf", "gif", "jpeg", "tiff", "bmp", "avi"]
#TODO find uppercase 
	response = input("Would you like to detect all the media file types? y or n")
	if response is 'y' or response is 'Y':
		for media_file_extension in media_file_extensions:
			print("Finding ", media_file_extension)
			subprocess.call(["find", "/home", "-type", "f", "-iname", "*." + media_file_extension])

purgeHackingTools()
purgeMediaFiles()
