# Basic BPE Tokenizer  

This project is a **simple tokenizer** based on **Byte Pair Encoding (BPE)**, inspired by Andrej Karpathy’s videos, implemented in **raw Python**.

The idea behind a tokenizer is to **convert human-readable text into tokens** (integers) to make it **machine-readable**.
- BPE is widely used in NLP (e.g., GPT models) to efficiently represent words as subword units.  
- This implementation **encodes** and **decodes** text using BPE, demonstrating how frequent byte pairs are merged into new tokens.

The first version works well, but when I implemented the visualizer, where I could see what each token means after merge, ponctuation and accent became a issue. Since UTF-8 had more than one byte for those chars, my code couldn't handle it. So I had two options:
1.  Use a larger string, and map all the chars, creating a new vocabulary, exchanging the use of UTF-8. This would be really efficient and optimized for Portuguese language, but it would limit the tokenizer based on the training string.

2. Create special treatment for accents and punctuations, treating UTF-8.

For the second version of the code, I decided to implement the first option, since the tokenizer is specific for Portuguese language.


📖 References
Byte Pair Encoding (BPE): [Paper](https://arxiv.org/abs/1508.07909)
Andrej Karpathy’s NLP videos: [YouTube](https://www.youtube.com/@AndrejKarpathy)
