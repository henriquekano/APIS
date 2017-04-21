from zenpy import Zenpy
import requests
import json
import slack_wrapper

creds = {
	'email' : '',
	'password' : '',
	'subdomain': ''
}
zendesk_support_group_id = ''
slack_token = ''

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

for support_ticket in support_open_tickets(creds):
	r = ticket_sla(support_ticket.id, creds)
	policy_metrics = r.json()['ticket']['slas']['policy_metrics']
	achieved_metrics = filter_achieved_metrics(policy_metrics)
	if achieved_metrics:
		message = "Ticket {0}({1}): {2}".format(
			support_ticket.id,
			support_ticket.assignee.name,
			str(
				json.dumps(
					format_metrics_message(achieved_metrics)
				)
			)
		)
		slack_wrapper.message_channel(slack_token, "#realsuporte", message)