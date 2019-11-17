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

############# Make sure preliminary problems are solved
response = raw_input("Are the Forensic Questions solved?")
print("Moving On")


############# Enable the Firewall
response = raw_input("Would you like to enable UFW Firewall? y or n")
if response is 'y' or response is 'Y':
	os.system("sudo ufw enable")


############# Install openssh-server
response = raw_input("Would you like to download openssh-server? y or n")
if response is 'y' or response is 'Y':
	os.system("sudo apt install openssh-server")


############# Disable Root Login
print("Prerequisites: openssh-server must be installed")
response = raw_input("Would you like to disable root login? y or n")
if response is 'y' or response is 'Y':
	os.system("sudo cp /etc/ssh/sshd_config /home")
	listLines = []
	with open("/etc/ssh/sshd_config", "rt") as readOnlyFile:
		listLines = list(readOnlyFile)
	for line in listLines:
		print(line)
	
	with open("/etc/ssh/sshd_config", "wt") as disableRootLoginFile:
		for line in listLines:
			if ("PermitRootLogin" in line) and ("#" not in line):
				disableRootLoginFile.write("PermitRootLogin no")
			else:
				disableRootLoginFile.write(line)
