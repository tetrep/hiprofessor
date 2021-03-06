#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import hpdb;
import pycurl
import cStringIO
import os;
	
print "Content-type: text/html"
print


print """
<html>
<body>
<script type="text/javascript"> 
	function toggle(name) {
		var ele = document.getElementById(name);
		if(ele.style.display == "block") {
			ele.style.display = "none";
		}
		else {
			ele.style.display = "block";
		}
	} 
</script>
"""
#<div id="some_text" style="width:80%; height: auto; margin-left: auto; margin-right:auto;padding: 20px; border: 1px solid black; color:C40000; font-family:verdana; font-size:40px">
#<b>HiProfessor</b>
#</div>
form = cgi.FieldStorage()
crn = form.getvalue("classcrn", "")

if crn!="":
	l = hpdb.get_class_location(crn)
	for loc in l:
		typ = ''
		if loc[9] == 'LEC':
			typ = 'Lecture'
		elif loc[9] == 'STU':
			typ = 'Studio'
		elif loc[9] == 'LAB':
			typ = 'Lab'
		elif loc[9] == 'REC':
			typ = 'Recitation'
		elif loc[9] == 'SEM':
			typ = 'Seminar'
		elif loc[9] == 'TES':
			typ = 'Test day'
		else:
			typ = loc[9]
		days = ""
		for d in loc[10:14]:
			if d == "M":
				days += ' '+'Mon'	
			elif d == "T":
				days += ' '+'Tues'	
			elif d == "W":
				days += ' '+'Wed'	
			elif d == "R":
				days += ' '+'Thurs'	
			elif d == "F":
				days += ' '+'Fri'	
		print """<script>
		parent.loadClass(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
</script>""" % (loc[0],loc[1],'\''+loc[2]+'\'','\''+str(loc[3])+'\'','\''+loc[4]+'\'','\''+str(loc[5])+'\'','\''+loc[6]+'\'','\''+str(loc[7])+'\'','\''+str(loc[8])+'\'','\''+str(days)+'\'','\''+str(typ)+'\'','\''+str(crn)+'\'')
print """<div id="menyou" style="width:80%; height: auto; margin-left: auto; margin-right:auto; padding: 20px; border: 1px solid black;font-family:verdana;color:C40000;font-size:18px;">"""

print '<a style="font-family:verdana;margin-left:10px;font-size:18px;color:#C40000;text-decoration:none;white-space:pre;" href="javascript:toggle(\'serch\');"><b>Class Search</b></a>'
print '<br/>'
print '<a style="font-family:verdana;margin-left:10px;font-size:18px;color:#C40000;text-decoration:none;white-space:pre;" href="javascript:toggle(\'usr\');"><b>User Features</b></a>'
print '</div>'
print """<div id="serch" style="display:none;width:80%; height: auto; margin-left: auto; margin-right:auto; margin-top:10px; padding: 20px; border: 1px solid black;font-family:verdana;color:C40000;font-size:18px;">"""
print """<form name="dropdown" action="searchresults.cgi" method="POST">

Department
<br/> 
<select name="dept" >
<option value="" selected="selected"></option>"""

depts = hpdb.get_departments()
for d in depts:
	print '<option value="'+d+'">'+d+'</option>'

print '</select>'
print """
<br/>
<br/>
Title <br/>
<input type="text" name="title">"""
print '<br/>'
print '<br/>'
print 'Semester'
print '<br/>'
print '<select name="semester">'
print '<option value="fall12" selected="selected">Fall 2012</option>'
print '</select>'

print """<br/>
<input type="submit" value="Search"/>
</form>
</div>"""
print """<div id="usr" style="display:none;width:80%; height: auto; margin-left: auto; margin-right:auto; margin-top:10px;padding: 20px; border: 1px solid black;font-family:verdana;color:C40000;font-size:18px;">"""

if cgi.FieldStorage().has_key("ticket"):
	ticket = cgi.FieldStorage()["ticket"].value
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'https://cas-auth.rpi.edu/cas/serviceValidate')
	c.setopt(c.POSTFIELDS, 'ticket='+ticket+'&service=http://ec2-107-20-104-15.compute-1.amazonaws.com/cgi-bin/search.cgi')
	c.setopt(c.WRITEFUNCTION, buf.write)
	c.perform()
	if '<cas:user>' in buf.getvalue():
		user = buf.getvalue()[buf.getvalue().index('<cas:user>')+10:buf.getvalue().index('</cas:user>')]
		hpdb.add_login(user,os.getenv("REMOTE_ADDR"),os.getenv("HTTP_USER_AGENT"));
	buf.close()
user = hpdb.check_login(os.getenv("REMOTE_ADDR"),os.getenv("HTTP_USER_AGENT"))
if user != "":
	print '<form name="user" action="schedule.cgi" method="GET">'
	print "Welcome user " + user + "!"
	print '<input name="sched" type="submit" value="Schedule"/>'
	print '<input name="logout" type="submit" value="Logout"/>'
	print "</form>"
else:
	print """<form name="login" style="margin-left:auto;margin-right:auto" action="login.cgi">
	<input type="submit" value="Login"/>
</form>"""
print "</div>"
print """</body>
</html>"""
