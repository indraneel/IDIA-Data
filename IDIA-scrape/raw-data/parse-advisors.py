from BeautifulSoup import BeautifulSoup
import re
import os
import json

REQUIRED_FIELDS = 12

def parse(dirpath, filename, output, stats, complete, error):
    print "working on = " + os.sep.join([dirpath, filename])
    name = filename[:-5]
    name += ".txt"
    index_html = open(os.sep.join([dirpath,filename]), 'r')
    # targetFile = open(os.sep.join(["../parsed-data/", name]), 'w')
    soup = BeautifulSoup(index_html)
    #classRegex = "01\:[0-9]{3}\:[0-9]{3}\:[0-9]{2}"
    
    if soup.findAll(text="Access Denied"):
	print "SKIPPING",name,"\tnot authed"
	stats['error'] += 1
	error.append(name)
	return
    # registration entry 
    table = soup.findAll("table", {"class": "Content"} )
    # deal with various table cases
    print "table length =", len(table)
    """
    if len(table) is 6:
	print "SKIPPING",name,"\tlist of confs"
	stats['error'] += 1
	error.append(name)
	return
    """

    stats['complete'] += 1
    complete.append(name)
    if table:
	# a working page seems to have 3 <table class="Content>'s
	# second table is the important one	
	table = table[1]
	tbodies = table.findAll("tbody") #first four are important
	item = {}
	for tbody in tbodies:
	    rows = tbody.findAll("tr")
	    for row in rows:
		cols = row.findAll("td")
		key = None
		is_key = True
		count = 0
		for col in cols:
		    val = col.text.strip().replace("&nbsp;", " ")
		    if not val:
			continue
		    if is_key is True:
			# print "----------"
			val = val.replace(":", "")
			is_key = False 
			item[val] = ""
			key = val
		    else:
			# print "value:"
			if key == "Email" or key == "Billing Email":
			    link = col.findAll("a", href=True)[0]['href'][7:]
			    val = link.strip().replace("&nbsp;", " ")
			is_key = True
			count += 1
			item[key] = val
			# print "{",key, ":", item[key],"}"

	
	output.append(item)

count = 0
list_of_files = {}
output = []
stats = {'complete':0, 'error':0}
complete = []
error = []
for (dirpath, dirnames, filenames) in os.walk("./advisors"):
    for filename in filenames:
        if filename[-5:] == ".html":
	    parse(dirpath, filename, output, stats, complete, error)

"""
with open("./registration-entries-stats.json", "w") as outfile:
    json.dump(stats, outfile)


f = open("./registration-entries-completed.txt", "w")
for c in complete:
    f.write(c)
    f.write("\n")
f.close()

f = open("./registration-entries-errored.txt", "w")
for e in error:
    f.write(e)
    f.write("\n")
f.close()


"""

print json.dumps(output)
with open("./stats/advisors.json", "w") as outfile:
    json.dump(output, outfile)
