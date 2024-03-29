from django.core.management.base import BaseCommand, CommandError
from stats.models import AgentStats, AgentManager, ManagerStats
import csv
import os
import collections

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        help = "Loads data from casework.csv into our AgentStats model"
        
        caseworkcsv = 'static/casework.csv'
        onlinecsv = 'static/online.csv'
        csatcsv = 'static/csat.csv'
        
        agent_cases_worked_dict = collections.defaultdict(list)
        agent_days_worked_dict = collections.defaultdict(list)
        agent_online_dict = collections.defaultdict(list)
        agent_csat_dict = collections.defaultdict(list)
        agent_total_surveys_dict = collections.defaultdict(list)
        agent_emails_sent_dict = collections.defaultdict(list)

        manager_csat_dict = collections.defaultdict(list)
        manager_online_dict = collections.defaultdict(list)
        
        roster = {}
        grand_total = {}

        def getDaysWorked(agent):
            return len(agent_days_worked_dict[agent])


        def getCasesWorked(agent):
            return len(agent_cases_worked_dict[agent])


        def getCasesPerDay(manager, agent):
            try: 
                return round(roster[manager][agent]['Cases Worked'] / roster[manager][agent]['Days Worked'], 2)
            except:
                return None

        
        def getAvgOnline(manager, agent):
            try:
                return round(sum(agent_online_dict[agent]) / 3600 / roster[manager][agent]['Days Worked'], 2)
            except:
                return None


        def getCasesPerHour(manager, agent):
            try:
                return round(roster[manager][agent]['Cases Worked'] / (roster[manager][agent]['Average Online Time'] * roster[manager][agent]['Days Worked']), 2)
            except:
                return None
        

        def getTotalSurveys(agent):
            return len(agent_total_surveys_dict[agent])

        
        def getCSAT(agent):
            return round(sum(agent_csat_dict[agent]) / len(agent_csat_dict[agent]), 2)


        def getEmailsSent(agent):
            return sum(agent_emails_sent_dict[agent])

        
        def getSTR(manager, agent):
            try:
                return float(round(roster[manager][agent]['Surveys Taken'] / roster[manager][agent]['Emails Sent'] * 100, 2))
            except:
                return None

        
        def managerOnline(manager):
            try:
                return round(sum(manager_online_dict[manager]) / 3600 / grand_total[manager]['Days Worked'], 2)
            except:
                return None


        def managerCSAT(manager):
            return round(sum(manager_csat_dict[manager]) / len(manager_csat_dict[manager]), 2)


        def managerCasesPerHour(manager):
            try:
                return round(grand_total[manager]['Cases Worked'] / (grand_total[manager]['Average Online Time'] * grand_total[manager]['Days Worked']), 2)
            except:
                return None

        def managerCasesPerDay(manager):
            try: 
                return round(grand_total[manager]['Cases Worked'] / grand_total[manager]['Days Worked'], 2)
            except:
                return None


        def managerSTR(manager):
            try:
                return float(round(grand_total[manager]['Surveys Taken'] / grand_total[manager]['Emails Sent'] * 100, 2))
            except:
                return None


        with open(caseworkcsv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # initializes dictionary and adds cases worked to final dict
                if row['User: Manager: Full Name'] not in roster:
                    roster[row['User: Manager: Full Name']] = {}
                if row['User: Full Name'] not in roster[row['User: Manager: Full Name']]:
                    roster[row['User: Manager: Full Name']][row['User: Full Name']] = {}
        
                agent_cases_worked_dict[row['User: Full Name']].append(row['Case: Case Number'])
                agent_emails_sent_dict[row['User: Full Name']].append(int(row['Case Messages Sent Count']))
            
                if row['Accept Date'].split()[0] not in agent_days_worked_dict[row['User: Full Name']]:
                    agent_days_worked_dict[row['User: Full Name']].append(row['Accept Date'].split()[0])

        with open(onlinecsv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Service Presence Status: Developer Name'] == "Online" and row['Status Duration'] != '':
                    agent_online_dict[row['User: Full Name']].append(int(row['Status Duration']))
                    manager_online_dict[row['User: Manager: Full Name']].append(int(row['Status Duration']))

        with open(csatcsv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                agent_total_surveys_dict[row['Agent: Full Name']].append(row['Case: Case Number'])
                agent_csat_dict[row['Agent: Full Name']].append(int(row['K Rating']))
                agent_csat_dict[row['Agent: Full Name']].append(int(row['C Rating']))
                manager_csat_dict[row['Team Manager']].append(int(row['K Rating']))
                manager_csat_dict[row['Team Manager']].append(int(row['C Rating']))

        # Example Dict Format: roster['Dylan Cook']['Agent Name']['Stat'] = ${stat}
        # Below code stores stats for individual agents

        for manager, value in roster.items():
            for agent, value2 in value.items():
                roster[manager][agent]['Days Worked'] = getDaysWorked(agent)
                roster[manager][agent]['Cases Worked'] = getCasesWorked(agent)
                roster[manager][agent]['Average Online Time'] = getAvgOnline(manager, agent)
                roster[manager][agent]['Cases Per Day'] = getCasesPerDay(manager, agent)
                roster[manager][agent]['Cases Per Hour'] = getCasesPerHour(manager, agent)
                roster[manager][agent]['CSAT'] = getCSAT(agent)
                roster[manager][agent]['Surveys Taken'] = getTotalSurveys(agent)
                roster[manager][agent]['Emails Sent'] = getEmailsSent(agent)
                roster[manager][agent]['STR'] = getSTR(manager, agent)

        for manager, value in roster.items():
            for agent, value2 in value.items():
                if manager not in grand_total:
                    grand_total[manager] = {}
                if 'Cases Worked' not in grand_total[manager]:
                    grand_total[manager]['Cases Worked'] = 0
                if 'Days Worked' not in grand_total[manager]:
                    grand_total[manager]['Days Worked'] = 0
                if 'Surveys Taken' not in grand_total[manager]:
                    grand_total[manager]['Surveys Taken'] = 0
                if 'Emails Sent' not in grand_total[manager]:
                    grand_total[manager]['Emails Sent'] = 0
                grand_total[manager]['Cases Worked'] += roster[manager][agent]['Cases Worked']
                grand_total[manager]['Days Worked'] += roster[manager][agent]['Days Worked']
                grand_total[manager]['Surveys Taken'] += roster[manager][agent]['Surveys Taken']
                grand_total[manager]['Emails Sent'] += roster[manager][agent]['Emails Sent']

        for manager, value in grand_total.items():
            grand_total[manager]['Average Online Time'] = managerOnline(manager)
            grand_total[manager]['CSAT'] = managerCSAT(manager)
            grand_total[manager]['Cases Per Hour'] = managerCasesPerHour(manager)
            grand_total[manager]['Cases Per Day'] = managerCasesPerDay(manager)
            grand_total[manager]['Survey Take Rate'] = managerSTR(manager)
        
        
        changed_agent = 0
        new_agent = 0

        changed_manager = 0
        new_manager = 0
        null_agent = 0
        
        old_data_agents = [item.name for item in AgentStats.objects.all()]
        csv_agents = []
        
        for manager, agentdict in roster.items():
            for agent, statsdict in agentdict.items():
                if AgentStats.objects.filter(name=agent).exists():
                    stat = AgentStats.objects.get(name=agent)
                    stat.cases_worked = roster[manager][agent]['Cases Worked']
                    stat.days_worked = roster[manager][agent]['Days Worked']
                    stat.cases_per_day = roster[manager][agent]['Cases Per Day']
                    stat.average_online_time = roster[manager][agent]['Average Online Time']
                    stat.cases_per_hour = roster[manager][agent]['Cases Per Hour']
                    stat.csat = roster[manager][agent]['CSAT']
                    stat.surveys_taken = roster[manager][agent]['Surveys Taken']
                    stat.emails_sent = roster[manager][agent]['Emails Sent']
                    stat.survey_take_rate = roster[manager][agent]['STR']
                    stat.save()
                    changed_agent += 1
                    csv_agents.append(agent)
                else:
                    stat = AgentStats()
                    stat.name = agent
                    stat.manager = manager
                    stat.cases_worked = roster[manager][agent]['Cases Worked']
                    stat.days_worked = roster[manager][agent]['Days Worked']
                    stat.cases_per_day = roster[manager][agent]['Cases Per Day']
                    stat.average_online_time = roster[manager][agent]['Average Online Time']
                    stat.cases_per_hour = roster[manager][agent]['Cases Per Hour']
                    stat.csat = roster[manager][agent]['CSAT']
                    stat.surveys_taken = roster[manager][agent]['Surveys Taken']
                    stat.emails_sent = roster[manager][agent]['Emails Sent']
                    stat.survey_take_rate = roster[manager][agent]['STR']
                    stat.save()
                    new_agent += 1

        
        for datauser in old_data_agents:
            if datauser not in csv_agents:
                stat = AgentStats.objects.get(name=datauser)
                stat.cases_worked = None
                stat.days_worked = None
                stat.cases_per_day = None
                stat.average_online_time = None
                stat.cases_per_hour = None
                stat.csat = None
                stat.surveys_taken = None
                stat.emails_sent = None
                stat.survey_take_rate = None
                stat.save()
                null_agent += 1


        for man, statdict in grand_total.items():
            if ManagerStats.objects.filter(manager=man).exists():
                total = ManagerStats.objects.get(manager=man)
                total.cases_worked = grand_total[man]['Cases Worked']
                total.days_worked = grand_total[man]['Days Worked']
                total.cases_per_day = grand_total[man]['Cases Per Day']
                total.average_online_time = grand_total[man]['Average Online Time']
                total.cases_per_hour = grand_total[man]['Cases Per Hour']
                total.csat = grand_total[man]['CSAT']
                total.surveys_taken = grand_total[man]['Surveys Taken']
                total.emails_sent = grand_total[man]['Emails Sent']
                total.survey_take_rate = grand_total[man]['Survey Take Rate']
                total.save()
                changed_manager += 1
            else:
                total = ManagerStats()
                total.manager = man
                total.cases_worked = grand_total[man]['Cases Worked']
                total.days_worked = grand_total[man]['Days Worked']
                total.cases_per_day = grand_total[man]['Cases Per Day']
                total.average_online_time = grand_total[man]['Average Online Time']
                total.cases_per_hour = grand_total[man]['Cases Per Hour']
                total.csat = grand_total[man]['CSAT']
                total.surveys_taken = grand_total[man]['Surveys Taken']
                total.emails_sent = grand_total[man]['Emails Sent']
                total.survey_take_rate = grand_total[man]['Survey Take Rate']
                total.save()
                new_manager += 1
        

        print("{changed} agents had data re-loaded, {created} agents created with new data, {nullvalue} agents have a NULL statline updated.".format(
            changed=changed_agent, created=new_agent, nullvalue = null_agent
        ))

        print("{changed} manager totals had data re-loaded, {created} manager totals created with new data.".format(
            changed=changed_manager, created=new_manager
        ))