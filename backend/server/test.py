import spacy
from spacy.matcher import Matcher
from spacy.lang.en.stop_words import STOP_WORDS

# NLP and Matcher object
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
STOP_WORDS.remove("five")

print("while" in STOP_WORDS)

def preprocess_text(text):
    doc = nlp(text)
    # Remove punctuation and stop words
    tokens = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in STOP_WORDS]
    return " ".join(tokens)

# Define pattern class with corresponding patterns
# pattern8_countdown_timer = [
#     {"POS": "NUM", "OP": "?"},
#     {"LOWER": {"IN": ["hrs", "mins", "secs", "hours", "minutes", "seconds", "hr", "min", "sec"]}},
#     {"LOWER": {"IN": [":"]}},
#     {"POS": "NUM", "OP": "?"},
#     {"LOWER": {"IN": ["hrs", "mins", "secs", "hours", "minutes", "seconds", "hr", "min", "sec"]}},
#     {"LOWER": {"IN": [":"]}},
#     {"POS": "NUM", "OP": "?"},
#     {"LOWER": {"IN": ["hrs", "mins", "secs", "hours", "minutes", "seconds", "hr", "min", "sec"]}}
# ]

pattern1_nagging = [
    {"POS": "VERB", "OP":"?"},
    {"LEMMA": {"IN": ["rate", "upvote", "subscribe", "install"]}, "OP": "+"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["us", "app", "now", "image", "picture", "video", "feature", "product", "discount"]}, "OP": "+"},
    {"LOWER": {"IN": ["now", "continue", "discount"]}, "OP": "?"}
]
matcher.add("pattern8_countdown_timer", [pattern1_nagging])

# on match event handler
def on_match(doc, match_id, start, end, text_segment, segments):
    id = text_segment["id"] # segment id`
    pattern = nlp.vocab.strings[match_id]  # pattern match ID
    span = doc[start:end]  # matched span
    print(span.text)

text= "apple macbook air laptopmerchant video"

text= preprocess_text(text)
print(text)
# match patterns
doc = nlp(text)
matches = matcher(doc)
for match_id, start, end in matches:
    pattern = nlp.vocab.strings[match_id]  # pattern match ID
    span = doc[start:end]  # matched span
    print("doc.text", doc.text)
    print("span.text", span.text)

