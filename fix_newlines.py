import glob

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove literal \n that was accidentally injected
    content = content.replace('\\n', '')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Literal backslash-n removed from all HTML files.")
