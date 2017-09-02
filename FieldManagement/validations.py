from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import connection

def isCharacter(Character) :
	return ( ord("A")<=ord(Character)<=ord("Z") ) or ( ord("a")<=ord(Character)<=ord("z") ) 

def isDigit(Character) :
	return ord("0")<=ord(Character)<=ord("9") 

def validateCharString(Name):
	if Name == "" :
		return False
	for i in Name :
		if 	not isCharacter(i) :
			return False
	return True	

def validateNumString(Name): #assumes not none is checked for already
	if Name == None :
		return True
	if Name == "" :
		return False
	for i in Name :
		if 	not isDigit(i) :
			return False
	return True	

def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def exists(Variable,AttrName,Relation,Int=False) :
	print "SELECT * FROM %s WHERE %s = %s;" % (Relation,AttrName,Variable) 
	with connection.cursor() as cursor :
		if Int :
			cursor.execute("SELECT * FROM %s WHERE %s = %s;" % (Relation,AttrName,Variable) )
		else :	
			cursor.execute("SELECT * FROM %s WHERE %s = '%s';" % (Relation,AttrName,Variable) )
		Data = cursor.fetchall()
		if len(Data)==0 :
			return False
	return True	

def validateFloatingNumber( Number ) :
	try :
		FNumber = float(Number)
	except :
		return False
	else :
		return True				

def isApproved(Variable,AttrName,Relation) :

	with connection.cursor() as cursor :
		cursor.execute("SELECT * FROM %s WHERE %s = '%s' AND Approved = 1;" % (Relation,AttrName,Variable) )
		Data = cursor.fetchall()
		if Data == None :
			return False
	return True 		


			


