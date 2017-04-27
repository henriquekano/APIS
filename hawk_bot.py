from zenpy import Zenpy
import requests
import json
import slack_wrapper

config_path = './config.json'
# {}
def read_config():
	with open(config_path) as data_file:    
		data = json.load(data_file)
	return data

config = read_config()
creds = {
	'email' : config.get('configs').get('zendesk').get('account_email'),
	'password' : config.get('configs').get('zendesk').get('account_password'),
	'subdomain': config.get('configs').get('zendesk').get('subdomain')
}
zendesk_support_group_id = config.get('configs').get('zendesk').get('group_id')
slack_token = config.get('configs').get('slack').get('oauth_token')

# [Ticket]
def support_open_tickets(creds):
	zenpy_client = Zenpy(**creds)
	tickets = zenpy_client.search(
				type='ticket', 
				group_id=zendesk_support_group_id, 
				status=['open']
			)
	return tickets

# [{}]
def ticket_sla(ticket_id, creds):
	return requests.get(
		'https://pagarme.zendesk.com/api/v2/tickets/' + str(ticket_id) + '?include=slas', 
		auth=(creds.get('email'), creds.get('password'))
	)

# [{}]
def filter_achieved_metrics(slas):
	def achieved_status(sla):
		stage = sla['stage']
		return stage == 'achieved'
	#python 3's way of doing it...
	achieved_status_tickets = list(filter(achieved_status, slas))
	return achieved_status_tickets

# [{}]
def filter_near_achieve_metrics(slas):
	def minutes_from_achieving(minutes):
		def filter(sla):
			minutes_left = sla['minutes']
			return minutes_left >= -minutes and minutes_left <= 0
	#python 3's way of doing it...
	achieved_status_tickets = list(filter(minutes_from_achieving(20), slas))
	return achieved_status_tickets

def format_metrics_message(metrics):
	def format(metric):
		time = ''
		if metric.get('days') is not None:
			time += str(metric.get('days')) + ' dias '
		if metric.get('hours') is not None:
			time += str(metric.get('hours')) + ' horas '
		if metric.get('minutes') is not None:
			time += str(metric.get('days')) + ' minutos '
		return {'metric': metric['metric'], 'time': time}
	formatted_metrics = list(map(format, metrics))
	return formatted_metrics

def filter_dude(dudes, email):
	def filter_function(dude):
		return dude.get('email') == email
	return list(filter(filter_function, dudes))


for support_ticket in support_open_tickets(creds):
	r = ticket_sla(support_ticket.id, creds)
	policy_metrics = r.json()['ticket']['slas']['policy_metrics']
	achieved_metrics = filter_near_achieve_metrics(policy_metrics)
	if achieved_metrics:
		dudes = filter_dude(read_config().get('configs').get('dudes'), support_ticket.assignee.email)
		if dudes:
			at_name = dudes[0].get('slack').get('at_name')
			dm_channel = dudes[0].get('slack').get('dm_id')
			message = "Ticket {0}( {1} ): {2}".format(
				"https://pagarme.zendesk.com/agent/tickets/" + str(support_ticket.id),
				" @" + at_name,
				":tada:"
			)
			slack_wrapper.message_channel(slack_token, dm_channel, message)