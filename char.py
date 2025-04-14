import json

path = r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\datasets\train.txt"

with open(path, "r", encoding="utf-8") as file:
    text = file.read()
        
text = text.replace('\u200b', '')

with open(path, "w", encoding="utf-8") as file:
    file.write(text)

# Character-level tokens
tokens = list(text)
tokenizer_vocab = {i: char for i, char in enumerate(sorted(set(tokens)))}

for idx, char in tokenizer_vocab.items():
    print(f"{idx}: {repr(char)},")

# MERGE
# Mering pairs that start with whitespace
merged_pairs = set()
for i in range(len(tokens) - 1):
    if tokens[i] == ' ':
        merged_token = tokens[i] + tokens[i+1]
        merged_pairs.add(merged_token)
        
max_id = max(tokenizer_vocab.keys())
for merged_token in sorted(merged_pairs):  # Sort for consistency
    max_id += 1
    tokenizer_vocab[max_id] = merged_token

vocab_path = r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\vocab.json"
with open(vocab_path, "w", encoding="utf-8") as file:
    json.dump(tokenizer_vocab, file, ensure_ascii=False, indent=2)
    
# print(f"Vocabulary size: {len(tokenizer_vocab)}")