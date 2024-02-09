import spacy
from spacy.matcher import Matcher
import patterns

# NLP and Matcher object
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

# Define pattern class with corresponding patterns
matcher.add("nagging", patterns.patterns_nagging)
# matcher.add("forced_continuity", patterns.patterns_forced_continuity)
# matcher.add("roach_motel", patterns.patterns_roach_motel)
# matcher.add("price_comparison_prevention", patterns.patterns_price_comparison_prevention)
# matcher.add("intermediate_currency", patterns.patterns_intermediate_currency)
# matcher.add("privacy_zuckering", patterns.patterns_privacy_zuckering)
# matcher.add("social_pyramid", patterns.patterns_social_pyramid)
matcher.add("gamification", patterns.patterns_gamification)
# matcher.add("forced_enrollment", patterns.patterns_forced_enrollment)
matcher.add("default_choice", patterns.patterns_default_choice)
matcher.add("attention_distraction", patterns.patterns_attention_distraction)
matcher.add("disguised_ads", patterns.patterns_disguised_ads)
# matcher.add("friend_spam", patterns.patterns_friend_spam)
matcher.add("countdown_timer", patterns.patterns_countdown_timer)
matcher.add("limited_time_message", patterns.patterns_limited_time_message)
matcher.add("low_stock_message", patterns.patterns_low_stock_message)
matcher.add("high_demand_message", patterns.patterns_high_demand_message)
matcher.add("activity_message", patterns.patterns_activity_message)

# match patterns
def is_dark(text):
    doc = nlp(text)
    matches = matcher(doc)
    if matches:
        pattern= nlp.vocab.strings[matches[0][0]]
        print("text\n", text)
        print("pattern", pattern)
        return pattern
    return False