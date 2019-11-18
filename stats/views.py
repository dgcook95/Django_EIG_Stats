from django.shortcuts import render
from .models import AgentStats, AgentManager, ManagerStats
from .forms import ManagerForm

def home(request):
    template = 'stats/home.html'
    return render(request, template)

def stats(request):
    template = 'stats/stats.html'
    form = ManagerForm()
    if request.method == 'POST':
        form = ManagerForm(request.POST)
        if form.is_valid():
            agentinfo = form.cleaned_data['manager']
            stats = AgentStats.objects.filter(manager=agentinfo)
            man_stats = ManagerStats.objects.filter(manager=agentinfo)
            return render(request, template, {'stats': stats, 'man_stats': man_stats ,'form': form})
    else:
        return render(request, template, {'form': form})

