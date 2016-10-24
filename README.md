
This document shows how to add new users to mailchimp and insight.ly via scripts.  The following are the major steps:

(1) Pull all user data from globus 
(2) Clean the data and fill the relevent fields
(3) Pull the current data from insight.ly
(4) Compare globus and insigh.tly to find the users who need to be added to insight.ly
(5) Clean the new users data with Open Refine package 
(6) Push the new users data on insight.ly
(7) Pull the list of contacts specific to connect instances 
(8) Extract the first, last, and email fields from the insight.ly data 
(9) Push the csv file on Mailchimp

Now we look into each step in detail. 

(1) Pull all user data from globus 

The user information for all the connect instances are obtained by running the script at "/usr/local/gosync/user-info/gosync_userinfo"

$ ./gosync_userinfo user dump -t json > user_info.json

The json file contains the profile information for each user 

     username : dbala
     custom_fields : {u'first_name': u'Balamurugan', u'last_name': u'Desinghu', u'name': u'Balamuru
     gan Desinghu', u'country': u'US', u'field_of_science': u'Physics', u'email': u'dmbala@gmail.com', u'ph
one': u'9196996660', u'department': u'Computation Institute', u'organization': u'University of Chicago
', u'nonprofit': True, u'institution': u'University of Chicago'}
     first_name : Balamurugan
     ...

and also the project information for each user

     username : dbala
     status : active
     info : {'url': '/groups/fdb38a24-03c1-11e3-86f7-12313809f035/members/dbala'}
     role : member
     projects : ['freesurfer', 'duke', 'duke-swcstaff', 'MS-EinDRC', 'HTCC', 'SWC-OSG-IU15', 'ConnectTrain', 'cms', 'swc201412uc', 'duke-SWC-Duke15', 'DelhiWorkshop2015', 'OSG-Staff', 'atlas-org-uchicago', 'atlas', 'uchicago', 'xenon1t', 'atlas-wg-USAtlas-TechSupport', 'osg', 'uchicago-campus', 'UserSchool2016']
     ...
    

2) Clean the data and fill the relevant fields

It is convenient to use the python script `extract_fields_from_globusjson.py` to the relevant fields from the json file. 

     extract_fields_from_globusjson.py -i user_info.json > user_info.csv file

Some usernames such as test, jenkins, etc., are filtered out.  The following is the filter condition in the python script:

       if ('osg' not in lk) and ('connect' not in lk) and ('dgc' not in lk) and ('@' not in lk) and ('test' not in lk) and ('guest' not in lk) and ('fsurf' not in lk) and ('efdisk' not in lk) and ('user' not in lk) and ('jenkins' not in lk) :


3) Pull the current data from insight.ly

Go to insight.ly database, select the contacts, and then choose the option to export as csv file. You will get an email from insight.ly that provides a link to download the csv file. Click the link and get the zip file. The zip file is something like University_of_Chicago_Export_UJJE0G.zip. Unzip and you will see a file `Contacts.csv`. Usually, the list of users in Contacts.csv is more than what the list of users in `user_info.csv`, but this is okay. 

Extract the usernames from Contacts.csv:

    awk -F ',' '{print $74}' Contacts.csv  | sed  '/^$/d' > existing_users.txt


4) Compare globus and insigh.tly to find the users who need to be added to insight.ly

Get the list of new users who are not registered on insight.ly database

python find_new_users.py -i1 user_info_2016-10-20.csv -i2 existing_users.txt > new_contacts.csv


(5)  Clean the new users data with Open Refine package

For frequent updates this step may be discarded. Because `Open Refine` works well if the list of users are in the order of hundreds.  Usually, the new users are in the order of tens for a weekly or bi-weekly updates. 

(6) Push the new users data on insight.ly

On insight.ly, select import contacts, and choose `import contact as csv`. The import csv process on insight.ly is self guiding. After finishing the import, you get an email of summary. The summary contains information about which contacts are added and which are not added due to duplication. 

It is okay, even if the list of new users contains the old users, insight.ly should detect it.

(7)  Pull the list of contacts specific to connect instances 

Get the list of contacts under each contact tag such as osg-connect-users, etc. Then import as csv file. 

(8) Extract the first, last, and email fields from the insight.ly data 

As mentioned before, you get an email from insight.ly. Follow the email instructions and download the file. 

Open the csv file and delete the columns, except first, last and email address. 

9) Push the csv file on Mailchimp

Go to MailChimp, log in, and open the menu `List`. Under the `List` menu, you will see list that are specific to connect instances. Choose the correct list. 

Select the option `import subscribers` and then check the option `use the settings from last import`. 

You get an email that summarizes the import. 



