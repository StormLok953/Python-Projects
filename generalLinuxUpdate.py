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
	response = input("Would you like to enable UFW Firewall? y or n")
	if response is 'y' or response is 'Y':
		os.system("sudo ufw enable")


############# Install openssh-server
def installOpenSSHServer():
	response = input("Would you like to download openssh-server? y or n")
	if response is 'y' or response is 'Y':
		os.system("sudo apt install openssh-server")


############# Disable Root Login
def disableRootLogin():
	print("Prerequisites: openssh-server must be installed")
	response = input("Would you like to disable root login? y or n")
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
				else:
					disableRootLoginFile.write(line)

############## Enforce Password Policy 
def enforcePasswordPolicy():
	response = input("Would you like to enforce password complexity and length? y or n")
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
	

############# Force SSH to use Public Key Authentication
def forceSSHToUsePublicKeyAuthentication():
	print("Prerequisites: openssh-server must be installed")
	response = input("Force SSH to require public key authentication? ")
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
	
initiation()
enableUFWFirewall()
installOpenSSHServer()
disableRootLogin()
enforcePasswordPolicy()
forceSSHToUsePublicKeyAuthentication()
