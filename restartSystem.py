import subprocess, os, time, sys, json, grp, pwd

################### Restart sysctl
response = input("Restart sysctl? Y/N")
if response == "Y":
         os.system("sudo sysctl -p")
        

################## Find all media files and delete
mediaFileTypes = ["mp3", "mov", "mp4", "png", "pdf", "gif", "jpeg", "tiff", "bmp", "aav", "aac", "wav", "wma", "dts", "mpeg-1", "mpeg-2", "mpeg-4", "avi", "avchd"]
response = input("Find all media files? Y/N")
if response == "Y":
        for fileTypes in mediaFileTypes:
                subprocess.call(["find", "/", "-type", "f", "-iname", "*." + fileTypes])

