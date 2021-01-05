# Notify changes to IP address using email
This basic app is designed to work with a task shceduler, e.g. `cron` in linux. It will check against the [public API for whatismyip.com](https://www.whatismyip.com/api/) and record the fetchd IP address in a file. If the fetched IP address is different from the stored IP address, it will save the new address and then send an email to the configured address containing the new IP address.

The send-email-component of this app only works if you have a Gmail account that [allows Less Secure Apps](https://support.google.com/accounts/answer/6010255?hl=en).

## To run
Requires python 3 with [pip](https://pypi.org/) installed.

Steps:

1. Install required libs with `python -m pip install -r requirements.txt`
2. Create a file `.env` in the root directory of this project. Add credentials `GMAIL_USER` and `GMAIL_PASSWORD`. E.g. `GMAIL_USER=myemail@gmail.com`, same for password.
3. Do a test run to make sure everything works: `python whatisit.py`
    - if successful, the new file `current_ip` should contain your current IP address, an email should be sent, and there will be a log file created. Check the log
    - if it fails, check the created log file for errors

## To schedule regular runs
If on linux, use `cron`. If you haven't used `cron` before you can learn about it [here](https://opensource.com/article/17/11/how-use-cron-linux).

If you jus want to get it running every minute do the following.

1. `crontab -e` to edit the `cron` jobs
2. Select editor (nano is recommended for beginners)
3. At the bottom of the file, add `* * * * * python3 ~/whats-my-ip-again/whatisit.py`
    - specify filename/location as appropriate. The above assumes you cloned it into your user home directory
4. Save the file (CTRL+S) and exit (CTRL+X)

The `cron` scheduler should now pick up this task and execute it regularly.