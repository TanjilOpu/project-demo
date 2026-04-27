from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='librarian_dashboard'),
    path('books/', views.librarian_books, name='librarian_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('return/<int:borrow_id>/', views.mark_returned, name='mark_returned'),
    path('students/', views.students_list, name='librarian_students'),
    path('students/<int:user_id>/block/', views.block_student, name='block_student'),
    path('students/<int:user_id>/unblock/', views.unblock_student, name='unblock_student'),
    path('students/<int:user_id>/history/', views.student_history, name='student_history'),
    path('history/', views.borrow_history, name='borrow_history'),
]
