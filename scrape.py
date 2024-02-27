#!/usr/bin/env python3
import requests
import json
import itertools
import time
import sqlite3
import random
import os
from settings import *

if not os.path.exists("infinite-craft.db"):
    print("""There is no infinite-craft.db file!
Make SURE you are in the right directory. To change your directory, use the following command :
cd path/to/infinite-craft.db
(Right click on infinite-craft.db to copy file path)""")
    if not input("Are you sure you want to start a new database? You can use the one on the github page. [Y/n]").lower().startswith("y"):
        exit(1)

conn = sqlite3.connect('infinite-craft.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS combination
             (id INTEGER PRIMARY KEY, ingr1 TEXT, ingr2 TEXT, out TEXT UNIQUE)''')

def combine(elem):
    time.sleep(API_DELAY)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://neal.fun/infinite-craft/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
    }

    params = {
        'first': elem[0],
        'second': elem[1],
    }

    response = requests.get('https://neal.fun/api/infinite-craft/pair', params=params, headers=headers)

    if response.status_code == 200:
        output = json.loads(response.text)
        return output
    else if not response.ok:
        print(f"API DIED WITH CODE {response.status_code}!!!! EXITING IMMEDIATELY!!!!")
        return None
    else:
        if not input(f"Warning! Response is code {response.status_code}, which is OK but unexpected. Continue anyways? (May break) [Y/N]").lower().startswith("y"):
            exit(1)
        output = json.loads(response.text)
        return output
        

def main():
    print("Starting, press CTRL+C or close this window to stop")

    api_gives_info = True

    # Fetch current combinations from the database
    c.execute("SELECT out FROM combination")
    current = [row[0] for row in c.fetchall()]
    if not current:
        current = ["Water", "Fire", "Wind", "Earth"]
    try:
        while api_gives_info:
            combinations = list(itertools.combinations_with_replacement(current, 2))
            random.shuffle(combinations)
            for combination in combinations:
                c.execute("SELECT * FROM combination WHERE (ingr1=? AND ingr2=?) OR (ingr1=? AND ingr2=?)", (combination[0], combination[1], combination[1], combination[0]))
                existing_combination = c.fetchone()
                if existing_combination:
                    print(f"{combination[0]} + {combination[1]} -> skip...")
                    continue

                result = combine(combination)
                
                if result is None:
                    api_gives_info = False
                    break
                
                
                if result["result"] not in current:
                    c.execute("INSERT INTO combination (ingr1, ingr2, out) VALUES (?, ?, ?)", (combination[0], combination[1], result['result']))
                    conn.commit()
                    current.append(result["result"])
                    
                print(f"{combination[0]} + {combination[1]} -> {result['result']}{' (NEW)' if c.rowcount > 0 else ''}{' (FIRST EVER)' if result['isNew'] else ''}")
                
    except KeyboardInterrupt:
        print("Exiting")
    except Exception as e:
        print(f"{type(e)}: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
