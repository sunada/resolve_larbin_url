#!/usr/bin/python

import adns
import sys
import time

def read_file(fr):
    hosts = []
    file = open(fr)
    lines = file.readlines()
    for line in lines:
        hosts.append(line[7:-2])
    file.close()
    return hosts

def write_file(fw,ress):
    file=open(fw,'a')
    if isinstance(ress, dict): 
        for res in ress:
            #print res[0]
            #print ress[res]
            file.write(ress[res]+'		'+res[0]+'\n')
    elif isinstance(ress, list):
        for res in ress:
            file.write(res + '\n')
    else:
        pass
    file.close()

class QueryEngine(object):

    def __init__(self,s=None):
        self._s = s or adns.init(adns.iflags.noautosys)
        self._queries = {}
        self.ip_host = {}
        self.host_noip = []
         
    def submit(self,qname,rr,flags=0):
        q=self._s.submit(qname,rr,flags)
        self._queries[q] = qname,rr,flags

    def run(self,timeout = 0):
        for q in self._s.completed():
            answer = q.check()
            qname,rr,flags = self._queries[q]
            del self._queries[q]
            if answer[3]:
                self.ip_host[answer[3]] = qname
            #print qname, '		',answer[3]
            else:
                #print 'no answer: ', qname
                self.host_noip.append(qname)


    def finished(self):
        return not len(self._queries)

    def get_ip_host(self):
        return self.ip_host

    def get_host_noip(self):
        print 'len(self.host_noip): ', len(self.host_noip)
        return self.host_noip

def resolveDns(fr,fw,intensity):
    hosts = read_file(fr)
    start = time.time()
    qe = QueryEngine()
    for host in hosts:
        qe.submit(host,adns.rr.AAAA)

    while not qe.finished():
        qe.run()

    print 'time cost:',time.time()-start
    ip_host = qe.get_ip_host()
    write_file(fw,ip_host)
    host_noip = qe.get_host_noip()
    #print 'len(host_noip): ', len(host_noip)
    write_file(fw+'_failed_resolve', host_noip)    
    return len(hosts), len(ip_host)

if __name__=='__main__':
    filename=sys.argv[1]
    savename=sys.argv[2]
    
    host_cnt, IP_cnt = resolveDns(filename, savename, intensity = 500)
    print 'Resolve ' + unicode(host_cnt) + ' domains and get '\
          + unicode(IP_cnt) + ' IPv6 address.'
