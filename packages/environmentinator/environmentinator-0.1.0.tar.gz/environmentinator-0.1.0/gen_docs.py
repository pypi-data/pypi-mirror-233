
import subprocess
import os
import sys

sys.path.append(
  os.path.dirname(__file__)
)

# This import of environmentinator comes from __file__/..'s folder, 
# so it'll always be up to date!
import environmentinator
# 'pdoc' is not the same as 'pdoc3', yay naming ambiguities.
# fortunately we pass the library name explicitly,
# and the same thing would be necessary for eg the module 'PIL' from the library 'Pillow'
pdoc = environmentinator.ensure_module('pdoc', 'pdoc3')
import pdoc

doc_folder = os.path.abspath(
  os.path.join(os.path.dirname(__file__), 'www_docs')
)
os.makedirs(doc_folder, exist_ok=True)

context = pdoc.Context()
environmentinator_pdoc_mod = pdoc.Module('environmentinator', context=context)
pdoc.link_inheritance(context)

index_html_f = os.path.join(doc_folder, 'index.html')
with open(index_html_f, 'w') as fd:
  fd.write(environmentinator_pdoc_mod.html())

import webbrowser
webbrowser.open('file://'+index_html_f)

