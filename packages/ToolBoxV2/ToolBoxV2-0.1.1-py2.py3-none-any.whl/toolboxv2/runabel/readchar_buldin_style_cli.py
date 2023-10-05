"""Console script for toolboxv2. min dep readchar Style"""

# Import default Pages
import sys
import os
from platform import system

# Import public Pages
import readchar
from toolboxv2 import App, Style

NAME = "cli"

def user_input(app: App):
    get_input = True
    command = ""
    print_command = []
    helper = ""
    helper_index = 0
    options = []
    sh_index = 0
    session_history = [[]]
    session_history += [c for c in app.command_history]

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

        elif key == b'\x08' or key == b'\x7f' or key == '\x08' or key == '\x7f':
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

        to_print = app.PREFIX + app.pretty_print(print_command + [command + Style.Underline(Style.Bold(helper))])
        if do:
            to_print += " | " + Style.Bold(options[helper_index]) + " " + str(options)
        sys.stdout.write("\033[K")
        print(to_print, end="\r")

    sys.stdout.write("\033[K")
    print(app.PREFIX + app.pretty_print(print_command) + "\n")

    app.command_history.append(print_command)

    return print_command


def command_runner(app, command, args):
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
                        print(Style.RED(f"Error removing module {command[1]}\nERROR:\n{e}"))

                    try:
                        app.save_load(command[1])
                    except Exception as e:
                        print(Style.RED(f"Error adding module {command[1]}\nERROR:\n{e}"))
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
            app.reset()
            app.remove_all_modules()
            app.load_all_mods_in_file()

    elif command[0].lower() == 'app-info':
        print(f"{app.id = }\n{app.stuf_load = }\n{app.mlm = }\n{app.auto_save = }"
              f"\n{app.AC_MOD = }\n{app.debug = }")
        print(f"PREFIX={app.PREFIX}"
              f"\nMACRO={app.pretty_print(app.MACRO[:7])}"
              f"\nMODS={app.pretty_print(app.MACRO[7:])}"
              f"\nSUPER_SET={app.pretty_print(app.SUPER_SET)}")

    elif command[0].lower() == "exit":  # builtin events(exit)
        if input("Do you want to exit? (y/n): ") in ["y", "yes", "Y"]:
            app.save_exit()
            app.exit()

    elif command[0].lower() == "help":  # logs(event(helper))
        n = command[1] if len(command) > 2 else ''
        app.help(n)

    elif command[0].lower() == 'load-mod':  # builtin events(event(cloudM(_)->event(Build)))
        if len(command) == 2:
            if app.save_load(command[1]):
                app.new_ac_mod(command[1])
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
            for mod_name in res:
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

        if len(command) > 1:
            if command[1].lower() in app.SUPER_SET:
                app.run_function(command[1], command[1:])

    elif app.AC_MOD:  # builtin events(AC_MOD(MOD))
        if command[0].lower() in app.SUPER_SET:
            app.run_function(command[0], command)
        else:
            print(Style.RED("function could not be found"))

    else:  # error(->)
        print(Style.YELLOW("[-] Unknown command:") + app.pretty_print(command))


def run(app: App, *args):
    while app.alive:
        print("", end="" + "->>\r")
        command = user_input(app)
        commands = []
        for com in command:
            commands.append(com.strip())
        command_runner(app, command, args)
