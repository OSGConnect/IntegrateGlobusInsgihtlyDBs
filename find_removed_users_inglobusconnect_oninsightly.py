#!/usr/bin/python
#title           :find_removed_users.py
#author          :Bala
#date            :March-16-2017
#version         :1.0
#usage           :python program.py -i1 InsightlyContacts.csv -i2 rejected_list.dat
#help            :python program.py --help
#notes           :finds list of removed users in InsightlyContacts.csv w.r.t rejected_list.dat. 
#                The rejected_list.dat is obtained by doing a cut and paste from the list of rejected users
#                under connect group. 
#python_version  :2.7

import argparse

def match_rejected_users(infile, userlist):
    """ Filter the rejected users from the Insight.ly database """
    local_list = userlist
    with open(infile,'r') as f:
        for line in f:
            line.rstrip()
            user_property = line.split(",") 
            user_property[-1] = user_property[-1].rstrip()
            uname = user_property[73].replace(" ", "")
            Contact_tag = user_property[50].replace(" ", "")
            if "removed" not in Contact_tag and "xd-" not in uname and  len(Contact_tag) > 0 :
                len_local_list = len(local_list)
                if len_local_list > 0:
                    for ruser in local_list: 
                        if uname == ruser:
                            local_list.remove(ruser)
                            print line.rstrip()
                            #print ruser, Contact_tag, len(local_list)
    return 0

def get_globus_usernames(infile):
    """ read the rejected users that appear on the globus connect portal """
    user_list = []
    with open(infile,'r') as f:
        for line in f:
            newline= line.rstrip()
            user_property = newline.split(" ") 
            for word in user_property:
                if "@globusid.org" in word:
                    uname =  word.replace("@globusid.org","")
                    user_list.append(uname)
    return user_list

def get_args():
    """ Get the arguments for this program: Two input files are required. One contains the list of usernames from Insightly and the other is the list of rejected users from Globus under connect group  """
    parser = argparse.ArgumentParser(description='This script finds the list of removed users who are  not dagged as removed users in Insightly.  Usage: python program.py -i1 InsightContacts.csv -i2 rejected_list.dat ')
    parser.add_argument('-i1','--inputfile1', help='Record file 1',required=True)
    parser.add_argument('-i2','--inputfile2', help='Record file 2', required=True)
    args = parser.parse_args()
    return args
 
if __name__ == "__main__":
    arg_option = get_args() 
    print arg_option, type(arg_option), arg_option.inputfile1
    insightly_file, rejected_file = arg_option.inputfile1, arg_option.inputfile2
    globus_rejectednames = get_globus_usernames(rejected_file)
    match_rejected_users(insightly_file, globus_rejectednames)
 


