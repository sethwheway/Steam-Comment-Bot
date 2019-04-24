# SteamCommentSpamBot

A quick Python 3.6+ script to post the contents of a text file onto one or multiple Steam profile comments.


## Usage
Change the variables `script_name`, `delay`, `session_id`, `login_secure` and `last_comment` 
at the top of the file as you wish.
A delay of at least 15 seconds is recommended though smaller delays may work for shorter text files.
The session id and login secure can be obtained from your browser cookies from a logged in Steam account.
The `last_comment` variable will be the last thing posted to the comment page. This must be under 1000 characters.

This script preserves new lines from the script file though `\n` newlines can be added.
This script will automatically split lines to adhere to the Steam comment character limit.

To run the script, simply invoke it through a terminal with a list of Steam64 IDs separated with spaces.
E.g. `SteamCommentSpamBot.py 76561199795927971 76561199100511319`

I've included the script to the Bee Movie along with the bot. This is the default.


As with any spammer, please be nice to your friends and to the Steam servers.
I am not responsible for any bans you may receive, though if used properly, this is unlikely.

<3
