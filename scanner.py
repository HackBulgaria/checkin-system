from subprocess import check_output

import urllib 
import urllib2
import time
import re
import sys
import os

def send_code(mac):
    url = 'https://data.hackbulgaria.com/education/api/set-check-in/'
    values = {
        'mac' : mac,
        'token' : get_token(),
    }
    try:
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req, timeout=4)

        if response.getcode() == 200:
            print ("checked successfully")
        if response.getcode() == 404:
            print (mac + " user not found")

    except Exception, detail:
        print detail
        print values


def get_macs():
    print("Hello I will check for macs now!")
    result = check_output(["sudo", "nmap", "-sP", "-n", "192.168.0.0/24"])
    #No no not do it this way!
    macs_alive = re.findall(r'[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}', result)
    
    for mac in macs_alive:
        send_code(mac)
        time.sleep(2)


def get_token():
    key_file_name = os.path.dirname(os.path.abspath(__file__)) + '/unique.key'
    print(key_file_name)
    if os.path.isfile(key_file_name):
        hash_code = tuple(open(key_file_name, 'r'))[0]
    else:
        hash_code = os.urandom(16).encode('hex')
        with open(key_file_name, 'w') as key_file: key_file.write(hash_code)
    
    return hash_code

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--get-token':
	print(get_token())
    else:
        get_macs()
