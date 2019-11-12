import subprocess, os, time, sys, json, grp, pwd

current_working_user = "cyberpatriot"

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

####################### Password Policy
response = input("Change Password Policy? Y/N")
if response == "Y":
	listLines = []
	with open("/etc/login.defs", "rt") as readOnlyFile:
		listLines =  list(readOnlyFile)
	for lines in listLines:
		print(lines)

	with open("/etc/login.defs", "wt") as passwdFile:
		for line in listLines:
			if ("PASS_MAX_DAYS"  in line) and ("#" not in line):
				passwdFile.write("PASS_MAX_DAYS   90\n")
			elif ("PASS_MIN_DAYS" in line) and ("#" not in line):
				passwdFile.write("PASS_MIN_DAYS   7\n")
			elif ("PASS_WARN_AGE" in line) and ("#" not in line):
				passwdFile.write("PASS_WARN_AGE   14\n")
			else:
				passwdFile.write(line)	
	os.system("sudo apt-get install libpam-cracklib")
	listLines = []
	with open("/etc/pam.d/common-password", "r") as readOnlyFile:
		listLines =  list(readOnlyFile)
	for lines in listLines:
		print(lines)

	with open("/etc/pam.d/common-password", "w") as pamFile:
		for line in listLines:
			if ("pam_unix.so"  in line) and ("#" not in line):
				pamFile.write("password        [success=1 default=ignore]      pam_unix.so obscure use_authtok try_first_pass sha51 minlen=8 remember=5\n")
			elif ("pam_cracklib.so" in line) and ("#" not in line):
				pamFile.write("password        [success=1 default=ignore]      pam_unix.so obscure use_authtok try_first_pass sha512 ucredit=1 lcredit=1 dcredit=1 ocredit=1\n")
			else:
				pamFile.write(line)

	os.system("sudo cp -n /etc/pam.d/common-auth backup/common-auth")
	with open("/etc/pam.d/common-auth", "a") as commonAuth:
		commonAuth.write("\nauth required pam_tally2.so deny=5 onerr=fail unlock_time=1800")

	for userData in current_users:
		print(userData.get("user"))
		if userData is not current_working_user: 
			proc = subprocess.Popen(["sudo", "passwd", userData]}, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			proc.stdin.write("Cyberpatriot1!\n".encode("ascii"))
			proc.stdin.write("Cyberpatriot1!\n".encode("ascii"))
			proc.stdin.flush()
			time.sleep(1)
	
		 
########################### Disable root login
response = input("Disable Root Login? Y/N")
if response == "Y":
	os.system("sudo passwd -dl root")



############# Install open openssh-server
response = input("Download openssh-server? Y/N")
if response == "Y":
	os.system("sudo apt install openssh-server")
