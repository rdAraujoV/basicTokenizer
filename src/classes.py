import json
import re
from string import punctuation
import unicodedata

class DatasetLoader:
    
    def __init__(self, path):
        self.path = path
        self.text = self._load_text()

    def _load_text(self):
        with open(self.path, "r", encoding="utf-8") as file:
            return file.read()

    def clean_text(self):
        text = self.text

        # 1) Normalize to NFC so accents are single code‑points (keeps é, ñ, etc.)
        text = unicodedata.normalize('NFC', text)

        # 2) Drop control chars (except newline/tab)
        text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

        # 3) Whitelist Latin letters, combining marks, digits, punctuation, whitespace
        def keep_char(c):
            cat = unicodedata.category(c)
            # Letters: must be Latin
            if cat.startswith('L'):
                # e.g. 'LATIN SMALL LETTER E', 'GREEK …' will be rejected
                return 'LATIN' in unicodedata.name(c, '')
            # Combining accents/marks
            if cat.startswith('M'):
                return True
            # Numbers
            if cat.startswith('N'):
                return True
            # Punctuation
            if cat.startswith('P'):
                return True
            # Whitespace (spaces, tabs, newlines)
            if c.isspace():
                return True
            return False

        cleaned = ''.join(c for c in text if keep_char(c))

        # 4) Collapse multiple spaces/newlines
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

        self.text = cleaned

    def get_text(self):
        return self.text
    
    def save_text(self, text):
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(text)

class BPETokenizer:
    
    def __init__(self, text, num_merges=10):
        self.text = text
        self.num_merges = num_merges
        self.tokens = list(text)
        self.vocab = {}
        self.merge_history = []
        self.max_id = 0
    
    def build_initial_vocab(self):
        tokens = list(self.text)
        self.tokens = tokens
        self.vocab = {str(i): char for i, char in enumerate(sorted(set(tokens)))}
        self.max_id = len(self.vocab) - 1
    
    def apply_whitespace_merges(self):
        merged_tokens = []
        i = 0
        while i < len(self.tokens):
            if self.tokens[i] == ' ' and i + 1 < len(self.tokens):
                merged_tokens.append(self.tokens[i] + self.tokens[i + 1])
                i += 2
            else:
                merged_tokens.append(self.tokens[i])
                i += 1
        self.tokens = merged_tokens
            
    def get_stats(self, tokens):
        pair_counts = {}
    
        for i in range(len(tokens) - 1):
            pair = (tokens[i], tokens[i+1])
            if pair in pair_counts:
                pair_counts[pair] += 1
            else:
                pair_counts[pair] = 1
            
        return pair_counts
    
    def is_punctuation(self, token):
        return all(unicodedata.category(char).startswith('P') for char in token)
    def is_merge_allowed(self, pair):
        a, b = pair
        allowed_punct_pairs = {('!', '!'), ('.', '.'), ('?', '!')}
        
        # Whitespace + whitespace
        if a.isspace() and b.isspace():
            return False

        # Punctuation atomic
        if (a in punctuation or b in punctuation) and (a, b) not in allowed_punct_pairs:
            return False
        
        if self.is_punctuation(a) or self.is_punctuation(b):
            return False

        # Newline merges
        if '\n' in a or '\n' in b:
            return False

        # Digit + letter
        if (a[-1].isdigit() and b[0].isalpha()) or (a[-1].isalpha() and b[0].isdigit()):
            return False
        
        # Whitespace between letters or digits
        if a[-1].isalnum() and b[0].isspace():
            return False
        if a[-1].isspace() and b[0].isalnum():
            return False    
        
        # letter or digit + whitespace (word end)
        if a.endswith(" ") or b.startswith(" "):
            return False
        
        return True
        
    def merge_pair(self, tokens, pair):
        merged = []
        i = 0
        while i < len(tokens) - 1:
            if (tokens[i], tokens[i + 1]) == pair:
                merged.append(tokens[i] + tokens[i + 1])
                i += 2
            else:
                merged.append(tokens[i])
                i += 1
        if i == len(tokens) - 1:
            merged.append(tokens[-1])
        return merged
    
    def run_merges(self):
        merges = []
        tokens = self.tokens
        
        for _ in range(self.num_merges):
            stats = self.get_stats(tokens)
            stats = {pair: count for pair, count in stats.items() if self.is_merge_allowed(pair)}    
            if not stats:
                break
            
            most_common = max(stats.items(), key=lambda x: x[1])[0] 
            new_token = most_common[0] + most_common[1]
            
            self.max_id += 1
            self.vocab[str(self.max_id)] = new_token
            
            tokens = self.merge_pair(tokens, most_common)
            merges.append(most_common)
        self.tokens = tokens
        self.merge_history = merges
        return tokens, self.vocab, merges
    
    def save_vocab(self, vocab_path):
        with open(vocab_path, "w", encoding="utf-8") as file:
            json.dump(self.vocab, file, ensure_ascii=False, indent=2)
            
    def save_merges(self, merge_path):
        with open(merge_path, "w", encoding="utf-8") as file:
            json.dump(self.merge_history, file, ensure_ascii=False, indent=2)