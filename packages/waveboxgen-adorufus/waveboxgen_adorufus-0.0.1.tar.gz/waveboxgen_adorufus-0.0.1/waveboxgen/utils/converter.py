import re


def to_camel_case_with_capitalize(text):
    # Split the text into words using spaces or underscores as separators
    words = re.split(r'[-_\s]+', text)

    # Capitalize the first letter of each word
    camel_case_words = [word.capitalize() for word in words]

    # Join the words together to form the camel case string
    camel_case_text = ''.join(camel_case_words)

    return camel_case_text

def to_snake_case(text):
   # Replace hyphens and spaces with underscores
    text = re.sub(r'[-\s]', '_', text)
    
    # Split the text into words based on uppercase letters and underscores
    words = re.split(r'([A-Z]+|[a-z]+|[_]+)', text)
    
    # Filter out empty strings and convert to lowercase
    snake_case_words = [word.lower() for word in words if word and word not in ["-", "_"]]

    # Join the words together with underscores to form the snake case string
    snake_case_text = '_'.join(snake_case_words)

    return snake_case_text