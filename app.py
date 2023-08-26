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

def parse_date_range(input_text):
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
            response = f"Okay, your out-of-office is scheduled from {start_date.strftime('%d %B')} to {end_date.strftime('%d %B')}."
        else:
            response = "I'm sorry, I couldn't understand the dates."
    else:
        response = "I'm sorry, I couldn't understand the request."
    
    return response

def parse_ooo_request(input_text):
    # Process the input text with spaCy
    doc = nlp(input_text)
    
    # Check for different patterns based on cases
    response = ""
    if "from" in input_text and "to" in input_text:
        response = parse_date_range(input_text)
    
    # Handle other cases here if needed
    
    if not response:
        response = "I'm sorry, I couldn't understand the request."
    
    return response

# Test cases
input_text = "Schedule my out of office from 1 June to 5 June"
response = parse_ooo_request(input_text)
print(response)

input_text = "Schedule my out of office from 1 June to tuesday"
response = parse_ooo_request(input_text)
print(response)

input_text = "Schedule my out of office from today to tomorrow"
response = parse_ooo_request(input_text)
print(response)

input_text = "Schedule my out of office from today to 28 August"
response = parse_ooo_request(input_text)
print(response)
