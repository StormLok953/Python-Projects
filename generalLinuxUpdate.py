import subprocess, os, time, sys, json, grp, pwd

def get_file(filepath):
        with open(filepath, "r") as fileObject:
                out = fileObject.read().splitlines()
        return out

if "CyberPatriot" not in os.getcwd():
        print("Please run the script from the CyberPatriot directory.")
        exit()

#check if running under root user
if os.geteuid() != 0:
        print("Please run the script as root.")
        exit()

#check if the forensic questions are complete
input("Are the forensics questions complete?")
print("Moving On")

#check if the firefox setting is correct
input("Are the Firefox settings correct?")
print("Moving On")

#check sudoers
input("Check the sudoers in /etc/sudoers")
print("Moving On")

#get /etc/passwd info
passwdObject = get_file("/etc/passwd")
current_users = []
for line in passwdObject:
        user, encryption, uid, gid, info, homeDir, shell = line.split(":")
        current_users.append({"user": user, "encryption": encryption, "uid": uid, "gid": gid, "info": info, "homeDir":homeDir, "shell": shell})

###################Disable Guest user
response = input("Disable Guest User? Y/N")
if response == "Y":
        with open("/etc/lightdm/lightdm.conf", "a") as guestFile:
                guestFile.write("allow-guest=false")

#################### Secure Network
response = input("Secure Network? Y/N")
if response == "Y":
        with open("/etc/sysctl.conf", "a") as networkConfig:
                input("Enabling Syn Cookie Protection")
networkConfig.write("\nnet.ipv4.tcp_syncookies = 1")
                input("Disable IPv6")
                networkConfig.write("\nnet.ipv6.conf.all.disable_ipv6 = 1")
                networkConfig.write("\nnet.ipv6.conf.default.disable_ipv6 = 1")
                networkConfig.write("\nnet.ipv6.conf.lo.disable_ipv6 = 1")
                input("Disable IP Forwarding")
                networkConfig.write("\nnet.ipv4.ip_forward = 0")

###################Enable Firewall
response = input("Enable Firewall? Y/N")
if response == "Y":
        os.system("sudo ufw enable")


