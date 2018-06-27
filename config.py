'''This is the channel where the bot tells it has gone online, and it uses the channel to remember what its main server is.'''
welcome_channel = 457270968440848385

'''The amount of time before the activity is lowered. The default is 3600.0, at which rate players' activity lowers 10% per day
and about 50% per week. Lowering this number will speed that up.

The higher the value, the more are spammy moments filtered out.
The lower the value, the longer it takes for beta players do be considered inactive.
(You don't want to encourage spam to gain beta, but you don't wanna kick beta too soon either)'''
down_time = 3600.0

'''This is the current database file. When changing this name,
make sure to format with reset.py if you are unsure if the file has been formatted yet.'''
database = 'database.db'

'''The prefix that the bot should accept for its commands'''
prefix = '!'

'''The token to log in with your bot. This is like a password, do not share this with anyone!'''
TOKEN = 'your_token_here_please'
