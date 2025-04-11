import json

text = open(r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\datasets\wikiChars.txt", "r", encoding="utf-8")
text = text.read()

text = text.replace('\u200b', '')
with open(r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\datasets\wikiChars.txt", "w", encoding="utf-8") as file:
    file.write(text)

tokens = list(text)

tokenizer_vocab = {i: char for i, char in enumerate(sorted(set(tokens)))}

for idx, char in tokenizer_vocab.items():
    print(f"{idx}: {repr(char)},")

with open(r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\vocab.json", "w", encoding="utf-8") as file:
    json.dump(tokenizer_vocab, file, ensure_ascii=False, indent=2)
    
print(f"Vocabulary size: {len(tokenizer_vocab)}")