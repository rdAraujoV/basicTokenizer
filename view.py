import json

path = r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\vocab.json"

with open(path, "r", encoding="utf-8") as file:
    vocab = json.load(file)
    
token_to_id = {v: k for k, v in vocab.items()}
sorted_tokens = sorted(token_to_id.keys(), key=lambda x: -len(x))

def tokenize(text):
    tokens = []
    i = 0
    while i < len(text):
        matched = False
        for token in sorted_tokens:
            if text.startswith(token, i):
                tokens.append(token_to_id[token])
                i += len(token)
                matched = True
                break
        if not matched:
            print(f"Unknown token: {text[i]!r}")
            i += 1
    return tokens

user_input = input(">> ")
token_ids = tokenize(user_input)

for token_id in token_ids:
    token = vocab[token_id]
    
print("Token IDs:", token_ids)

tokens = [vocab[token_id] for token_id in token_ids]
print("Tokens:", tokens)