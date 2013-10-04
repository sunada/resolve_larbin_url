resolve_larbin_url
==================

index is a file of urls fetched by larbin.
getDisHosts.py will write distinct hosts of these urls to a new file.
resolve_adns.py will resolve ipv6 addresses of these hosts.

To run the program, you should install libraries of adns and adns-python.

Steps:

1. $ cd adns_1.4-2+ipv6

2. $ ./configure

3. $ make

4. # make install

5. $ cd ../adns-python-1.2.1-IPv6

6. $ python setup.py build

7. # python setup.py install


Q&A
Q: 1. How to run it? Example:

A:
$ ./getDisHosts.py index hosts

index: a file of urls

hosts: to record the distinct hosts

the script getDishosts.py will also create another file named hostsDup to save the duplicated hosts.

$ ./resolve_adns.py hosts

hosts: created by getDisHosts.py

the script of resolve_adns.py will create a file named hostIP to save the ipv6 addresses. 

Q: 2. When run the resolve_adns.py, the system spouts an error: libadns.so.1: cannot open shared object file: No such file or directory.

A:
This is because libadns.so.1 is not in the shared lib path. You can do this to resolve the problem:

$vim /etc/ld.so.conf
add the path of libadns.so.1 (usually the '/usr/local/lib') to the file and save it
$ ldconfig

Then you will find no error spouts.
