# Phases 4 & 5 Markdown File

Phase 4 asks for a modification on the example file, and Phase 5 asks for a custom application of the skills learned in this module.
That will be documented here. It is linked in both the project README.md file and the index.md file in the docs folder.

## Phase 4: Technical Modification

For my technical modification I increased the size of the corpus by making each category have four documents, or lines of text. Each sentence had either the category or a synonym for the category in it.

With the added text, the top tokens changed for the majority of the categories with the exception of the CAT category. Only one word changed while in the other categories the order of the words changed if not the word themselves. However, "the" stayed as the top token in all four categories.

Original Top Tokens

![Original Top Tokens](/docs/images/top_tokens.png)

Phase 4 Top Tokens

![Phase 4 Top Tokens](/docs/images/p4_top_tokens.png)

The words in the top global tokens changed, again with the exception of the word "the" staying at the top.

Top 10 Global Tokens

![Top Global Tokens](/docs/images/global_tokens.png)

Phase 4 Top 10 Global Tokens

![Phase 4 Top 10 Global Tokens](/docs/images/p4_global_tokens.png)

The top bigrams moved around in the top 10, but most of them stayed in the top 10.

Top 10 Bigrams

![Top 10 Bigrams](/docs/images/bigram.png)

Phase 4 Top Bigrams

![Phase 4 Top Bigrams](/docs/images/p4_bigram.png)

The number of co-occurrences increased, which makes sense since there were more occurrences of the category since I added more documents to the corpus.

Co-Occurrences

![Co-Occurrences](/docs/images/context.png)

Phase 4 Co-Occurrences

![Phase 4 Co-Occurrences](/docs/images/p4_context.png)

## Phase 5: Custom Application

### Choosing Data

I knew for my custom application that I wanted to change the dataset completely, so that was what I figured out first. I looked through dataset of social media posts and found one consisting of twitter (currently called X) posts about the Pfizer covid vaccine. I chose this dataset because I could easily put it into categories based on the user location. I chose 4 locations varied throughout the world; England, India, Canada, and South Africa. I then picked 6 tweets from each country. I tried to vary them from different locations in the spreadsheet and ones that didn't have too many special characters in it. This was not a very scientific process but since I don't know how to upload it as a file that was what I went with.

Original Data Source: https://www.kaggle.com/datasets/gpreda/pfizer-vaccine-tweets

### Cleaning the Text

When considering how to clean the text I made sure # and @ were in the special characters to be removed as these are common in tweets but do not hold any significance for the meaning of the tweet itself. I later added - to the list as it was used frequently in covid-19.

I initially left all of the other configurations from the example the same, changing the categories as needed in order to get the correct outputs for this dataset. However, when I did that "the" was the top token in the Canada category. I didn't want stop words in my data so I added that in as a part of the cleaning process.

Initial Frequency of Tokens

![Initial Frequency of Tokens](/docs/images/canada_first_try.png)

Frequency of Tokens after removing stop words.

![Removing Stop Words](/docs/images/canada_stop_words.png)

### TroubleShooting

When I ran it, the output of the context for was blank.

![blank output](/docs/images/context_blank.png)

I used AI to help me fix it, which wound up being very helpful as I didn't actually understand what it was doing, which is why I made a mistake. Because I just looked at the code and not the notes as closely as I should have I thought section 7 was calling the categories, not the tokens themselves. Therefore, my targets should be tokens dealing with covid-19 or the vaccines, not the names of the categories. As suggested by AI, I looked back at the top global tokens and picked "vaccine", "pfizer", "covid19", and "pfizerbiotech".

![context correct](/docs/images/context_twitter.png)

Since I uploaded the whole file to AI, it also showed me that the order I cleaned and tokenized the text should be switched. I needed to strip special characters and make all text lowercase before removing the stop words so that everything was caught correctly.

### Results

Lastly, I created graphs of the top 5 tokens for each category instead of just for Canada.

![Canada top 5 tokens](/docs/images/canada_top_5.png)

![England top 5 tokens](/docs/images/england_top_5.png)

![India top 5 tokens](/docs/images/india_top_5.png)

![South Africa top 5 tokens](/docs/images/southafrica_top_5.png)

Also worth looking at to analyze is the context, or words around the top 3 tokens, and the top bigrams.

![context correct](/docs/images/context_twitter.png)

![top bigrams](/docs/images/top_bigrams.png)

hen what does it mean - screen shots of results and answer questions from the top of the doucment about the purpose of this project.
