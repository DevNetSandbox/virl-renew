# -*- coding: utf-8 -*-
import json
import time
import re
import logging
from gzip import GzipFile
import urllib2
import cookielib

if __name__ == "__main__":
    url_base = 'http://10.10.20.160'
    username = 'uwmadmin'
    password = 'password'
    #login
    login_url = url_base+'/login/'
    
    #s = requests.session()
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [
        ("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.5) Gecko/20031107 Debian/1.5-3"),
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
        ("Referer", login_url),
    ]
    #for session id token
    http = opener.open(login_url)
    content = http.read()
    http.close()
    m = re.search('name="csrf_token" type="hidden" value="([^"]+)"',  content)
    csrf_token = m.group(1)
    
    time.sleep(5)
    opener.addheaders = [
        ("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.5) Gecko/20031107 Debian/1.5-3"),
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
        ("Referer", login_url),
        ('Content-Type', 'application/x-www-form-urlencoded'),
    ]
    params = 'csrf_token={0}&username={1}&password={2}&submit=Login'.format(csrf_token, username, password)
    http = opener.open(login_url, params)
    content = http.read()
    http.close()
    time.sleep(2)
    
    #get license status
    status_url = url_base + '/admin/salt/'
    for retry in xrange(3):
        try:
            http = opener.open(status_url)
            content = http.read()
            http.close()
        except Exception,e:
            continue
        
        #check license count
        m = re.search('<dt>Allowed Cisco node count:</dt><dd>([0-9]+)',  content)
        licenses = int(m.group(1))
        if licenses>5:
            print('VIRL license accquired already, no renew required')
            exit(0)
        #renew license page
        print('Renew license {0} times...'.format(retry+1))
        renew_url = url_base + '/admin/salt/?renew=1'
        try:
            content = opener.open(renew_url)
        except Exception, e:
            pass
        time.sleep(10)    
        