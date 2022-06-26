# Steam-Comment-Bot
***

A Python 3.6+ script to post the contents of a text file onto one or multiple Steam profiles

Running the source will require Python to be installed and for you to install the dependencies listed in requirements.txt.

## Usage
Edit the `config.toml` file to configure the bot. Descriptions of what each configurable are in the file.  
Note however:

> A delay of at least 15 seconds is recommended though smaller delays may work for shorter text files.
> 
> You are limited to 5 comments on a profile that has not added you as a friend.
> 
> The `session id` and `login secure` can be obtained from your browser cookies from a logged in Steam account. Google how to do that.
>
> `final_comment` will be the last thing posted (and so will appear first in the comment list). This *must* be under 1000 characters.

This script preserves newlines from the text file. Extra newlines can be added with the `\n` token.  
The program will automatically split the script into chunks so no comment exceeds the 1000 character Steam comment limit.  
You can manually cause a split by inserting `<--! Split !-->` as a seperate line.

The script to the Bee Movie has been included and is used by default.
***

<em>
As with any bot, please be nice to your friends and to the Steam servers.
I am not responsible for any bans, temporary or otherwise you may receive.
</em>
