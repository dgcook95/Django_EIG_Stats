from django import forms
from .models import AgentStats, AgentManager

MANAGER_CHOICES = [
        ('Dylan Cook', 'Dylan Cook'),
        ('Griselda Hopingardner', 'Griselda Hopingardner'),
        ('Jack Brittain', 'Jack Brittain'),
        ('Thomas Wilcox', 'Thomas Wilcox'),
        ('Trevor Linton', 'Trevor Linton'),
        ('Christopher Banda', 'Christopher Banda'),
        ('Selena Rubio Saldana', 'Selena Rubio Saldana'),
        ('John Lane', 'John Lane'),
        # ('Nedra Galloway', 'Nedra Galloway (no data yet)'),
        # ('Alexander Jericoff', 'Alexander Jericoff (no data yet)'),
    ]

class ManagerForm(forms.ModelForm):

    manager = forms.ChoiceField(choices=MANAGER_CHOICES)
    
    class Meta:
        model = AgentManager
        fields = ['manager']
        labels = {'manager ': 'Manager'}
        

