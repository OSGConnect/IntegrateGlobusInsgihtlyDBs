#!/usr/bin/python
#title           :extract_user_information_from_json.py  
#author          :Bala
#date            :July-6-2016
#version         :1.0
#usage           :python program.py -i userinfo.json 
#help            :python program.py --help
#notes           :Extracts user information from the globus database
#python_version  :2.7

import sys
import argparse
import re
import os.path
from collections import defaultdict

def get_contact_tag(line, match_tag_dict):
    """ From the list of project name, attach tag for each user """
    tag_list = [" "]*len(match_tag_dict)
    count = 0 
    for word in line: 
        for key, value in match_tag_dict.items():
            if key in word.lower():
                tag_list[count] = value
                count = count + 1 
                if count == len(match_tag_dict): 
                    count = 0
    # Do a reverse sort so that if there are empty spaces they go to the end
    tag_list.sort(reverse=True)

    # Bring the tag osg-connect-users to the front. 
    try:
        i = tag_list.index('osg-connect-users')
        tag_list[i], tag_list[0] = tag_list[0], tag_list[i]
    except ValueError:
        pass

    return tag_list

def extract_fields_from_file(infile, begin_pattern, end_pattern, key_list):
    """ Extract few fields for each user: username, name, email, phone, institute, department,FOS """
    user_id = defaultdict(list)
    with open(infile,'r') as f:
        for line in f:
            line.rstrip()
            if begin_pattern in line:
                user_property = [" "]*len(key_list)
                # Inner loop goes through begin to end. Here, the relevant fields 
                #are extracted as per the list given in key_list
                for line in f:
                    line.rstrip()
                    if end_pattern in line:
                        uname = user_property[0].replace(" ", "")
                        
                        fullname = "somevalue"
                        if 'PROFILE' in key_list[0]:
                            fullname = user_property[1].strip()
                        if fullname:
                            for i in user_property:
                                user_id[uname].append(i)
                        break
                    for i in range(0,len(key_list)):
                        if key_list[i] in line: 
                            key, value  = line.split(":",1)
                            if value and not value.isspace(): 
                                user_property[i] = value.replace('\n','').replace('[','').replace(']','').replace(',','').replace('\'','')
                            # The fullname need to be separated into first and last name. 
                            if 'PROFILE fullname' in key_list[i] and (len(value) > 1) and value and not value.isspace():
                                first_name = value.split()[0].replace('\n','')
                                last_name  = value.split()[-1].replace('\n','')
                                if first_name and not last_name: last_name = first_name
                                if last_name and not first_name: first_name = last_name
                                user_property[1] = first_name + ", "+ last_name

    return user_id

def get_args():
    """ Get the arguments for this program: Requires an input file that has user information from globus """
    parser = argparse.ArgumentParser(description='This script get user information username.  Usage: python program.py -i userinfo.json')
    parser.add_argument('-i','--inputfile', dest="filename", help='input file',required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arg_option = get_args() 
    input_file = arg_option.filename 

#Define patterns and tags
    #tag_ref_dict = {'osg':'osg-connect-users', 'atlas':'atlas-connect-users', 'cms': 'cms-connect-users', 'duke':'duke-ci-connect-users', 'uchicago':'uchicago-ci-connect-users', 'old-ConnectTrain': 'old-ConnectTrain'}
    tag_ref_dict = {'osg':'osg-connect-users', 'atlas':'atlas-connect-users', 'cms': 'cms-connect-users', 'duke':'duke-ci-connect-users', 'uchicago':'uchicago-ci-connect-users'}
    start_pattern = 'BEGIN'
    stop_pattern = 'END'
    profile_fields_list = [ 'PROFILE username', 'PROFILE fullname', 'PROFILE email', 'PROFILE-custom  phone', 'PROFILE-custom  institution', 'PROFILE-custom  department', 'PROFILE-custom  field_of_science' ]
    project_fields_list = ['SELECTED  username','SELECTED  projects' ]

# Extract the profile and project information of each user
    user_profile = extract_fields_from_file(input_file, start_pattern, stop_pattern, profile_fields_list) 
    user_project = extract_fields_from_file(input_file, start_pattern, stop_pattern, project_fields_list) 


    # Print the header for the csv file 
    print "Username, FirstName, LastName, Email, Phone, Organization Name, Department, Field of Science, ContactTag 1, ContactTag 2, ContactTag 3, ContactTag 4, ContactTag 5, ContactTag 6, Project Name 1 "

    # Based on the key value print both records
    for k in user_profile.iterkeys():
        lk = k.lower()
        if ('osg' not in lk) and ('connect' not in lk) and ('dgc' not in lk) and ('@' not in lk) and ('test' not in lk) and ('guest' not in lk) and ('fsurf' not in lk) and ('efdisk' not in lk) and ('user' not in lk) and ('jenkins' not in lk) :
            for field in user_profile[k]:
                print field, ",",  

            # Tag each user. The tags are osg, atlas, etc.
            contact_tag = get_contact_tag(user_project[k], tag_ref_dict) 
            cat_tag = " "
            for tag in contact_tag: 
                print tag, ", ",
                cat_tag = cat_tag + tag
            cat_tag = cat_tag.replace(" ","")
            if cat_tag == "":
                print "no_contact_tag, ",
            else:
                print " ,",
            print user_project[k][1],   
            print " "
    
    
