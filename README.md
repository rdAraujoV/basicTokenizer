Basic BPE Tokenizer

📌 Overview

This project is a Byte Pair Encoding (BPE) Tokenizer, inspired by Andrej Karpathy’s NLP videos, implemented in pure Python.

A tokenizer is a crucial component in Natural Language Processing (NLP) that converts human-readable text into machine-readable tokens (integers). BPE is widely used in state-of-the-art NLP models (e.g., GPT, BERT) to create efficient subword representations.

🔍 Features

Byte Pair Encoding (BPE) Tokenization for efficient text segmentation.

Custom handling of UTF-8 multibyte characters (accents, punctuation, special symbols).

Encoding & Decoding for reversible text processing.

Visualization support to see token mappings.

🛠️ Implementation Details

1️⃣ Tokenization Process

Preprocessing: Convert text into UTF-8 byte representations.

Multibyte Character Merging:

Since UTF-8 encodes some characters using multiple bytes (e.g., é, ã, ç), this phase pre-emptively merges them into single tokens.

Byte Pair Encoding (BPE) Merging:

Identify the most frequent adjacent byte pairs.

Merge them into a new token.

Repeat until a stopping criterion is met (e.g., frequency threshold).

Final Tokenization Output: A list of token IDs representing the input text.

2️⃣ Decoding Process

Reverses the encoding by mapping token IDs back to their original characters.

🚀 Improvements & Fixes

🔹 Handling UTF-8 Multibyte Characters

The first version of this tokenizer struggled with accents and punctuation because UTF-8 represents some characters using multiple bytes. This caused incorrect token merges.

✅ Solution: Implemented a pre-merge phase to detect and merge multibyte characters before applying BPE, ensuring correct tokenization for languages like Portuguese.

🧠 References & Learning Resources

Byte Pair Encoding (BPE) Paper: https://arxiv.org/abs/1508.07909

Andrej Karpathy’s NLP Videos: https://www.youtube.com/@AndrejKarpathyYouTube

Hugging Face Tokenizers: https://github.com/huggingfaceGitHub

📌 Future Improvements

Optimize merging strategy to further improve efficiency.

Implement vocabulary size control for dynamic tokenization.

Add subword sampling for better generalization.