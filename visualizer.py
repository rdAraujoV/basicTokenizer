from app import tokenizer_vocab, tokens

decoded_vocab = ''.join(
    chr(byte) if isinstance(byte, int) and byte < 256 else str(byte)
    for byte in tokenizer_vocab.keys()
)

vocab_output = []
for token in tokens:
    if token in tokenizer_vocab:
        vocab_output.append(f"{token} = \"{tokenizer_vocab[token]}\"")

print("[" + ", ".join(vocab_output) + "]")