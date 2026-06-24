# 
# File: main.py
# Author: Ruezgar Guenduez
# E-Mail: ruezgar.guenduez@gmail.com
#

### imports ###
import json
from func import *

def main():
    ### init ###
    with open(getConfigPath()) as f:
        data = json.load(f)
    
    if not dataIsValid(data):
        print("Your Configuration file must include these:\n",
              " sender-address: string\n", 
              " sender-pw: string\n", 
              " recipients: string array\n", 
              " file-attachments: string array\n",
              "Please update your configuration")
        exit()

    sendMail(data)

if __name__ == "__main__":
    main()