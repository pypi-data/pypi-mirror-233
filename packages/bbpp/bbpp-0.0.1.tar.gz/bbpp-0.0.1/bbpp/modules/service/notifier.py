from subprocess import Popen


class OSAScriptNotifier:
    @classmethod
    def notify(cls, title: str, message: str, sound: str = "Crystal"):
        notification = f'display notification "{message}" with title "{title}" sound name "{sound}"'
        # notification = 'display notification "' + message + '" with title "' + title + '" sound name "Crystal"'
        Popen(['osascript', '-e', notification])
