from datasets import load_dataset

dataset = load_dataset("oscar", "unshuffled_deduplicated_pt", split="train", streaming=True, trust_remote_code=True)

target_size_bytes = 10 * 1024 * 1024  # 10 MB
collected = []
total_size = 0

for sample in dataset:
    text = sample['text']
    text_bytes = len(text.encode('utf-8'))
    if total_size + text_bytes > target_size_bytes:
        break
    collected.append(text)
    total_size += text_bytes
    
small_corpus = "\n".join(collected)

# Save
with open("trainingSet.txt", "w", encoding="utf-8") as f:
    f.write(small_corpus)