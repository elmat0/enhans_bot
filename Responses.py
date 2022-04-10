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
# HTML / Emojis should work
cmd_msgs = {
	"start" : {
		"EN" : "Send me an image to upscale."
		}
	,"help" : {
		"EN":"""
			Send me an image to upscale or try these commands:
			<pre>
				/start
				\t\t Restart.

				/help
				\t\t This help.
			</pre>
			"""
		}
	,"upscale_start" : {
		"EN" : "⏳ Upscaling..."
		}
	,"upscale_end" : {
		"EN" : "⌛ Done!"
		}
	,"upscale_error" : {
		"EN" : "💥 Something went wrong..."
		}
}

# fix above indentation
for cmd in cmd_msgs:
	for lang in cmd_msgs[cmd]:
		cmd_msgs[cmd][lang] = textwrap.dedent(cmd_msgs[cmd][lang])


# Poor mans chat bot
def sample_responses(input_text):
	user_message  = str(input_text).lower()

	if user_message in ("hello", "hi", "hey", "gday"):
		return "Hallo!"
