from config import prefix

# Checks if an input requests a given command
def is_command(message,commandlist,help=False):
    """Check if the message starts with the given command or its aliases.

    Keyword arguments:
    message -> the Discord message
    commandlist -> list of possible commands that return True if the prefix is put in front of them
    help -> when set to True, return True when the message starts with the prefix, then help, and then the command.
    """
    for command in commandlist:
        if message.content.startswith(prefix + command) and help == False:
            return True
        if message.content.startswith(prefix + 'help ' + command) and help == True:
            return True
    return False

# Makes sure the message has at least the needed amount of users.
# If the message contains emojis, they should be converted to ids as well. Mentions have priority, however.
# The command should return the given amount of user ids, or, if equal to -1, should return them all.
def users(message,amount = -1, delete_duplicates = True):
    """Return the requested amount of user ids in a list. If the amount is -1, all users are given.

    Keyword arguments:
    message -> the Discord message to inspect
    amount -> the wanted amount of users in a list
    delete_duplicates -> filter out users that are mentioned twice in the message
    """
    user_table = [person.id for person in message.mentions]

    if delete_duplicates == True:
        user_table = list(set(user_table))

    if max(amount,1) > len(user_table):
        return False

    if amount == -1:
        return user_table

    return [user_table[i] for i in range(amount)]
