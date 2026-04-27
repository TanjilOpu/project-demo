from django.contrib import admin
from django.urls import path, include
from books.views import public_catalogue

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', public_catalogue, name='home'),
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('librarian/', include('admin_panel.urls')),
]
