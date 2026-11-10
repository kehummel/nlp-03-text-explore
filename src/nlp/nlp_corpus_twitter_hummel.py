"""nlp_corpus_twitter_hummel.py - Module 3 Script.

Author: Kim Hummel
Date: 2026 November

This project used Denise Case's npl_corpus_explore.py as a template.

Purpose

  Perform exploratory analysis of a small, controlled text corpus.
  Demonstrate how structure emerges from token distributions,
  category comparisons, and co-occurrence patterns.

Analytical Questions

- What tokens dominate each category?
- How do categories differ in vocabulary?
- What words appear in similar contexts?
- What structure is visible before using any models?

Notes:
- This module focuses on exploratory analysis (EDA), not modeling.
- Results here prepare for later work with pipelines and embeddings.

Run from root project folder with:

  uv run python -m nlp.nlp_corpus_twitter_hummel
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

from collections import defaultdict
import logging
from pathlib import Path

from datafun_toolkit.logger import get_logger, log_header, log_path
import matplotlib.pyplot as plt
import polars as pl

print("Imports complete.")


# ============================================================
# Configure Logging
# ============================================================

LOG: logging.Logger = get_logger("CI", level="DEBUG")

ROOT_PATH: Path = Path.cwd()
SCRIPTS_PATH: Path = ROOT_PATH / "scripts"

log_header(LOG, "MODULE 3: CORPUS EXPLORATION")
LOG.info("START script.....")

log_path(LOG, "ROOT_PATH", ROOT_PATH)
log_path(LOG, "SCRIPTS_PATH", SCRIPTS_PATH)

LOG.info("Logger configured.")

# ============================================================
# Section 2. Define Corpus (Labeled Text Documents)
# ============================================================

# A corpus is a collection of documents.
# Each document includes a category and text.

corpus: list[dict[str, str]] = [
    # Tweets from England
    {
        "category": "England",
        "text": "2nd delivery of pfizer Covid19 vaccs potentially 1050 doses to be delivered in 72hours",
    },
    {
        "category": "England",
        "text": "Did no one in Govt check moving Pfizer second jab from 3 to 12 weeks prior to statement - no of course they didn't.",
    },
    {
        "category": "England",
        "text": "Great to help vaccinate some of the most vulnerable in our local community. Long way to go but the virus WILL be dead!",
    },
    {
        "category": "England",
        "text": "Becky and Alex today vaccinating at KGH today. Success day regardless of the snow. Proud of everybody that made it",
    },
    {
        "category": "England",
        "text": "Cheeky little booster today Counting myself lucky to have had the opportunity to not just have 1 or 2 but now",
    },
    {
        "category": "England",
        "text": "Last minute appointments are coming up now and then at Calderdale for staff to get their first covid vaccines.",
    },
    # Tweets from Canada
    {
        "category": "Canada",
        "text": "Study: adverse effects of the #PfizerBioNTech vaccine against #COVID19 are likely to be mild to moderate and clear",
    },
    {
        "category": "Canada",
        "text": "Why did @fordnation decide against bringing the #PfizerBioNTech vaccine directly into #LongTermCare homes",
    },
    {
        "category": "Canada",
        "text": "New: Canada expecting #PfizerBiontech to beef up deliveries in June by 5 million doses, bringing that month's ship",
    },
    {
        "category": "Canada",
        "text": "11 new #Covid19 deaths in #BC as the province also Friday announces 624 new cases. ",
    },
    {
        "category": "Canada",
        "text": "Now we know why Moderna CEO dumped his stock the day after their mRNA double shot vaccine was approved by FDA. ",
    },
    {
        "category": "Canada",
        "text": "With thousands of folks already signed up, don't miss the opportunity to join us tomorrow! Less than a day left",
    },
    # Tweets from India
    {
        "category": "India",
        "text": "Sonia Acevedo(41), a Portuguese nurse has died after two days of taking the Pfizer-BioTechs Corona Virus vaccine",
    },
    {
        "category": "India",
        "text": "The South African coronavirus variant is better at breaking through the Pfizer/BioNTech vaccine's defenses than",
    },
    {
        "category": "India",
        "text": "First shipment of Pfizer Covid-19 vaccine reaches France on Saturday. Vaccination of first dose begins on sunday.",
    },
    {
        "category": "India",
        "text": "#US States To Start Getting #PfizerBioNTech Covid-19 Vaccine From Monday",
    },
    {
        "category": "India",
        "text": "The World Health Organization has granted its first emergency use validation to #Biontech-Pfizer's #Covid_19_vaccine.",
    },
    {
        "category": "India",
        "text": "How #Israel launched the world's fastest #COVID19 vaccination drive",
    },
    # Tweets from South Africa
    {
        "category": "South Africa",
        "text": "Every single vaccination helps us reach population immunity, which helps individuals, communities and the country",
    },
    {
        "category": "South Africa",
        "text": "After the double espresso of no guns for self defense got people to ultimately distrust the @MYANC and the 2nd",
    },
    {
        "category": "South Africa",
        "text": "Unvaccinated people are 20 times more likely to die from Covid complications than those who have received the Pfizer",
    },
    {
        "category": "South Africa",
        "text": "MEDICAL SCIENTISTS ARE WINNING 'Pfizer data suggests COVID-19 shot protects against SA variant'",
    },
    {
        "category": "South Africa",
        "text": "vaccinated. More than 1.1 million new cases have been confirmed in the past week and the death toll is above 306,000",
    },
    {
        "category": "South Africa",
        "text": "Chile's President, @sebastianpinera has described the start of his country's national coronavirus immunization program",
    },
]

# Show results
print(f"Corpus contains {len(corpus)} documents.")


# ============================================================
# Section 3. Tokenize and Clean Text
# ============================================================

# Tokenization splits text into word-like units.

# Stop words are very common words that often add little meaning
# for simple frequency analysis.
STOP_WORDS: set[str] = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
}


# Define a function to tokenize text by lowercasing, splitting on whitespace,
# and stripping common punctuation. We also filter out very short tokens (length <= 2).
# This simple tokenizer is sufficient for our small, controlled corpus.
# Use the string strip() method to remove punctuation from the beginning and end of each token.
def tokenize(text: str) -> list[str]:
    """Tokenize the input text into a list of cleaned tokens."""
    tokens = [t.strip(".,:;!?()[]\"'@#-") for t in text.lower().split()]
    return [t for t in tokens if len(t) > 2 and t not in STOP_WORDS]


# Define a new empty list to hold the token records we will create.
records_list: list[dict[str, str]] = []

# Loop through each document, tokenize the text,
# and create a record for each token with its category and
# add it to our list of records.
for doc in corpus:
    # Call our function to tokenize the text of the current document.
    tokens = tokenize(doc["text"])
    # Loop through each token produced by the tokenizer and
    # create a record that includes the category of the document and the token itself.
    # Append this record to our list of records.
    for token in tokens:
        records_list.append({"category": doc["category"], "token": token})

# Create a Polars DataFrame from the list of token records for easier analysis.
token_df: pl.DataFrame = pl.DataFrame(records_list)

# Show results
print("Tokenization complete.")
print(token_df.head(10))

# ============================================================
# Section 4. Compute Global Token Frequencies
# ============================================================

# Frequency distribution = how often each token appears.

# Create a DataFrame that groups the tokens by their text and
# counts how many times each token appears across the entire corpus.
global_freq_df: pl.DataFrame = (
    token_df.group_by("token").len().sort("len", descending=True)
)

# Show results
print("Top global tokens:")
print(global_freq_df.head(10))


# ============================================================
# Section 5. Compute Token Frequencies by Category
# ============================================================

# Compare token usage across categories.

# Create a new DataFrame that groups the tokens by both their category and text,
# counts how many times each token appears within each category,
# and sorts the results first by category and then by frequency in descending order.
# This shows which tokens are most common within each category.
category_freq_df: pl.DataFrame = (
    token_df.group_by(["category", "token"])
    .len()
    .sort(["category", "len"], descending=True)
)

# Show results
print("Top tokens by category:")
print(category_freq_df.head(3))


# ============================================================
# Section 6. Identify Top Tokens per Category
# ============================================================

# Show top tokens per category.


# Define a new empty dictionary to store the top tokens for each category.
top_per_category_dict: dict[str, list[str]] = {}

# Loop through each unique category in the token DataFrame,
# filter the category frequency DataFrame to get the top 5 tokens for that category,
# and store the list of top tokens in the dictionary.
# Also, print the top tokens for each category.
for category in token_df["category"].unique().to_list():
    subset_df = category_freq_df.filter(pl.col("category") == category).head(5)
    top_tokens_list = subset_df["token"].to_list()
    top_per_category_dict[category] = top_tokens_list

    # Show results for this category
    print(f"{category.upper()} top tokens: {top_tokens_list}")


# ============================================================
# Section 7. Analyze Co-occurrence (Context Windows)
# ============================================================

# Co-occurrence examines which tokens appear near each other.

# Define how many tokens on each side of a target token we include as context.
# A window size of 2 means:
#   - up to 2 tokens before the target token
#   - up to 2 tokens after the target token
# The target token itself is not included in its context list.
WINDOW_SIZE: int = 2

#  Define a new empty dictionary to store the co-occurrence information.
# The keys will be target tokens,
# and the values will be lists of context tokens that appear near the target token.
co_occurrence_dict: dict[str, list[str]] = defaultdict(list)

# Loop through each document in the corpus, tokenize the text,
# and for each token, determine its context tokens based on the defined window size.
for doc in corpus:
    tokens = tokenize(doc["text"])
    for i, token in enumerate(tokens):
        start = max(0, i - WINDOW_SIZE)
        end = min(len(tokens), i + WINDOW_SIZE + 1)
        context = tokens[start:end]
        for ctx in context:
            if ctx != token:
                co_occurrence_dict[token].append(ctx)

# Show results
for target in ["vaccine", "pfizer", "covid19", "pfizerbiontech"]:
    print(f"\nContext for '{target}':")
    print(co_occurrence_dict[target][:10])

# ============================================================
# Section 8. Create Bigrams (Local Word Pairs) and Compute Frequencies
# ============================================================

# Bigrams combine each word with the next word in the text.
# This helps us capture local structure: how words are used together,
# not just which words appear individually.

# Bigrams capture pairs of consecutive tokens.

# Define a new empty list to hold the bigram tuples we will create.
bigrams_list: list[tuple[str, str]] = []

# Loop through each document in the corpus, tokenize the text,
# and create bigrams by pairing each token with the next token in the list.
for doc in corpus:
    tokens = tokenize(doc["text"])
    for i in range(len(tokens) - 1):
        bigrams_list.append((tokens[i], tokens[i + 1]))

# Create a DataFrame from the list of bigram tuples,
# where each bigram is represented as a single string with the two tokens separated by a space.
bigram_df: pl.DataFrame = pl.DataFrame(
    {"bigram": [f"{a} {b}" for a, b in bigrams_list]}
)

# Create a new DataFrame that groups the bigrams by their text
# and counts how many times each bigram appears,
# then sorts the results by frequency in descending order.
bigram_freq_df: pl.DataFrame = (
    bigram_df.group_by("bigram").len().sort("len", descending=True)
)

# Show results
print("Top bigrams:")
print(bigram_freq_df.head(10))


# ============================================================
# Section 9. Visualize Token Frequencies
# ============================================================

print("IMPORTANT: Close chart window to continue execution.")

# Define a new DataFrame that filters the category frequency DataFrame
# to get the top 5 tokens for the "Canada" category.
canada_df = category_freq_df.filter(pl.col("category") == "Canada").head(5)

# Create a figure that is 8 inches wide and 4 inches tall
plt.figure(figsize=(8, 4))

# Add a bar chart to the figure using the tokens as the x-axis and their frequencies as the y-axis.
plt.bar(canada_df["token"], canada_df["len"])

# Define the x-axis tick parameters to rotate the labels by 45 degrees for better readability.
# The gca() function gets the current axes of the plot, and tick_params() is used to set the rotation of the x-axis labels.
ax = plt.gca()
ax.tick_params(axis="x", labelrotation=45)

# Set the title and labels for the axes of the plot.
plt.title("Case Example: Top Tokens (Canada Category)\n(Close this window to continue)")
plt.xlabel("Token")
plt.ylabel("Frequency")

# Adjust the layout of the plot to prevent overlap and ensure everything fits well.
plt.tight_layout()

# Display the plot on the screen.
# The execution of the script will pause until the plot window is closed.
plt.show()

# to get the top 5 tokens for the "England" category.
england_df = category_freq_df.filter(pl.col("category") == "England").head(5)

# Create a figure that is 8 inches wide and 4 inches tall
plt.figure(figsize=(8, 4))

# Add a bar chart to the figure using the tokens as the x-axis and their frequencies as the y-axis.
plt.bar(england_df["token"], england_df["len"])

# Define the x-axis tick parameters to rotate the labels by 45 degrees for better readability.
# The gca() function gets the current axes of the plot, and tick_params() is used to set the rotation of the x-axis labels.
ax = plt.gca()
ax.tick_params(axis="x", labelrotation=45)

# Set the title and labels for the axes of the plot.
plt.title(
    "Case Example: Top Tokens (England Category)\n(Close this window to continue)"
)
plt.xlabel("Token")
plt.ylabel("Frequency")

# Adjust the layout of the plot to prevent overlap and ensure everything fits well.
plt.tight_layout()

# Display the plot on the screen.
# The execution of the script will pause until the plot window is closed.
plt.show()

# to get the top 5 tokens for the "India" category.
india_df = category_freq_df.filter(pl.col("category") == "India").head(5)

# Create a figure that is 8 inches wide and 4 inches tall
plt.figure(figsize=(8, 4))

# Add a bar chart to the figure using the tokens as the x-axis and their frequencies as the y-axis.
plt.bar(india_df["token"], india_df["len"])

# Define the x-axis tick parameters to rotate the labels by 45 degrees for better readability.
# The gca() function gets the current axes of the plot, and tick_params() is used to set the rotation of the x-axis labels.
ax = plt.gca()
ax.tick_params(axis="x", labelrotation=45)

# Set the title and labels for the axes of the plot.
plt.title("Case Example: Top Tokens (India Category)\n(Close this window to continue)")
plt.xlabel("Token")
plt.ylabel("Frequency")

# Adjust the layout of the plot to prevent overlap and ensure everything fits well.
plt.tight_layout()

# Display the plot on the screen.
# The execution of the script will pause until the plot window is closed.
plt.show()

# to get the top 5 tokens for the "South Africa" category.
southafrica_df = category_freq_df.filter(pl.col("category") == "South Africa").head(5)

# Create a figure that is 8 inches wide and 4 inches tall
plt.figure(figsize=(8, 4))

# Add a bar chart to the figure using the tokens as the x-axis and their frequencies as the y-axis.
plt.bar(southafrica_df["token"], southafrica_df["len"])

# Define the x-axis tick parameters to rotate the labels by 45 degrees for better readability.
# The gca() function gets the current axes of the plot, and tick_params() is used to set the rotation of the x-axis labels.
ax = plt.gca()
ax.tick_params(axis="x", labelrotation=45)

# Set the title and labels for the axes of the plot.
plt.title(
    "Case Example: Top Tokens (South Africa Category)\n(Close this window to continue)"
)
plt.xlabel("Token")
plt.ylabel("Frequency")

# Adjust the layout of the plot to prevent overlap and ensure everything fits well.
plt.tight_layout()

# Display the plot on the screen.
# The execution of the script will pause until the plot window is closed.
plt.show()
# ============================================================
# Section 10. Interpret Results and Identify Patterns
# ============================================================

print("\nCASE GENERAL OBSERVATIONS:")

print("- Tokens cluster by category (Canada, England, India, South Africa).")
print("- Words that appear in similar contexts behave similarly.")
print("- Co-occurrence reveals contextual relationships between words.")
print("- Bigrams capture local structure beyond single tokens.")
print("- Patterns emerge before any machine learning is applied.")

print("\nYOURNAME SPECIFIC OBSERVATIONS:")
print("TODO")


# ============================================================
# END
# ============================================================

LOG.info("========================")
LOG.info("Pipeline executed successfully!")
LOG.info("========================")
LOG.info("END main()")
