import sys

import asks
import trio

targets = sys.argv[1:]

script_name = "beemovie.txt"
final_comment = "Bee Movie (2007) - 6.2/10\nhttp://www.imdb.com/title/tt0389790/\n\n\
Barry B. Benson, a bee just graduated from college, is disillusioned at his lone career choice: \
making honey. On a special trip outside the hive, Barry's life is saved by Vanessa, a florist in New York City. \
As their relationship blossoms, he discovers humans actually eat honey, and subsequently decides to sue them"

delay = 20

session_id = ""
login_secure = ""
steam_id = login_secure[:login_secure.index("%")]

pages = [""]
with open(script_name, "r") as f:
    for line in f.readlines():
        if "<--! Split --!>" in line:
            pages.append("")
        elif len(pages[-1]) + len(line) > 999:
            pages.append(line)
        else:
            pages[-1] += line

pages.reverse()
pages.append(final_comment) if final_comment else None


async def comment_task(target):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}
    cookies = {"steamLoginSecure": login_secure, "sessionid": session_id}

    for i, p in enumerate(pages):
        data = {"comment": p, "count": "6", "sessionid": session_id}
        resp = (await asks.post(f"https://steamcommunity.com/comment/Profile/post/{target}/-1/",
                                headers=headers, cookies=cookies, data=data)).json()

        if resp.get("success", False) is not True:
            if resp.get("success", False) == "The settings on this account do not allow you to add comments.":
                print(f"Account {target} either doesn't allow posting or your entered information is incorrect")
                print("Make sure all your entered info is correct and the delay is sufficient")
                return
            else:
                print(f"An error occured while commenting on {target}'s profile with error code: "
                      f"{resp.get('error', f'Unknown error')}")
                print("Make sure all your entered info is correct and the delay is sufficient")
                return

        else:
            print(f"{i + 1}/{len(pages)} on {target}'s profile")

        await trio.sleep(delay)


async def main():
    print(f"Estimated time: {((len(pages) * delay) / 60):.1f} minutes")
    async with trio.open_nursery() as n:
        for t in targets:
            n.start_soon(comment_task, t)

    print("Finished")


trio.run(main)
