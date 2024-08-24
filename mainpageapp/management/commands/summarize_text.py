from transformers import pipeline

# Function to split text into chunks
def chunk_text(text, chunk_size):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

# Open and read the article
with open(r"D:\projects(personal)\INFomatics\INFomatics\mainpageapp\management\commands\article.txt", "r", encoding="utf8") as f:
    to_tokenize = f.read()

# Initialize the HuggingFace summarization pipeline
summarizer = pipeline("summarization")

# Define chunk size (based on the model's maximum token length, typically less to avoid issues)
chunk_size = 800

# Summarize each chunk and combine the results
summarized_text = []
for chunk in chunk_text(to_tokenize, chunk_size):
    summarized_chunk = summarizer(chunk, min_length=75, max_length=100)
    summarized_text.append(summarized_chunk[0]['summary_text'])

# Combine summarized chunks into one text
final_summary = ' '.join(summarized_text)

# Print summarized text
print(final_summary)
