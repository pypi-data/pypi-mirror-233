import curses
import os
import sys
import threading
import time
from platform import system

import readchar
from rich import box

from toolboxv2 import remove_styles
from toolboxv2 import Style as tbStyle
from toolboxv2.utils.toolbox import get_app, App

NAME = "cliv2"

from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import Progress, TimeElapsedColumn, SpinnerColumn, TextColumn

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress
from rich.live import Live
from rich.style import Style as riStyle
from rich.table import Table
import time
import psutil
from rich.console import Console
from rich.progress import Progress


console = Console()


def user_input(app: App, print):
    get_input = True
    command = ""
    print_command = []
    helper = ""
    helper_index = 0
    options = []
    sh_index = 0
    session_history = [[]]
    session_history += [c for c in app.command_history]
    print()
    while get_input:

        key = readchar.readkey()

        if key == b'\x05' or key == '\x05':
            print('\033', end="")
            get_input = False
            command = "EXIT"

        elif key == readchar.key.LEFT:
            if helper_index > 0:
                helper_index -= 1

        elif key == readchar.key.RIGHT:
            if helper_index < len(options) - 1:
                helper_index += 1

        elif key == readchar.key.UP:
            sh_index -= 1
            if sh_index <= 0:
                sh_index = len(session_history) - 1
            command = ""
            print_command = session_history[sh_index]

        elif key == readchar.key.DOWN:
            sh_index += 1
            if sh_index >= len(session_history):
                sh_index = 0
            command = ""
            print_command = session_history[sh_index]

        elif key == b'\x08' or key == '\x7f':
            if len(command) == 0 and len(print_command) != 0:
                command = print_command[-1]
                command = command[:-1]
                print_command = print_command[:-1]
            else:
                command = command[:-1]
        elif key == b' ' or key == ' ':
            print_command.append(command)
            command = ""
        elif key == readchar.key.ENTER:
            get_input = False
            print_command.append(command)
        elif key == b'\t' or key == '\t':
            command += helper
        else:
            if type(key) == str:
                command += key
            else:
                command += str(key, "ISO-8859-1")

        options = list(set(app.autocompletion(command)))

        if helper_index > len(options) - 1:
            helper_index = 0

        helper = ""
        do = len(options) > 0
        if do:
            helper = options[helper_index][len(command):].lower()

        to_print = app.PREFIX + app.pretty_print(print_command + [command + tbStyle.Underline(tbStyle.Bold(helper))])
        if do:
            to_print += " | " + tbStyle.Bold(options[helper_index]) + " " + str(options)
        print(to_print)

    print()

    app.command_history.append(print_command)

    return print_command


def command_runner(app, command, args, print, input, advance):
    if command[0] == '':  # log(helper)
        print("Pleas enter a command or help for mor information")

    elif command[0].lower() == '_hr':
        if len(command) == 2:
            if input(f"Do you to hot-reloade {'alle mods' if len(command) <= 1 else command[1]}? (y/n): ") in \
                ["y", "yes", "Y"]:

                if command[1] in app.MOD_LIST.keys():
                    app.reset()
                    try:
                        app.remove_mod(command[1])
                    except Exception as e:
                        print(tbStyle.RED(f"Error removing module {command[1]}\nERROR:\n{e}"))

                    try:
                        app.save_load(command[1])
                    except Exception as e:
                        print(tbStyle.RED(f"Error adding module {command[1]}\nERROR:\n{e}"))
                elif command[1] == "-x":
                    app.reset()
                    app.remove_all_modules()
                    while 1:
                        try:
                            com = " ".join(sys.orig_argv)
                        except AttributeError:
                            com = "python3 "
                            com += " ".join(sys.argv)
                        os.system(com)
                        print("Restarting..")
                        exit(0)
                else:
                    print(f"Module not found {command[1]} |  is case sensitive")
        else:
            advance(2)
            app.reset()
            advance(29)
            app.remove_all_modules()
            advance(29)
            app.load_all_mods_in_file()
            advance(29)

    elif command[0].lower() == 'app-info':
        print(f"{app.id = }\n{app.stuf_load = }\n{app.mlm = }\n{app.auto_save = }"
              f"\n{app.AC_MOD = }\n{app.debug = }")
        print(f"PREFIX={app.PREFIX}"
              f"\nMACRO={app.pretty_print(app.MACRO[:7])}"
              f"\nMODS={app.pretty_print(app.MACRO[7:])}"
              f"\nSUPER_SET={app.pretty_print(app.SUPER_SET)}")

    elif command[0].lower() == "exit":  # builtin events(exit)
        advance(100)
        if input("Do you want to exit? (y/n): ") in ["y", "yes", "Y"]:
            app.save_exit()
            app.exit()

    elif command[0].lower() == "help":  # logs(event(helper))
        n = command[1] if len(command) > 2 else ''
        app.help(n)

    elif command[0].lower() == 'load-mod':  # builtin events(event(cloudM(_)->event(Build)))
        if len(command) == 2:
            advance(3)
            if app.save_load(command[1]):
                advance(50)
                app.new_ac_mod(command[1])
                advance(30)
        else:
            p = "_dev" if app.dev_modi else ""

            def do_helper(_mod):
                if "mainTool" in _mod:
                    return False
                if not _mod.endswith(".py"):
                    return False
                if _mod.startswith("__"):
                    return False
                if _mod.startswith("test_"):
                    return False
                return True

            res = list(filter(do_helper, os.listdir(f"./mods{p}/")))
            len_res = len(res)//99
            for mod_name in res:
                advance(len_res)
                mod_name_refracted = mod_name.replace(".py", '')
                print(f"Mod name : {mod_name_refracted}")
                app.SUPER_SET += [mod_name_refracted]
            print()

    elif command[0] == '..':
        app.reset()

    elif command[0] == 'cls':
        if system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    elif command[0] == 'mode':
        help_ = ['mode:live', 'mode:debug', 'mode', 'mode:stuf', 'app-info']
        app.SUPER_SET += help_
        app.MACRO += help_
        print(f"{'debug' if app.debug else 'live'} \n{app.debug=}\n{app.id=}\n{app.stuf_load=}")

    elif command[0] == 'mode:live':
        app.debug = False
        app.dev_modi = False

    elif command[0] == 'mode:debug':
        app.debug = True
        app.dev_modi = True

    elif command[0] == 'mode:stuf':
        app.stuf_load = not app.stuf_load

    elif command[0] == 'run-i':

        if len(command) > 1:
            app.run_runnable(command[1])
        else:
            app.show_runnable()

    elif command[0].lower() in app.MOD_LIST.keys():
        app.new_ac_mod(command[0])
        advance(10)

        if len(command) > 1:
            if command[1].lower() in app.SUPER_SET:
                advance(5)
                app.run_function(command[1], command[1:])
                advance(80)

    elif app.AC_MOD:  # builtin events(AC_MOD(MOD))
        if command[0].lower() in app.SUPER_SET:
            advance(5)
            app.run_function(command[0], command)
            advance(80)
        else:
            print(tbStyle.RED("function could not be found"))

    else:  # error(->)
        print(tbStyle.YELLOW("[-] Unknown command:") + app.pretty_print(command))


def convert_command_history(history):
    if len(history) == 0:
        return ""
    s = "\n".join(
        [
            ' '.join(
                (
                    ['>' + c if c == command[0] else c for c in command if
                     c.strip() and "\\" not in c and len(c) > 4 and command and c != '']
                ) if isinstance(command, list) else command
            ) for command in history if command and command != ''
        ]
    )
    while "\n\n" in s:
        s = s.replace("\n\n", "\n")
    return "History\n" + s


class ConsoleInterface:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.create_layout()
        self.content = {
            "output": ["-*#*-"],
            "input": [],
            "help": [],
            "index-output": 0,
            "index-input": 0,
            "index-help": 0,
            "Maxlines-output": 0,
            "Maxlines-help": 0,
        }
        self.panels = ["output", "input", "help"]
        self.log_file_pos = 0
        self.progress = Progress(
        )

    def show_logs_in_help(self, file_name):
        # Open the log file
        with open(f"../logs/{file_name}.log", "r") as file:
            # Seek to the last read position
            file.seek(self.log_file_pos)

            # Read the logs
            logs = file.read()

            # Update the current position in the file
            self.log_file_pos = file.tell()

        # Update the help panel with the logs
        self.update_panel("help", logs)

    def scroll_down(self, name: str, amount: int = 1):
        if self.content["index-" + name] < len(self.content[name]):
            self.content["index-" + name] += amount
            self.print_panel(name)

    def scroll_up(self, name, amount=1):
        if self.content["index-" + name] > 0:
            self.content["index-" + name] -= amount
            self.print_panel(name)

    def create_layout(self):
        self.layout.split(
            Layout(name="upper", size=3),
            Layout(name="lower"),
            Layout(name="input", size=3),
        )
        self.layout["upper"].split_row(
            Layout(name="system_info")
        )
        self.layout["lower"].split_row(
            Layout(name="output"),
            Layout(name="help", size=16),
        )

    def update_panel(self, panel_name, content, prefix='\n'):

        def compensate(x):
            for key, style in tbStyle.style_dic.items():
                if key == "END":
                    key = 'reset'
                if style in x:
                    x = x.replace(style,
                                  '[' + key.lower() + ']')
            return x
            # text, styles = remove_styles(x, infos=True)
            # rich_styles = [style.lower() for style in styles]
            # for style in rich_styles:
            #     text = '[' + style + ']' + text
            # return text

        def add_to_content():
            def add_to_content_(data):
                data_list = compensate(data).split("\n")
                added = 0
                for line in data_list:
                    if line and len(line):
                        self.content[panel_name].append(line)
                        added += 1
                for _ in range(added):
                    print("scroll_down",  len(self.content[panel_name]), console.size.height - 9, self.content["index-" + panel_name], len(self.content[panel_name]))
                    if (panel_name in ["output", "help"] and len(self.content[panel_name]) > console.size.height - 9 and
                        self.content["index-" + panel_name] < len(self.content[panel_name])+(console.size.height - 9)):
                        self.print_panel(panel_name)
                        time.sleep(0.02)
                        self.scroll_down(panel_name, 1)
                    else:
                        break

            if isinstance(content, list):
                for content_ in content:
                    context = prefix + str(content_)
                    add_to_content_(context)
            elif isinstance(content, str):
                context = prefix + content
                add_to_content_(context)
            elif isinstance(content, dict):
                for key, content_ in content.items():
                    context = prefix + key + ":" + str(content_)
                    add_to_content_(context)
            else:
                context = prefix + f"UST({type(content)})" + ":" + str(content)
                add_to_content_(context)

        if panel_name == "input":
            self.layout[panel_name].update(Panel(compensate(content), title=panel_name))
            return

        add_to_content()

        self.print_panel(panel_name)

    def print_panel(self, panel_name=""):

        def get_context(idc):
            cont = self.content[idc]
            if idc in ["output", "help"]:
                if self.content["index-" + idc]:
                    return "\n".join(cont[int(self.content["index-" + idc]):])
                cont = "\n".join(cont)
            return "".join(cont)

        if panel_name == "":
            for name in self.panels:
                self.layout[name].update(Panel(get_context(name), title=name))
        else:
            self.layout[panel_name].update(Panel(get_context(panel_name), title=panel_name))


    def update_system_info(self):
        cpu_usage = psutil.cpu_percent()
        mem_info = psutil.virtual_memory()
        # psutil.cpu_stats()
        self.layout["system_info"].update(
           Panel(f"CPU Usage: {cpu_usage}% Memory Usage: {mem_info.percent}%", title="System Info"))

    def run_command_with_loading_animation(self, app, commands, args, up, guit):

        task = self.progress.add_task(f"[cyan]Running command: {' '.join(commands)}...", total=100)
        # Run the command in a separate thread and update the progress
        def advance(x):
            self.progress.update(task, advance=x)

        def run_command():
            # Run the command
            command_runner(app, commands, args, up, guit, advance)
            # Mark the task as completed
            self.progress.update(task, completed=100)
        threading.Thread(target=run_command).start()
        # Display the progress bar until the task is completed
        while not self.progress.finished:
            self.layout["input"].update(Panel(self.progress, title=' '.join(commands)))
            # self.update_panel("input", self.progress)
            self.progress.refresh()
            self.progress.update(task, advance=0.09)
            time.sleep(0.02)


    def run(self, app, args):
        def up(x='', *args, **kwargs):
            s = str(x)
            if args:
                s += ' '.join(args)
            self.update_panel("output", s)
            self.show_logs_in_help(app.logging_filename)

        def udp(x='', *args, **kwargs):
            s = str(x)
            self.update_panel("input", s)

        def guit(x='', *args, **kwargs):
            if '\n' in x:
                up(x)
            else:
                udp(x)
            commands_ = user_input(app, udp)
            if commands_:
                return ' '.join(commands_)
            return ''

        with Live(self.layout, refresh_per_second=24, transient=True) as live: #screen=True
            live.console.print("Stating Display")
            self.update_system_info()
            app.print = up
            self.update_panel("help", convert_command_history(app.command_history[::-1]))
            up("Welcome to The ToolBoxV2")
            oau = 1
            oad = 1
            ohu = 1
            ohd = 1
            while app.alive:
                self.update_system_info()
                command = user_input(app, udp)
                commands = []
                for com in command:
                    commands.append(com.strip())
                self.content['help'] = []
                if len(commands) == 1:
                    if commands[0] == 'a-':
                        self.scroll_down('output', oau)
                        oad = 1
                        oau += 1
                    elif commands[0] == 'a+':
                        self.scroll_up('output', oad)
                        oau = 1
                        oad += 1
                    elif commands[0] == 'h-':
                        self.scroll_down('help', ohu)
                        ohd = 1
                        ohu += 1
                    elif commands[0] == 'h+':
                        self.scroll_up('help', ohd)
                        ohu = 1
                        ohd += 1
                    else:
                        self.run_command_with_loading_animation(app, commands, args, up, guit)
                else:
                    self.run_command_with_loading_animation(app, commands, args, up, guit)
                if not commands:
                    commands = ''
                help_text = app.help(commands[0])
                if help_text == "invalid":
                    help_text = convert_command_history(app.command_history[::-1])
                self.update_panel("help", help_text)

    def loading_animation(self):
        with Progress() as progress:
            task = progress.add_task("[cyan]Loading...", total=100)
            while not progress.finished:
                progress.update(task, advance=0.5)
                time.sleep(0.005)


def main(app, args):
    console_interface = ConsoleInterface()
    console_interface.create_layout()
    console_interface.run(app, args)


def run(a, b):
    main(a, b)


if __name__ == "__main__":
    main(get_app(), None)
