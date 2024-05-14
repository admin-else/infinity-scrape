#!/usr/bin/env python3
import sqlite3
import random
import os

if not os.path.exists("infinite-craft.db"):
    print(
        """There is no infinite-craft.db file!
Make SURE you are in the right directory. To change your directory, use the following command :
cd path/to/infinite-craft.db
(Right click on infinite-craft.db to copy file path)"""
    )
    exit(1)

conn = sqlite3.connect("infinite-craft.db")
cursor = conn.cursor()

base = set(["Water", "Fire", "Wind", "Earth"])
# title will make stuff that uses wrong case right like anime -> Anime
targets = set([input("Enter your desired element: ").title()])
steps = {}

while not targets.issubset(base):
    # Fixed this and removed the random() function
    #    so the code is more efficient
    target = list(targets)[0]
    while target in base:
        targets.remove(target)
        target = list(targets)[0]
    cursor.execute("SELECT ingr1, ingr2 FROM combination WHERE out LIKE ?", [target])
    ingr = cursor.fetchone()
    if ingr is None:
        print(f"Cannot find recipie for {target}...")
        exit(1)

    steps[target] = (ingr[0], ingr[1])
    targets.add(ingr[0])
    targets.add(ingr[1])
    targets.remove(target)

cursor.close()
conn.close()

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
