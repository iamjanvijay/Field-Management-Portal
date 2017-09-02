from django.conf.urls import include, url
from register import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'FieldManagement.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^/student', views.student_registration, name = "SRegister" ),
    url(r'^/professor', views.professor_registration, name = "PFRegister" ),
    url(r'^/plotmanager', views.plotmanager_registration, name = "PMRegister" ),
]