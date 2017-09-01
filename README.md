# Field-Management-Portal
Django based Field Management Portal to automate the process of land allocation.
Field Management is a Web Project written in Django 1.8 in Python 2.7

Section 1 - Requirements
	Python 2.7
	Django 1.8
	MySQL-Python [MySQLdb]
	MySQl Server

Section 2 - Running the Program
	To run passport_management you need to follow the following steps -
		1.Open Terminal/CMD.
		2.Change to projects home directory.
		3.If you are running the app for first time follow the following steps to create database and users with appropriate permissions -
			A.Open MySQL prompt with root access.
			B.Run the following command - 'source backupfile.sql'
		4.Run the Django web server to use the project using command - 'python manage.py runserver 80'

Section 3 - Explaining Project Structure
	The project contains 6 apps.
		1. dashboard 				//App for providing functionalities for dashboard
		2.login						//App for authenticating user,professor admin student plot-manager
		3.register					//App for registering user,professor student plot-manager

		
	1. - Dashboard Contains  views -
		A. requestsAdmin : Concerns with the request Admin recieves for Approval
		B. requestsProf : Concerns with the request Professor recieves for Approval
		C. HomeDashboard : Concern with Dashboard Home
		D. Profile : Concerns with Admin's Profile
		E. ReservePlots : concerns with Reservation of Plots
		F. ReservedPlots : allows users to view their reseved plots
		G. ShowMangedPlots : shows the plots managed by manager
		H. UpcomingReservations : shows the upcoming reservations
	2.login - Contains following views - 
		A.admin_login : allows admin login
		B.student_login
		C.plotManager_login : allows plot manager to login
		D.Loginlogout : for logout

	3.pmappl - Once user is authenticated, this app allows him to do following -
		A.student_registration
		B.professor_registration
		C.plotmanager_registration
			for allowing different users of portal to register
