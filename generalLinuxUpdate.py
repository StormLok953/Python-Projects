import subprocess, os, time, time, sys, json, grp, pwd

def get_file(filepath):
	with open(filepath, "r") as f:
		out = f.read().splitlines()
	return out

def get_output(command, outfile = None):
	if outfile is None:
		c = command
	else:
		c = "{} | tee {}".format(command, outfile)
	
	command_out = subprocess.Popen(c, 
		shell = True,
		stdout = subrprocess.PIP,
		executable="/bin/bash")
	return command_out.stdout.read().decode().splitlines()

if "CyberPatriot" not in os.getcwd():
	print("Please run script from the CyberPatriot directory.")
	exit()
if os.geteuid() != 0:
	print("Please run the script as root.")
	exit()

############# Create backup file
def initiation():
	os.system("mkdir ~/backup")


############# Make sure preliminary problems are solved
	response = input("Are the Forensic Questions solved?")
	print("Moving On")


############# Enable the Firewall
def enableUFWFirewall():
	response = input("Would you like to enable UFW Firewall? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo ufw enable")

############# Update OS and Kernel
def updateOSAndKernel():
	response = input("Would you like to update OS? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo apt-get update")
		os.system("sudo apt-get upgrade")

	response = input("Would you like to update Kernel? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo apt-get dist-upgrade")

############# Install openssh-server
def installOpenSSHServer():
	response = input("Would you like to download openssh-server? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo apt install openssh-server")


############# Disable Root Login
def disableRootLogin():
	print("Prerequisites: openssh-server must be installed")
	response = input("Would you like to disable root login? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo cp /etc/ssh/sshd_config ~/backup")
		listLines = []
		with open("/etc/ssh/sshd_config", "rt") as readOnlyFile:
			listLines = list(readOnlyFile)
		for line in listLines:
			print(line)
		with open("/etc/ssh/sshd_config", "wt") as disableRootLoginFile:
			for line in listLines:
				if ("PermitRootLogin" in line) and ("#" not in line):
					disableRootLoginFile.write("PermitRootLogin no\n")
				if ("PermitEmptyPasswords" in line) and ("#" not in line):
					disableRootLoginFile.write("PermitEmptyPasswords no")
				if ("Protocol 1,2" in line) and ("#" not in line):
					disableRootLoginFile.write("Protocol 2")
				else:
					disableRootLoginFile.write(line)

############## Enforce Password Policy 
def enforcePasswordPolicy():
	response = input("Would you like to enforce password complexity and length? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo apt-get install libpam-cracklib")
		os.system("sudo cp /etc/pam.d/common-password ~/backup")
		listLines = []
		with open("/etc/pam.d/common-password", "rt") as readOnlyFile:
			listLines = list(readOnlyFile)
		for line in listLines:
			print(line)

		with open("/etc/pam.d/common-password", "wt") as passwordComplexityAndLength:
			for line in listLines:
				if ("pam_unix.so" in line) and ("#" not in line):
					passwordComplexityAndLength.write("password	[success=1 default=ignore]	pam_unix.so obsure sha512 minlen=8 remember=5\n") 
				elif ("pam_cracklib.so" in line) and ("#" not in line):
					passwordComplexityAndLength.write("password	requisite		pam_cracklib.so retry=3 minlen=8 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1\n")
				else:
					passwordComplexityAndLength.write(line)
	
	response = input("Would you like to enforce password history? [y/n]")
	if response is 'y' or response is 'Y':
		listLines = []
		with open("/etc/login.defs", "rt") as readOnlyFile:
			listLines = list(readOnlyFile)
		for line in listLines:
			print(line)

		with open("/etc/login.defs", "wt") as passwordHistory:
			for line in listLines:
				if ("PASS_MAX_DAYS" in line) and ("#" not in line):
					passwordHistory.write("PASS_MAX_DAYS	90\n")
				elif ("PASS_MIN_DAYS" in line) and ("#" not in line):
					passwordHistory.write("PASS_MIN_DAYS	10\n")
				elif ("PASS_WARN_AGE" in line) and ("#" not in line):
					passwordHistory.write("PASS_WARN_AGE	7\n")
				else:
					passwordHistory.write(line)	

############# Force SSH to use Public Key Authentication
def forceSSHToUsePublicKeyAuthentication():
	print("Prerequisites: openssh-server must be installed")
	response = input("Force SSH to require public key authentication? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo cp /etc/ssh/sshd_config ~/backup")
		listLines = []
		with open("/etc/ssh/sshd_config", "rt") as readOnlyFile:
			listLines = list(readOnlyFile)
		for line in listLines:
			print(line)

		with open("/etc/ssh/sshd_config", "wt") as publicKeyAuthentication:
			for line in listLines:
				if ("PasswordAuthentication yes" in line):
					publicKeyAuthentication.write("PasswordAuthentication no\n")
				elif ("PubkeyAuthentication no" in line):
					publicKeyAuthentication.write("PubkeyAuthentication yes\n")
				else:
					publicKeyAuthentication.write(line)	

############### Disable FTP Service
def disableFTPService():
	print("Prerequisites: Update and Upgrade System")
	response = input("Disable FTP Service? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo apt-get remove pure-ftpd")
	
############### Disable Guest Account
def disableGuestAccount():
	response = input("Disable Guest Account? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo cp /etc/lightdm/lightdm.conf ~/backup")
		listLines = []
		with open("/etc/lightdm/lightdm.conf", "wt") as guestAccountDisable:
			guestAccountDisable.write("[SeatDefaults]\n")
			guestAccountDisable.write("user-session=ubuntu\n")
			guestAccountDisable.write("greeter-session=unity-greeter\n")
			guestAccountDisable.write("allow-guest=false\n")

############### Removing Apache2
def removeApache():
	response = input("Disable Apache2? [y/n]")
	if response is 'y' or response is 'Y':
		os.system("sudo service apache2 stop")
		os.system("sudo apt purge apache2")
		os.system("sudo apt-get purge apache2-utils apache2.2-bin apache2-common")
		os.system("sudo apt-get autoremove")
	print("Test Apache-2 with \"sudo service apache-2 start\"")
	print("Should say \"unrecognized service\"")
		
initiation()
enableUFWFirewall()
updateOSAndKernel()
installOpenSSHServer()
disableRootLogin()
enforcePasswordPolicy()
forceSSHToUsePublicKeyAuthentication()
disableFTPService()
disableGuestAccount()
removeApache()
