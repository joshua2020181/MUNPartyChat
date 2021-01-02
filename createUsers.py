import sys
import os
import getopt
sys.path.insert(0, "D:\MUNPartyChat\mysite") 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'mysite.settings')

import django
django.setup()

from django.contrib.auth.models import User

def createUser(**kwargs):
    vals = {}
    for k in kwargs:
        if kwargs[k] is not None: #transfer all non-None args to new dict
            vals[k] = kwargs[k]
    if not vals:
        print("No values provided!")
    else:
        User.objects.create_user(**vals)

def fromFile(filename):
    pass

def cmdline(argv):
    uservalues = {
        "username": None,
        "password": None,
        "first_name": None,
        "last_name": None,
        }
    mode = None
    filename = ""
    try:
       opts, args = getopt.getopt(argv,"hu:p:",["help", "print", "create", "delete", "fromFile=", "username=", "password=", "firstName=", "lastName="])
    except getopt.GetoptError:
       print('For help: createUsers.py -h')
       sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('modes: --create, --delete, --print, --fromFile <fileName>')
            print('other args: -u <username> -p <password> --firstName <first name> --lastName <last name>')
            sys.exit()
        elif opt == '--create':
            mode = "create"
        elif opt == '--print':
            print(User.objects.values())
            sys.exit()
        elif opt == '--delete':
            mode = "delete"
        elif opt == '--fromFile':
            mode = "fromFile"
            filename = arg
        elif opt in ("-u", "--username"):
            uservalues["username"] = arg
        elif opt in ("-p", "--password"):
            uservalues["password"] = arg
        elif opt == '--firstName':
            uservalues["first_name"] = arg
        elif opt == '--lastName':
            uservalues["last_name"] = arg
        
    if mode == "create":
        createUser(**uservalues)
    elif mode == "delete":
        print("delete user blah blah")
    elif mode == "fromFile":
        fromFile(filename)

if __name__ == "__main__":
    cmdline(sys.argv[1:])