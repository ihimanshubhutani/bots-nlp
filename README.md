## Purpose 
Built this as small part of a project where I can schedule meeting based using NLP library to understand date and time range.

# Date Range Parser

This Python script uses spaCy and regular expressions to parse date ranges specified in text input and provide responses.


## Requirements

- Python 3.x
- spaCy
- dateparser

You can install the required packages using the following commands:

```bash
pip install spacy
pip install dateparser
python -m spacy download en_core_web_sm
```

## Example Usage

```bash
import spacy
import re
import dateparser
from datetime import datetime, timedelta

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# ... (rest of the code) ...

# Test cases
test_cases = [
    "Schedule ooo from today to next monday",
    "Schedule my out of office from 1 June to tuesday",
    "Schedule meeting from 1 June to 5 June",
    # Add more test cases as needed
]

for input_text in test_cases:
    response = parse_request(input_text)
    print(response)
```
