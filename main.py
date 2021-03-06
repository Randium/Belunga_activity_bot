from config import prefix, TOKEN, welcome_channel, down_time
from check import is_command, users, numbers
import threading
import discord
import asyncio
import sqlite3

client = discord.Client()
conn = sqlite3.connect('database.db')
c = conn.cursor()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    main_guild = client.get_channel(welcome_channel).guild
    messenger = message.author
    temp_msg = []

    # Check if the user already exists in the database. If not, create 'em.
    c.execute("SELECT * FROM 'users' WHERE id =?",(messenger.id,))
    if c.fetchone() == None:
        c.execute("INSERT INTO 'users'('id','name') VALUES (?,?);",(messenger.id,messenger.name))
        print("New user! User {} has been registered to the bot.".format(message.author.name))
        conn.commit()

    # Give the user a point to their score
    c.execute("UPDATE 'users' SET spam_activity= spam_activity +1 WHERE id=?;",(messenger.id,))
    c.execute("UPDATE 'users' SET name =? WHERE id =?",(messenger.name,messenger.id))
    conn.commit()

    # Ignore commands if they are not in the right channel
    if message.channel.id not in [251873803779571714, welcome_channel]:
        return

    # Activity check
    if is_command(message,['act','activity','myact']):
        if users(message) == False:
            c.execute("SELECT activity + spam_activity FROM 'users' WHERE id =?",(messenger.id,))
            msg = await message.channel.send("You have an activity score of **{} points!**".format(int(c.fetchone()[0])))
            temp_msg.append(msg) # temp
            if len(message.content.split(' ')) > 1:
                await asyncio.sleep(3)
                msg = await message.channel.send('**Tip:** Did you mean to see someone else\'s activity? You\'ll have to ping \'em, sorry.')
                temp_msg.append(msg)
        else:
            target = users(message)[0]
            c.execute("SELECT activity + spam_activity FROM 'users' WHERE id =?",(target,))
            score = c.fetchone()
            if score == None:
                msg = await message.channel.send("This user hasn't said anything yet! This means they've got a score of zero.")
                temp_msg.append(msg) # temp
            else:
                msg = await message.channel.send("**{}** has an activity score of **{} points!**".format(main_guild.get_member(int(target)).name,int(score[0])))
                temp_msg.append(msg) # temp
    if is_command(message,['act','activity','myact'],True):
        msg_send = "**Usage:** See one's activity score.\n\n`" + prefix + "activity <user>`\n\nThe user argument is optional.\n**Examples:** `!activity`, `!activity @Randium#6521`"
        msg = await message.channel.send(msg_send)
        temp_msg.append(msg) # temp

    # Leaderboard command
    if is_command(message,['lead','leaderboard']):
        c.execute("SELECT * FROM 'users'")
        leaderboard = [[user[2] + user[3],user[0]] for user in c.fetchall()]
        leaderboard.sort(reverse=True)
        msg = "**Most active users:**\n\n"
        player_found = False
        msg_table = []

        if numbers(message) == False or numbers(message)[0] > 50:
            maximum = 5
        else:
            maximum = numbers(message)[0]

        for i in range(min(maximum,len(leaderboard))):
            if int(message.author.id) == int(leaderboard[i][1]):
                player_found = True
            if main_guild.get_member(int(leaderboard[i][1])) == None:
                msg += "**{}. <@{}>** - {} points\n".format(i+1,leaderboard[i][1],int(leaderboard[i][0]))
            else:
                msg += "**{}. {}** - {} points\n".format(i+1,main_guild.get_member(int(leaderboard[i][1])).name,int(leaderboard[i][0]))
            if i % 20 == 19:
                msg_table.append(msg)
                msg = ""

        if player_found == False:
            msg += "\n\n**__Your position:__**\n"
            for i in range(len(leaderboard)):
                if int(message.author.id) == int(leaderboard[i][1]):

                    if main_guild.get_member(int(leaderboard[i-1][1])) == None:
                        msg += "**{}. <@{}>** - {} points\n".format(i,leaderboard[i-1][1],int(leaderboard[i-1][0]))
                    else:
                        msg += "**{}. {}** - {} points\n".format(i,main_guild.get_member(int(leaderboard[i-1][1])).name,int(leaderboard[i-1][0]))

                    if main_guild.get_member(int(leaderboard[i][1])) == None:
                        msg += "**{}. <@{}>** - {} points\n".format(i+1,leaderboard[i][1],int(leaderboard[i][0]))
                    else:
                        msg += "**{}. {}** - {} points\n".format(i+1,main_guild.get_member(int(leaderboard[i][1])).name,int(leaderboard[i][0]))

                    if i < len(leaderboard) - 1:
                        if main_guild.get_member(int(leaderboard[i+1][1])) == None:
                            msg += "**{}. <@{}>** - {} points\n".format(i+2,leaderboard[i+1][1],int(leaderboard[i+1][0]))
                        else:
                            msg += "**{}. {}** - {} points\n".format(i+2,main_guild.get_member(int(leaderboard[i+1][1])).name,int(leaderboard[i+1][0]))
        msg_table.append(msg)

        for msg in msg_table:
            if msg != '':
                msg = await message.channel.send(msg)
                temp_msg.append(msg)
    if is_command(message,['lead','leaderboard'],True):
        msg_send = "**Usage:** See a leaderboard of the most active users\n\n`" + prefix + "leaderboard`"
        await message.channel.send(msg_send)
        temp_msg.append(msg)

    await asyncio.sleep(120)
    for msg in temp_msg:
        await msg.delete()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.get_channel(welcome_channel).send('Beep boop! I just went online!')

# Thread that lowers activity
def punish_inactives():
  threading.Timer(down_time, punish_inactives).start()
  conn2 = sqlite3.connect('database.db')
  c2 = conn2.cursor()
  print('Purging!')
  c2.execute("SELECT * FROM 'users'")
  leaderboard = [[user[2],user[1]] for user in c2.fetchall() if user[2] > 0]
  leaderboard.sort(reverse = True)
  print(leaderboard[0:min(3,len(leaderboard)])
  c2.execute("UPDATE 'users' SET spam_activity = 0 WHERE spam_activity > 2*spam_filter;")
  c2.execute("UPDATE 'users' SET activity = activity + spam_activity*spam_activity/-spam_filter + 2*spam_activity;")
  c2.execute("UPDATE 'users' SET activity= activity*0.9958826236;")
  c2.execute("UPDATE 'users' SET spam_activity = 0")
  conn2.commit()

punish_inactives()
client.run(TOKEN)
