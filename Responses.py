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
# TODO: this is probably nicer stored externally as yaml
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

				/settings
				\t\t Configure default settings.

				/upscale
				\t\t Upscale an image.

			</pre>
			"""
		,"DE" : """
			Diese Befehle ausprobieren.
			<pre>
				/starten
				\t\t Nue Starten.

				/hiflen
				\t\t Diese hilfen.

				/einstellungen
				\t\t Konfigurieren von Standardeinstellungen.

				/skalieren
				\t\t Bildteil vergrößern.

			</pre>
			"""
		}
	,"settings" : {
		
		"EN" : """
			Settings:
			<pre>
				/language [EN|DE]
				\t\t Change language.
			</pre>
			"""

		
		,"DE" : """
			Einstellungen:
			<pre>
				/sprache [EN|DE]
				\t\t Wechsle auf Deutsch.
			</pre>
			"""
		}

	,"upscale_start" : {
		"EN" : "Upscaling..."
		,"DE" : "Skalierening..."  # heh
		}

	,"upscale_error" : {
		"EN" : "🙁 Something went wrong!"
		,"DE" : "🙁 Etwas schief gelaufen!" 
		}
	,
	"language_select" : {
		"EN" : "Select Language:"
		,"DE" : "Select Language:"  # TODO
		}
	,
	"language_set" : {
		"EN" : "Language set to EN!"
		,"DE" : "Language set to DE!"  # TODO
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



