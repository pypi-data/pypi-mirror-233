import json
import os
import re
from pathlib import Path
from functools import partial


def _ex(e, x):
    if e is None:
        e = []
    elif isinstance(e, str):
        e = [e]
    elif isinstance(e, tuple):
        e = list(e)

    if not x:
        return e
    if isinstance(x, str):
        x = [x]
    for extention in x:
        e.append(f"\.{extention}$")

    return e


def load_conf(path=Path.home() / ".config/trixli/config.json"):
    try:
        return json.load(open(path, "r"))
    except FileNotFoundError:
        return {"ignore": [".local", "node_module", "site-packages"]}


def colorize(line, regexps):
    RED = "\033[31"
    BACK = "\033[m"
    for regexp in regexps:
        line = re.sub(regexp, Color.RED + r"\1" + Color.ENDC, line)

    return line


def match_in_file(compiled_re, max_len, path):
    if not os.path.isfile(path):
        return
    with open(path, "r") as fp:
        line_number = 1
        try:
            for line in fp:
                if _match_all(string=line, regexps=compiled_re):
                    line = colorize(line.strip(), compiled_re)
                    response = f"{path}:{line_number}> {line}"
                    print(response[:max_len])
                line_number += 1
        except UnicodeDecodeError as error:
            pass


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    RED = "\033[31m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def _match_all(string, regexps):
    for regexp in regexps:
        if re.search(regexp, string) is None:
            return False
    return True


def _match_one(string, regexps):
    for regexp in regexps:
        if re.search(regexp, string):
            return True
    return False


def _matches(string, regexps):
    matches = []
    for regexp in regexps:
        result = re.search(regexp, string)
        if result is None:
            return False
        matches.append(result)

    return result


def index_path(path):
    if path:
        return path
    return Path.home() / ".fython.json"


def compile_re(regexps, with_group: bool = True):
    if with_group:
        return [re.compile("(" + str(regexp) + ")") for regexp in regexps]
    else:
        return [re.compile(str(regexp)) for regexp in regexps]


def _walk(path: Path, ignore, functor, patterns):
    try:
        for path_object in path.iterdir():
            if _match_one(string=str(path_object), regexps=ignore):
                continue
            if _match_one(string=str(path_object), regexps=patterns):
                functor(path=path_object)
            if path_object.is_dir():
                _walk(
                    path=path_object, ignore=ignore, functor=functor, patterns=patterns
                )

    except PermissionError as e:
        pass
        # print("Could not go to", e)


def _f(paths: list, functor, p=".", ignore=None):

    if ignore is None:
        ignore = []
    else:
        ignore = list(ignore)

    conf = load_conf()
    if conf_ignore := conf.get("ignore"):
        ignore.extend(conf_ignore)

    ignore = compile_re(regexps=ignore)
    patterns = compile_re(regexps=paths)
    _walk(path=Path(p), ignore=ignore, functor=functor, patterns=patterns)
