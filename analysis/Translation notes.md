# Deepchecks

Calculates metadata automatically

- text length
- average word length
- max word length
- % special characters
- % punctuation
- language
- average words per sentence
- lexical density (proportion of N/V/AdV/AdJ to rest of text or percentage of unique words in the text, higher means more compelx)

and some metrics with models (didnt work for me)

- reading ease (with model)
- sentiment (with model)
- subjectivity (with model)
- toxicity (with model)
- fluencey (with model)
- formality (with model)
- unique nouns (with model)

Then runs heurisic checks based on these rules, like

1. Outlier ratio for each property is < than 5%

Inights found

- Helps find things like short words with lots of punctuation
- very long inputs and outputs
- degnerate inputs and outputs kind of -- low lexical density and lots of special characters
- duplicates -- exact matches

# Improvements

- They dont do a good job of linking to the raw data so I can contextualize a metric
- These metrics are useful guideposts to find weird points (positive feedback)

Research angle

- How does interactive system people help people reason with outliers across these different dimensions?
- Do people primarily use heuristics or just full outlier methods
