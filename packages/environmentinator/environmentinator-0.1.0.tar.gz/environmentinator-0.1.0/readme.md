
# Environmentinator

Python library to ensure the runtime executing your code meets application requirements.

Capabilities include:

 - Ensure a python runtime version is `>` or `<` Major.Minor version requirements (eg "only let this tool run on python `3.10+`")
 - Ensure `pip` packages are installed, installing them to a `.pyenv` folder if they do not exist on the host


# Example usage

```python
# We do not assume environmentinator has been installed,
# so we have one prelude to pip install it
try:
    import environmentinator
except:
    import pip
    pip.main(['install', '--user', 'environmentinator'])
    import environmentinator

# First arg is comparison expression; eg '==3.10', '<3.7', '>=3.8'
# Second argument is an optional list of alternative folders to
# search for python runtimes that could match the requested version,
# if the current one does not match.
environmentinator.ensure_py_version('>3.8',)


# If json5 exists in `.pyenv` great, if not use pip to install with `--target=.pyenv`
json5 = environmentinator.ensure_module('json5')


```


# Generating Library Docs

```bash
python gen_docs.py

```

# Examples

See `./examples/` for all examples.

 - `example_01.py`

![example_01](./examples/example_01.jpg)


