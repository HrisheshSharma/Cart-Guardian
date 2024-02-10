#1. Nagging: Trying to force the users to perform some actions like subscribing to newsletters, giving ratings, etc.
pattern1_nagging = [
    {"POS": "VERB", "OP":"?"},
    {"LEMMA": {"IN": ["rate", "upvote", "subscribe", "install"]}, "OP": "+"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["us", "app", "now", "image", "picture", "video", "feature", "product", "discount"]}, "OP": "+"},
    {"LOWER": {"IN": ["now", "continue", "discount"]}, "OP": "?"}
]
#Sample: "Kindly do upvote us to continue.", "Please install this app now."

pattern2_nagging = [
    {"LEMMA": {"IN": ["redirect", "close", "skip", "watch"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["ad", "session", "video", "site", "website", "page", "popup", "banner", "advertisment", "advertisements", "ads", "advertisement"]}, "OP": "+"},
    {"LOWER": {"IN": ["after", "in", "while"]}, "OP": "?"},
    {"IS_DIGIT": True, "OP": "*"},
    {"LOWER": {"IN": ["ad", "session", "video", "site", "website", "page", "popup", "banner", "advertisment", "advertisements", "ads", "advertisement"]}, "OP": "?"},
    {"LEMMA": {"IN": ["ends", "finish", "seconds", "minutes"]}, "OP": "?"}
    
]
#Sample: "Skip this ad in 5 seconds", "You will be redirected to the site after ad ends."


pattern3_nagging = [
    {"LOWER": {"IN": ["watch"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["ad", "advertisement", "session", "video", "clip", "commercial", "promo", "promotional"]}, "OP": "+"},
    {"LOWER": {"IN": ["to"]}, "OP": "?"},
    {"LOWER": {"IN": ["unlock", "earn", "get", "collect", "gain", "access", "continue"]}, "OP": "+"}
]
#Sample: "Watch the ad to unlock the feature.", "Watch the promotional video to continue."

pattern4_nagging = [
    {"LOWER": {"IN": ["unlock", "earn", "get", "collect", "gain", "access"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["by", "after", "post"]}},
    {"LEMMA": {"IN": ["watch"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["ad", "session"]}}
]
#Sample: "Unlock great discounts by watching these 3 ad", "Earn 10 credits after watching the ad."

pattern5_nagging = [
    {"LEMMA": {"IN": ["star"]}},
    {"LEMMA": {"IN": ["rate", "review", "rating"]}}
]
#Sample: "Give us star rating"

patterns_nagging = [pattern1_nagging, pattern2_nagging, pattern3_nagging
, pattern4_nagging, pattern5_nagging]

#2. Bait and Switch: Luring the users with an attractive offer and then changing the terms and conditions.

pattern1_bait_and_switch = [
    {"LOWER": {"IN": ["free", "auto", "cancel"]}},
    {"IS_ALPHA": True, "OP": "?"},
    {"LOWER": {"IN": ["trial", "renew", "anytime"]}}
]
#Sample: "Free trial", "Auto renew", "Subscribe to our newsletter and get a free trial"

pattern2_bait_and_switch = [
    {"LOWER": {"IN": ["start", "turn", "add", "yes", "next", "sign", "ok", "continue", "unlock", "subscribe", "confirm", "setup", "signup"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["free", "earn", "discount", "coupon", "sale", "notifications"]}, "OP": "+"},
    {"LOWER": {"IN": ["on", "in", "up", "off", "now"]}, "OP": "*"}
]
#Sample: "Subscribe now", "Turn on notifications", "Add to cart", "Continue to checkout", "Unlock the feature", "Confirm the order", "Setup your account"

pattern3_bait_and_switch = [
    {"LEMMA": {"IN": ["sign", "signup", "register", "join", "subscribe"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["agree", "accept", "comfortable", "policy", "terms", "condition"]}, "OP": "+"},
]
#Sample: "By signing up, you agree to our terms and conditions."

patterns_bait_and_switch = [pattern1_bait_and_switch, pattern2_bait_and_switch, pattern3_bait_and_switch]

#3. Roach Motel: Making it difficult for the users to cancel a subscription or opt-out of a service.
pattern1_roach_motel = [
    {"LEMMA": {"IN": ["cancel", "unsubscribe", "discontinue", "delete", "leave", "pause", "exit", "opt out"]}, "OP": "+"},
    {"LEMMA": {"IN": ["account", "subscription", "membership", "service", "plan", "renewal", "auto-renewal", "auto-renew", "auto-renewing", "auto-renewed"]}, "OP": "+"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["call", "give", "phone", "contact", "email"]}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["call", "only"]}, "OP": "?"}
]
#Sample: "To delete the account, please email to our agent.", "To unsubscribe from the service, call us only."

pattern2_roach_motel = [
    {"LOWER": {"IN": ["call", "give", "contact", "email"]}, "OP": "+"},
    {"LOWER": {"IN": ["us", "agent"]}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["cancel", "unsubscribe", "discontinue", "delete", "leave", "pause", "exit", "opt out"]}, "OP": "+"},
]
#Sample: "Call us to cancel the subscription", "Give us a call to unsubscribe"
patterns_roach_motel = [pattern1_roach_motel, pattern2_roach_motel]


#4. Price Comparison Prevention: Preventing the users from comparing the prices of the products or services with other platforms.

pattern1_intermediate_currency = [
    {"LOWER": {"IN": ["buy", "get", "collect", "earn", "gain", "unlock"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["credit", "badge", "star", "point", "reward", "token"]}}
]
#Sample: "Buy this to get 5 flipkart points", "Collect 10 credits to unlock the feature"
patterns_intermediate_currency = [pattern1_intermediate_currency]

#5. Privacy Zuckering: Misleading the users into sharing more personal information than they intended to.

pattern1_privacy_zuckering = [
    {"LOWER": {"IN": ["upload", "sync", "share", "add", "invite", "gift", "ask", "refer", "signup"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["friends", "contacts", "location"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["earn", "rewards", "money", "points", "discounts", "unlock", "gain", "credits", "tokens"]}, "OP": "*"}
]
#Sample: "Upload your contacts", "Share your location", "Invite your friends"
patterns_privacy_zuckering = [pattern1_privacy_zuckering]


#6. Forced Enrollment: Forcing the users to enroll in a service or subscribe to a newsletter without their consent.
pattern1_forced_enrollment = [
    {"LOWER": {"IN": ["join", "subscribe"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["terms", "policies"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["conditions", "policies"]}}
]
#Sample: "Join us to get the latest updates on our terms and conditions", "Subscribe to our newsletter to get the latest policies"

pattern2_forced_enrollment = [
    {"LEMMA": {"IN": ["permission", "click", "agree", "join", "select"]}, "OP": "+"},
    {"LOWER": {"IN": ["terms", "policies"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["conditions", "policies"]}}
]
#Sample: "By giving us permission, you agree to our terms and conditions", "By clicking on the button, you agree to our policies"
patterns_forced_enrollment = [pattern1_forced_enrollment, pattern2_forced_enrollment]

#7. Default Choice: Making a choice the default option, which is difficult to change or opt-out from.


pattern1_default_choice = [
    {"LEMMA": {"IN": ["click", "press", "subscribe", "use"]}, "OP": "+"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["button", "check"]}, "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["permission", "consent", "terms", "conditions", "policy"]}, "OP": "+"},
]
#Sample: "Click on the button to give us permission", "Press the button to agree to our terms and conditions"
patterns_default_choice = [pattern1_default_choice]

#8. False Hierarchy: Misleading the users into believing that they are making a decision, when in reality, they are not.

# pattern1_false_hierarchy = [
#     {"LOWER": {"IN": ["start", "turn", "add", "yes", "next", "sign", "ok", "continue", "unlock", "subscribe", "confirm", "setup"]}, "OP": "+"},
#     {"LOWER": {"IN": ["on", "in", "up", "off", "now", "thanks", "up", "later", "anytime", "no", "not", "later", "cancel", "skip", "exit"]}, "OP": "?"}
# ]
# patterns_false_hierarchy = [pattern1_false_hierarchy]

#9. Countdown Timer: Creating a sense of urgency by displaying a countdown timer for a limited time offer.

pattern1_countdown_timer = [
    {"POS": "NUM"},
    {"LOWER": {"IN": [":"]}},
    {"POS": "NUM"},
    {"LOWER": {"IN": [":"]}},
    {"POS": "NUM"},
    {"LOWER": {"IN": [":"]}, "OP": "?"},
    {"POS": "NUM", "OP": "?"}
]
#Sample: "00:00:00", "00:00:00:00"

pattern2_countdown_timer = [
    {"LOWER": {"IN": ["hrs", "mins", "secs"]}}
]

pattern3_countdown_timer = [{"TEXT": {"REGEX": "[0-9]{2}:[0-9]{2}:[0-9]{2}"}}]

pattern4_countdown_timer = [
    {"POS": "NUM", "OP": "?"},
    {"LOWER": {"IN": ["hrs", "mins", "secs", "hours", "minutes", "seconds", "hr", "min", "sec"]}},
    {"LOWER": {"IN": [":"]}, "OP": "?"},
    {"POS": "NUM", "OP": "?"},
    {"LOWER": {"IN": ["hrs", "mins", "secs", "hours", "minutes", "seconds", "hr", "min", "sec"]}},
    {"LOWER": {"IN": [":"]}, "OP": "?"},
    {"POS": "NUM", "OP": "?"},
    {"LOWER": {"IN": ["hrs", "mins", "secs", "hours", "minutes", "seconds", "hr", "min", "sec"]}}
]
#Sample: "2 hours 30 minutes 45 seconds", "2 hrs 30 mins 45 secs", "2:30:45"

patterns_countdown_timer = [pattern1_countdown_timer, pattern2_countdown_timer, pattern3_countdown_timer, pattern4_countdown_timer]

#10. Limited Time Message: Displaying a message that the offer is available for a limited time only.

pattern1_limited_time_message = [
    {"LOWER": {"IN": ["sale", "offer", "deal", "apply", "order"]}},
    {"LOWER": {"IN": ["ends", "by", "valid", "open", "available"]}},
    {"LOWER": "soon", "OP": "?"},
    {"POS": "PUNCT", "OP": "*"},
    {"POS": "NUM", "OP": "*"}
]
#Sample: "Sale ends soon", "Offer valid for 2 days", "Deal available by 31st July"

pattern2_limited_time_message = [
    {"LOWER": "limited"},
    {"LOWER": "time"},
    {"LOWER": "only", "OP": "?"}
]

pattern3_limited_time_message = [
    {"LOWER": {"IN": ["ends", "valid", "open", "available", "order"]}},
    {"LOWER": {"IN": ["by", "for", "in", "on", "at", "within", "soon"]}},
    {"POS": "NUM"}
]
#Sample: "Sale ends by 31st July", "Offer valid for 2 days", "Deal available within 2 hours"

patterns_limited_time_message = [pattern1_limited_time_message, pattern2_limited_time_message, pattern3_limited_time_message]

#11. Low Stock Message: Displaying a message that the product is available in limited stock only.
pattern1_low_stock_message = [
    {"LOWER": {"IN": ["limited", "low", "left"]}},
    {"LOWER": {"IN": ["supply", "stock", "quantity", "availability"]}}
]

pattern2_low_stock_message = [
    {"LOWER": "only", "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": {"IN": ["left", "available"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["stock", "supply"]}, "OP": "+"}
]
#Sample: "Limited stock", "Low availability", "Only 5 left", "Only 5 available"
pattern3_low_stock_message = [
    {"LOWER": {"IN": ["left", "available"]}},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["stock"]}}
]
#Sample: "Only 5 left", "Only 5 available"
patterns_low_stock_message = [pattern1_low_stock_message, pattern2_low_stock_message, pattern3_low_stock_message]

#12. High Demand Message: Displaying a message that the product is in high demand.

pattern1_high_demand_message = [
    {"IS_ALPHA": True, "OP": "*"},
    {"LOWER": "high"},
    {"LOWER": "demand"}
]
pattern2_high_demand_message = [
    {"LEMMA": {"IN": ["order", "book"]}, "OP": "?"},
    {"POS": "AUX", "OP": "?"},
    {"LEMMA": {"IN": ["reserve"]}},
]
#Sample: "Order now", "Book now", "Reserve now"
pattern3_high_demand_message = [
    {"LEMMA": {"IN": ["sell", "finish"]}},
    {"LOWER": {"IN": ["fast", "quick"]}}
]

patterns_high_demand_message = [pattern1_high_demand_message, pattern2_high_demand_message, pattern3_high_demand_message]

#13. Activity Message: Displaying a message that the product is in high demand.

pattern1_activity_message = [
    {"LOWER": {"IN": ["items"]}, "OP": "+"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["order", "purchase", "subscribe", "view", "book", "visit", "sell", "save", "look"]}},
    {"LOWER": {"IN": ["by", "in"]}}
]

pattern2_activity_message = [
    {"LEMMA": {"IN": ["people", "person", "visitor", "user"]}, "OP": "+"},
    {"POS": "NOUN", "OP": "?"},
    {"IS_ALPHA": True, "OP": "*"},
    {"LEMMA": {"IN": ["order", "purchase", "subscribe", "view", "book", "visit", "sell", "save", "look", "buy"]}}
]
#Sample: "Order by people", "Purchase by user", "Visit by person"

patterns_activity_message = [pattern1_activity_message, pattern2_activity_message]