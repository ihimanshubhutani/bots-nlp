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

def parse_date_range(input_text, keyword):
    # Define a pattern to match the "from [start date] to [end date]" format
    date_range_pattern = r"from (.+) to (.+)"
    
    # Search for date ranges using the pattern
    match = re.search(date_range_pattern, input_text)
    
    if match:
        start_date_str = match.group(1)
        end_date_str = match.group(2)
        
        start_date = dateparser.parse(start_date_str)
        end_date = dateparser.parse(end_date_str)
        
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
    response = ""
    if "from" in input_text and "to" in input_text:
        response = parse_date_range(input_text, keyword)
    elif "next" in input_text and any(token.text in weekday_mapping for token in doc):
        # Handle cases like "next Monday to Tuesday"
        current_date = datetime.now()
        
        tokens = [token for token in doc if token.text in weekday_mapping]
        start_weekday, end_weekday = tokens[0].text, tokens[1].text
        
        start_days_until_weekday = (weekday_mapping[start_weekday] - current_date.weekday()) % 7
        end_days_until_weekday = (weekday_mapping[end_weekday] - current_date.weekday()) % 7
        
        # Special case handling when transitioning from end of week to start of next week
        if start_days_until_weekday <= end_days_until_weekday:
            start_date = current_date + timedelta(days=start_days_until_weekday)
            end_date = current_date + timedelta(days=end_days_until_weekday)
        else:
            start_date = current_date + timedelta(days=start_days_until_weekday)
            end_date = current_date + timedelta(days=end_days_until_weekday + 7)
        
        response = f"Okay, your {keyword} is scheduled from {start_date.strftime('%d %B')} to {end_date.strftime('%d %B')}."
    
    # Handle other cases here if needed
    
    if not response:
        response = f"I'm sorry, I couldn't understand the {keyword} request."
    
    return response

# Test cases

input_text = "Schedule ooo from 1 June to 5 June"
response = parse_request(input_text)
print(response)

input_text = "Schedule my out of office from 1 June to tuesday"
response = parse_request(input_text)
print(response)

input_text = "Schedule meeting from 1 June to 5 June"
response = parse_request(input_text)
print(response)

input_text = "Schedule a meeting from 1 June to tuesday"
response = parse_request(input_text)
print(response)

input_text = "Schedule meeting from today to tomorrow"
response = parse_request(input_text)
print(response)

input_text = "Schedule meeting from yesterday to tomorrow"
response = parse_request(input_text)
print(response)

input_text = "Schedule meeting from today to monday"
response = parse_request(input_text)
print(response)


