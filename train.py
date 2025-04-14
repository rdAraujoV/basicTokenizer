import json

path = r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\datasets\trainingSet.txt"

with open(path, "r", encoding="utf-8") as file:
    text = file.read()
        
text = text.replace('\u200b', '')

with open(path, "w", encoding="utf-8") as file:
    file.write(text)

# Character-level tokens
tokens = list(text)
tokenizer_vocab = {str(i): char for i, char in enumerate(sorted(set(tokens)))}

# MERGE
# Merging pairs that starts with whitespace
merged_pairs = set()
for i in range(len(tokens) - 1):
    if tokens[i] == ' ':
        merged_token = tokens[i] + tokens[i+1]
        merged_pairs.add(merged_token)
        
max_id = max(int(k) for k in tokenizer_vocab.keys())
for merged_token in sorted(merged_pairs):
    max_id += 1
    tokenizer_vocab[str(max_id)] = merged_token
    
# Merging common pairs
def get_stats(ids):
    pair_counts = {}
    
    for i in range(len(ids) - 1):
        pair = (ids[i], ids[i+1])
        
        if pair in pair_counts:
            pair_counts[pair] += 1
        else:
            pair_counts[pair] = 1
        
    return pair_counts

def merge_pair(tokens, merge):
    merged = []
    i = 0
    while i < len(tokens) - 1:
        if (tokens[i], tokens[i + 1]) == merge:
            merged.append(tokens[i] + tokens[i + 1])
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    if i == len(tokens) - 1:
        merged.append(tokens[-1])
    return merged

def run_bpe_merges(tokens, vocab, num_merges):
    merges = []
    
    for _ in range(num_merges):
        stats = get_stats(tokens)
        if not stats:
            break
        
        most_common = max(stats.items(), key=lambda x: x[1])[0] 
        new_token = most_common[0] + most_common[1]
        
        max_id = max(int(k) for k in vocab.keys())
        vocab[str(max_id + 1)] = new_token
        
        tokens = merge_pair(tokens, most_common)
        merges.append(most_common)
    
    return tokens, vocab, merges


tokens, tokenizer_vocab, merge_history = run_bpe_merges(tokens, tokenizer_vocab, num_merges=10000)

vocab_path = r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\vocab.json"

with open(vocab_path, "w", encoding="utf-8") as file:
    json.dump(tokenizer_vocab, file, ensure_ascii=False, indent=2)

merge_path = r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\merges.json"
with open(merge_path, "w", encoding="utf-8") as file:
    json.dump(merge_history, file, ensure_ascii=False, indent=2)