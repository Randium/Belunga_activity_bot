# Belunga_activity_bot
This bot is one that monitors players' activity and gives them a score based on it. It is meant as a suggestion for belungawhale's werewolf server, though it may have other applications later on as well.

## Python packages
There are a few packages that the program may not have. As the bot is using the rewrite version of discord.py, if any packages aren't downloaded correctly, set up

    pip install threading  
    pip install discord.py  
    pip install https://github.com/Rapptz/discord.py/archive/rewrite.zip  
 
## Setting up the bot
Once you have all packages installed, fill in all the data in config.py, and run

    python reset.py
  
to format the database. The database isn't formatted on GitHub yet _(GitHub doesn't like binary files)_, so make sure to run this before starting the bot. Running in the terminal

    python main.py
    
should then successfully launch the bot.

## The database file
The database is in an SQLite format. If you are unfamiliar with this, SQLite is a database that is relatively small and can store lots of data quite efficiently. As long as the Discord server has under 100'000 members, you should be good to go.
If you want to browse through the database manually, consider using phpliteadmin or install a DB Browser for SQLite.
