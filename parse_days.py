import re

def extract_days(message):
    message = message.lower()
    
    # Try months
    month_match = re.search(r'(\d+)\s*month', message)
    if month_match:
        return int(month_match.group(1)) * 30
        
    # Try weeks
    week_match = re.search(r'(\d+)\s*week', message)
    if week_match:
        return int(week_match.group(1)) * 7
        
    # Try days
    day_match = re.search(r'(\d+)\s*day', message)
    if day_match:
        return int(day_match.group(1))
        
    return 1 # default
    
print(extract_days("what is the price of rice in next 3 months"))
