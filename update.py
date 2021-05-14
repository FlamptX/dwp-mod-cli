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
LOCAL_DIR = "./"

def github_sync():
    with open("./data/auth.txt") as file:
        token = file.readline()
    with open("./data/auth.txt", "w") as file:
        file.write("")
    with open("./data/config.txt") as file:
        config = file.readline()
    with open("./data/config.txt", "w") as file:
        file.write("")

    remote_sha = fetch_remove_sha()
    local_sha = fetch_local_sha(False)
    if remote_sha != local_sha:
        with open("./data/auth.txt", "w") as file:
            file.write(token)
        with open("./data/config.txt", "w") as file:
            file.write(config)
        print(f"{WARNING}New version found. Consider updating via mod update. (this message can also be caused when changing contents of files and you can disable it via mod autocheck off){ENDC}")

def update():
    with open("./data/auth.txt") as file:
        token = file.readline()
    with open("./data/config.txt") as file:
        config = file.readline()

    remote_sha = fetch_remove_sha()
    local_sha = fetch_local_sha(True)
    if remote_sha != local_sha:
        check_output("git pull origin " + BRANCH)
        print(f"{OKGREEN}The local repo has been updated){ENDC}")
        with open("./data/auth.txt", "w") as file:
            file.write(token)
        with open("./data/config.txt", "w") as file:
            file.write(config)
    else:
        print("The local repo is already up-to-date.")

def fetch_remove_sha():
    req_url = "https://api.github.com/repos/" + \
            USERNAME + "/" + REPO + "/branches/" + BRANCH
    resp = urlopen(req_url)
    resp_str = str(resp.read(), encoding="utf-8")
    resp_data = json.loads(resp_str);
    remote_sha = resp_data["commit"]["sha"]
    return remote_sha

def fetch_local_sha(way):
    if way:
        command = "git checkout " + BRANCH
        check_output(command)
    command = "git rev-parse HEAD"
    local_sha = str(check_output(command), encoding="utf-8")
    return local_sha[:-1]  # remove newline


if __name__ == "__main__":
    if args.state is None:
        github_sync()
    else:
        if args.state == "update":
            update()
        elif args.state not in ["on", "off"]:
            print(f"{FAIL}Invalid state argument given. It must be either on or off.){ENDC}")
        else:
            with open("./data/config.txt", "w") as file:
                file.write(args.state)
                with open("./data/config.txt") as file:
                    state = file.readline()
                if state == "on":
                    github_sync()