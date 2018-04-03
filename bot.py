#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import urllib.request, json
import random
import sleekxmpp
from optparse import OptionParser
import string
from sleekxmpp.exceptions import IqError, IqTimeout

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

class SendMsgBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = message
        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler("ssl_invalid_cert", self.discard)

    def discard(self, event, cert, direct):
        return

    def start(self, event):
        self.send_presence()
        self.get_roster()
        for to_user in self.recipient:
            send_msg=random.choice(self.msg)
            self.send_message(mto=to_user,mbody=send_msg,mtype='chat')
            print("message sent "+to_user)
        self.disconnect(wait=False)

def start_xmpp(username,password,user_list,content,proxy):
    xmpp = SendMsgBot(username+"@x.connected2.me", password, user_list, content)
    xmpp.register_plugin('xep_0030')
    xmpp.register_plugin('xep_0199')
    with open(proxy) as f:
        proxies = f.readlines()
    proxies = [x.strip() for x in proxies]
    try:
        proxy=random.choice(proxies)
        proxy_ip,proxy_port = proxy.split(':')
        xmpp.use_proxy = True
        xmpp.proxy_config = {
            'host': proxy_ip,
            'port': proxy_port,
            'username':'',
            'password':''}
        if xmpp.connect(reattempt=False):
            xmpp.process(block=True)
            print("process done")
        else:
            print("error on connect.")
    except IqError as e:
	    print('error'+e)

if __name__ == '__main__':
    optp = OptionParser()
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)
    optp.add_option('--proxy', help='set proxy file',
                    action='store_const', dest='proxy',
                    const=5, default='proxies.txt')
    optp.add_option('-m', '--message', help='set message file',
                    action='store_const', dest='message',
                    const=5, default='messages.txt')
    optp.add_option("-u", "--username", dest="username",
                    help="set username")
    optp.add_option("-p", "--password", dest="password",
                    help="set password")
    opts, args = optp.parse_args()
    if opts.username is None:
        opts.username = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s %(message)s')
    user_list = []
    username = opts.username
    password = opts.password
    with open(opts.message) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    hdr = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    while True:
        user_list = []
        req = urllib.request.Request("https://api.c2me.cc/b/shuffle_filter?nick="+username+"&password="+password+"&distance=110&order_by_last_online",headers=hdr)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read().decode())
        for user in data["online_users"]:
            user_list.append(user["nick"]+"@x.connected2.me")
        start_xmpp(username,password,user_list,content,opts.proxy)
