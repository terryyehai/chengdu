import os
import re

print("Starting removal script...")

# 尋找 完整圖片展示區塊 的 Regex
# 匹配 <!-- 完整圖片展示區塊 --> 直到 </div>
pattern = re.compile(r'<!-- 完整圖片展示區塊 -->\s*<div style="padding: 16px 16px 0;">\s*<img src="images/Day\d+\.png"[^>]+>\s*</div>', re.DOTALL)

for i in range(1, 10):
    filename = f"day{i}.html"
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找出所有匹配的區塊
        matches = pattern.findall(content)
        
        if len(matches) > 1:
            # 只保留第一個，其他的移除
            print(f"[{filename}] Found {len(matches)} blocks. Keeping only the first one.")
            
            # 以第一個 match 分隔，將後面的 match 都替換為空字串
            first_match = matches[0]
            
            # 我們可以用 sub 來做，但更安全的是找到第一筆之後的內容，再做取代
            # 這裡簡單一點：找到所有的起迄 index，除了第一個以外，剩下的從後面開始刪除
            
            # 使用 finditer 找出所有的 match object
            match_objects = list(pattern.finditer(content))
            
            # 從最後一個開始刪除，這樣才不會影響前面的 index
            for match in reversed(match_objects[1:]):
                start = match.start()
                end = match.end()
                content = content[:start] + content[end:]
                
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[{filename}] Cleaned successfully.")
        else:
            print(f"[{filename}] No duplicate blocks found (Count: {len(matches)}).")
    else:
        print(f"[{filename}] File not found.")

print("Done.")
