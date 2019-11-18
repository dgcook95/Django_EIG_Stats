from django.db import models

class AgentStats(models.Model):
    name = models.CharField(max_length=50)
    manager = models.CharField(max_length=50)
    cases_worked = models.IntegerField(null=True)
    days_worked = models.IntegerField(null=True)
    cases_per_day = models.FloatField(null=True)
    average_online_time = models.FloatField(null=True)
    cases_per_hour = models.FloatField(null=True)
    csat = models.FloatField(null=True)
    surveys_taken = models.IntegerField(null=True)
    emails_sent = models.IntegerField(null=True)
    survey_take_rate = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

class AgentManager(models.Model):
    name = models.CharField(max_length=50)
    manager = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ManagerStats(models.Model):
    manager = models.CharField(max_length=50)
    cases_worked = models.IntegerField(null=True)
    days_worked = models.IntegerField(null=True)
    cases_per_day = models.FloatField(null=True)
    average_online_time = models.FloatField(null=True)
    cases_per_hour = models.FloatField(null=True)
    csat = models.FloatField(null=True)
    surveys_taken = models.IntegerField(null=True)
    emails_sent = models.IntegerField(null=True)
    survey_take_rate = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.manager