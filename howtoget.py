#!/usr/bin/env python3
import sqlite3
import random
import os

if not os.path.exists("infinite-craft.db"):
    print("""There is no infinite-craft.db file its reqired to search for recipies!
make SURE you are in the right directory (to change your directory use cd).""")
    exit(1)

conn = sqlite3.connect('infinite-craft.db')
c = conn.cursor()

base = set(["Water", "Fire", "Wind", "Earth"])
targets = set([input("what do you want: ").title()]) # title will make stuff that uses wrong case right like anime -> Anime
steps = {}

while True:
    if targets.issubset(base):
        break
    target = random.choice(list(targets)) # ummm this is kinda stupid but it works ig...
    if target in base:
        continue
    c.execute("SELECT ingr1, ingr2 FROM combination WHERE out LIKE ?", [target])
    ingr = c.fetchone()
    if ingr == None:
        print(f"didn't find source of {target}...")
        exit(1)

    steps[target] = (ingr[0], ingr[1])
    targets.add(ingr[0])
    targets.add(ingr[1])
    targets.remove(target)

c.close()

sorted_steps = []
made = base
while len(sorted_steps) != len(steps):
    target = random.choice(list(steps.keys()))
    ingr1, ingr2 = steps[target]
    text = f"{ingr1} + {ingr2} -> {target}"
    if ingr1 in made and ingr2 in made and text not in sorted_steps:
        made.add(target)
        sorted_steps.append(text)

text = ""
for i, line in enumerate(sorted_steps):
    text += f"{i+1}. {line}\n"

print(text)
