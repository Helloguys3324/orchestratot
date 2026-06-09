import math
with open('AGENTS.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

chunk_size = 50
num_chunks = math.ceil(len(lines) / chunk_size)

for i in range(num_chunks):
    chunk_lines = lines[i*chunk_size : (i+1)*chunk_size]
    with open(f'/tmp/chunk_agents_{i+1}.txt', 'w', encoding='utf-8') as out:
        out.writelines(chunk_lines)

print(num_chunks)
