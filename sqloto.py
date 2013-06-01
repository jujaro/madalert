import sqlite3 as lite
from cmd import Cmd
from collections import namedtuple
import os

DATABASEFILENAME = os.path.join(
	os.path.expanduser('~'),
	'madalert.db'
	)
	
con = lite.connect(DATABASEFILENAME)
cur = None

def pprinttable(rows):
	if len(rows) > 1:
		headers = rows[0]._fields
		lens = []
		for i in range(len(rows[0])):
			lens.append(
					len(
						str(max([x[i] for x in rows] + \
								[headers[i]],key=lambda x:len(str(x))))
						)
					)
		formats = []
		hformats = []
		for i in range(len(rows[0])):
			if isinstance(rows[0][i], int):
				formats.append("%%%dd" % lens[i])
			else:
				formats.append("%%-%ds" % lens[i])
			hformats.append("%%-%ds" % lens[i])
		pattern = " | ".join(formats)
		hpattern = " | ".join(hformats)
		separator = "-+-".join(['-' * n for n in lens])
		print hpattern % tuple(headers)
		print separator
		for line in rows:
			print pattern % tuple(line)
	elif len(rows) == 1:
		row = rows[0]
		hwidth = len(max(row._fields,key=lambda x: len(x)))
		for i in range(len(row)):
			print "%*s = %s" % (hwidth,row._fields[i],row[i])

class Sqlitecmd(Cmd):
	def default(self,line):
		if line[0] in ["q","e"]:
			quit()
		try:
			if line == "commit":
				print "result=",con.commit()
			if line == "rollback":
				print "result=",con.rollback()
			else:
				self.runsql(line)
		except Exception,e:
			print "Error performing sql:",e

	def namedtuple(self,rows,titles):
		titles = [t[0] for t in titles]
		Row = namedtuple('Row',titles)
		result = []
		for r in rows:
			result += [Row(*r)]
		return result

	def runsql(self,sql):
		global cur
		cur = con.cursor()
		cur.execute(sql)
		rows = cur.fetchall()
		if rows:
			nt = self.namedtuple(rows[0:40],cur.description)
			pprinttable(nt)
		else:
			print "Nothing returned"
		#format = ""
		#for c in cur.description:
		#	format += "%s,"
		#print format % tuple([d[0] for d in cur.description])
		#pprinttable(rows[0:10])
		#for row in :
		#	print format % tuple(row)

cmd = Sqlitecmd()
cmd.onecmd("SELECT NAME FROM sqlite_master WHERE type='table'")
cmd.cmdloop()


