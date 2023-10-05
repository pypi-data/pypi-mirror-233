import click
import readline
import shlex
import types
from typer import Typer, Abort, Exit
from cmd import Cmd
from pathlib import Path
from typing import Any, Callable, List, Optional, Union


class TyperCmd(Cmd):

    # Allow dashes
    identchars = Cmd.identchars + "-"

    nohelp = "No help on %s"
    nocommand = "Command not found: %s"

    prompt: Optional[Union[str, Callable[..., str]]] = Cmd.prompt

    def __init__(
        self,
        typer: Typer,
        hist_file: Optional[str] = None,
        *args,
        **kwargs,
    ):
        assert isinstance(typer, Typer)

        super().__init__(*args, **kwargs)

        self.old_completer: Optional[Callable] = None
        self.old_delims: Optional[str] = None

        # Set the history file
        hist_file = hist_file or Path.home() / ".typer-history"
        self.hist_file: str = hist_file

        self.typer = typer
        self._bind_commands(self.typer)

    def preloop(self):
        # read our history
        if readline:
            try:
                readline.read_history_file(self.hist_file)
            except IOError:
                pass

    def postloop(self):
        # Write our history
        if readline:
            readline.set_history_length(1000)
            try:
                readline.write_history_file(self.hist_file)
            except IOError:
                pass

    # We need to override this to fix readline
    def cmdloop(self, intro: str = None):
        self.preloop()
        # stash the current completer
        if self.completekey and readline:
            self.old_completer = readline.get_completer()
            self.old_delims = readline.get_completer_delims()
            readline.set_completer(self.complete)
            readline.set_completer_delims(" \n\t")
            to_parse = self.completekey + ": complete"
            readline.parse_and_bind(to_parse)
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                print(self.intro)
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    try:
                        line = input(self.get_prompt())
                    except EOFError:
                        # exit when got a EOFError like Ctrl+Z
                        break
                    except KeyboardInterrupt:
                        # Ctrl+C will not exit
                        continue
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
        # restore to the default completer
        finally:
            self.postloop()
            if self.completekey and readline:
                if self.old_completer:
                    readline.set_completer(self.old_completer)
                if self.old_delims:
                    readline.set_completer_delims(self.old_delims)

    def get_prompt(self) -> Optional[str]:
        return self.prompt

    def emptyline(self) -> bool:
        # we don't want to repeat the last command if nothing was typed
        return False

    def default(self, line: str):
        print(self.nocommand % line)

    def get_names(self) -> List[str]:
        # Do dir(self) instead of dir(self.__class__)
        return dir(self)

    def do_help(self, arg: str):
        if not arg:
            self.typer(args=["--help"], prog_name='', standalone_mode=False)
            return
        try:
            do_fun = getattr(self, "do_" + arg, None)
            doc = do_fun.__doc__
            if doc:
                print(doc)
                return
            else:
                self.typer(args=[arg, "--help"], prog_name='', standalone_mode=False)
                return
        except AttributeError:
            pass

    def do_quit(self, arg) -> bool:
        return True

    def do_exit(self, arg) -> bool:
        return True

    def print_topics(
        self, header: Any, cmds: Optional[List[str]], cmdlen: int, maxcol: int
    ):
        if cmds:
            print(header)
            if self.ruler:
                print(str(self.ruler * len(header)))
            self.columnize(cmds, maxcol - 1)

    def _bind_commands(self, typer: Typer):
        self.is_single_cmd = len(typer.registered_commands) == 1
        for command_info in typer.registered_commands:
            name = command_info.callback.__name__
            setattr(self, f"do_{name}", types.MethodType(self._typer_invoke(name), name))
        for typer_info in typer.registered_groups:
            name = typer_info.name
            setattr(self, f"do_{name}", types.MethodType(self._typer_invoke(name), name))

    def _typer_invoke(self, name: str):
        def invoke_(name: str, arg: str):
            if self.is_single_cmd:
                args = shlex.split(arg)
            else:
                args = [name] + shlex.split(arg)
            try:
                self.typer(args=args, prog_name='', standalone_mode=False)
            except click.ClickException as e:
                e.show()
            except (Abort, Exit):
                pass
            return False

        invoke_.__name__ = "do_%s" % name
        return invoke_
