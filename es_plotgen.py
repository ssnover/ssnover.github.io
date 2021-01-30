#!/usr/bin/python3

import json 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from git import Repo
import shutil
import os

gc = gspread.service_account(filename='spanish-2021-plotting-b4933b87bb8c.json')
gsheet = gc.open_by_key("12KCONdOaUDQiKJN_qVyg5UThw-cOb47TEZh9tbDlnE8")
mydata = gsheet.sheet1.get_all_records()

weeks = np.arange(0, 52+1, step=1)
hours_completed= np.array([])
baseline_hours = np.array([])

for entry in mydata:
    entry_date_str = entry["Week Starts Date"]
    if len(entry_date_str) > 0:
        entry_date = datetime.strptime(entry_date_str, "%m/%d/%Y")
        if entry_date <= datetime.today():
            hours_completed = np.append(hours_completed, [entry["Completed Hours"]])
    baseline_hours = np.append(baseline_hours, [entry["Expected Hours"]])


plt.figure()
_, ax = plt.subplots()
baseline_plot = ax.plot(baseline_hours, color='r', lw=2)
ax.fill_between(weeks[:len(hours_completed)], baseline_hours[:len(hours_completed)], hours_completed, alpha=0.3, color='g')
progress_plot = plt.plot(hours_completed)
plt.setp(progress_plot, color='g', linewidth=2.0)
plt.grid(True)
ax.set(xlim=(0, len(weeks) - 1), ylim=(0, None), xticks=4*weeks[0:int(len(weeks)/4) + 1], yticks=np.array([0, 100, 200, 300]))
plt.gca().set_aspect(1/10)
plt.title("Hours of Spanish Comprehensible Input 2021")
plt.savefig("test.svg")

repo_path = os.getenv("GITHUB_IO_REPO_PATH")
if repo_path is None:
    repo_path = "/home/ssnover/dev/mygithubpage"
repo = Repo(repo_path)
svg_path = repo_path + os.sep + 'graphs' + os.sep + "comprehensible-input-graph.svg"
if not repo.bare:
    shutil.copyfile("./test.svg", svg_path)
    if repo.is_dirty():
        repo.index.add([svg_path])
        repo.index.commit("Auto-commit: Update graph")
        repo.remote().push()
