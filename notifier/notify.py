import platform

if platform.system() == "Linux":
    from .linux_notify import send_notification
else:
    def send_notification(title, message):
        pass
