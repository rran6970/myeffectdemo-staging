from django.core.management.base import BaseCommand, CommandError
from challenges.models import Challenge, ChallengeParticipant
import datetime
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage

class Command(BaseCommand):
    def handle(self, *args, **options):
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        challenges = Challenge.objects.filter(event_start_date=tomorrow)
        if challenges:
            template = get_template('emails/action_reminder.html')
            subject = 'My Effect - Action Reminder'
            for challenge in challenges:
                action_name = challenge.title
                event_start_date = challenge.event_start_date
                self.stdout.write("sending reminders for action: " + challenge.title)
                participants = ChallengeParticipant.objects.filter(challenge=challenge, status="approved")
                to = []
                for participant in participants:
                    to.append(str(participant.user.email))

                self.stdout.write(str(to))
                from_email = 'info@myeffect.ca'
                content = Context({ 'first_name': participant.user.first_name, 'action_name': action_name, 'event_start_date': event_start_date})
                render_content = template.render(content)
                try:
                    mail = EmailMessage(subject, render_content, from_email, to)
                    mail.content_subtype = "html"
                    mail.send()
                    print("success")
                except Exception, e:
                    print e
        else:
            self.stdout.write("no action starts tomorrow")

        self.stdout.write("done")