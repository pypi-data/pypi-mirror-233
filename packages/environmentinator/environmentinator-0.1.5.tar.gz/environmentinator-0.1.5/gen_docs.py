
import subprocess
import os
import sys
import tempfile
import traceback
import shutil
import distutils.dir_util

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

yn = input('Publish content to branch www? ')
if 'y' in yn.lower():
  www_branch_folder = os.path.join(tempfile.gettempdir(), 'environmentinator-www')
  try:
    if os.path.exists(www_branch_folder):
      try:
        shutil.rmtree(www_branch_folder)
      except:
        traceback.print_exc()
        if os.name == 'nt':
          os.system('rmdir /S /Q "{}"'.format(www_branch_folder))

    os.makedirs(www_branch_folder, exist_ok=True)
    #subprocess.run([
    #  'git', 'clone', 'https://github.com/jeffrey-p-mcateer/environmentinator'
    #])
    distutils.dir_util.copy_tree(
      os.path.dirname(__file__),
      www_branch_folder
    )
    print('Open {}'.format(www_branch_folder))
    os.chdir(www_branch_folder)
    git_branch_out = subprocess.check_output(['git', 'branch']).decode('utf-8')
    if not 'www' in git_branch_out:
      # create the new branch
      subprocess.run([
        'git', 'branch', 'www'
      ])
    # Checkout the www branch
    subprocess.run([
      'git', 'checkout', 'www'
    ])
    # Copy over our website files
    shutil.copy(index_html_f, 'index.html')
    # Remove all files from 'master', we only want index.html and the .git folder in this branch.
    # and maybe .gitignore.
    paths_to_keep = [
      '.git',
      '.gitignore',
      'index.html'
    ]
    cwd_path_names = [x for x in os.listdir()]
    for path_name in cwd_path_names:
      if not path_name in paths_to_keep:
        print('Removing {}'.format(path_name))
        if os.path.isdir(path_name):
          shutil.rmtree(path_name)
        else:
          os.remove(path_name)

    subprocess.run([
      'git', 'status'
    ])

    subprocess.run([
      'git', 'add', '-A', '.'
    ])

    subprocess.run([
      'git', 'commit', '-a', '-m', 'gen_docs.py update to www branch.'
    ])

    try:
      subprocess.run([
        'git', 'push', '-u', 'origin', 'www'
      ])
    except:
      traceback.print_exc()
    
    subprocess.run([
      'git', 'push', '-f', 'origin', 'www'
    ])

  except:
    traceback.print_exc()
  finally:
    if not 'DEBUG' in os.environ and os.path.exists(www_branch_folder):
      try:
        shutil.rmtree(www_branch_folder)
      except:
        traceback.print_exc()
        if os.name == 'nt':
          os.system('rmdir /S /Q "{}"'.format(www_branch_folder))

