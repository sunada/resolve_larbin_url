#!/usr/bin/python
#
# ./getDisHosts.py src_dir des_file
#
# receive:
# src_dir: directory used to save htmls and urls by larbin
# des_file: the file to save distinct hosts
# 
# return:
# the script create two files. The 'dest_file' save distinct hosts;
# the 'dest_file'+'Dup' save the duplicated hosts and the account of duplicated time.
#
# Example:
# ./getDisHosts.py /home/admin /home/admin/hostsFromLarbin
# You will see two new files 'hostsFromLarbin' and 'hostsFromLarbinDup' created by the script

import re
import os
import sys

#dirName=sys.argv[1]
#if not dirName[-5:]=='/save':
#	dirName+='/save'

#dirs=os.listdir(dirName)
# prepare to remove the newest dir and the file of IP_port
#dirs.sort()

#get domains
pattern = re.compile('http://.+?/')
domains = []
domainNew={}
domainDup={}

urlfile=sys.argv[1]

disHostsFile=sys.argv[2]
dupHostsFile=sys.argv[2]+'Dup'
domainFile=open(disHostsFile,'a')
domainDupFile=open(dupHostsFile,'a')

#for dir in dirs[:]:
#	name=dirName+'/'+dir+'/index'	
lines = open(urlfile)
for line in lines:
	domain=pattern.findall(line)[0]
	if domain in domainDup:
		domainDup[domain]+=1
	elif domain in domainNew:
		domainDup[domain]=1
	else:
		domainNew[domain]=1
		domainFile.write(domain+'\n')
#domainFile.close()
lines.close()
sum=0

for item in domainDup:
	tmp= str(item)+' '+str(domainDup[item])
	domainDupFile.write(tmp+'\n')
	sum+=domainDup[item]
domainDupFile.write('Dup ip sum: '+str(sum)+'\n')
domainDupFile.close()

