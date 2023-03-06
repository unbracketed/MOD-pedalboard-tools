"""
An application for managing and advanced editing of MOD pedalboards
"""
from enum import Enum

import toga
from toga.style.pack import Pack

from .pedalboard import get_pedalboard_list, get_pedalboard


class Views(Enum):
    DEFAULT = 1
    PEDALBOARD_LIST = 2
    WEB_UI = 3


class MODPowerTools(toga.App):
    webview = None
    pedalboard_list = None
    current_view = Views.DEFAULT

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
        cmd_open_browser = toga.Command(
            self.handler_open_browser,
            text="Open Web Interface",
            tooltip="Open the current pedalboard in the web interface",
            icon=toga.Icon.DEFAULT_ICON,
            group=pedalboard_actions
        )

        self.main_window.toolbar.add(cmd_load_pedalboards, cmd_open_browser)
        self.main_window.show()

    def handler_load_pedalboards(self, widget):
        self.prepare_view(Views.PEDALBOARD_LIST)
        self.pedalboard_table = toga.Table(
            headings=["Pedalboards"],
            data=get_pedalboard_list(),
            on_select=self.pedalboard_row_selected,
        )
        self.main_box.add(self.pedalboard_table)

    def pedalboard_row_selected(self, table, row):
        snapshot_list, addressing_list = get_pedalboard(row.pedalboards)
        self.snapshot_table = toga.Table(
            headings=["Snapshots"],
            data=snapshot_list
        )
        # self.addressing_table = toga.Table(
        #     headings=["Mappings"],
        #     data=addressing_list
        # )
        addr_table_data = [
            [
                addressing_list["Page 1"]["subpage 1"]["knob_1"].get("label", "empty"),
                addressing_list["Page 2"]["subpage 1"]["knob_1"].get("label", "empty"),
                addressing_list["Page 3"]["subpage 1"]["knob_1"].get("label", "empty"),
                addressing_list["Page 4"]["subpage 1"]["knob_1"].get("label", "empty"),
                addressing_list["Page 5"]["subpage 1"]["knob_1"].get("label", "empty"),
                addressing_list["Page 6"]["subpage 1"]["knob_1"].get("label", "empty"),
                addressing_list["Page 7"]["subpage 1"]["knob_1"].get("label", "empty"),
                addressing_list["Page 8"]["subpage 1"]["knob_1"].get("label", "empty"),
            ],
            [
                addressing_list["Page 1"]["footswitch_B"].get("label", "empty"),
                addressing_list["Page 2"]["footswitch_B"].get("label", "empty"),
                addressing_list["Page 3"]["footswitch_B"].get("label", "empty"),
                addressing_list["Page 4"]["footswitch_B"].get("label", "empty"),
                addressing_list["Page 5"]["footswitch_B"].get("label", "empty"),
                addressing_list["Page 6"]["footswitch_B"].get("label", "empty"),
                addressing_list["Page 7"]["footswitch_B"].get("label", "empty"),
                addressing_list["Page 8"]["footswitch_B"].get("label", "empty"),
            ]
        ]
        print(addr_table_data)
        self.addr_page_table = toga.Table(
            headings = ["Page 1", "Page 2", "Page 3", "Page 4", "Page 5", "Page 6", "Page 7", "Page 8"],
            data=addr_table_data
        )
        self.main_box.add(self.snapshot_table, self.addr_page_table)

    def handler_open_browser(self, widget):
        self.prepare_view(Views.WEB_UI)
        self.webview = toga.WebView(
            style=Pack(flex=1),
            url="http://moddwarf.local"
        )
        self.main_window.fullscreen = True
        self.main_box.add(self.webview)

    def prepare_view(self, next_view):
        if self.current_view == Views.PEDALBOARD_LIST:
            self.main_box.remove(self.pedalboard_table)
        elif self.current_view == Views.WEB_UI:
            self.main_box.remove(self.webview)
        self.current_view = next_view


def main():
    return MODPowerTools()
