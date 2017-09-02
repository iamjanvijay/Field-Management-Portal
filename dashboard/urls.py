from django.conf.urls import include, url
from dashboard import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'FieldManagement.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'FieldManagement.views.home', name='home'),
    url(r'^/$', views.HomeDashboard, name = "Homedashboard" ),
    url(r'^/profile$', views.Profile, name = "Profile" ),
    url(r'^/requestsadmin', views.requestsAdmin, name = "RequestsAdmin" ),
    url(r'^/reserveplots', views.ReservePlots, name = "ReservePlots" ),
    url(r'^/reservedPlots', views.ReservedPlots, name = "ReservedPlots" ),
    url(r'^/requestsprofessor', views.requestsProf, name = "AdvisorReq" ),
    url(r'^/allocatePlots', views.AllocatePlot, name = "AllocatePlot" ),
    url(r'^/managedPlots', views.ShowMangedPlots, name = "ManagedPlots" ),
    url(r'^/UpcomingReservations', views.UpcomingReservations, name = "UpcomingReservations" ),
    
]
