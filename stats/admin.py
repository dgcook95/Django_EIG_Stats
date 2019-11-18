from django.contrib import admin
from stats.models import AgentStats, AgentManager

admin.site.register(AgentStats)
admin.site.register(AgentManager)
