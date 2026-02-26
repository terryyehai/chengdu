import os
import glob
import re

new_head_tags = '''  <link rel="manifest" href="./manifest.json" />
  <link rel="icon" href="./panda-icon-192.png" type="image/png" />
  <link rel="apple-touch-icon" href="./panda-icon-192.png" />
'''

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # ensure new tags don't exist yet
    if 'panda-icon-192.png' not in content:
        # replace theme-color tag with itself + the new tags
        content = re.sub(r'(<meta name="theme-color" content=".*?" />)', r'\1\n' + new_head_tags, content)
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Icon head tags successfully re-injected using regex sub")
