"""
An application for managing and advanced editing of MOD pedalboards
"""
import json

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import paramiko


def connect_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('moddwarf.local', username='root', password='mod')
    return client


def get_pedalboard_list():
    client = connect_ssh()
    stdin, stdout, stderr = client.exec_command('ls -l .pedalboards')
    pb_list = list(stdout)[1:]
    pb_list = [pbdir.split(' ')[-1].strip('\n') for pbdir in pb_list]
    return pb_list

def get_pedalboard(pb_path):
    client = connect_ssh()
    pb_name, _ = pb_path.split('.')

    #
    # Pedalboard definition
    pb_data_path = f".pedalboards/{pb_path}/{pb_name}.ttl"
    stdin, stdout, stderr = client.exec_command(f'cat {pb_data_path}')
    pb_ttl = list(stdout)

    #
    # Snapshots
    #
    pb_snapshots_path = f".pedalboards/{pb_path}/snapshots.json"
    stdin, stdout, stderr = client.exec_command(f'cat {pb_snapshots_path}')
    pb_snapshots = list(stdout)
    snapshot_data = json.loads("".join(pb_snapshots))
    snapshot_names = [sn["name"] for sn in snapshot_data["snapshots"]]
    print(snapshot_names)

    #
    # Addressings
    #
    pb_adressings_path = f".pedalboards/{pb_path}/addressings.json"
    stdin, stdout, stderr = client.exec_command(f'cat {pb_adressings_path}')
    pb_addressings = list(stdout)
    addressing_data = json.loads("".join(pb_addressings))
    addressing_names = addressing_data.keys()
    print(addressing_names)


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
        pedalboard_list = toga.Table(
            headings=["Pedalboards"],
            data=get_pedalboard_list(),
            on_select=self.pedalboard_row_selected)
        self.main_box.add(pedalboard_list)

    def pedalboard_row_selected(self, table, row):
        get_pedalboard(row.pedalboards)


def main():
    return MODPowerTools()
