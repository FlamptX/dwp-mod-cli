import argparse
import os
import requests

parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("user", nargs='?', default="")
parser.add_argument("duration", nargs='?', default="")
parser.add_argument('reason', nargs='*', default="")
args = parser.parse_args()

if args.command not in ["warn", "kick", "ban", "tempban", "mute", "unmute"]:
    print("Unknown command.")
elif args.user == "":
    print("Missing the user ID argument.")
elif args.duration == "":
    print("Missing the duration argument.")
else:
    try:
        user_id = int(args.user)
    except ValueError:
        print("Invalid user ID type. It must be int64 type")
    else:
        with open("./data/auth.txt") as file:
            token = file.readline()[:-2]
        if token == "":
            print("Run the command mod login before using the commands")
        else:
            headers = {
                "authorization": token
            }
            data = {
                "content": f"?{args.command} {user_id} {args.duration} {' '.join(args.reason)}"
            }
            r = requests.post(f"https://discord.com/api/v8/channels/842377245867507742/messages", data=data, headers=headers)
            if int(r.status_code) == 200:
                print("Command sucessfully used.")
            else:
                print("Command failed. Make sure that you logged in with a valid token.")
