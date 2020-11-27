"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
        
        path('indexcopy/', indexcopy_view),
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from hmsSite.views import index_view, addProject_view, search_view, individual_project_page_view, pheme_login, logout, edit_project_view, eoi_view, still_relevant_view


admin.site.site_header = 'Research Project Administration'
admin.site.site_title = 'Research Project Administration'
admin.site.index_title = 'Research Project Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', index_view),
    path('addprojectpage/', addProject_view),
    path('search/', search_view),
    path('project/<int:id_num>/', individual_project_page_view, name='project-id'),
    path('project/<int:id_num>/eoi/', eoi_view, name='project-eoi'),
    path('project/<int:id_num>/edit/', edit_project_view, name='edit-project'),
    path('project/<int:id_num>/relevant/', still_relevant_view, name='relevant-project'),
    path('', index_view, name='home'),
    path('login/', pheme_login, name='login'),
    path('logout/', logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'hmsSite.views.error_403_view'
handler404 = 'hmsSite.views.error_404_view'
handler500 = 'hmsSite.views.error_500_view'
