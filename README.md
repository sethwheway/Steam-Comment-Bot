# SteamCommentSpamBot

A quick Python 3.6+ script to post the contents of a text file onto one or multiple Steam profiles.


## Usage
Change the variables `script_name`, `delay`, `session_id`, `login_secure` and `final_comment` 
at the top of the file as you need. `session_id` and `login_secure` are required.
A delay of at least 20 seconds is recommended though smaller delays may work for shorter text files.
The session id and login secure can be obtained from your browser cookies from a logged in Steam account. You can Google how to do that.
The `final_comment` variable will be the last thing posted to the comment page. This must be under 1000 characters.

This script preserves newlines from the text file. Extra newlines(`\n`) can be added.
The program will automatically split the script into chunks so no comment exceeds the 1000 character Steam comment limit.
You can manually cause a split by inserting `<--! Split !-->` as a seperate line

To run the script, invoke it through a terminal with a list of Steam64 IDs separated with spaces.
E.g. `SteamCommentSpamBot.py 76561199795927971 76561199100511319`

The script to the Bee Movie has been included with this repo and is used by default.


As with any bot, please be nice to your friends and to the Steam servers.
I am not responsible for any bans temporary or otherwise you may receive, though if used properly, this is unlikely.

Please note you are limited to 5 comments on a profile that has not added you as a friend.
