from django import forms

class PrelaunchEmailsForm(forms.Form):
	first_name = models.CharField(max_length=50)
	email = models.EmailField()

	def save_email(self):
		pass