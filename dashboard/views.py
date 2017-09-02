from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import connection
from FieldManagement import validations
from FieldManagement import views as FMviews
from collections import namedtuple
from FieldManagement.validations import exists,validateEmail,validateFloatingNumber,isApproved
from django.contrib.auth.models import User
import datetime,calendar
# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)

@login_required
def requestsAdmin(request):
	UserID = request.user.username
	if UserID[:2] != "AD" : #if not admin redirect to home
		return redirect(FMviews.home)
	
	if request.method == 'GET' :

		# professor requests
		professorRequests = ()
		with connection.cursor() as cursor :
			cursor.execute( "SELECT * FROM ProfApproved NATURAL JOIN Professor WHERE AdminID = '%s' AND Approved = 0;" % ( request.user ) )	
			data = namedtuplefetchall(cursor)
			if data!= None :
				professorRequests = data

		# plotmanager request
		plotmanagersRequests = ()
		with connection.cursor() as cursor :
			cursor.execute( "SELECT * FROM MangApproved NATURAL JOIN PlotManager WHERE AdminID = '%s' AND Approved = 0;" % ( request.user ) )	
			data = namedtuplefetchall(cursor)
			if data!= None :
				plotmanagersRequests = data

		context = { 'professorRequests' : professorRequests , 'plotmanagersRequests' : plotmanagersRequests}

		# print "This" , context['professorRequests']

		return render(request,"requestsToAdmin.html",context)
	else :

		PostData = request.POST

		for i in PostData :
			if i == 'csrfmiddlewaretoken' :
				continue
			# print i , PostData[i]

			if i[0:2]=="PM" and PostData[i] == "APP" :
				with connection.cursor() as cursor :
					cursor.execute("UPDATE MangApproved SET Approved = 1 WHERE MangID = '%s';" % (i));
					cursor.execute("SELECT * FROM PlotManager WHERE MangID = '%s';" % (i));
					DataDict = dictfetchall(cursor)[0]
					user = User.objects.create_user(username=DataDict['MangID'],password=DataDict['Password'],first_name=DataDict['FirstName'])
			elif	i[0:2]=="PM" and PostData[i] == "DIS" :
				with connection.cursor() as cursor :
					cursor.execute("DELETE FROM MangApproved WHERE MangID = '%s';" % (i) )
					cursor.execute("DELETE FROM PlotManager WHERE MangID = '%s';" % (i) )
			elif i[0:2]=="PF" and PostData[i] == "APP" :
				with connection.cursor() as cursor :
					cursor.execute("UPDATE ProfApproved SET Approved = 1 WHERE ProfID = '%s';" % (i))
					cursor.execute("SELECT * FROM Professor WHERE ProfID = '%s';" % (i));
					DataDict = dictfetchall(cursor)[0]
					user = User.objects.create_user(username=DataDict['ProfID'],password=DataDict['Password'],first_name=DataDict['FirstName'])

			elif	i[0:2]=="PF" and PostData[i] == "DIS" :
				with connection.cursor() as cursor :
					cursor.execute("DELETE FROM ProfApproved WHERE ProfID = '%s';" % (i) )
					cursor.execute("DELETE FROM Professor WHERE ProfID = '%s';" % (i) ) 

		professorRequests = ()
		with connection.cursor() as cursor :
			cursor.execute( "SELECT * FROM ProfApproved NATURAL JOIN Professor WHERE AdminID = '%s' AND Approved = 0;" % ( request.user ) )	
			data = namedtuplefetchall(cursor)
			if data!= None :
				professorRequests = data

		# plotmanager request
		plotmanagersRequests = ()
		with connection.cursor() as cursor :
			cursor.execute( "SELECT * FROM MangApproved NATURAL JOIN PlotManager WHERE AdminID = '%s' AND Approved = 0;" % ( request.user ) )	
			data = namedtuplefetchall(cursor)
			if data!= None :
				plotmanagersRequests = data

		context = { 'professorRequests' : professorRequests , 'plotmanagersRequests' : plotmanagersRequests}

		return render(request,"requestsToAdmin.html",context) 	

def requestsProf(request) :
	UserID = request.user.username
	if UserID[:2] != "PF" : #if not professor redirect to home
		return redirect(FMviews.home)
	
	if request.method == 'GET' :
		print "printing table"
		# professor requests
		studentRequests = ()
		with connection.cursor() as cursor :
			cursor.execute( "SELECT * FROM Advisor NATURAL JOIN Student WHERE ProfID = '%s' AND Approved = 0;" % ( request.user ) )	
			data = namedtuplefetchall(cursor)
			if data!= None :
				studentRequests = data

		context = { 'studentRequests' : studentRequests }

		# print "This" , context['professorRequests']

		return render(request,"requestToProf.html",context)
	else :

		PostData = request.POST

		for i in PostData :
			if i == 'csrfmiddlewaretoken' :
				continue
			# print i , PostData[i]

			if PostData[i] == "APP" :
				with connection.cursor() as cursor :
					cursor.execute("UPDATE Advisor SET Approved = 1 WHERE StudID = '%s';" % (i));
					cursor.execute("SELECT * FROM Student WHERE StudID = '%s';" % (i));
					DataDict = dictfetchall(cursor)[0]
					user = User.objects.create_user(username=DataDict['StudID'],password=DataDict['Password'],first_name=DataDict['FirstName'])
			elif PostData[i] == "DIS" :
				with connection.cursor() as cursor :
					cursor.execute("DELETE FROM Advisor WHERE StudID = '%s';" % (i) )
					cursor.execute("DELETE FROM Student WHERE StudID = '%s';" % (i) )

		studentRequests = ()
		with connection.cursor() as cursor :
			cursor.execute( "SELECT * FROM Advisor NATURAL JOIN Student WHERE ProfID = '%s' AND Approved = 0;" % ( request.user ) )	
			data = namedtuplefetchall(cursor)
			if data!= None :
				studentRequests = data

		context = { 'studentRequests' : studentRequests }

		# print "This" , context['professorRequests']

		return render(request,"requestToProf.html",context) 		

@login_required
def HomeDashboard(request) :
	context = { 'UserType' : request.user.username[0:2] }
	print context
	return render( request,"dashboard.html", context)

@login_required
def AllocatePlot(request) :
	UserID = request.user.username
	if UserID[:2] != "AD" : #if not admin redirect to home
		return redirect(FMviews.home)
	if request.method == 'GET' :
		return render(request,'allocatePlot.html')
	else :
		PostData = request.POST

		PlotID = PostData['PlotID']
		ApproxArea = PostData['ApproxArea']
		Texture = PostData['Texture']
		Drainage = PostData['Drainage']
		WaterHoldingCapacity = PostData['WaterHoldingCapacity']
		Aeration = PostData['Aeration']
		Location = PostData['Location']
		Rating = PostData['Rating']
		MangID = PostData['MangID']

		isDataValidate = True

		isPlotIDValidate = (PlotID != None ) and (not exists(PlotID,"PlotID","Plot"))  and (PlotID[0:2] == "PL") and validations.validateNumString(PlotID[2:12]) and (len(PlotID)==12)
		isDataValidate &= isPlotIDValidate
		isApproxAreaValidate = (ApproxArea!=None) and validateFloatingNumber(ApproxArea) and (500.0<=float(ApproxArea)<=1500.0)  and len(str((float(ApproxArea)-int(float(ApproxArea)))))==3
		isDataValidate &= isApproxAreaValidate
		isRatingValidate = (Rating!=None) and validateFloatingNumber(Rating) and (0.0<=float(Rating)<=5.0)  and len(str((float(Rating)-int(float(Rating)))))==3
		isDataValidate &= isRatingValidate
		isLocationValidate = (Location!=None)
		isDataValidate &= isLocationValidate
		isMangIDValidate = (MangID != None) and exists(MangID,"MangID","PlotManager") and isApproved(MangID,"MangID","MangApproved")
		isDataValidate &= isMangIDValidate

		if isDataValidate :

			with connection.cursor() as cursor :

				try :

					cursor.execute("SELECT * FROM SoilType WHERE Texture = '%s' AND Drainage = '%s' AND WaterHoldingCapacity = '%s' AND Aeration = '%s';" % (Texture,Drainage,WaterHoldingCapacity,Aeration) )
					Data = cursor.fetchall()
					N = 0
					# print Data
					if len(Data) == 0 :
						# print "Here"
						cursor.execute("SELECT * FROM SoilType;") 
						temp = cursor.fetchall()
						if temp != None  :
							N = len(temp) + 1
						cursor.execute("INSERT INTO SoilType(Texture,Drainage,WaterHoldingCapacity,Aeration) VALUES('%s','%s','%s','%s');" % (Texture,Drainage,WaterHoldingCapacity,Aeration) )
					else :
						N = Data[0][0]
						print N	
					print ("INSERT INTO Plot VALUES('%s',%s,%s,'%s',%s,'%s');" % (PlotID,ApproxArea,N,Location,Rating,MangID))		
					cursor.execute("INSERT INTO Plot VALUES('%s','%s',%s,'%s',%s,'%s');" % (PlotID,ApproxArea,N,Location,Rating,MangID))	
				except Exception, e:
					context = {  'DBerror' : str(e) ,}
					return render(request,"allocatePlot.html",context)			
				else :
					context = { 'RegSuccess' : True ,}
					return render(request,"allocatePlot.html",context)	

		else :

			context = {'isLocationValidate' : not isLocationValidate,'isPlotIDValidate' : not isPlotIDValidate ,'isApproxAreaValidate' : not isApproxAreaValidate, 'isRatingValidate' : not isRatingValidate, 'isMangIDValidate' : not isMangIDValidate }
			print context
			return render(request,"allocatePlot.html",context)


@login_required
def Profile(request):
	UserID = request.user.username

	if UserID[:2] == "AD" :
		if request.method == "GET" :
			context = {}
			with connection.cursor() as cursor :
				cursor.execute("SELECT * FROM Admin WHERE AdminID = '%s';" % (UserID) )
				context = dictfetchall(cursor)
			context = context[0]			
			return render(request,"AdminProfile.html",context)
	if UserID[:2] == "ST" :
			pass
	if UserID[:2] == "PF" :
			pass
	if UserID[:2] == "PM" :	
			pass


@login_required
def ReservePlots(request): 
	UserID = request.user.username
	if UserID[:2] != "ST" and UserID[:2] != "PF"   :
		return redirect(FMviews.home)
	if request.method == "POST" :
		StartDate = request.POST['StartDate']
		EndDate = request.POST['EndDate']
		try :
			SD = datetime.date(*map(int,StartDate.split('-')))
			ED = datetime.date(*map(int,EndDate.split('-')))
		except :
			with connection.cursor() as cursor :
				cursor.execute("SELECT * FROM Plot NATURAL JOIN SoilType;")
				PlotData = namedtuplefetchall(cursor)
			return render(request,'ReservePlots.html',{'PlotData':PlotData,'mindate':str(datetime.date.today()),'maxdate':str(add_months((datetime.date.today()),6)),'Message':'Invalid Dates !'})	
		else :
			if SD>ED and SD <= datetime.date.today():
				with connection.cursor() as cursor :
					cursor.execute("SELECT * FROM Plot NATURAL JOIN SoilType;")
					PlotData = namedtuplefetchall(cursor)
				return render(request,'ReservePlots.html',{'PlotData':PlotData,'mindate':str(datetime.date.today()),'maxdate':str(add_months((datetime.date.today()),6)),'Message':'Invalid Dates ! SD<=ED !'})					
	if request.method == "GET" :
		with connection.cursor() as cursor :
			cursor.execute("SELECT * FROM Plot NATURAL JOIN SoilType;")
			PlotData = namedtuplefetchall(cursor)
		return render(request,'ReservePlots.html',{'PlotData':PlotData,'mindate':str(datetime.date.today()),'maxdate':str(add_months((datetime.date.today()),6))})	
	elif request.POST['Book'] == "None" :
		PlotChecked = request.POST['Check']
		StartDate = request.POST['StartDate']
		EndDate = request.POST['EndDate']
		Data = ()
		with connection.cursor() as cursor :
			cursor.execute("SELECT * FROM Plot NATURAL JOIN SoilType;")
			PlotData = namedtuplefetchall(cursor)
		with connection.cursor() as cursor :
			print ("SELECT * FROM Reservations WHERE PlotID = '%s' AND Status='CONFIRM' AND StartDate<=date('%s') AND  EndDate>=date('%s');" % (PlotChecked,EndDate,StartDate) )
			cursor.execute("SELECT * FROM Reservations WHERE PlotID = '%s' AND Status='CONFIRM' AND StartDate<=date('%s') AND  EndDate>=date('%s');" % (PlotChecked,EndDate,StartDate) )
			Data = cursor.fetchall()
		if len(Data) == 0 :
			return render(request,'ReservePlots.html',{'StartDate':StartDate,'EndDate':EndDate,'PlotData':PlotData,'mindate':str(datetime.date.today()),'maxdate':str(add_months((datetime.date.today()),6)),'plotcheck' : PlotChecked,'Available':"Y"})
		else :		
			return render(request,'ReservePlots.html',{'StartDate':StartDate,'EndDate':EndDate,'PlotData':PlotData,'mindate':str(datetime.date.today()),'maxdate':str(add_months((datetime.date.today()),6)),'plotcheck' : PlotChecked,'Available':"N"})
	elif request.POST['Check'] == "None" :
		print "Booking"	, request.POST
		PlotChecked = request.POST['Book']
		StartDate = request.POST['StartDate']
		EndDate = request.POST['EndDate']
		print PlotChecked,StartDate,EndDate
		with connection.cursor() as cursor :
			cursor.execute("INSERT INTO Reservations(PlotID,StartDate,EndDate,Status) VALUES('%s',date('%s'),date('%s'),'%s');" % (PlotChecked,StartDate,EndDate,'CONFIRM') )
			cursor.execute("SELECT * FROM Reservations;")
			N = 10+len(cursor.fetchall())
			print "N is ",N
			if UserID[:2] == "ST" :
				print ("INSERT INTO StudReserves VALUES(%s,'%s');" % (N,UserID) )
				cursor.execute("INSERT INTO StudReserves VALUES(%s,'%s');" % (N,UserID) )
			else :
				print ("INSERT INTO ProffReserves VALUES(%s,'%s');" % (N,UserID)) 
				cursor.execute("INSERT INTO ProffReserves VALUES(%s,'%s');" % (N,UserID) )
		print "Hello!"		
		with connection.cursor() as cursor :
			cursor.execute("SELECT * FROM Plot NATURAL JOIN SoilType;")
			PlotData = namedtuplefetchall(cursor)
		return render(request,'ReservePlots.html',{'Message':'Booking Successful !','PlotData':PlotData,'mindate':str(datetime.date.today()),'maxdate':str(add_months((datetime.date.today()),6))})

@login_required
def ReservedPlots(request) :
	UserID = request.user.username
	if UserID[:2] != "ST" and UserID[:2] != "PF"   :
		return redirect(FMviews.home)
	with connection.cursor() as cursor :
		if UserID[:2] == "PF" :
			print ("SELECT * FROM Plot NATURAL JOIN Reservations NATURAL JOIN ProffReserves NATURAL JOIN CancelReason WHERE ProfID = '%s' AND EndDate >= date('%s')" % (UserID,str(datetime.date.today())) )
			cursor.execute("SELECT * FROM Plot NATURAL JOIN Reservations NATURAL JOIN ProffReserves NATURAL JOIN CancelReason WHERE ProfID = '%s' AND EndDate >= date('%s')" % (UserID,str(datetime.date.today())) )
		else :	
			cursor.execute("SELECT * FROM Plot NATURAL JOIN  Reservations NATURAL JOIN StudReserves NATURAL JOIN CancelReason WHERE StudID = '%s' AND EndDate >=  date('%s')" % (UserID,str(datetime.date.today())) )
		CanPlotData = dictfetchall(cursor)
		# print CanPlotData
		if UserID[:2] == "PF" :
			print ("SELECT * FROM Plot NATURAL JOIN Reservations NATURAL JOIN ProffReserves WHERE ProfID = '%s' AND EndDate >=  date('%s') AND Status='CONFIRM'" % (UserID,str(datetime.date.today())) )
			cursor.execute("SELECT * FROM Plot NATURAL JOIN Reservations NATURAL JOIN ProffReserves WHERE ProfID = '%s' AND EndDate >= date('%s') AND Status='CONFIRM'" % (UserID,str(datetime.date.today())) )
		else :	
			cursor.execute("SELECT * FROM Plot NATURAL JOIN  Reservations NATURAL JOIN StudReserves  WHERE StudID = '%s' AND EndDate >= date('%s') AND Status='CONFIRM'" % (UserID,str(datetime.date.today())) )
		ConPlotData = dictfetchall(cursor)	
		print ConPlotData
	
	return render(request,'ReservedPlots.html',{'ConPlotData':ConPlotData,'CanPlotData':CanPlotData})

@login_required
def ShowMangedPlots(request) :			
	UserID = request.user.username
	if UserID[:2] != "PM" :
		return redirect(FMviews.home)
	PlotData = []	
	with connection.cursor() as cursor :
		cursor.execute("SELECT * FROM Plot NATURAL JOIN SoilType WHERE MangID = '%s';" % (UserID) )
		PlotData = dictfetchall(cursor)
	return render(request,'ManagedPlots.html',{'PlotData':PlotData})

@login_required
def UpcomingReservations(request) :			
	UserID = request.user.username
	if UserID[:2] != "PM" :
		return redirect(FMviews.home)
	UPlotData = []	
	CPlotData = []
	if request.method == "GET" :
		with connection.cursor() as cursor :
			cursor.execute("SELECT * FROM Reservations NATURAL JOIN Plot WHERE MangID = '%s' AND StartDate >= date('%s') ORDER BY StartDate;" % (UserID,str(datetime.date.today())) )
			UPlotData = dictfetchall(cursor)	
			cursor.execute("SELECT * FROM Reservations NATURAL JOIN Plot WHERE MangID = '%s' AND EndDate >= date('%s') AND StartDate < date('%s') ORDER BY StartDate;" % (UserID,str(datetime.date.today()),str(datetime.date.today())) )
			CPlotData = dictfetchall(cursor)				
		return render(request,'UpcomingReservations.html',{'UPlotData':UPlotData, 'CPlotData':CPlotData})
	elif request.POST['Reason']==None :
		with connection.cursor() as cursor :
			cursor.execute("SELECT * FROM Reservations NATURAL JOIN Plot WHERE MangID = '%s' AND StartDate >= date('%s') ORDER BY StartDate;" % (UserID,str(datetime.date.today())) )
			UPlotData = dictfetchall(cursor)	
			cursor.execute("SELECT * FROM Reservations NATURAL JOIN Plot WHERE MangID = '%s' AND EndDate >= date('%s') AND StartDate < date('%s') ORDER BY StartDate;" % (UserID,str(datetime.date.today()),str(datetime.date.today())) )
			CPlotData = dictfetchall(cursor)				
		return render(request,'UpcomingReservations.html',{'UPlotData':UPlotData, 'CPlotData':CPlotData,'Message':"Need To Specify A reason to Cancel Reservation !"})	 	
	else :
		CanResvID = request.POST['CanResvID']
		Reason = request.POST['Reason']
		with connection.cursor() as cursor :
			cursor.execute("UPDATE Reservations SET Status = 'CANCEL' WHERE ResvID = '%s';" % (CanResvID) );
			cursor.execute("INSERT INTO CancelReason VALUES('%s','%s');" % (CanResvID,Reason) )		
		with connection.cursor() as cursor :
			cursor.execute("SELECT * FROM Reservations NATURAL JOIN Plot WHERE MangID = '%s' AND StartDate >= date('%s') ORDER BY StartDate;" % (UserID,str(datetime.date.today())) )
			UPlotData = dictfetchall(cursor)	
			cursor.execute("SELECT * FROM Reservations NATURAL JOIN Plot WHERE MangID = '%s' AND EndDate >= date('%s') AND StartDate < date('%s') ORDER BY StartDate;" % (UserID,str(datetime.date.today()),str(datetime.date.today())) )
			CPlotData = dictfetchall(cursor)				
		return render(request,'UpcomingReservations.html',{'UPlotData':UPlotData, 'CPlotData':CPlotData,'Message':"Cancellation Successful !"})	 






		







