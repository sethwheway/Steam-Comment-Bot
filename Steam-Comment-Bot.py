import sys
from time import sleep

from colorama import Style, Fore
from requests import post
from tqdm import tqdm, trange

targets = sys.argv[1:]
if not targets:
    print(Fore.RED + "No Steam IDs specified. Quitting")
    quit()

script_name = "beemovie.txt"
final_comment = "Bee Movie (2007) - 6.2/10\nhttp://www.imdb.com/title/tt0389790/\n\n\
Barry B. Benson, a bee just graduated from college, is disillusioned at his lone career choice: \
making honey. On a special trip outside the hive, Barry's life is saved by Vanessa, a florist in New York City. \
As their relationship blossoms, he discovers humans actually eat honey, and subsequently decides to sue them"

delay = 12

session_id = "REPLACE_ME"
login_secure = "REPLACE_ME"

pages = [""]
with open(script_name, "r") as f:
    for line in f.readlines():
        if "<--! Split !-->" in line:
            pages.append("")
        elif len(pages[-1]) + len(line) > 999:
            pages.append(line)
        else:
            pages[-1] += line

pages.reverse()
if final_comment:
    pages.append(final_comment)

error = False
for page in (page_bar := tqdm(pages)):
    for target in targets:
        # Don't ask me why the session ID is required twice. Steam's entire web infra sucks
        data = {"comment": page, "sessionid": session_id, "feature2": -1}
        cookies = {"sessionid": session_id, "steamLoginSecure": login_secure}
        resp = post(f"https://steamcommunity.com/comment/Profile/post/{target}/-1", data=data, cookies=cookies)

        if not (json := resp.json()).get("success") is True:
            page_bar.write(Fore.RED + f"An error has occured with {target}! Skipping them from now on")
            page_bar.write(str(json) + Style.RESET_ALL)
            targets.remove(target)
            error = True
            continue

    if not targets:
        print(Fore.RED, end="")  # Hack to make the progress bar go red
        page_bar.close()
        print(Style.BRIGHT + "\nAll targets errored before all comments were posted!")
        quit()

    page_bar.update()

    if page_bar.n != len(pages):
        bar_format = f"Comment {page_bar.n}/{len(pages)} successful. Delaying " + r"[{n_fmt}/{total_fmt}s]"
        for _ in trange(delay, bar_format=bar_format, leave=False):
            sleep(1)

print("\nDone" + (" with one or more errors along the way!" if error else "!"))
