from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta


@shared_task
def send_due_reminders():
    from books.models import Borrow

    reminder_date = timezone.now().date() + timedelta(days=2)
    borrows = Borrow.objects.filter(
        is_returned=False,
        due_date=reminder_date,
        reminder_sent=False,
    ).select_related('user', 'book')

    sent_count = 0
    for borrow in borrows:
        subject = 'MBSTU Seminar Library — Book Due Soon'
        message = (
            f'Dear {borrow.user.name},\n\n'
            f'This is a reminder that the following book is due in 2 days:\n\n'
            f'  Book     : {borrow.book.title}\n'
            f'  Author   : {borrow.book.author}\n'
            f'  Issued   : {borrow.issue_date}\n'
            f'  Due Date : {borrow.due_date}\n\n'
            f'Please return or renew the book before the deadline to avoid being blocked.\n\n'
            f'Visit the library portal: {settings.SITE_URL}\n\n'
            f'MBSTU Seminar Library'
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[borrow.user.email],
            fail_silently=True,
        )
        borrow.reminder_sent = True
        borrow.save()
        sent_count += 1

    return f'Sent {sent_count} reminder(s).'
