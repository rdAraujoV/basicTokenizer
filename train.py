from classes import DatasetLoader, BPETokenizer

loader = DatasetLoader(r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\datasets\trainingSet.txt")
text = loader.get_text()
loader.save_text(text)

tokenizer = BPETokenizer(text, num_merges=1000)
tokenizer.build_initial_vocab()
tokenizer.apply_whitespace_merges()
tokens, vocab, merges = tokenizer.run_merges()

tokenizer.save_vocab(r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\vocab.json")
tokenizer.save_merges(r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\merges.json")