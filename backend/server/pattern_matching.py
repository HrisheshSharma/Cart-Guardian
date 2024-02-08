import spacy
from spacy.matcher import Matcher
import json

import patterns

import pprint
pp = pprint.PrettyPrinter()

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

# on match event handler
def on_match(doc, match_id, start, end, text_segment, segments):
    id = text_segment["id"] # segment id`
    # segment_info = text_segment # segment info
    pattern = nlp.vocab.strings[match_id]  # pattern match ID
    span = doc[start:end]  # matched span
    # print(span.text)

    # update segments object
    if str(id) not in segments.keys():
        text_segment["span"] = span.text
        segments[str(id)] = {}
        segments[str(id)]["segment_info"] = text_segment
        segments[str(id)]["text_analysis"] = {}
        segments[str(id)]["text_analysis"][pattern] = {"doc": doc.text, "span": span.text, "span_length": len(span.text)}
    else:
        if str(pattern) not in segments[str(id)]["text_analysis"].keys():
            segments[str(id)]["text_analysis"][str(pattern)] = {"doc": doc.text, "span": span.text, "span_length": len(span.text)}
        else:
            current_span_length = segments[str(id)]["text_analysis"][str(pattern)]["span_length"]
            if(len(span.text) > current_span_length):
                segments[str(id)]["text_analysis"][str(pattern)] = {"doc": doc.text, "span": span.text, "span_length": len(span.text)}

# match patterns
def match_patterns(text_segments):
    segments = {}
    for text_segment in text_segments:
        doc = nlp(text_segment)
        matches = matcher(doc)
        print(matches)
        for match_id, start, end in matches:
            print(doc, match_id, start, end, text_segment, segments)
            on_match(doc, match_id, start, end, text_segment, segments)
    return segments


print(match_patterns(["rate this app now"]))