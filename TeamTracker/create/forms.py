from django import forms


class WorkerCreationForm(forms.Form):
    email = forms.EmailField(label='Worker Email')
