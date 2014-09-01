import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import matplotlib
import sqlite3 as s3
import console
scoreDir = 'Stats/'

def initProgram():
	user = raw_input('\nEnter username\n').lower()
	conn = s3.connect('password.db')
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS passwords(username TEXT,password TEXT)')
	c.execute('SELECT username FROM passwords WHERE username =?',(user,))
	isTrue = c.fetchall()
	print len(isTrue)
	if len(isTrue)==0:
		init = raw_input('A user with this name could not be found would you like to create a account?(y/n)\n').lower()
		if init == 'y':
			createAccount(user)
		elif init == 'n':
			menu1()
		else: 
			initProgram()
	passw1 = raw_input('Enter Password\n')
	conn = s3.connect('password.db')
	c = conn.cursor()
	conn.text_factory = str
	c.execute('SELECT password FROM passwords WHERE  username=?',(user,))
	user2 = c.fetchone()
	c.close()
	user2 = ''.join(user2)
	if passw1 == user2:
		return user
	else:
		print 'Password and Username do not match!\n'
		initProgram()

def createAccount(user):
	password = raw_input('Create a password. Warning! Password cannot be change or retrieved once set!\n')
	conn = s3.connect('password.db')
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS passwords(username TEXT,password TEXT)')
	c.execute('INSERT INTO passwords(username, password) VALUES(?,?)',(user,password))
	c.execute('CREATE TABLE IF NOT EXISTS '+user+'(score INT)')
	conn.commit()
	c.close()
	textfile = open(scoreDir+user+'.txt', 'a')
	textfile.close()

def getRaw(a,b,c, one, two, three):
	totalScore = a + b + c
	myScore = one + two + three
	wrongScore = totalScore - myScore
	wrongScore = wrongScore * 0.25
	rawScore = myScore - wrongScore
	return rawScore

def menu1():
	print 'What would you like to do?\n'
	print 'Login(l)\nQuit(q)\n'
	inp = raw_input().lower()
	if inp == 'q':
		console.clear()
		sys.exit()
	elif inp == 'l':
		user = initProgram()
		menu2(user)
	else: 
		menu1()

def menu2(user):
	print 'What would you like to do?\n'
	print 'Enter New Scores(n)\nView Result Graph(r)\nCompare Scores(c)\nQuick Input(qi)Logout(lo)\nQuit(q)'
	inp = raw_input().lower()
	if inp == 'q':
		console.clear()
		sys.exit()
	elif inp == 'n':
		newTest(user)
	elif inp == 'r':
		grapher(user)
		plt.show()
		plt.close()
		menu2(user)
	elif inp == 'c':
		str = raw_input('Enter usernames of the people you want to compare to yourself seperated by spaces\n')
		arr = str.split()
		comparePlot(arr,user)
		plt.show()
		plt.close()
		menu2(user)
	elif inp == 'lo':
		menu1()
	elif inp == 'qi':
		score = raw_input('Enter score out of 2400')
		writeToFile(user,score)	
	else:
		menu2(user)
		
def newTest(user):
	print 'Type q to exit at any time.'
	critRaw = getReading(user)
	mathRaw = getMath(user)
	writeRaw = getWriting(user)
	totalScore = matchScores(critRaw,mathRaw,writeRaw)
	writeToFile(username,totalScore)

def getReading(user):
	read1 = raw_input( 'Enter First Critical Reading Score.(Max 24)\n')
	if read1 == 'q':
		menu2(user)
		return ''
	if int(read1) > 24:
		read1 = raw_input( 'Enter First Critical Reading Score.(Max 24)\n')
	read2 = raw_input( 'Enter Second Critical Reading Score.(Max 24)\n')
	if read2 == 'q':
		menu2(user)
		return ''
	if int(read2) > 24:
		read2 = raw_input( 'Enter Second Critical Reading Score.(Max 24)\n')
	read3 = raw_input( 'Enter Third Critical Reading Score.(Max 19)\n')
	if read3 == 'q':
		menu2(user)
		return ''
	if int(read3) > 19:
		read3 = raw_input( 'Enter Third Critical Reading Score. (Max. 19)\n')
	raw = round(getRaw(24,24,19,int(read1),int(read2),int(read3)))
	return raw

def getMath(user):
	read1 = raw_input( 'Enter First Math Score.(Max 20)\n')
	if read1 == 'q':
		menu2(user)
		return ''
	if int(read1) > 20:
		read1 = raw_input( 'Enter First Math Score.(Max 20)\n')
	read2 = raw_input( 'Enter Second Math Score.(Max 18)\n')
	if read2 == 'q':
		menu2(user)
		return ''
	if int(read2) > 18:
		read2 = raw_input( 'Enter Second Math Score.(Max 18)\n')
	read3 = raw_input( 'Enter Third Math Score.(Max 16)\n')
	if read3 == 'q':
		menu2(user)
		return ''
	if int(read3) > 16:
		read3 = raw_input( 'Enter Third Math} Score. (Max. 16)\n')
	raw = round(getRaw(20,18,16,int(read1),int(read2),int(read3)))
	return raw
	
def getWriting(user):
	read1 = raw_input('Enter First Writing Score.(Max 35)\n')
	if read1 == 'q':
		menu2(user)
		return ''
	if int(read1) > 35:
		read1 = raw_input('Enter First Writing Score.(Max 35)\n')
	read2 = raw_input( 'Enter Second Writing Score.(Max 14)\n')
	if read2 == 'q':
		menu2(user)
		return ''
	if int(read2) > 14:
		read2 = raw_input('Enter Second Writing Score.(Max 14)\n')
	raw = round(getRaw(35,14,0,int(read1),int(read2),0),0)
	return raw
	
def matchScores(a,b,c):
	file = open('tables/chart.txt','r')
	convertArr = file.read().splitlines()
	file.close()
	file2 = open('tables/write.txt','r')
	essayArr = file2.read().splitlines()
	file2.close()
	reader=convertArr.index(str(int(a))+' ')
	readArr = convertArr[reader+1].split()
	readIn = readArr[0]
	mather=convertArr.index(str(int(b))+' ')
	mathArr = convertArr[mather+1].split()
	mathIn = mathArr[1]
	writer=essayArr.index(' '+str(int(c))+' ')
	writeArr = essayArr[writer+1].split()
	writeScore = int(raw_input('Enter Essay Score. (Max 12)\n'))
	scoreIndex = 12 - writeScore
	writeIn = writeArr[scoreIndex]
	print '\n'
	print 'Your total SAT score out of a possible 2400 is:\n'
	print int(readIn) + int(mathIn) + int(writeIn)
	return int(readIn) + int(mathIn) + int(writeIn)
	
def writeToFile(user,score):
	#statFile = open(scoreDir+user+'.txt','a')
	#statFile.write(str(score)+'\n')
	#statFile.close()
	conn = s3.connect('password.db')
	c = conn.cursor()
	c.execute('INSERT INTO '+user+'(score) VALUES(?)',(score,))
	conn.commit()
	c.close()
	menu2(user)

def grapher(user):
	#statFile1 = open(scoreDir+user+'.txt','r')
	#statsArr = statFile1.readlines()
	conn = s3.connect('password.db')
	c = conn.cursor()
	c.execute('SELECT score FROM '+user)
	tupleArr = c.fetchall()
	statsArr = []
	for tup in tupleArr:
		statsArr.append(int(tup[0]))
	print  statsArr
	#statsArr = map(lambda s: s.strip(), statsArr)
	#statsArr = map(lambda s: int(s), statsArr)
	size = len(statsArr)
	if size ==  0:
		print 'You Have Not Completed Any Previous Tests.\n'
		newTest(user)
		return ''
	numElems = []
	for x in range(1,size+1):
		numElems.append(x)
	mini = min(statsArr)
	#statFile1.close()
	fig = plt.figure(1)
	plt.plot(numElems,statsArr, 'o-',label = user)
	fig.suptitle('SAT Score History')
	axisArr =[]
	axisArr.append(0)
	axisArr.append(size)
	axisArr.append(mini-100)
	axisArr.append(2400)
	plt.xlabel('Attempt Number')
	plt.ylabel('Score')
	plt.xticks(np.arange(min(numElems), max(numElems)+1, 1.0))
	plt.yticks(np.arange(min(statsArr)-150,2400,100.0))
	fig.subplots_adjust(bottom=0.2)

def comparePlot(arr,name):
	grapher(name)
	for user in arr:
		grapher(user)
	plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),fancybox=True, shadow=True, ncol=5)

menu1()()
