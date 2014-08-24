import os
import json
from flask import Flask, render_template, request, Response, jsonify
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.idia
reg_entries = db['registration-entries']
advisors = db['advisors']

def schools():
    schools = set()
    all_entries = reg_entries.find(fields={'School':True})
    for ent in all_entries:
	schools.add(ent['School'])
    ret = [s for s in schools]
    return ret

"""
def process_cursor(cursor):
    for document in cursor:
	process_document(document)

def multi_school():
    cursors = reg_entries.parallel_scan(4)
    threads = [
	    threading.Thread(target=process_cursor, args=(cursor,))
	    for cursor in cursors]

    for thread in threads:
	thread.start()

    for thread in threads:
	thread.join()
"""

def get_email(full_name):
    multiple_options = False
    options = []
    first = last = ""
    if full_name.count(' ') > 1:
	multiple_options = True
	parts = full_name.split(" ")
	first = ' '.join([p for p in parts[:-1]])
	last = ''.join(parts[-1:])
	options.append((first,last))	
	first = ''.join(parts[:1])
	last = ' '.join(parts[1:])
	options.append((first,last))	
    elif full_name.count(' ') == 1:
	first, last = full_name.split(" ")
    else:
	first = full_name

    if multiple_options:
	for o in options:
	    advisor = advisors.find_one({'First Name':o[0],'Last Name':o[1]},fields={'Email':True})
	    if advisor:
		break
    else:
	advisor = advisors.find_one({'First Name':first,'Last Name':last},fields={'Email':True})
    if advisor:
	return advisor['Email']
    else:
	return ""

def entries(school=None):
    result = []
    if school:
	all_entries = reg_entries.find({'School':school},fields={'_id':False, 'School':True, 'Conference':True,
	'Number Of Students':True, 'Advisor':True, 'Number Of Chaperones':True})
    else:
	all_entries = reg_entries.find(fields={'_id':False, 'School':True, 'Conference':True,
	'Number Of Students':True, 'Advisor':True, 'Number Of Chaperones':True})
    for ent in all_entries:
	ent['NumberOfStudents'] = ent['Number Of Students']

	ent['NumberOfChaperones'] = ent['Number Of Chaperones']
	ent['Email'] = get_email(ent['Advisor'])
	result.append(ent)
    result.sort(key=lambda x: x['Conference'], reverse=True)
    return result

@app.route('/')
def home():
    return render_template('index.html', schools=schools(), data=entries())

"""
@app.route('/school', methods=['POST','GET'])
def route_school():
    if request.method == 'POST':
	school_name = request.form['name']
    elif request.method == 'GET':
	school_name = request.args.get('name','')

    return Response(json.dumps(entries(school_name), status=200, mimetype="application/json"))
"""

@app.route('/schools')
def route_schools():
    return Response(json.dumps(schools()), status=200, mimetype="application/json")

@app.route('/entries', methods=['POST', 'GET'])
def route_entries():
    if request.method == 'POST':
	school_name = request.form['schoolname']
	return Response(json.dumps(entries(school_name)), status=200, mimetype="application/json")

    return Response(json.dumps(entries()), status=200, mimetype="application/json")

@app.route('/conferences')
def route_conferences():
    pass

@app.route('/search', methods=['POST', 'GET'])
def route_search():
    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
