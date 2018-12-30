import sys
import threading
import time

import requests

steam_ids = sys.argv[1:]

script_name = "short.txt"
delay = 3

session_id = ""
login_secure = ""
steam_id = login_secure[:login_secure.index("%")]

last_comment = ""


script = []
with open(script_name, "r") as f:
    oscript = [l for l in f]

temp = ""
for l in oscript:
    if len(temp) + len(l) > 999:
        script.append(temp)
        temp = l
    else:
        temp = temp + l
        if oscript.index(l) == len(oscript) - 1:
            script.append(temp)

script.reverse()
script.append(last_comment) if last_comment else None


class Thread(threading.Thread):
    def __init__(self, account_id):
        threading.Thread.__init__(self)
        self.stop = False
        self.done = False
        self.id = account_id
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"}
        self.cookies = {"steamLoginSecure": login_secure,
                        "sessionid": session_id}

    def run(self):
        for self.i, s in enumerate(script):
            if self.stop: return
            r = requests.post(f"https://steamcommunity.com/comment/Profile/post/{self.id}/-1/",
                              headers=self.headers,
                              cookies=self.cookies,
                              data={"comment": s, "count": "6", "sessionid": session_id})

            if r.json().get("success", True) is False:
                if r.json()["error"] == "The settings on this account do not allow you to add comments.":
                    print(f"Something went wrong with {self.id}'s profile :-(")
                    print(f"Account {self.id} either doesn't allow posting or your entered information is incorrect")
                    print(f"Skipping {self.id}")
                    print(r.json())
                    self.stop = False
                    return
                print(f"Something went wrong with {self.id}'s profile :-(")
                print("Make sure all your entered info is correct and the delay long enough")
                print(f"Retrying comment {self.i + 1}")
                print(r.json())
                self.i -= 1
            else:
                print(f"{self.i + 1}/{len(script)} on {self.id}'s profile")

            time.sleep(delay)
        print()
        self.stop = True


print(f"Estimated time: {((len(script) * delay) / 60):.1f} minutes")

thread_list = []
for i, sid in enumerate(steam_ids):
    thread_list.append(Thread(sid))
    thread_list[i].start()

try:
    while not all(t.stop for t in thread_list):
        time.sleep(1)
except KeyboardInterrupt:
    print(f"Quitting")
    for t in thread_list:
        t.stop = True
        quit()
