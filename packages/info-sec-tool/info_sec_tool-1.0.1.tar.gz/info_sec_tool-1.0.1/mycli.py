#!/usr/bin/env python

import argparse
import subprocess
def Command(text):
    print("="*80)
    command = input(" "*6+f"FBC: {text} :> ")
    return command
def run(args):
    print(args)
    subprocess.run(['python', args.file])

def main():
    parameters = {
        "recertification":["recert","recet","rct"]
    }
    parser = argparse.ArgumentParser(description='Run a Python file')
    parser.add_argument('file', type=str, help='the Python file to be executed')
    parser.add_argument('-file1', type=str, help='the Python file to be executed')
    args = parser.parse_args()
    print(args)
    command = Command("Enter Command")
    print(command)
    breaker =True
    while breaker:
        if command.lower() in parameters['recertification']:
            print("-"*50+"\n"+" Enter Recert Type eg Postilion, direct inject etc"+"\n"+"-"*50)
            recert_type = Command("Enter Recertification type")
            if recert_type in ["exit","out","ex","terminate","break"]:
                breaker = False
            
 

if __name__ == '__main__':
    main()