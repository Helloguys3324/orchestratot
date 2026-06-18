import math
with open('docs/ARCHITECTURE_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

chunk_size = 500
num_chunks = math.ceil(len(content) / chunk_size)

for i in range(num_chunks):
    chunk_content = content[i*chunk_size : (i+1)*chunk_size]
    with open(f'/tmp/chunk_arch_{i+1}.txt', 'w', encoding='utf-8') as out:
        out.write(chunk_content)

print(num_chunks)
