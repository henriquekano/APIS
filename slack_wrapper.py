from slackclient import SlackClient

def message_channel(token, channel, message):
	sc = SlackClient(token)
	sc.api_call(
	  "chat.postMessage",
	  channel=str(channel),
	  text=str(message)
	)