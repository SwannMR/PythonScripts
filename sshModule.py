#! /usr/bin/python
import os
import paramiko
import optparse
import re
import subprocess

class sshclient():
	def __init__(self, username, host, password, port=22122):
        	self.connection = paramiko.SSHClient()
		self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.connection.connect("%s" % (host), username="%s" % (username), password="%s" % (password), port=port, timeout=120)

	def command(self, cmd):
# Version on AM02 has a time out included
#            	stdin,stdout,stderr = self.client.exec_command("""%s""" % (cmd),timeout=900)
            	stdin,stdout,stderr = self.connection.exec_command("""%s""" % (cmd))
            	err = stderr.readlines()
            	data = stdout.readlines()
            	return data
	
	def scp(self,src,dst):
		scp = self.connection.open_sftp()
 		print ("copying %s" % src)
		try:
			scp.put(src,dst)
			scp.close()
		except:
			print("The file could not be copied. Check your source and destination locations are correct")	
			scp.close()
			return 0

	def close(self):
           	self.connection.close()

def getBranches():
	"""
	Process the vibe.conf file on EHL heandend. Extract
	the vibe tunnel name and inet address and return
	a dictionary of branch (key) and inet ip address
	"""
	vibe_conf = open("/home/michael/ellerines/ellerines-vibe.conf", "r")
	branches = {}
	for line in vibe_conf:
        	if re.search("name",line):
                	branch = re.search('(".*.")',line, re.IGNORECASE)
                	branch = branch.group(1)
                	branch = re.sub('"','',branch)
                	brnum = re.search('(BR[:\d]\d{3,4})',branch,re.IGNORECASE)
                	if brnum:
                        	brnum = brnum.group(1)
				brnum = re.sub(r'BR:''(?i)','',brnum, re.IGNORECASE)
				brnum = re.sub(r'BR','',brnum)
	# Get Inet Address
        	if re.search("network.10.60.*32 ", line):
                	# define a default variable before entering a check
                	inet = re.search('(network )(\d*.\d*.\d*.\d*)', line)
                	inet =  inet.group(2)
			branches[brnum] = inet
	vibe_conf.close()
	return branches

def checkHost(ip):
	""" 
	check if the host is pingable. If alive
	return True else return False
	"""
        alive = subprocess.call("ping -c 3 %s" % ip,
			shell=True,
			stdout=open('/dev/null', 'w'),
			stderr=subprocess.STDOUT)
	if alive == 0:
                return True
        else:
                return False

def process_cmd(result):
        result = "".join(result)
        result = re.sub("\n","",result)
        return result

def main():
    	parser = optparse.OptionParser()
    	parser.add_option("--branch", "-b", dest="branch", help="Connect to EHL branch")
    	parser.add_option("--all", "-A", dest="all", help="Run report for all branches")
    	options, arguments = parser.parse_args()
    	if options.branch:
        	host = m.getHost("%s" % (options.branch))
        	getData(host)
    	if options.all:
        	hosts = m.getAllHosts()
        	getData(hosts)

#if __name__ == "__main__":
#    	main()
