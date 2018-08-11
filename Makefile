install: 
	rm /usr/bin/jonas /usr/bin/jonasadm
	ln  -s $(shell pwd)/jonas.py /usr/bin/jonas
	ln  -s $(shell pwd)/jonasadm.py /usr/bin/jonasadm
