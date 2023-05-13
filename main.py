import requests
import os
import json
import numpy as np
import matplotlib.pyplot as plt

FILE_PATH = "problems_file"

def fetch_data(path):
    print("Contacting the CodeForces API...")
    r = requests.get("https://codeforces.com/api/problemset.problems")
    with open(path, "w") as f:
        f.write(r.text)
    clean_data(path)

def clean_data(path):
    with open(path, "r") as f:
        raw_string = f.read()
    raw_json = json.loads(raw_string)["result"]
    problems = raw_json["problems"]
    statistics = raw_json["problemStatistics"]
    problem_list = []
    for i in range(0, len(problems)):
            problem_list.append(problems[i])
            problem_list[i]["solvedCount"] = statistics[i]["solvedCount"]
    dumped = json.dumps(problem_list, indent = 4)
    with open(path, "w") as f:
        f.write(dumped)

def read_data(path):
    with open(path, "r") as f:
        return json.loads(f.read())

def get_input():
    inp = input("> ")
    rating = int(inp.split(' ')[0])
    min_contest_id = int(inp.split(' ')[1])
    return rating, min_contest_id

def problem_filter(problem):
    return (problem["contestId"] > min_contest_id and
            problem["rating"] == rating if "rating" in problem else False)

if not os.path.isfile(FILE_PATH):
    fetch_data(FILE_PATH)
    
print("Input format:\nRating MinimumContestID")
problems = read_data(FILE_PATH)
while True:
    tag_distribution = {}
    rating, min_contest_id = get_input()
    filtered_problems = list(filter(problem_filter, problems))
    
    print("Found", len(filtered_problems), "problems with these filters!")
    for problem in filtered_problems:
        for tag in problem["tags"]:
            if tag not in tag_distribution:
                tag_distribution[tag] = 0
            tag_distribution[tag] += 1

    tags = []
    tag_counts = list(tag_distribution.values())

    tag_counts.sort()
    for value in tag_counts:
        for tag in list(tag_distribution.keys()):
            if tag_distribution[tag] == value and tag not in tags:
                tags.append(tag)
    #deleting *special tag and its correspoding value
    for i in range(0, len(tags)):
        if tags[i] == "*special":
            del tags[i]
            del tag_counts[i]
            break
    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = np.arange(len(tags))
    ax.barh(y_pos, tag_counts, align='center')
    ax.set_yticks(y_pos, labels=tags)
    ax.invert_yaxis()
    plt.title("Tag distribution for rating {}\nShowing data for contests with contestId more than {}".format(rating, min_contest_id))
    plt.show()
