trixli is a bunch of cli script to help on a daily basis.


## Install

```
pip install traxix.trixli
```

## Usage

All the command have cli `--help` command. 

### again

Match the given pattern against bash_history. A like "Ctrl-r" but with multiple patterns.

```
again export PATH
again my complicated command
```


### f

Find paths matching the given patterns.

Args:
p: path from where to begin
e: file extension

Example:

`find` equivalents:
```
f foo bar
find . |grep foo |grep bar
```

```
f -p /tmp -e py hello world
find /tmp -name "*.py" |grep hello |grep world
```

### fr 

Like `grep -r` with multiple patterns

```
fr -e py from foo
find . -name "*.py" -exec grep from '{}' \; |grep foo
```

### fe

Like `f` but offers to open it with `emacsclient` 


### pexor.py

Indexes imports from python file. Helpful to find code exampls using a certain package.

```
pexor.py --output=imports.json
```
Will generate a dict in a json file. Keys been modules or functions and values files where to find them.
