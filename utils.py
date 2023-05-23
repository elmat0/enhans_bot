import sqlite3


def corpus_purge():
    conn = sqlite3.connect('corpus.db')
    conn.execute('DROP TABLE links')
    conn.commit()
    conn.close()

def corpus_show():
    conn = sqlite3.connect('corpus.db')
    cursor = conn.execute('SELECT summary_long FROM links')   
    for row in cursor:
        print(row)
    conn.close()



def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator



