from urllib.request import urlopen
from http.client import HTTPResponse
from subprocess import call, check_output
import json
import os
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("state", nargs='?', default=None)
args = parser.parse_args()

# Configurations
USERNAME = "FlamptX"
REPO = "dwp-mod-cli"
BRANCH = "main"
LOCAL_DIR = "git-repo"

OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'

def github_sync(directory):
    with open("./data/auth.txt") as file:
        token = file.readline()
    with open("./data/auth.txt", "w") as file:
        file.write("")

    os.chdir(directory)
    remote_sha = fetch_remove_sha()
    local_sha = fetch_local_sha()
    if remote_sha != local_sha:
        with open("./data/auth.txt", "w") as file:
            file.write(token)
        print(f"{WARNING}New version found. Consider updating via mod update. (this message can also be caused when changing contents of files and you can disable it via mod autocheck off)")

def update():
    with open("./data/auth.txt") as file:
        token = file.readline()

    os.chdir(directory)
    remote_sha = fetch_remove_sha()
    local_sha = fetch_local_sha()
    if remote_sha != local_sha:
        check_output("git pull origin " + BRANCH)
        print(f"{OKGREEN}The local repo has been updated")
        with open("./data/auth.txt", "w") as file:
            file.write(token)
    else:
        print(f"{OKGREEN}The local repo is already up-to-date")

def fetch_remove_sha():
    req_url = "https://api.github.com/repos/" + \
            USERNAME + "/" + REPO + "/branches/" + BRANCH
    resp = urlopen(req_url)
    resp_str = str(resp.read(), encoding="utf-8")
    resp_data = json.loads(resp_str);
    remote_sha = resp_data["commit"]["sha"]
    return remote_sha

def fetch_local_sha():
    command = "git checkout " + BRANCH
    check_output(command)
    command = "git rev-parse HEAD"
    local_sha = str(check_output(command), encoding="utf-8")
    return local_sha[:-1]  # remove newline


if __name__ == "__main__":
    if args.state is None:
        with open("./data/config.txt") as file:
            state = file.readline()
        if state == "on":
            github_sync(LOCAL_DIR)
    else:
        if args.state == "update":
            update()
        elif args.state not in ["on", "off"]:
            print("Invalid state argument given. It must be either on or off.")
        else:
            with open("./data/config.txt", "w") as file:
                file.write(args.state)
