import subprocess, os, time, sys, json, grp, pwd

################### Restart sysctl
response = input("Restart sysctl? Y/N")
if response == "Y":
         os.system("sudo sysctl -p")
