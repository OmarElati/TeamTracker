from django import forms


class WorkerCreationForm(forms.Form): # Form class for creating a worker
    email = forms.EmailField(label='Worker Email')
