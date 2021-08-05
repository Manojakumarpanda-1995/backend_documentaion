import pyDes
from pyDes import *
import json,base64,pyDes
import random
import string
import hashlib
from django.conf import settings
secret_key=getattr(settings,"SECRET_KEY",None)

def generate_passwords(password):
    return hashlib.sha256("{}{}".format(secret_key,password).encode()).hexdigest()


def encryption(s_string):
    s_string=s_string.encode('ascii','ignore').decode("ascii")
    k=triple_des("av9ZxAuuf7DBZiix",CBC,"jvz8bUAx")
    p=len(s_string)%8
    s=k.encrypt(str(s_string)+(8-p)*'0')
    # print(s)
    b=base64.b64encode(s)
    # print(b)
    l=b.decode('utf-8')
    return l

def decryption(encstring):
    k=triple_des("av9ZxAuuf7DBZiix",CBC,"jvz8bUAx")
    # p=len(encstring)%8
    # print(p)
    g=base64.b64decode(encstring)
    # print(g)
    j=k.decrypt(g)
    # print(j)
    l=j.decode("utf-8","ignore").strip("0").strip('\x00')
    return l

# For generated Password
def random_alphaNumeric_string(lettersCount, digitsCount):
    sampleStr = ''.join((random.choice(string.ascii_letters) for i in range(lettersCount)))
    sampleStr += ''.join((random.choice(string.digits) for i in range(digitsCount)))
    
    # Convert string to list and shuffle it to mix letters and digits
    sampleList = list(sampleStr)
    random.shuffle(sampleList)
    finalString = ''.join(sampleList)
    return finalString


def removeSpecialCharacters(value):
    return ''.join([e for e in value if e.isalnum()])