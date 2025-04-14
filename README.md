The idea is to create a simple tokenizer for Portuguese Language.

# First step, create a char-level tokenizer
- The data is a bunch of Wikipedia pages in Portuguese.
- It’s encoded in bytes with UTF-8.
  - This causes problems with multi-byte characters; some chars, like `é`, are encoded as multiple bytes.
- Instead of single-byte tokenization for the vocab, I’ll use individual Unicode tokenization.
- This way, I can visualize tokens I won’t need, such as `↑`, and clean the dataset for better tokenization.
- First step concluded, achieving a vocab size of 124.
  ### Analysis of the Vocabulary
  #### Character Categories:
  - **Whitespace**: `\t` (tab), `\n` (newline), ` ` (space).
  - **Punctuation**: `!`, `"`, `#`, `$`, `%`, `&`, `'`, `(`, `)`, `*`, `,`, `-`, `.`, `/`, `:`, `;`, `?`, `@`, `[`, `]`, `` ` ``, `–`, `—`, `‘`, `’`, `“`, `”`.
  - **Digits**: `0–9`.
  - **Letters**:
    - Uppercase ASCII: `A–Z`.
    - Lowercase ASCII: `a–z`.
    - Accented/special letters: `ª`, `À`, `Á`, `Ã`, `Å`, `Æ`, `É`, `Í`, `Ö`, `Ú`, `à`, `á`, `â`, `ã`, `ä`, `å`, `ç`, `é`, `ê`, `í`, `ñ`, `ó`, `ô`, `õ`, `ö`, `ú`, `ü`, `ÿ`.
  - **Symbols**: `°` (degree), `²` (superscript two), `´` (acute accent), `º` (masculine ordinal).

With that, the 124 tokens will be stored in the vocab file.
# Second step, BPE pair merging
- First, we map all the common token pairs on the data.
- Now, we need to merge those pairs to become a new token.
  - I'll do a fine-tunning merge. Starting with the pairs that starts with a whitespace (currently refers to the token: 2). So we can have pairs that indicates a start of a word.
# The vocab file
It’s where every token is stored.