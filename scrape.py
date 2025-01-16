#!/usr/bin/env python3
# import asyncio
import os
import random
import sqlite3
import time

# import aiosqlite
import backoff
import json
import requests

import settings as s

if not os.path.exists("infinite-craft.db"):
    print(
        """There is no infinite-craft.db file!
Make SURE you are in the right directory. To change your directory, use the following command :
cd path/to/infinite-craft.db
(Right click on infinite-craft.db to copy file path)"""
    )
    if (
        not input(
            "Are you sure you want to start a new database? "
            "You can use the one on the github page. [Y/n]"
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


def are_chars_in_string(chars, string):
    return any(1 for c in chars if c in string)


@backoff.on_exception(backoff.expo, [requests.exceptions.RequestException, json.decoder.JSONDecodeError], max_time=60)
def combine(combination):
    try:
        response = requests.get(
            "https://neal.fun/api/infinite-craft/pair",
            params={"first": combination[0], "second": combination[1]},
            headers=s.HEADERS,
        )
        if not response.ok:
            print(f"Bad status code {response.status_code}")
        response = response.json()
    except Exception as e:
        print("got exeption:", e)
        return
    return response


def main():
    newAdditions, firstEvers, crafts = 0, 0, 0
    print("Connected!")
    api_gives_info = True

    # Fetch current combinations from the database
    c.execute("SELECT out FROM combination")
    current = [row[0] for row in c.fetchall()]
    if not current:
        current = ["Water", "Fire", "Wind", "Earth"]
    try:
        print("Starting, press CTRL+C or close this window to stop")
        print("Done...")
        start_time = time.time()
        while api_gives_info:
            combination = [random.choice(current), random.choice(current)]
            if s.SIMPLE_COMBINES:
                if are_chars_in_string(s.NON_SIMPLE_CHARS, combination[0]) or are_chars_in_string(
                    s.NON_SIMPLE_CHARS, combination[1]
                ):
                    continue

            text = f"{combination[0]} + {combination[1]} -> "

            if s.CHECK_IF_ALREADY_DONE:
                c.execute(
                    "SELECT * FROM combination "
                    "WHERE (ingr1=? AND ingr2=?) OR (ingr1=? AND ingr2=?)",
                    (combination[0], combination[1], combination[1], combination[0]),
                )
                existing_combination = c.fetchone()
                if existing_combination:
                    print(text + "skip... (already done)")
                    continue

            result = combine(combination)
            if not result:
                continue

            text += result["result"]
            crafts += 1
            if result["result"] not in current:
                c.execute(
                    "INSERT INTO combination (ingr1, ingr2, out) VALUES (?, ?, ?)",
                    (combination[0], combination[1], result["result"]),
                )
                conn.commit()
                newAdditions += 1
                current.append(result["result"])
                if c.rowcount > 0:
                    text += " (NEW)"
                if result["isNew"]:
                    firstEvers += 1
                    text += " (FIRST EVER)"
            print(text)

    except KeyboardInterrupt:
        print("Exiting")
    except Exception as e:
        print(f"{type(e)}: {e}")
    finally:
        conn.close()

    print(f"Found {newAdditions} new combinations and {firstEvers} first ever combinations in {time.time()-start_time:.1f}s!")


if __name__ == "__main__":
    main()
