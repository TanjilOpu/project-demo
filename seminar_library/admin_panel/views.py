from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from books.models import Book, Borrow
from accounts.models import User


def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            messages.error(request, 'Access denied.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@librarian_required
def dashboard(request):
    active_borrows = Borrow.objects.filter(is_returned=False).select_related('user', 'book')
    overdue = [b for b in active_borrows if b.is_overdue]
    total_books = Book.objects.count()
    total_students = User.objects.filter(role='student').count()
    blocked_students = User.objects.filter(is_blocked=True).count()
    return render(request, 'admin_panel/dashboard.html', {
        'active_borrows': active_borrows,
        'overdue_borrows': overdue,
        'total_books': total_books,
        'total_students': total_students,
        'blocked_students': blocked_students,
    })


@librarian_required
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        category = request.POST.get('category', '').strip()
        quantity = int(request.POST.get('quantity', 1))

        if not title or not author or not category:
            messages.error(request, 'Title, author, and category are required.')
        else:
            Book.objects.create(
                title=title, author=author, category=category,
                total_quantity=quantity, available_quantity=quantity
            )
            messages.success(request, f'Book "{title}" added successfully.')
            return redirect('librarian_books')

    return render(request, 'admin_panel/add_book.html')


@librarian_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title).strip()
        book.author = request.POST.get('author', book.author).strip()
        book.category = request.POST.get('category', book.category).strip()
        new_total = int(request.POST.get('quantity', book.total_quantity))
        diff = new_total - book.total_quantity
        book.total_quantity = new_total
        book.available_quantity = max(0, book.available_quantity + diff)
        book.save()
        messages.success(request, 'Book updated.')
        return redirect('librarian_books')
    return render(request, 'admin_panel/edit_book.html', {'book': book})


@librarian_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted.')
        return redirect('librarian_books')
    return render(request, 'admin_panel/delete_book.html', {'book': book})


@librarian_required
def librarian_books(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'admin_panel/books.html', {'books': books})


@librarian_required
def mark_returned(request, borrow_id):
    borrow = get_object_or_404(Borrow, pk=borrow_id, is_returned=False)
    if request.method == 'POST':
        borrow.is_returned = True
        borrow.return_date = timezone.now().date()
        borrow.save()
        borrow.book.available_quantity += 1
        borrow.book.save()
        messages.success(request, f'Book "{borrow.book.title}" marked as returned.')
    return redirect('librarian_dashboard')


@librarian_required
def block_student(request, user_id):
    student = get_object_or_404(User, pk=user_id, role='student')
    if request.method == 'POST':
        student.is_blocked = True
        student.save()
        messages.success(request, f'{student.name} has been blocked.')
    return redirect('librarian_students')


@librarian_required
def unblock_student(request, user_id):
    student = get_object_or_404(User, pk=user_id, role='student')
    if request.method == 'POST':
        student.is_blocked = False
        student.save()
        messages.success(request, f'{student.name} has been unblocked.')
    return redirect('librarian_students')


@librarian_required
def students_list(request):
    students = User.objects.filter(role='student').order_by('name')
    return render(request, 'admin_panel/students.html', {'students': students})


@librarian_required
def student_history(request, user_id):
    student = get_object_or_404(User, pk=user_id, role='student')
    borrows = Borrow.objects.filter(user=student).select_related('book').order_by('-created_at')
    return render(request, 'admin_panel/student_history.html', {
        'student': student,
        'borrows': borrows,
    })


@librarian_required
def borrow_history(request):
    borrows = Borrow.objects.all().select_related('user', 'book').order_by('-created_at')
    return render(request, 'admin_panel/borrow_history.html', {'borrows': borrows})