#!/usr/bin/env python3
import requests
import itertools
import backoff
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

@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_time=60)
def save_request(combination):
    response = requests.post('https://neal.fun/api/infinite-craft/pair', params={"first": combination[0], "second": combination[1]}, headers=HEADERS)
    return response.json()

def main():
    newAdditions, firstEvers = 0, 0
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
            print("Generating Combinations...")
            combinations = list(itertools.combinations_with_replacement(current, 2))
            print("Shuffeling Combinations...")
            random.shuffle(combinations)
            print("Done...")
            for combination in combinations:
                if SIMPLE_COMBINES:
                    if NON_SIMPLE_CHARS in combination[0] or NON_SIMPLE_CHARS in combination[1]:
                        print(f"{combination[0]} + {combination[1]} -> skip... (not simple)")
                        continue
                
                if CHECK_IF_ALREADY_DONE:
                    c.execute(
                        "SELECT * FROM combination WHERE (ingr1=? AND ingr2=?) OR (ingr1=? AND ingr2=?)",
                        (combination[0], combination[1], combination[1], combination[0]),
                    )
                    existing_combination = c.fetchone()
                    if existing_combination:
                        print(f"{combination[0]} + {combination[1]} -> skip... (already done)")
                        continue
                
                result = save_request(combination)
                

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
                if result["isNew"]:
                    firstEvers += 1
                    print(" (FIRST EVER)", end="", flush=False)
                print()  # newline clears the buffer/flushes to stdout all at once

    except KeyboardInterrupt:
        print("Exiting")
    except Exception as e:
        print(f"{type(e)}: {e}")
    finally:
        conn.close()
        
    print(f"Found {newAdditions} new combinations and {firstEvers} first ever combinations!")

if __name__ == "__main__":
    main()

