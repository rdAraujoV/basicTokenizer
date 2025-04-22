import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.classes import DatasetLoader, BPETokenizer
import matplotlib.pyplot as plt

def evaluate_tokenizer(path, merge_range, sample_limit=5000):
    loader = DatasetLoader(path)
    text = loader.get_text()

    # Limit the evaluation to a sample if needed
    words = text.split()
    if len(words) > sample_limit:
        words = words[:sample_limit]
    eval_text = ' '.join(words)

    results = []

    for num_merges in merge_range:
        tokenizer = BPETokenizer(eval_text, num_merges=num_merges)
        tokenizer.build_initial_vocab()
        tokenizer.apply_whitespace_merges()
        tokens, _, _ = tokenizer.run_merges()

        token_count = len(tokens)
        word_count = len(eval_text.split())

        avg_tokens_per_word = token_count / word_count
        vocab_size = len(tokenizer.vocab)

        results.append((num_merges, avg_tokens_per_word, vocab_size))
        print(f"Merges: {num_merges:5d} | Avg tokens/word: {avg_tokens_per_word:.3f} | Vocab size: {vocab_size}")

    return results

def plot_results(results):
    merges = [r[0] for r in results]
    avg_tokens = [r[1] for r in results]
    vocab_sizes = [r[2] for r in results]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel("Number of Merges")
    ax1.set_ylabel("Avg Tokens per Word", color="tab:blue")
    ax1.plot(merges, avg_tokens, color="tab:blue", label="Avg Tokens/Word")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Vocab Size", color="tab:red")
    ax2.plot(merges, vocab_sizes, color="tab:red", label="Vocab Size")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    fig.tight_layout()
    plt.title("Merge Impact on Tokenization")
    plt.show()
    
path = r"C:\Users\rodri\OneDrive\Documents\Coding Projects\tokenizer\basicTokenizer\datasets\trainingSet.txt"
results = evaluate_tokenizer(path, merge_range=range(0, 2000, 50))
plot_results(results)
