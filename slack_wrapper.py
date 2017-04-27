from slackclient import SlackClient

def message_channel(token, channel, message):
	sc = SlackClient(token)
	message = sc.api_call(
	  "chat.postMessage",
	  channel=str(channel),
	  text=str(message),
	  parse='full',
	  link_names=1
	)
	return message