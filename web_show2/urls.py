"""web_show2 URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
"""
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', include('webApp.login.urls')),
    path('collect/', include('webApp.collect.urls')),
    path('certificate/', include('webApp.certificate.urls')),
    path('exam/', include('webApp.exam.urls')),
    path('account/', include('webApp.account.urls')),
    path('testsinfo/', include('webApp.testsinfo.urls')),
    path('personnel/', include('webApp.personnel.urls')),
    path('waste/', include('webApp.waste.urls')),
    path('expenditure_management/', include('webApp.expenditure_management.urls')),
    path('approval_administration/', include('webApp.approval_administration.urls')),
    path('financial_management/', include('webApp.financial_management.urls')),
    path('storage/', include('webApp.storage.urls')),
    path('monitor/', include('webApp.monitor.urls')),
    path('offshore/', include('phoneAPP.offshore.urls')),
    path('examine/', include('phoneAPP.examine.urls')),
    path('weixin/', include('webApp.weixin.urls')),
    path('mirror/', include('webApp.mirror.urls')),
]
