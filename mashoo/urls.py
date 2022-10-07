"""mashoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name="index.html")),
    path('',include('theme.urls')),
    path('',include('snooker.urls') ),
    path('', include('expenses.urls')),
    path('', include('employees.urls')),
    path('', include('futsal.urls')),
    path('', include('rental.urls')),
    path('', include('smsSetting.urls')),
    path('', include('accounting.urls')),
    path('', include('cafeteria.Items.urls')),
    path('', include('cafeteria.purchases.urls')),
    path('', include('cafeteria.sales.urls')),
    path('', include('cafeteria.salesTerminal.urls')),
    path('', include('cafeteria.suppliers.urls')),
    path('', include('cafeteria.customers.urls')),
    path('', include('cafeteria.CafeteriaExpenses.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
