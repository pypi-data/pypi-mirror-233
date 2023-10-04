import environmentinator

json5 = environmentinator.ensure_module('json5')

print(f'I have loaded json5 from {json5}')

# We can specify addtl pip args as well, these are added after "python -m pip install --target={}"
torch = environmentinator.ensure_module('torch', 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117')

print(f'I have loaded torch from {torch}')


import code
vars = globals()
vars.update(locals())
code.interact(local=vars)
