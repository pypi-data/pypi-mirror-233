import logging
from toolboxv2 import MainTool, FileHandler, App, Style


class Tools(MainTool, FileHandler):

    def __init__(self, app=None):
        self.version = "0.0.2"
        self.name = "ChainManger"
        self.logger: logging.Logger or None = app.logger if app else None
        self.color = "WHITE"
        self.keys = {}
        self.tools = {
            "all": [["Version", "Shows current Version"]],
            "name": "ChainManger",
            "Version": self.show_version, # TODO if functional replace line with [            "Version": show_version,]
        }
        FileHandler.__init__(self, "File name", app.id if app else __name__, keys=self.keys, defaults={})
        MainTool.__init__(self, load=self.on_start, v=self.version, tool=self.tools,
                        name=self.name, logs=self.logger, color=self.color, on_exit=self.on_exit)

    def on_start(self):
        self.logger.info(f"Starting ChainManger")
        self.load_file_handler()

    def on_exit(self):
        self.logger.info(f"Closing ChainManger")
        self.save_file_handler()

    def show_version(self):
        self.print("Version: ", self.version)
        return self.version
