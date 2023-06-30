from django.core.mail import send_mail
from django.http import HttpResponse
from django.test import TestCase

class MyTestCase(TestCase):
    def test_example(self):
        # Your test code here
        pass

def test_email_view(request):
    subject = 'Test Email'
    message = 'This is a test email'
    from_email = 'oe.etudiant@gmail.com'
    recipient_list = ['omaratitek5@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    return HttpResponse('Test email sent')
