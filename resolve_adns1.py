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

    def __init__(self,fr, fw, intensity, s=None):
        self._s = s or adns.init(adns.iflags.noautosys)
        self.fr = fr
        self.fw = fw
        self.intensity = intensity
        self._queries = {}
        self.ip_host = {}
        self.host_noip = []
        
    def submit(self,qname,rr,flags=0):
        q=self._s.submit(qname,rr,flags)
        self._queries[q] = qname,rr,flags

    def run(self,timeout = 10):
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

    def resolveDns(self):
        hosts= read_file(self.fr)
	cnt = len(hosts)
        start = time.time()
        tmp = 0
        while hosts:
            #print 'len(hosts): ', len(hosts)
            #print 'len(self.ip_host):', len(self.ip_host)
            #print 'len(self.host_noip):', len(self.host_noip)
            #print 'tmp:', tmp
            while hosts and len(self._queries) < self.intensity:
                tmp += 1
                host = hosts.pop()
                self.submit(host,adns.rr.AAAA)

            while not self.finished():
                self.run()

        print 'time cost:',time.time() - start
        write_file(self.fw,self.ip_host)
        #print 'len(host_noip): ', len(host_noip)
        write_file(self.fw+'_failed_resolve', self.host_noip)    
        return cnt, len(self.ip_host), len(self.host_noip)

if __name__=='__main__':
    filename=sys.argv[1]
    savename=sys.argv[2]
    
    qe = QueryEngine(filename, savename, intensity = 100)
    host_cnt, IP_cnt, unresolve_cnt = qe.resolveDns()
    print 'Resolve ' + unicode(host_cnt) + ' domains and get '\
          + unicode(IP_cnt) + ' IPv6 address.(' + unicode(unresolve_cnt) + ' unresolved)'
