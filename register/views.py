from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import connection
from FieldManagement import validations
from FieldManagement.validations import exists,validateEmail,validateFloatingNumber,isApproved
# Create your views here.

@csrf_protect
def student_registration(request) :

	if request.method == 'POST' :  # if its a post request
		# getting data out of form
		StudID = request.POST.get('StudID')
		FirstName = request.POST.get('FirstName')
		MiddleName = request.POST.get('MiddleName')
		LastName = request.POST.get('LastName')
		DeptID = request.POST.get('DeptID')
		Sex = request.POST.get('Sex')
		MobileNo = request.POST.get('MobileNo')
		Course = request.POST.get('Course')
		ProfID = request.POST.get('ProfID')
		EmailID = request.POST.get('EmailID')
		Password = request.POST.get('Password')
		RePassword = request.POST.get('RePassword')

		isValidateData = True

		isStudIDValidate = (StudID != None ) and (not exists(StudID,"StudID","Advisor")) and (not exists(StudID,"StudID","Student")) and (StudID[0:2] == "ST") and validations.validateNumString(StudID[2:12]) and (len(StudID)==12)
		isValidateData &= isStudIDValidate
		isFirstNameValidate = (FirstName != None ) and validations.validateCharString(FirstName)
		isValidateData &= isFirstNameValidate
		isMiddleNameValidate = validations.validateCharString(MiddleName) or (MiddleName=="") 
		isValidateData &= isMiddleNameValidate
		isLastNameValidate = validations.validateCharString(FirstName) or (LastName=="") 
		isValidateData &= isLastNameValidate
		isDeptIDValidate = (DeptID != None ) and (exists(DeptID,"DeptID","Department",True)) and validations.validateNumString(DeptID)
		isValidateData &= isDeptIDValidate
		isMobileNoValid = (MobileNo != None ) and validations.validateNumString(MobileNo) and MobileNo[0]!="0" and (len(MobileNo) == 10) and (not exists(MobileNo,"MobileNo","Student"))
		isValidateData &= isMobileNoValid
		isEmailIDValid = validateEmail(EmailID) and (not exists(EmailID,"EmailID","Student"))
		isValidateData &= isEmailIDValid
		isProfIDValid = (ProfID != None) and exists(ProfID,"ProfID","Professor") and isApproved(ProfID,"ProfID","ProfApproved")
		isValidateData &= isProfIDValid
		isPasswordValid = (Password != None) and (len(Password)>=8 and len(Password)<=16)
		isValidateData &= isPasswordValid
		isRePasswordValid = (Password==RePassword)
		isValidateData &= isRePasswordValid
		
		if isValidateData :

			with connection.cursor() as cursor :

				try :
					if MiddleName != "" and LastName != "" :
						cursor.execute("INSERT INTO Student(StudID,FirstName,MiddleName,LastName,DeptID,Sex,MobileNo,Course,EmailID,Password) VALUES ('%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s');" % (StudID,FirstName,MiddleName,LastName,DeptID,Sex,MobileNo,Course,EmailID,Password))
					elif MiddleName == "" and LastName != "" :
						cursor.execute("INSERT INTO Student(StudID,FirstName,LastName,DeptID,Sex,MobileNo,Course,EmailID,Password) VALUES ('%s','%s','%s',%s,'%s','%s','%s','%s','%s');" % (StudID,FirstName,LastName,DeptID,Sex,MobileNo,Course,EmailID,Password))
					elif MiddleName != "" and LastName == "" :
						cursor.execute("INSERT INTO Student(StudID,FirstName,MiddleName,DeptID,Sex,MobileNo,Course,EmailID,Password) VALUES ('%s','%s','%s',%s,'%s','%s','%s','%s','%s');" % (StudID,FirstName,MiddleName,DeptID,Sex,MobileNo,Course,EmailID,Password))
					else :
						cursor.execute("INSERT INTO Student(StudID,FirstName,DeptID,Sex,MobileNo,Course,EmailID,Password) VALUES ('%s','%s',%s,'%s','%s','%s','%s','%s');" % (StudID,FirstName,DeptID,Sex,MobileNo,Course,EmailID,Password))
					cursor.execute("INSERT INTO Advisor VALUES('%s','%s',%s);" % (ProfID,StudID,0))	
				except Exception, e:
					context = {  'DBerror' : str(e) ,}
					return render(request,"student_register.html",context)					
				else :
					context = { 'RegSuccess' : True ,}
					return render(request,"home.html",context)	

		else :
			context = {'isProfIDValid' : not isProfIDValid ,'isStudIDValidate' : not isStudIDValidate, 'isFirstNameValidate' : not isFirstNameValidate, 'isMiddleNameValidate' : not isMiddleNameValidate, 'isLastNameValidate' : not isLastNameValidate, 'isDeptIDValidate' : not isDeptIDValidate,'isMobileNoValid' : not isMobileNoValid, 'isEmailIDValid' : not isEmailIDValid, 'isPasswordValid' : not isPasswordValid, 'isRePasswordValid' : not isRePasswordValid}
			return render(request,"student_register.html",context)	
		
	else : # if its a get request
		return render(request,"student_register.html",{})

@csrf_protect
def professor_registration(request) :

	if request.method == 'POST' :  # if its a post request
		# getting data out of form
		ProfID = request.POST.get('ProfID')
		FirstName = request.POST.get('FirstName')
		MiddleName = request.POST.get('MiddleName')
		LastName = request.POST.get('LastName')
		DeptID = request.POST.get('DeptID')
		Sex = request.POST.get('Sex')
		MobileNo = request.POST.get('MobileNo')
		Designation = request.POST.get('Designation')
		AdminID = request.POST.get('AdminID')
		EmailID = request.POST.get('EmailID')
		Password = request.POST.get('Password')
		RePassword = request.POST.get('RePassword')

		isValidateData = True

		isProfIDValidate = (ProfID != None ) and (not exists(ProfID,"ProfID","ProfApproved")) and (not exists(ProfID,"ProfID","Professor")) and (ProfID[0:2] == "PF") and validations.validateNumString(ProfID[2:12]) and (len(ProfID)==12)
		isValidateData &= isProfIDValidate
		isFirstNameValidate = (FirstName != None ) and validations.validateCharString(FirstName)
		isValidateData &= isFirstNameValidate
		isMiddleNameValidate = validations.validateCharString(MiddleName) or (MiddleName=="") 
		isValidateData &= isMiddleNameValidate
		isLastNameValidate = validations.validateCharString(FirstName) or (LastName=="") 
		isValidateData &= isLastNameValidate
		isDeptIDValidate = (DeptID != None ) and (exists(DeptID,"DeptID","Department",True)) and validations.validateNumString(DeptID)
		isValidateData &= isDeptIDValidate
		isMobileNoValid = (MobileNo != None ) and validations.validateNumString(MobileNo) and MobileNo[0]!="0" and (len(MobileNo) == 10) and (not exists(MobileNo,"MobileNo","Professor"))
		isValidateData &= isMobileNoValid
		isEmailIDValid = validateEmail(EmailID) and (not exists(EmailID,"EmailID","Professor"))
		isValidateData &= isEmailIDValid
		isAdminIDValidate = (AdminID != None) and exists(AdminID,"AdminID","Admin")
		isValidateData &= isAdminIDValidate
		isPasswordValid = (Password != None) and (len(Password)>=8 and len(Password)<=16)
		isValidateData &= isPasswordValid
		print "Password : ",Password
		print "Re-Password : ",RePassword		
		isRePasswordValid = (Password==RePassword)
		isValidateData &= isRePasswordValid
		
		if isValidateData :

			with connection.cursor() as cursor :

				try :
					if MiddleName != "" and LastName != "" :
						cursor.execute("INSERT INTO Professor(ProfID,FirstName,MiddleName,LastName,DeptID,Sex,MobileNo,Designation,EmailID,Password) VALUES ('%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s');" % (ProfID,FirstName,MiddleName,LastName,DeptID,Sex,MobileNo,Designation,EmailID,Password))
					elif MiddleName == "" and LastName != "" :
						cursor.execute("INSERT INTO Professor(ProfID,FirstName,LastName,DeptID,Sex,MobileNo,Designation,EmailID,Password) VALUES ('%s','%s','%s',%s,'%s','%s','%s','%s','%s');" % (ProfID,FirstName,LastName,DeptID,Sex,MobileNo,Designation,EmailID,Password))
					elif MiddleName != "" and LastName == "" :
						cursor.execute("INSERT INTO Professor(ProfID,FirstName,MiddleName,DeptID,Sex,MobileNo,Designation,EmailID,Password) VALUES ('%s','%s','%s',%s,'%s','%s','%s','%s','%s');" % (ProfID,FirstName,MiddleName,DeptID,Sex,MobileNo,Designation,EmailID,Password))
					else :
						cursor.execute("INSERT INTO Professor(ProfID,FirstName,DeptID,Sex,MobileNo,Designation,EmailID,Password) VALUES ('%s','%s',%s,'%s','%s','%s','%s','%s');" % (ProfID,FirstName,DeptID,Sex,MobileNo,Designation,EmailID,Password))
					cursor.execute("INSERT INTO ProfApproved VALUES('%s','%s',%s);" % (ProfID,AdminID,0))	
				except Exception, e:
					context = {  'DBerror' : str(e) ,}
					return render(request,"professor_register.html",context)					
				else :
					context = { 'RegSuccess' : True ,}
					return render(request,"home.html",context)	

		else :
			context = {'isProfIDValidate' : not isProfIDValidate ,'isAdminIDValidate' : not isAdminIDValidate, 'isFirstNameValidate' : not isFirstNameValidate, 'isMiddleNameValidate' : not isMiddleNameValidate, 'isLastNameValidate' : not isLastNameValidate, 'isDeptIDValidate' : not isDeptIDValidate,'isMobileNoValid' : not isMobileNoValid, 'isEmailIDValid' : not isEmailIDValid, 'isPasswordValid' : not isPasswordValid, 'isRePasswordValid' : not isRePasswordValid}
			return render(request,"professor_register.html",context)	
		
	else : # if its a get request
		return render(request,"professor_register.html",{})	


@csrf_protect
def plotmanager_registration(request) :

	if request.method == 'POST' :  # if its a post request
		# getting data out of form
		MangID = request.POST.get('MangID')
		FirstName = request.POST.get('FirstName')
		MiddleName = request.POST.get('MiddleName')
		LastName = request.POST.get('LastName')
		Sex = request.POST.get('Sex')
		MobileNo = request.POST.get('MobileNo')
		Experience = request.POST.get('Experience')
		AdminID = request.POST.get('AdminID')
		EmailID = request.POST.get('EmailID')
		Password = request.POST.get('Password')
		RePassword = request.POST.get('RePassword')

		isValidateData = True

		isMangIDValidate = (MangID != None ) and (not exists(MangID,"MangID","MangApproved")) and (not exists(MangID,"MangID","PlotManager")) and (MangID[0:2] == "PM") and validations.validateNumString(MangID[2:12]) and (len(MangID)==12)
		isValidateData &= isMangIDValidate
		isFirstNameValidate = (FirstName != None ) and validations.validateCharString(FirstName)
		isValidateData &= isFirstNameValidate
		isMiddleNameValidate = validations.validateCharString(MiddleName) or (MiddleName=="") 
		isValidateData &= isMiddleNameValidate
		isLastNameValidate = validations.validateCharString(FirstName) or (LastName=="") 
		isValidateData &= isLastNameValidate
		isMobileNoValid = (MobileNo != None ) and validations.validateNumString(MobileNo) and MobileNo[0]!="0" and (len(MobileNo) == 10)  and (not exists(MobileNo,"MobileNo","PlotManager"))
		isValidateData &= isMobileNoValid
		isEmailIDValid = validateEmail(EmailID) and (not exists(EmailID,"EmailID","PlotManager"))
		isValidateData &= isEmailIDValid
		isExperienceValid = (Experience!=None) and validateFloatingNumber(Experience) and len(Experience)<=5 and (0.0<=float(Experience)<=50.0)  and len(str((float(Experience)-int(float(Experience)))))==3
		isValidateData &= isExperienceValid
		isAdminIDValidate = (AdminID != None) and exists(AdminID,"AdminID","Admin")
		isValidateData &= isAdminIDValidate
		isPasswordValid = (Password != None) and (len(Password)>=8 and len(Password)<=16)
		isValidateData &= isPasswordValid
		# print "Password : ",Password
		# print "Re-Password : ",RePassword		
		isRePasswordValid = (Password==RePassword)
		isValidateData &= isRePasswordValid
		
		if isValidateData :

			with connection.cursor() as cursor :

				try :
					if MiddleName != "" and LastName != "" :
						cursor.execute("INSERT INTO PlotManager(MangID,FirstName,MiddleName,LastName,Sex,MobileNo,Experience,EmailID,Password) VALUES ('%s','%s','%s','%s','%s','%s',%s,'%s','%s');" % (MangID,FirstName,MiddleName,LastName,Sex,MobileNo,Experience,EmailID,Password))
					elif MiddleName == "" and LastName != "" :
						cursor.execute("INSERT INTO PlotManager(MangID,FirstName,LastName,Sex,MobileNo,Experience,EmailID,Password) VALUES ('%s','%s','%s','%s','%s',%s,'%s','%s');" % (MangID,FirstName,LastName,Sex,MobileNo,Experience,EmailID,Password))
					elif MiddleName != "" and LastName == "" :
						cursor.execute("INSERT INTO PlotManager(MangID,FirstName,MiddleName,Sex,MobileNo,Experience,EmailID,Password) VALUES ('%s','%s','%s','%s','%s',%s,'%s','%s');" % (MangID,FirstName,MiddleName,Sex,MobileNo,Experience,EmailID,Password))
					else :
						cursor.execute("INSERT INTO PlotManager(MangID,FirstName,Sex,MobileNo,Experience,EmailID,Password) VALUES ('%s','%s','%s','%s',%s,'%s','%s');" % (MangID,FirstName,Sex,MobileNo,Experience,EmailID,Password))
					cursor.execute("INSERT INTO MangApproved VALUES('%s','%s',%s);" % (MangID,AdminID,0))	
				except Exception, e:
					context = {  'DBerror' : str(e) ,}
					return render(request,"plotmanager_register.html",context)					
				else :
					context = { 'RegSuccess' : True ,}
					return render(request,"home.html",context)	

		else :
			context = {'isExperienceValid' : not isExperienceValid,'isMangValidate' : not isMangIDValidate ,'isAdminIDValidate' : not isAdminIDValidate, 'isFirstNameValidate' : not isFirstNameValidate, 'isMiddleNameValidate' : not isMiddleNameValidate, 'isLastNameValidate' : not isLastNameValidate, 'isMobileNoValid' : not isMobileNoValid, 'isEmailIDValid' : not isEmailIDValid, 'isPasswordValid' : not isPasswordValid, 'isRePasswordValid' : not isRePasswordValid}
			return render(request,"plotmanager_register.html",context)	
		
	else : # if its a get request
		return render(request,"plotmanager_register.html",{})				





















