from django_cron import CronJobBase, Schedule
from django.core.management import call_command

class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 1
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'mycleancity.my_cron_job'

 	def do(self):
		call_command('send_mail')