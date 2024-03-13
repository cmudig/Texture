const code_empty = `import pandas as pd

# Note: function must be called transform!
def transform(col: pd.Series) -> pd.Series:
  pass
`;

const code_str_len = `import pandas as pd

# length (in characters)
def transform(col: pd.Series):
  return col.str.len()
`;

const code_str_words = `import pandas as pd

# number of words
def transform(col: pd.Series):
  return col.str.split().str.len()
`;

const code_str_special_chars = `import pandas as pd

# percentage of special characters in the string
def transform(col: pd.Series):
  return col.apply(get_special_char_percentage)

import string
def get_special_char_percentage(s: str):
  special_chars = set(string.punctuation)
  num_special_chars = sum(1 for c in s if c in special_chars)
  return num_special_chars / len(s)
`;

const code_max_word_len = `import pandas as pd

def transform(col: pd.Series):
  return col.apply(get_max_word_len)

def get_max_word_len(s: str):
  return max([len(w) for w in s.split()])
`;

const code_avg_word_len = `import pandas as pd

def transform(col: pd.Series):
  return col.apply(get_avg_word_len)

def get_avg_word_len(s: str):
  return sum([len(w) for w in s.split()]) / len(s.split())
`;

export const sampleTransforms = {
  Empty: {
    code: code_empty,
    schema: { name: "", type: "number", num_replies: "single" },
  },
  "Number of characters": {
    code: code_str_len,
    schema: { name: "num_characters", type: "number", num_replies: "single" },
  },

  "Number of words": {
    code: code_str_words,
    schema: { name: "num_words", type: "number", num_replies: "single" },
  },
  "% special characters": {
    code: code_str_special_chars,
    schema: { name: "perc_special", type: "number", num_replies: "single" },
  },
  "Max word length": {
    code: code_max_word_len,
    schema: { name: "max_word_len", type: "number", num_replies: "single" },
  },
  "Average word length": {
    code: code_avg_word_len,
    schema: { name: "avg_word_len", type: "number", num_replies: "single" },
  },
};
