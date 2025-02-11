# Basic BPE Tokenizer  

This project is a **simple tokenizer** based on **Byte Pair Encoding (BPE)**, inspired by Andrej Karpathy’s videos, implemented in **raw Python**.

The idea behind a tokenizer is to **convert human-readable text into tokens** (integers) to make it **machine-readable**.
- BPE is widely used in NLP (e.g., GPT models) to efficiently represent words as subword units.  
- This implementation **encodes** and **decodes** text using BPE, demonstrating how frequent byte pairs are merged into new tokens.

### **1️⃣ Encoding Phase** (Text ➡️ Tokens)
In this implementation, I started turning a raw string of text, the first chapter of Proverbs in Portuguese, into a raw bytes UTF-8 list:
text = 'Provérbios 1 Propósito e tema 1- Provérbios de Salomão, filho de Davi, rei de Israel. 2- Eles ajudarão a adquirir a sabedoria e a instrução; a compreender as palavras que dão entendimento;'
tokens = text.encode(encoding='UTF-8', errors='strict')
print(text, "\n")
print(list(tokens))

Then, I implemented the merge, findig the pairs that occours the most and creating a new token, exchanging it in the main token list. The merge has to be stored, for further 'unmerging' at the decoding phase.
def get_stats(ids):
    pair_counts = {}
    
    for i in range(len(ids) - 1):
        pair = (ids[i], ids[i+1])
        
        if pair in pair_counts:
            pair_counts[pair] += 1
        else:
            pair_counts[pair] = 1
        
    return pair_counts

def merge(ids, pair, new_token):
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i+1]) == pair:
            new_ids.append(new_token)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids
            
stats = get_stats(tokens)

FREQUENCY_THRESHOLD = 4

merge_history = []

while stats:
    most_frequent_pair = max(stats, key=stats.get)
    
    highest_frequency = stats[most_frequent_pair]
    if highest_frequency < FREQUENCY_THRESHOLD:
        break
    
    new_token = max(tokens) + 1
    merge_history.append((new_token, most_frequent_pair))
    
    tokens = merge(tokens, most_frequent_pair, new_token) 
    stats = get_stats(tokens)

With that, the encoding phase is finished. The string: "Provérbios de Salomão, filho de Davi, rei de Israel. 2- Eles ajudarão a adquirir a sabedoria e a instrução; a compreender as palavras que dão entendimento;" turning into: [80, 114, 111, 118, 195, 169, 114, 98, 105, 111, 115, 197, 101, 32, 83, 97, 108, 111, 109, 199, 44, 32, 102, 105, 108, 104, 111, 197, 101, 32, 68, 97, 118, 105, 44, 32, 114, 101, 105, 197, 101, 32, 73, 115, 114, 97, 101, 108, 46, 32, 50, 45, 32, 69, 108, 101, 115, 196, 106, 117, 100, 97, 114, 199, 196, 196, 100, 113, 117, 105, 114, 105, 114, 196, 32, 115, 97, 98, 101, 100, 111, 114, 105, 97, 32, 101, 196, 32, 105, 110, 115, 116, 114, 117, 195, 167, 199, 59, 196, 32, 99, 111, 109, 112, 114, 101, 200, 100, 101, 114, 196, 115, 32, 112, 97, 108, 97, 118, 114, 97, 115, 32, 113, 117, 101, 197, 199, 32, 200, 116, 200, 100, 105, 109, 200, 116, 111, 59]

### **2️⃣ Decoding Phase** (Tokens ➡️ Text)
Now, implementing the decoding process, basically inverting the encoding
def decode(tokens, merge_history):
    for new_token, pair in reversed(merge_history):
        decoded_tokens = []
        i = 0
        while i < len(tokens):
            if tokens[i] == new_token:
                decoded_tokens.extend(pair)
            else:
                decoded_tokens.append(tokens[i])
            i += 1
        tokens = decoded_tokens
        
    return bytes(tokens).decode('UTF-8')

decoded_text = decode(tokens, merge_history)
print("\nDecoded Text:\n", decoded_text)

Turning: [80, 114, 111, 118, 195, 169, 114, 98, 105, 111, 115, 197, 101, 32, 83, 97, 108, 111, 109, 199, 44, 32, 102, 105, 108, 104, 111, 197, 101, 32, 68, 97, 118, 105, 44, 32, 114, 101, 105, 197, 101, 32, 73, 115, 114, 97, 101, 108, 46, 32, 50, 45, 32, 69, 108, 101, 115, 196, 106, 117, 100, 97, 114, 199, 196, 196, 100, 113, 117, 105, 114, 105, 114, 196, 32, 115, 97, 98, 101, 100, 111, 114, 105, 97, 32, 101, 196, 32, 105, 110, 115, 116, 114, 117, 195, 167, 199, 59, 196, 32, 99, 111, 109, 112, 114, 101, 200, 100, 101, 114, 196, 115, 32, 112, 97, 108, 97, 118, 114, 97, 115, 32, 113, 117, 101, 197, 199, 32, 200, 116, 200, 100, 105, 109, 200, 116, 111, 59] back to the raw string: "Provérbios de Salomão, filho de Davi, rei de Israel. 2- Eles ajudarão a adquirir a sabedoria e a instrução; a compreender as palavras que dão entendimento;"


📖 References
Byte Pair Encoding (BPE): [Paper](https://arxiv.org/abs/1508.07909)
Andrej Karpathy’s NLP videos: [YouTube](https://www.youtube.com/@AndrejKarpathy)