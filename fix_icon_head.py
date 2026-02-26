import os
import glob

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
        # Easy insert right before <link rel="preconnect"
        content = content.replace('  <link rel="preconnect"', new_head_tags + '  <link rel="preconnect"')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Icon head tags successfully re-injected using replace")
