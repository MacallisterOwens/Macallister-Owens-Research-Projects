from celery import shared_task
from hmsSite.models import Project
from datetime import date
import os

@shared_task
def project_reminder():
    projs = Project.objects.all()
    today = date.today
    for p in projs:
        delta = today - p.last_reminder
        if(p.approved == True and p.email_sent == True):
            if(delta.days > 13):
                p.approved = False
                p.email_sent = False
                p.archive()
        elif(p.approved == True and delta.month >= 6):
            p.last_reminder = date.today
            p.email_sent = True
            reversedUrl = ''
            if os.environ.get('DJANGO_ENV') == 'production':
                reversedUrl = 'https://researchprojectsdemo.azurewebsites.net/project/' + str(p.id) + '/relevant/'
            else:
                reversedUrl = 'http://127.0.0.1:8000/project/' + str(p.id) + '/relevant/'
            p.user.email_user(
                'IMPORTANT: Your project - ' + p.title + ' - will expire in 2 weeks',
                'Hello ' + p.user.get_full_name() + ',\r\n\r\nYour project - ' + p.title + ' - will expire two weeks from now unless action is taken.\r\n\r\n'
                + 'Please confirm whether your project is ongoing and still relevant by following <a href=\"' + reversedUrl + '\" target=\"_blank\"this link<a/>\r\n\r\nThis is an automated email. Please do not reply to it.',
                ''
            )

        
