# import ast #converts string literal to dictionary
import mechanize
# import re
# import requests
import sys
import getpass
import os 

content = []
with open("./raw-data/stats/registration-entries-errored.txt", "r") as errlog:
   content = errlog.readlines()

ids = []
for c in content:
    c = c[:-1]
    arr = c.split("-")
    ids.append(arr[3])

raw_files_dir = "./raw-data/"

def build_url(ID, url=None):
    if url:
	return url+str(ID)
    else:
	return "http://idia.net/RegistrationArea/ConferenceRegistrationEntry.aspx?ID="+str(ID)

"""
if len(sys.argv) < 2:
    print "Usage: python scrape.py <username>"
    sys.exit(0)

# save auth information
username = sys.argv[1]
password = getpass.getpass()
"""

username = "ProhitI"
password = "purohit"

# urls
baseURL = "http://idia.net"

""" get errored pages """


# create browser object

br = mechanize.Browser()
br.open(baseURL)
assert br.viewing_html()

# select and submit form
# print br.response().read()
br.select_form(nr=0)
br.form['UserName'] = username
br.form['Password'] = password
br.submit()

assert br.viewing_html()
for i in ids:
    curr = build_url(i)
    print "starting ", curr
    try:
	br.open(curr)
	assert br.viewing_html()
    except:
	continue

    
    """
    for link in br.links():
	# school
	if link.url.startswith("/Admin/School.aspx?ID"):
	    temp = link.url.split("=")
	    school_url = build_url(link.url, "http://idia.net") 
	    print "\t trying ",school_url
	    try:
		br.open(school_url)
		assert br.viewing_html()
	    except:
		continue
	    file_name = "School-"+str(temp[1])+".html"
	    target_file = open(raw_files_dir+"/schools/"+file_name, "w")
	    target_file.write(br.response().read())

	# advisor 
	if link.url.startswith("/Admin/User.aspx?ID"):
	    temp = link.url.split("=")
	    advisor_url = build_url(link.url, "http://idia.net") 
	    print "\t trying ",advisor_url
	    try:
		br.open(advisor_url)
		assert br.viewing_html()
	    except:
		continue
	    file_name = "User-"+str(temp[1])+".html"
	    target_file = open(raw_files_dir+"/advisors/"+file_name, "w")
	    target_file.write(br.response().read())
	    br.open(curr)
	    assert br.viewing_html()
    """



    file_name = "Conference-Registration-Entry-"+str(i)+".html"
    target_file = open(raw_files_dir+"/registration-entries/"+file_name, "w")
    target_file.write(br.response().read())

