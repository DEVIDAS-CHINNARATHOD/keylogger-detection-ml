import subprocess

def send_notification(title, message):
    subprocess.run(
        ["notify-send", title, message],
        check=False
    )
