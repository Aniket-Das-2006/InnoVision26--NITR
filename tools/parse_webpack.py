with open(r'D:\NITR\webpack.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

import re
print("Code length:", len(code))
# Find chunkId mappings
# e.g. {123:"abc", ...}
matches = re.findall(r'(\{[0-9]+:[^}]+\})', code)
for m in matches:
    print("Match:", m[:200])

# Look for .js references or hash mappings
hashes = re.findall(r'[a-f0-9]{16}', code)
print(f"Hashes found: {len(hashes)}")
