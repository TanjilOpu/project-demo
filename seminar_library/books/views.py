from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Book, Borrow


def public_catalogue(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'books/catalogue.html', {'books': books})


@login_required
def book_list(request):
    books = Book.objects.all().order_by('title')
    active_borrow = Borrow.objects.filter(
        user=request.user, is_returned=False
    ).select_related('book').first()
    return render(request, 'books/book_list.html', {
        'books': books,
        'active_borrow': active_borrow,
    })


@login_required
def borrow_book(request, book_id):
    if request.user.is_blocked:
        messages.error(request, 'Your account is blocked. Please return overdue books first.')
        return redirect('book_list')

    active_borrow = Borrow.objects.filter(user=request.user, is_returned=False).first()
    if active_borrow:
        messages.error(request, 'You already have a borrowed book. Return it before borrowing another.')
        return redirect('book_list')

    book = get_object_or_404(Book, pk=book_id)
    if not book.is_available:
        messages.error(request, 'This book is currently unavailable.')
        return redirect('book_list')

    if request.method == 'POST':
        due = timezone.now().date() + timedelta(days=7)
        Borrow.objects.create(user=request.user, book=book, due_date=due)
        book.available_quantity -= 1
        book.save()
        messages.success(request, f'You have borrowed "{book.title}". Due date: {due}')
        return redirect('my_borrows')

    return render(request, 'books/borrow_confirm.html', {'book': book})


@login_required
def renew_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, pk=borrow_id, user=request.user, is_returned=False)

    if borrow.is_renewed:
        messages.error(request, 'You have already renewed this book once. It cannot be renewed again.')
        return redirect('my_borrows')

    if borrow.is_overdue:
        messages.error(request, 'This book is overdue and cannot be renewed.')
        return redirect('my_borrows')

    if request.method == 'POST':
        borrow.due_date += timedelta(days=7)
        borrow.is_renewed = True
        borrow.reminder_sent = False
        borrow.save()
        messages.success(request, f'Book renewed! New due date: {borrow.due_date}')
        return redirect('my_borrows')

    return render(request, 'books/renew_confirm.html', {'borrow': borrow})


@login_required
def my_borrows(request):
    active = Borrow.objects.filter(user=request.user, is_returned=False).select_related('book').first()
    history = Borrow.objects.filter(user=request.user, is_returned=True).select_related('book').order_by('-return_date')
    return render(request, 'books/my_borrows.html', {
        'active_borrow': active,
        'history': history,
    })
