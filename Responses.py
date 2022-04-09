#!/usr/env/python3
#
# enhance-bot
#
# Telegram bot to upscale images
#
# Store chatterbox logic / messages here

import textwrap
from datetime import datetime

# Keep our command messages together
# Hackish attempt at multiple languages
cmd_msgs = {
	"start" : {
		"EN" : "Hello!"
		,"DE" : "Hallo!"
		}

	,"help" : {
		"EN":"""
			Try these commands
			<pre>
				/start
				\t\t Restart.

				/help
				\t\t This help.

				/upscale
				\t\t Upscale an image.

				/language DE
				\t\t Switch to Deutsch.
			</pre>
			"""
		,"DE" : """
			Diese Befehle ausprobieren.
			<pre>
				/starten
				\t\t Nue Starten.

				/hiflen
				\t\t Diese hilfen.

				/skalieren
				\t\t Bildteil vergrößern.

				/sprache EN
				\t\t Wechsle auf Deutsch.
			</pre>
			"""
		}

	,"upscale_start" : {
		"EN" : "Upscaling..."
		,"DE" : "Skalierening..."  # heh
		}

	,"upscale_error" : {
		"EN" : ":( Something went wrong!"
		,"DE" : ":( Etwas schief gelaufen!" 
		}
}

# fix above indentation
for cmd in cmd_msgs:
	for lang in cmd_msgs[cmd]:
		cmd_msgs[cmd][lang] = textwrap.dedent(cmd_msgs[cmd][lang])


# Poor mans chat bot
def sample_responses(input_text):
	user_message  = str(input_text).lower()

	if user_message in ("hello", "hi"):
		return "Hallo!"


	if user_message in ("bye"):
		return "ZIEL"



