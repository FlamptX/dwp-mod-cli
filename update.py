from urllib.request import urlopen
from http.client import HTTPResponse
from subprocess import check_output
import json
import os
import sys

# Configurations
USERNAME = "FFlamptX"
REPO = ""
BRANCH = "master"
LOCAL_DIR = ""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def github_sync(directory):
    os.chdir(directory)
    remote_sha = fetch_remove_sha()
    local_sha = fetch_local_sha()
    if remote_sha != local_sha:
        check_output(["git", "pull", "origin", BRANCH])
        print("The local repo has been updated")
        return 1;
    else:
        print("The local repo is already up-to-date")
        return 0;


def fetch_remove_sha():
    req_url = "https://api.github.com/repos/" + \
            USERNAME + "/" + REPO + "/branches/" + BRANCH
    resp = urlopen(req_url)
    resp_str = str(resp.read(), encoding="utf-8")
    resp_data = json.loads(resp_str);
    remote_sha = resp_data["commit"]["sha"]
    return remote_sha


def fetch_local_sha():
    check_output(["git", "checkout", BRANCH])
    local_sha = str(check_output(["git", "rev-parse", "HEAD"]), encoding="utf-8")
    return local_sha[:-1]  # remove newline

if __name__ == "__main__":
    sys.exit(github_sync(LOCAL_DIR))