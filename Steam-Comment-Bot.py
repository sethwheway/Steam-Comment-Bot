from time import sleep

import toml
from colorama import Style, Fore
from requests import post
from tqdm import tqdm, trange

config = toml.load("config.toml")

if not (targets := config["targets"]):
    print(Fore.RED + "No Steam IDs specified. Quitting")
    quit()

if "REPLACE ME" in (config["session_id"], config["login_secure"]):
    print(Fore.RED + "The config file has not been completed. Quitting")
    quit()

script_name = config["script_name"]
final_comment = config["final_comment"]

delay = config["delay"]

session_id = config["session_id"]
login_secure = config["login_secure"]

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
        # Don't ask me why the session ID is required twice
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
        print(Fore.RED, end="")  # Makes the bar red
        page_bar.close()
        print(Style.BRIGHT + "\nAll targets errored before all comments were posted!")
        quit()

    page_bar.update()

    if page_bar.n != len(pages):
        bar_format = f"Comment {page_bar.n}/{len(pages)} successful. Delaying " + r"[{n_fmt}/{total_fmt}s]"
        for _ in trange(delay, bar_format=bar_format, leave=False):
            sleep(1)

print("\nDone" + (" with one or more errors along the way!" if error else "!"))
