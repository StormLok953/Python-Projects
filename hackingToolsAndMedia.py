import subprocess, os, time, sys, json, grp, pwd

################### Delete all Hacking Tools
hackingTools = ["zenmap", "nmap", "telnet", "hydra", "john", "nitko", "freeciv", "ophcrack", "kismet", "minetest"]
response = input("Remove Hacking Tools? Y/N")
if response == "Y":
        for hackingProgram in hackingTools:
                print("Removing ", hackingProgram)
                subprocess.call(["sudo", "apt-get", "purge", hackingProgram + "*", "-y"])

################## Find all media files and delete
mediaFileTypes = ["mp3", "mov", "mp4", "png", "pdf", "gif", "jpeg", "tiff", "bmp", "aav", "aac", "wav", "wma", "dts", "mpeg-1", "mpeg-2", "mpeg-4", "avi", "avchd"]
response = input("Find all media files? Y/N")
if response == "Y":
        for fileTypes in mediaFileTypes:
                subprocess.call(["find", "/", "-type", "f", "-iname", "*." + fileTypes])

################# Secure Ports

