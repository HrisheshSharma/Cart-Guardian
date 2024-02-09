import spacy
from spacy.matcher import Matcher
from spacy.lang.en.stop_words import STOP_WORDS
import patterns

# NLP and Matcher object
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
exclude_from_stop_words= ["please", "give", "us", "call", "five"]
for word in exclude_from_stop_words:
    STOP_WORDS.remove(word)

# Define pattern class with corresponding patterns
matcher.add("nagging", patterns.patterns_nagging)
matcher.add("bait_and_switch", patterns.patterns_bait_and_switch)
matcher.add("roach_motel", patterns.patterns_roach_motel)
matcher.add("intermediate_currency", patterns.patterns_intermediate_currency)
matcher.add("privacy_zuckering", patterns.patterns_privacy_zuckering)
matcher.add("forced_enrollment", patterns.patterns_forced_enrollment)
# matcher.add("false_heirarchy", patterns.patterns_false_hierarchy)
matcher.add("default_choice", patterns.patterns_default_choice)
matcher.add("countdown_timer", patterns.patterns_countdown_timer)
matcher.add("limited_time_message", patterns.patterns_limited_time_message)
matcher.add("low_stock_message", patterns.patterns_low_stock_message)
matcher.add("high_demand_message", patterns.patterns_high_demand_message)
matcher.add("activity_message", patterns.patterns_activity_message)

def preprocess_text(text):
    doc = nlp(text)
    # Remove punctuation and stop words
    tokens = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in STOP_WORDS]
    return " ".join(tokens)

# match patterns
def is_dark(text):
    text= preprocess_text(text)
    doc = nlp(text)
    matches = matcher(doc)
    if matches:
        pattern= nlp.vocab.strings[matches[0][0]]
        print("text\n", text)
        print("pattern", pattern)
        return pattern
    return False