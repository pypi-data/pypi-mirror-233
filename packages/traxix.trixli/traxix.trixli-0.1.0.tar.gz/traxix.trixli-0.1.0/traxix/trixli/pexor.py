import json
import ast
from fire import Fire
from traxix.trixli.utils import _f, index_path
from functools import partial
from pathlib import Path


def dict_add(d, k, v):

    if k in d:
        d[k].add(v)
    else:
        d[k] = {
            v,
        }


def json_converter(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


def parser(path, accumulator: list):
    print("path", path)
    try:
        for node in ast.parse(open(path, "r").read()).body:
            if not isinstance(node, ast.ImportFrom) and not isinstance(
                node, ast.Import
            ):
                continue
            for imp in node.names:
                dict_add(accumulator, imp.name, str(path))
            if isinstance(node, ast.ImportFrom):
                dict_add(accumulator, node.module, str(path))
    except FileNotFoundError:
        pass
    except SyntaxError:
        pass


def get_indexor(name, accumulator):
    if name == "python":
        return parser

    if name == "files":
        return files


def pexor(p=".", output: str = None, append=True, indexor="python"):
    accumulator = {}
    output = index_path(output)
    _f("\.py$", p=p, functor=get_indexor(indexor))

    if append:
        old = json.load(open(output, "r"))
        for k, v in old.items():
            if k in accumulator:
                accumulator[k].update(v)
            else:
                accumulator[k] = {
                    v,
                }

    json.dump(accumulator, open(output, "w"), indent=2, default=json_converter)


if __name__ == "__main__":
    Fire(pexor)
