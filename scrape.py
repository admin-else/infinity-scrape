#!/usr/bin/env python3
import sys
import requests
import itertools
import time
import sqlite3
import random
import os
from settings import *

if not os.path.exists("infinite-craft.db"):
    print(
        """There is no infinite-craft.db file!
Make SURE you are in the right directory. To change your directory, use the following command :
cd path/to/infinite-craft.db
(Right click on infinite-craft.db to copy file path)"""
    )
    if (
        not input(
            "Are you sure you want to start a new database? You can use the one on the github page. [Y/n]"
        )
        .lower()
        .startswith("y")
    ):
        exit(1)
print("Connecting to database...")
conn = sqlite3.connect("infinite-craft.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS combination
             (id INTEGER PRIMARY KEY, ingr1 TEXT, ingr2 TEXT, out TEXT UNIQUE)"""
)

newAdditions = 0
firstEvers = 0


def combine(elem, depth=10):
    if depth < 0:
        print("Too many retries, exiting...")
        return None
    time.sleep(API_DELAY)
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://neal.fun/infinite-craft/",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-GPC": "1",
        }

        params = {
            "first": elem[0],
            "second": elem[1],
        }

        response = requests.get(
            "https://neal.fun/api/infinite-craft/pair", params=params, headers=headers
        )

        if response.ok:
            return response.json()
        else:
            raise Exception("Response not OK")
    except KeyboardInterrupt:
        print("Recieved ctrl-c, quitting")
        return
    except:
        # wait an increasing amount of time to get out of rate limit and retry
        # first time retry imieadetly, because it might just be a network error
        # then keep increasing the retry timer
        timeout = 120 * (10 - depth)
        print(f"Response not OK, waiting {timeout}s and retrying.")
        time.sleep(timeout)
        return combine(elem, depth - 1)


def main():
    global newAdditions, firstEvers
    print("Connected!")
    api_gives_info = True

    # Fetch current combinations from the database
    c.execute("SELECT out FROM combination")
    current = [row[0] for row in c.fetchall()]
    if not current:
        current = ["Water", "Fire", "Wind", "Earth"]
    try:
        print("Starting, press CTRL+C or close this window to stop")
        while api_gives_info:
            combinations = list(itertools.combinations_with_replacement(current, 2))
            random.shuffle(combinations)
            for combination in combinations:
                c.execute(
                    "SELECT * FROM combination WHERE (ingr1=? AND ingr2=?) OR (ingr1=? AND ingr2=?)",
                    (combination[0], combination[1], combination[1], combination[0]),
                )
                existing_combination = c.fetchone()
                if existing_combination:
                    print(f"{combination[0]} + {combination[1]} -> skip...")
                    continue

                result = combine(combination)

                if result is None:
                    api_gives_info = False
                    break

                if result["result"] not in current:
                    c.execute(
                        "INSERT INTO combination (ingr1, ingr2, out) VALUES (?, ?, ?)",
                        (combination[0], combination[1], result["result"]),
                    )
                    conn.commit()
                    current.append(result["result"])
                    newAdditions += 1
                print(
                    f"{combination[0]} + {combination[1]} -> {result['result']}{' (NEW)' if c.rowcount > 0 else ''}",
                    end="",
                    flush=False,
                )
                # {' (FIRST EVER)' if fEverFlag else ''}
                if result["isNew"]:
                    firstEvers += 1
                    print(" (FIRST EVER)", end="", flush=False)
                    # fEverFlag = True
                print()

    except KeyboardInterrupt:
        print("Exiting")
    except Exception as e:
        print(f"{type(e)}: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

print(
    f"Found {newAdditions} new combinations and {firstEvers} first ever combinations!"
)
