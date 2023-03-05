"""
An application for managing and advanced editing of MOD pedalboards
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import paramiko


def get_pedalboard_list():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('moddwarf.local', username='root', password='mod')

    stdin, stdout, stderr = client.exec_command('ls -l .pedalboards')
    pb_list = list(stdout)[1:]
    pb_list = [pbdir.split(' ')[-1].strip('\n') for pbdir in pb_list]
    return pb_list



class MODPowerTools(toga.App):

    def startup(self):

        self.main_box = toga.Box()
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box

        pedalboard_actions = toga.Group("Pedalboards")
        cmd_load_pedalboards = toga.Command(
            self.handler_load_pedalboards,
            text="Load Pedalboards",
            tooltip="Load current pedalboards into the app",
            icon=toga.Icon.TOGA_ICON,
            group=pedalboard_actions,
        )

        self.main_window.toolbar.add(cmd_load_pedalboards)

        self.main_window.show()

    def handler_load_pedalboards(self, widget):
        pedalboard_list = toga.Table(headings=["Pedalboards"], data=get_pedalboard_list())
        self.main_box.add(pedalboard_list)

def main():
    return MODPowerTools()
