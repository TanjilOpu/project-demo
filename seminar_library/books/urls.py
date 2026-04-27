from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('renew/<int:borrow_id>/', views.renew_book, name='renew_book'),
    path('my-borrows/', views.my_borrows, name='my_borrows'),
]
