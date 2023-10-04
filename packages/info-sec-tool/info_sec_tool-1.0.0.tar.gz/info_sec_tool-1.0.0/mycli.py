#!/usr/bin/env python

import argparse
import subprocess

def run(args):
    subprocess.run(['python', args.file])

def main():
    parser = argparse.ArgumentParser(description='Run a Python file')
    parser.add_argument('file', type=str, help='the Python file to be executed')
    args = parser.parse_args()
    run(args)

if __name__ == '__main__':
    main()