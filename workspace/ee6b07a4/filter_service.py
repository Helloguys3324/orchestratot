import re
from better_profanity import profanity

class FilterService:
    def __init__(self):
        profanity.load_censor_words()
        # Add custom patterns for leetspeak or variations
        self.custom_patterns = [
            r"f\s*u\s*c\s*k",
            r"b\s*i\s*t\s*c\s*h"
        ]

    def is_profane(self, text: str) -> bool:
        if profanity.contains_profanity(text):
            return True
        
        for pattern in self.custom_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False