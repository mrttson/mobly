import code
import pprint

from mobly.controllers import android_device
from tools.snippet_shell import SnippetShell
from IPython.utils.capture import capture_output


class CustomSnippetShell(SnippetShell):

    def __init__(self):
        super().__init__(android_device.MBS_PACKAGE)
        self._console = None

    def start_console(self):
        # Set up initial console environment
        console_env = {
            'ad': self._ad,
            'pprint': pprint.pprint,
        }

        # Start the services
        self._start_services(console_env)

        # # Start the console
        # console_banner = self._get_banner(self._ad.serial)
        # code.interact(banner=console_banner, local=console_env)

        self._console = code.InteractiveConsole(locals=console_env)

    def stop_console(self):
        # Tear everything down
        self._ad.services.stop_all()

    def send(self, msg):
        with capture_output() as captured:
            self._console.push(msg)

        print(captured.stdout)
        print(captured.stderr)
        return captured.stdout


if __name__ == '__main__':
    shell = CustomSnippetShell()
    shell.load_device()
    shell.start_console()
    print(shell.send("s.wifiIsEnabled()"))
    shell.stop_console()
