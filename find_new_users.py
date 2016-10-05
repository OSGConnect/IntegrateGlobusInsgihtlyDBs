#!/usr/bin/python
#title           :find_new_users.py
#author          :Bala
#date            :Sept-6-2016
#version         :1.0
#usage           :python program.py -i1 userinfo.csv -i2 reference_list.dat
#help            :python program.py --help
#notes           :finds list of new users in userinfo.csv w.r.t reference_list.dat
#python_version  :2.7

import argparse
from collections import defaultdict

def get_userprofile(infile):
    """ Get user profile. """
    user_profile = defaultdict(list)
    with open(infile,'r') as f:
        for line in f:
            line.rstrip()
            user_property = line.split(",") 
            user_property[-1] = user_property[-1].rstrip()
            uname = user_property[0].replace(" ", "")
            user_profile[uname].append(line)
    return user_profile

def get_insightly_usernames(infile):
    """ Read list of users registered at insightly"""
    user_list = []
    with open(infile,'r') as f:
        for line in f:
            newline= line.rstrip()
            uname= newline.replace(" ", "")
            user_list.append(uname)
    return user_list

def get_globus_usernames(infile):
    """ read the full csv file from globus data and find the new users not registered at insightly """
    user_list = []
    with open(infile,'r') as f:
        for line in f:
            newline= line.rstrip()
            user_property = newline.split(",") 
            uname = user_property[0].replace(" ", "")
            user_list.append(uname)
    return user_list

def get_args():
    """ Get the arguments for this program: Two input files are required. One contains user information as csv file and the other contains list usernames alredy registered at Insightly  """
    parser = argparse.ArgumentParser(description='This script finds the list of new users not registered at insightly.  Usage: python program.py -i1 userinfo.csv -i2 reference_list.dat ')
    parser.add_argument('-i1','--inputfile1', help='Record file 1',required=True)
    parser.add_argument('-i2','--inputfile2', help='Record file 2', required=True)
    args = parser.parse_args()
    return args
 
if __name__ == "__main__":
    arg_option = get_args() 
    print arg_option, type(arg_option), arg_option.inputfile1
    userinfo_file, oldlist_file = arg_option.inputfile1, arg_option.inputfile2
    insightly_usernames = get_insightly_usernames(oldlist_file)
    globus_usernames = get_globus_usernames(userinfo_file)
    diff_list = list(set(globus_usernames) - (set(insightly_usernames)))
 
    user_globusprofile  = get_userprofile(userinfo_file)
    for uname in  diff_list: 
        #print user_globusprofile[uname]
        for word in user_globusprofile[uname]:
            print word,



