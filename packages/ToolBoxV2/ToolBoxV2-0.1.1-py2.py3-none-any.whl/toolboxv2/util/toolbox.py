"""Main module."""
import os
import sys
import time
from platform import node
from importlib import import_module
from inspect import signature

import requests

from toolboxv2.utils.file_handler import FileHandler
from toolboxv2.utils.tb_logger import setup_logging, get_logger
from toolboxv2.utils.Style import Style
import toolboxv2

import logging
from dotenv import load_dotenv
load_dotenv()

class AppArgs:
    init = None
    init_file = None
    update = False
    update_mod = None,
    delete_ToolBoxV2 = None
    delete_mod = None
    get_version = False
    mod_version_name = 'mainTool'
    name = 'main'
    modi = 'cli'
    port = 68945
    host = '0.0.0.0'
    load_all_mod_in_files = False
    live = False

    def default(self):
        return self


class ApiOb:
    token = ""
    data = {}

    def default(self):
        return self


class Singleton(type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


class App(metaclass=Singleton):
    def __init__(self, prefix: str = "", args=AppArgs().default()):
        t0 = time.time()
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath).replace("\\util", "")
        os.chdir(dname)
        print(f"Starting ToolBox as {prefix} from : ", Style.Bold(Style.CYAN(f"{os.getcwd()}")))

        if "test" in prefix:
            setup_logging(logging.NOTSET, name="toolbox-test", interminal=True,
                          file_level=logging.NOTSET).info("Logger initialized")
        elif "live" in prefix:
            setup_logging(logging.WARNING, name="toolbox-live", is_online=True
                          , online_level=logging.WARNING).info("Logger initialized")
        elif "debug" in prefix:
            setup_logging(logging.DEBUG, name="toolbox-debug", interminal=True,
                          file_level=logging.WARNING).info("Logger initialized")
        else:
            setup_logging(logging.ERROR, name=f"toolbox-{prefix}").info("Logger initialized")
        get_logger().info(Style.GREEN("Starting ToolBox"))

        if args.init:
            _initialize_toolBox(args.init, args.init_file)

        name = prefix + '-' + node()
        self.version = toolboxv2.__version__

        self.keys = {
            "MACRO": "macro~~~~:",
            "MACRO_C": "m_color~~:",
            "HELPER": "helper~~~:",
            "debug": "debug~~~~:",
            "id": "name-spa~:",
            "st-load": "mute~load:",
            "module-load-mode": "load~mode:",
            "comm-his": "comm-his~:",
            "develop-mode": "dev~mode~:",
        }

        defaults = {
            "MACRO": ['Exit'],
            "MACRO_C": {},
            "HELPER": {},
            "debug": not args.live,
            "id": name,
            "st-load": False,
            "module-load-mode": 'I',
            "comm-his": [[]],
            "develop-mode": False,
        }

        self.config_fh = FileHandler(name + ".config", keys=self.keys, defaults=defaults)
        self.config_fh.load_file_handler()

        self._debug = False

        self._debug = self.config_fh.get_file_handler(self.keys["debug"])
        self.command_history = self.config_fh.get_file_handler(self.keys["comm-his"])
        self.dev_modi = self.config_fh.get_file_handler(self.keys["develop-mode"])
        self.MACRO = self.config_fh.get_file_handler(self.keys["MACRO"])
        self.MACRO_color = self.config_fh.get_file_handler(self.keys["MACRO_C"])
        self.HELPER = self.config_fh.get_file_handler(self.keys["HELPER"])
        self.id = self.config_fh.get_file_handler(self.keys["id"])
        self.stuf_load = self.config_fh.get_file_handler(self.keys["st-load"])
        self.mlm = self.config_fh.get_file_handler(self.keys["module-load-mode"])

        self.auto_save = True
        self.PREFIX = Style.CYAN(f"~{node()}@>")
        self.MOD_LIST = {}
        self.logger: logging.Logger = get_logger()
        self.SUPER_SET = []
        self.AC_MOD = None
        self.alive = True

        print(
            f"SYSTEM :: {node()}\nID -> {self.id},\nVersion -> {self.version},\n"
            f"load_mode -> {'coppy' if self.mlm == 'C' else ('Inplace' if self.mlm == 'I' else 'pleas use I or C')}\n")

        if args.update:
            self.run_any("cloudM", "#update-core", [])

        if args.get_version:
            v = self.version
            if args.mod_version_name != "mainTool":
                v = self.run_any(args.mod_version_name, 'Version', [])
            print(f"Version {args.mod_version_name} : {v}")

        self.logger.info(
            Style.GREEN(
                f"Finish init up in t-{time.time() - t0}s"
            )
        )

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        if not isinstance(value, bool):
            self.logger.debug(f"Value must be an boolean. is : {value} type of {type(value)}")
            raise ValueError("Value must be an boolean.")

        self.logger.info(f"Setting debug {value}")
        self._debug = value

    def _coppy_mod(self, content, new_mod_dir, mod_name):
        mode = 'xb'

        self.logger.info(f" coppy mod {mod_name} to {new_mod_dir} size : {sys.getsizeof(content)/8388608:.3f} mb")

        if not os.path.exists(new_mod_dir):
            os.makedirs(new_mod_dir)
            with open(f"{new_mod_dir}/__init__.py", "w") as nmd:
                nmd.write(f"__version__ = '{self.version}'")

        if os.path.exists(f"{new_mod_dir}/{mod_name}.py"):
            mode = False
            with open(f"{new_mod_dir}/{mod_name}.py", 'rb') as d:
                runtime_mod = d.read()  # Testing version but not efficient
            if len(content) != len(runtime_mod):
                mode = 'wb'

        if mode:
            with open(f"{new_mod_dir}/{mod_name}.py", mode) as f:
                f.write(content)

    def _pre_lib_mod(self, mod_name):
        working_dir = self.id.replace(".", "_")
        lib_mod_dir = f"toolboxv2.runtime.{working_dir}.mod_lib."

        self.logger.info(f"pre_lib_mod {mod_name} from {lib_mod_dir}")

        postfix = "_dev" if self.dev_modi else ""
        mod_file_dir = f"./mods{postfix}/{mod_name}.py"
        new_mod_dir = f"./runtime/{working_dir}/mod_lib"
        with open(mod_file_dir, "rb") as c:
            content = c.read()
        self._coppy_mod(content, new_mod_dir, mod_name)
        return lib_mod_dir

    def _copy_load(self, mod_name):
        loc = self._pre_lib_mod(mod_name)
        return self.inplace_load(mod_name, loc=loc)

    def inplace_load(self, mod_name, loc="toolboxv2.mods."):
        if self.dev_modi and loc == "toolboxv2.mods.":
            loc = "toolboxv2.mods_dev."
        if mod_name.lower() in list(self.MOD_LIST.keys()):
            self.logger.info(f"Reloading mod from : { loc + mod_name}")
            self.remove_mod(mod_name)
        mod = import_module(loc + mod_name)
        mod = getattr(mod, "Tools")
        mod = mod(app=self)
        mod_name = mod.name
        self.MOD_LIST[mod_name.lower()] = mod
        color = mod.color if mod.color else "WHITE"
        self.MACRO.append(mod_name.lower())
        self.MACRO_color[mod_name.lower()] = color
        self.HELPER[mod_name.lower()] = mod.tools["all"]

        return mod

    def _get_function(self, name):

        self.logger.info(f"getting function : {name}")

        if not self.AC_MOD:
            self.logger.debug(Style.RED("No module Active"))
            return None

        if name.lower() not in self.SUPER_SET:
            self.logger.debug(Style.RED(f"KeyError: {name} function not found 404"))
            return None

        return self.AC_MOD.tools[self.AC_MOD.tools["all"][self.SUPER_SET.index(name.lower())][0]]

    def save_exit(self):
        self.logger.info(f"save exiting saving data to {self.config_fh.file_handler_filename} states of {self.debug=}"
                         f" {self.stuf_load=} {self.mlm=}")
        self.config_fh.add_to_save_file_handler(self.keys["debug"], str(self.debug))
        self.config_fh.add_to_save_file_handler(self.keys["st-load"], str(self.stuf_load))
        self.config_fh.add_to_save_file_handler(self.keys["module-load-mode"], self.mlm)
        self.config_fh.add_to_save_file_handler(self.keys["comm-his"], str(self.command_history))

    def load_mod(self, mod_name):

        self.logger.info(f"try opening module {mod_name} in mode {self.mlm}")

        if self.mlm == "I":
            return self.inplace_load(mod_name)
        elif self.mlm == "C":
            return self._copy_load(mod_name)
        else:
            self.logger.critical(f"config mlm must bee I (inplace load) or C (coppy to runtime load) is {self.mlm=}")
            raise ValueError(f"config mlm must bee I (inplace load) or C (coppy to runtime load) is {self.mlm=}")

    def load_all_mods_in_file(self, working_dir="mods"):

        t0 = time.time()

        iter_res = self.get_all_mods(working_dir)

        opened = 0
        for mod in iter_res:
            opened += 1
            self.logger.info(f"Loading module : {mod}")
            if self.debug:
                self.load_mod(mod)
                continue
            else:
                try:
                    self.load_mod(mod)
                except Exception as e:
                    self.logger.error(Style.RED("Error") + f" loading module {mod} {e}")

        self.logger.info(f"opened  : {opened} modules in t-{time.time()-t0}s")

        return True

    def get_all_mods(self, working_dir="mods"):
        self.logger.info(f"collating all mods in working directory {working_dir}")

        w_dir = self.id.replace(".", "_")

        if self.mlm == "C":
            if os.path.exists(f"./runtime/{w_dir}/mod_lib"):
                working_dir = f"./runtime/{w_dir}/mod_lib/"
        if working_dir == "mods":
            pr = "_dev" if self.dev_modi else ""
            working_dir = f"./mods{pr}"

        res = os.listdir(working_dir)

        self.logger.info(f"found : {len(res)} files")

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

        def r_endings(word: str):
            return word[:-3]

        return list(map(r_endings, filter(do_helper, res)))

    def remove_all_modules(self):
        iter_list = self.MOD_LIST.copy()

        self.exit_all_modules()

        for mod_name in iter_list.keys():
            self.logger.info(f"removing module : {mod_name}")
            try:
                self.remove_mod(mod_name)
            except Exception as e:
                self.logger.error(f"Error removing module {mod_name} {e}")

    def exit_all_modules(self):
        for mod in self.MOD_LIST.items():
            self.logger.info(f"closing: {mod[0]}")
            if mod[1]._on_exit:
                try:
                    mod[1]._on_exit()
                    self.print_ok()
                except Exception as e:
                    self.logger.debug(Style.YELLOW(Style.Bold(f"closing ERROR : {e}")))

    def print_ok(self):
        self.logger.info("OK")

    def remove_mod(self, mod_name):

        self.logger.info(f"Removing mod from sto")
        del self.MOD_LIST[mod_name.lower()]
        del self.MACRO_color[mod_name.lower()]
        del self.HELPER[mod_name.lower()]
        self.MACRO.remove(mod_name.lower())

    def colorize(self, obj):
        for pos, o in enumerate(obj):
            if not isinstance(o, str):
                o = str(o)
            if o.lower() in self.MACRO:
                if o.lower() in self.MACRO_color.keys():
                    obj[pos] = f"{Style.style_dic[self.MACRO_color[o.lower()]]}{o}{Style.style_dic['END']}"
        return obj

    def pretty_print(self, obj: list):
        if not isinstance(obj, list):
            raise ValueError(f"Invalid type {type(obj)} valid is list")
        obj_work = obj.copy()
        obj_work = self.colorize(obj_work)
        s = ""
        for i in obj_work:
            s += str(i) + " "
        return s

    def autocompletion(self, command):
        options = []
        if command == "":
            return options
        for macro in self.MACRO + self.SUPER_SET:
            if macro.startswith(command.lower()):
                options.append(macro)
        self.logger.info(f"Autocompletion in {command} aut : {options}")
        return options

    def exit(self):
        self.exit_all_modules()
        self.logger.info("Exiting ToolBox")
        print(Style.Bold(Style.CYAN("OK - EXIT ")))
        print('\033', end="")
        self.alive = False
        self.config_fh.save_file_handler()

    def help(self, command: str):
        if not self.AC_MOD and command == "":
            print(f"All commands: {self.pretty_print(self.MACRO)} \nfor mor information type : help [command]")
            return "intern-error"
        elif self.AC_MOD:
            print(Style.Bold(self.AC_MOD.name))
            self.command_viewer(self.AC_MOD.tools["all"])
            return self.AC_MOD.tools["all"]

        elif command.lower() in self.HELPER.keys():
            helper = self.HELPER[command.lower()]
            print(Style.Bold(command.lower()))
            self.command_viewer(helper)
            return helper
        else:
            print(Style.RED(f"HELPER {command} is not a valid | valid commands ar"
                            f" {self.pretty_print(list(self.HELPER.keys()))}"))
            return "invalid commands"

    def save_load(self, filename):
        self.logger.info(f"Save load module {filename}")
        if not filename:
            self.logger.warning("no filename specified")
            return False
        avalabel_mods = self.get_all_mods()
        i = 0
        fw = filename.lower()
        esist = False
        for mod in list(map(lambda x: x.lower(), avalabel_mods)):
            if fw == mod:
                filename = avalabel_mods[i]
                esist = True
                break
            i += 1

        if not esist:
            return "ModuleNotFoundError"

        if self.debug:
            return self.load_mod(filename)
        try:
            return self.load_mod(filename)
        except ModuleNotFoundError:
            self.logger.error(Style.RED(f"Module {filename} not found"))

        return False

    def reset(self):
        self.AC_MOD = None
        self.PREFIX = Style.CYAN(f"~{node()}@>")
        self.SUPER_SET = []

    def get_file_handler_name(self):
        if not self.AC_MOD:
            self.logger.debug(Style.RED("No module Active"))
            return None
        try:
            if self.AC_MOD.file_handler_filename:
                return self.AC_MOD.file_handler_filename
        except AttributeError as e:
            self.logger.error(Style.RED(f"AttributeError: {e} has no file handler 404"))
        return None

    def run_function(self, name, command):
        # get function
        self.logger.info(f"Start setup for : {name} function")

        function = self._get_function(name)
        res = {}
        if not function:
            self.logger.debug(Style.RED(f"Function {name} not found"))
            return False
        # signature function
        self.logger.info(f"profiling function")
        sig = signature(function)
        self.logger.info(f"signature : {sig}")
        args = len(sig.parameters)
        self.logger.info(f"args-len : {args}")
        self.logger.info(f"staring function")
        if args == 0:
            if self.debug:
                res = function()
            else:
                try:
                    self.print_ok()
                    print("\nStart function\n")
                    res = function()
                except Exception as e:
                    self.logger.error(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))
                    return res

        elif args == 1:
            if self.debug:
                res = function(command)
            else:
                try:
                    self.print_ok()
                    print("\nStart function\n")
                    res = function(command)
                except Exception as e:
                    self.logger.error(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))
                    return res

        elif args == 2:
            if self.debug:
                res = function(command, self)
            else:
                try:
                    self.print_ok()
                    print("\nStart function\n")
                    res = function(command, self)
                except Exception as e:
                    self.logger.error(Style.YELLOW(Style.Bold(f"! function ERROR : {e}")))
                    return res
        else:
            self.logger.error(Style.YELLOW(f"! to many args {args} def ...(u): | -> {str(sig)}"))
            return res

        self.logger.info(f"Execution done")
        if not res:
            self.logger.debug("No return value")
        else:
            self.logger.debug(res)

        return res

    def run_any(self, module_name: str, function_name: str, command: list):

        do_sto = self.AC_MOD is not None
        ac_sto = ""
        if do_sto:
            ac_sto = self.AC_MOD.name

        if module_name.lower() not in list(self.MOD_LIST.keys()):
            self.logger.warning(f"Module : {module_name}.{function_name} not online")
            self.save_load(module_name)

        self.new_ac_mod(module_name)
        res = self.run_function(function_name, command)

        if do_sto:
            self.new_ac_mod(ac_sto)

        return res

    def set_spec(self):
        self.SUPER_SET = []
        for spec in self.AC_MOD.tools["all"]:
            self.SUPER_SET.append(spec[0].lower())

    def new_ac_mod(self, name):
        self.logger.info(f"New ac mod : {name}")
        if name.lower() not in self.MOD_LIST.keys():
            self.logger.warning(f"Could not find {name} in {self.MOD_LIST.keys()}")
            return f"valid mods ar : {self.MOD_LIST.keys()}"
        self.AC_MOD = self.MOD_LIST[name.lower()]
        self.AC_MOD.stuf = self.stuf_load
        self.PREFIX = Style.CYAN(
            f"~{node()}:{Style.Bold(self.pretty_print([name.lower()]).strip())}{Style.CYAN('@>')}")
        self.set_spec()
        return True

    @staticmethod
    def command_viewer(mod_command):
        mod_command_names = []
        mod_command_dis = []
        print(f"\n")
        for msg in mod_command:
            if msg[0] not in mod_command_names:
                mod_command_names.append(msg[0])
                mod_command_dis.append([])

            for dis in msg[1:]:
                mod_command_dis[mod_command_names.index(msg[0])].append(dis)

        for tool_address in mod_command_names:
            print(Style.GREEN(f"{tool_address}, "))
            for log_info in mod_command_dis[mod_command_names.index(tool_address)]:
                print(Style.YELLOW(f"    {log_info}"))
            print("\n")

        return mod_command_names

    @debug.setter
    def debug(self, value):
        self._debug = value


def _initialize_toolBox(init_type, init_from):
    logger = get_logger()

    logger.info("Initialing ToolBox: " + init_type)
    if init_type.startswith("http"):
        logger.info("Download from url: " + init_from + "\n->temp_config.config")
        try:
            data = requests.get(init_from).json()["res"]
        except TimeoutError:
            logger.error(Style.RED("Error retrieving config information "))
            exit(1)

        init_type = "main"
    else:
        data = open(init_from, 'r+').read()

    fh = FileHandler(init_type + '-' + node() + ".config")
    fh.open_s_file_handler()
    fh.file_handler_storage.write(str(data))
    fh.file_handler_storage.close()

    logger.info("Done!")
