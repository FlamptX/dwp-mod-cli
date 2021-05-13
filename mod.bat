@echo off
setlocal EnableDelayedExpansion

if "%1" == "" (
    echo ========================================
    type name.txt
    echo Commands:
        echo HELP        List of the commands
        echo UPDATE      Check for a new version of the CLI and update if there is any
        echo AUTOCHECK   Whether to check if there is a new version on every command usage - Usage: mod autocheck on/off
        echo WARN        Warn a member - Usage: warn {user ID} {optional reason}
        echo LOGIN       Login with your token to make post requests to the discord api
        echo KICK        Kick a member - Usage: kick {user ID} {optional reason}
        echo BAN         Ban a user - Usage: ban {user ID} {optional reason}
        echo TEMPBAN     Temporary ban a user - Usage: tempban {user ID} {duration} {optional reason}
        echo             The duration must be in this format: amount + s/m/h/d - Example: 24h
        echo MUTE        Mute a member - Usage: mute {user ID} {optional duration} {optional reason}
        echo             The duration must be in this format: amount + s/m/h/d - Example: 10m
        echo UNMUTE      Unmute a member - Usage: unmute {user ID} {optional reason}
    echo\
    echo ========================================
) else (
    if "%1" == "help" (
        echo Commands:
        echo HELP       List of the commands
        echo UPDATE     Check for a new version of the CLI and update if there is any
        echo AUTOCHECK   Whether to check if there is a new version on every command usage - Usage: mod autocheck on/off
        echo WARN       Warn a member - Usage: warn {user ID} {optional reason}
        echo LOGIN      Login with your token to make post requests to the discord api
        echo KICK       Kick a member - Usage: kick {user ID} {optional reason}
        echo BAN        Ban a user - Usage: ban {user ID} {optional reason}
        echo TEMPBAN    Temporary ban a user - Usage: tempban {user ID} {duration} {optional reason}
        echo            The duration must be in this format: amount + s/m/h/d - Example: 24h
        echo MUTE       Mute a member - Usage: mute {user ID} {optional duration} {optional reason}
        echo            The duration must be in this format: amount + s/m/h/d - Example: 10m
        echo UNMUTE     Unmute a member - Usage: unmute {user ID} {optional reason}
        echo\
    ) else (
        if "%1" == "login" (
            set /p "token=Enter your discord token: "
            echo !token! > ./data/auth.txt
            echo Login saved.
        ) else (
            if "%~1" == "tempban" (
                python ./discord-commands/temp_commands.py %*
            ) else (
                if "%~1" == "mute" (
                    if "%~3" NEQ "" (
                        python ./discord-commands/temp_commands.py %*
                    )
                ) else (
                    if "%~1" == "update" (
                        python update.py update
                    ) else (
                        if "%~1" == "autochecheck" (
                            if "%~2" == "" (
                                echo Missing the state argument. Correct usage: mod autocheck on/off
                            ) else (
                                python update.py "%~2"
                            )
                        ) else (
                            python ./discord-commands/commands.py %*
                        )
                    )
                )
            )
        )
    )
)
python update.py