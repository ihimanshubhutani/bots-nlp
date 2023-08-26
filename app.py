import spacy
import re
import dateparser
from datetime import datetime, timedelta

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Define a dictionary to map weekdays to their corresponding numeric values
weekday_mapping = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

def remove_words(input_string, words_to_remove):
    cleaned_string = input_string
    for word in words_to_remove:
        cleaned_string = cleaned_string.replace(word, "")
    return cleaned_string


def parse_date_range(input_text, keyword,doc):
    # Define a pattern to match the "from [start date] to [end date]" format
    date_range_pattern = r"from (.+) to (.+)"
    
    # Search for date ranges using the pattern
    input_text =  remove_words(input_text,["next","upcoming"])
    
    match = re.search(date_range_pattern, input_text)

    if match:
        start_date_str = match.group(1)
        end_date_str = match.group(2)
        
        start_date = dateparser.parse(start_date_str,settings={'PREFER_DATES_FROM': 'future'})
        end_date = dateparser.parse(end_date_str,settings={'PREFER_DATES_FROM': 'future'})
        
        if start_date and end_date:
            response = f"Okay, your {keyword} is scheduled from {start_date.strftime('%d %B')} to {end_date.strftime('%d %B')}."
        else:
            response = "I'm sorry, I couldn't understand the dates."
    else:
        response = "I'm sorry, I couldn't understand the request."
    
    return response

def parse_request(input_text):
    # Process the input text with spaCy
    doc = nlp(input_text)
    
    # Determine if it's a meeting or out-of-office request
    is_meeting_request = any(token.text in ["meeting", "meet"] for token in doc)
    keyword = "meeting" if is_meeting_request else "out-of-office"
    
    # Check for different patterns based on cases
    response = parse_date_range(input_text, keyword,doc)

    
    # Handle other cases here if needed
    
    if not response:
        response = f"I'm sorry, I couldn't understand the {keyword} request."
    
    return response

# Test cases

test_cases = [
    "Schedule ooo from today to next monday",
    "Schedule my out of office from 1 June to tuesday",
    "Schedule meeting from 1 June to 5 June",
    "Schedule a meeting from 1 June to tuesday",
    "Schedule meeting from today to tomorrow",
    "Schedule meeting from yesterday to tomorrow",
    "Schedule meeting from monday to tuesday",
    "Schedule meeting from monday to tuesday",
    "Schedule meeting from monday to wednesday",
    "Schedule meeting from 25 to monday",
    "Schedule meeting from next monday to next tuesday",
]

for input_text in test_cases:
    response = parse_request(input_text)
    print(response)


