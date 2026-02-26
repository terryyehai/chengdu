import glob

files = glob.glob('*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace('\\n</head>', '\n</head>')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Literal '\\n' artifacts cleaned from headers")
