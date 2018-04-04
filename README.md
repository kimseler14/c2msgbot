# c2msgbot
connected2.me auto message to last online users

# requirements
* Python 3.6
* pip install sleekxmpp (https://github.com/fritzy/SleekXMPP)

# important
If you do not use a proxy server, you are blocked by the server in a short time. 
For this reason it is necessary to use a proxy server. Make sure you edit the proxy server file. 
Each line in the message file is retrieved separately and a random one is sent. 
The user name and password are determined by the server. You must use the MiTM method to obtain it.

# usage
python bot.py --help
```bash
Usage: bot.py [options]

Options:
  -h, --help            show this help message and exit
  -q, --quiet           set logging to ERROR
  -d, --debug           set logging to DEBUG
  -v, --verbose         set logging to COMM
  --proxy               set proxy file (default: proxies.txt)
  -m, --message         set message file (default: messages.txt)
  -u USERNAME, --username=USERNAME
                        set username
  -p PASSWORD, --password=PASSWORD
                        set password
```
