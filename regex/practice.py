import re

def test_regex(pattern, test_strings):
    for string in test_strings:
        print(string, ': ', re.findall(pattern, string))

# Basic Matching
# 1. Match a three-digit number
test1 = [
    "My PIN is 123.",
    "I live at 4567 Maple Street.",
    "Numbers like 89 and 6789."
]

# test_regex(r'\b\d{3}\b', test1)

# 2. Match a word boundary
test2 = [
    "The cat is on the mat.",
    "Catalog items are on sale.",
    "Concatenate these words."
]

# test_regex(r'\b[cC]at\b', test2)

# 3. Match any character except newline
test3 = [
    "Hello, World!",
    "This is a test.\nThis is only a test.",
    "Regex is powerful."
]

# test_regex(r'[^\n]*', test3)

# Quantifiers and Groups
# 4. Match zero or more digits
test4 = [
    "There are 42 apples.",
    "Total cost: $15.",
    "12345 and counting."
]

# test_regex(r'\d*', test4)

# 5. Match one or more digits
test5 = [
    "Product ID: 98765.",
    "There are no digits here.",
    "Find the numbers: 123 456 789."
]
# test_regex(r'\d+', test5)

# 6. Match an optional character
test6 = [
    "Color is spelled color in American English.",
    "Colour is the British spelling.",
    "Which color/colour do you prefer?"
]
# test_regex(r'[cC]olou?r', test6)

# 7. Match exactly three lowercase letters
test7 = [
    "abc",
    "abcd",
    "abcdef"
]
# test_regex(r'[a-z]{3}', test7)

# 8. Match three to five digits
test8 = [
    "Zip codes: 12345, 67890.",
    "Employee IDs: 456, 7890, 123.",
    "Range: 100-99999."
]

# test_regex(r'\d{3,5}', test8)

# Character Classes and Ranges
# 9. Match vowels
test9 = [
    "This is a test.",
    "Vowels are a, e, i, o, u.",
    "Cryptography."
]
# test_regex(r'[aeiou]', test9)

# 10. Match non-vowels
test10 = [
    "This is a test.",
    "Vowels are a, e, i, o, u.",
    "Cryptography."
]
# test_regex(r'[^aeiou]+', test10)
# test_regex(r'[^aeiou]', test10)

# 11. Match a range of characters
test11 = [
    "abcde",
    "ABCDE",
    "12345"
]
# test_regex(r'[a-e]', test11)

# 12. Match uppercase and lowercase letters
test12 = [
    "Hello, World!",
    "12345",
    "Uppercase and lowercase."
]
# test_regex(r'[a-zA-Z]+', test12)

# 13. Match a specific set of characters
test13 = [
    "a quick brown fox.",
    "Jumping over boulders.",
    "Catch the coyote."
]
# test_regex(r'[abcABC]', test13)

# Anchors and Boundaries
# 14. Match the start of a string
test14 = [
    "Start here.",
    "Middle of the sentence.",
    "End of the line."
]
# test_regex(r'^[Ss]', test14)


# 15. Match the end of a string
test15 = [
    "This is the end.",
    "Beginning and middle.",
    "Stop here."
]

# test_regex(r'\.$', test15)

# 16. Match word boundaries
test16 = [
    "The quick brown apple.",
    "Unbounded joy.",
    "Apple pies are delicious."
]

# test_regex(r'\b[aA]pple\b', test16)

# Special Characters
# 17. Escape a dot
test17 = [
    "a.b",
    "This is a test.",
    "Dot matrix."
]
# test_regex(r'a\.b', test17)

# 18. Escape a backslash
test18 = [
    "C:\\Users\\Admin",
    "Backslashes \\ are tricky.",
    "Escape sequences."
]
# test_regex(r'C:\\Users', test18)

# 19. Match a literal asterisk
test19 = [
    "Find the * asterisk.",
    "Multiplication * operation.",
    "Asterisks are common."
]
# test_regex(r'\*', test19)

# Lookaheads and Lookbehinds
# 20. Positive lookahead
test20 = [
    "foo bar",
    "foobar",
    "foo123bar"
]
# test_regex(r'foo(?=bar)', test20)

# 21. Negative lookahead
test21 = [
    "foobar",
    "foo123",
    "foo bar"
]
# test_regex(r'foo(?!bar)', test21)

# 22. Positive lookbehind
test22 = [
    "barfoo",
    "foobar",
    "123bar"
]

# 23. Negative lookbehind
test23 = [
    "foo bar",
    "bar123",
    "foobar"
]

# Combining Expressions
# 24. Match a phone number
test24 = [
    "(123) 456-7890",
    "Call me at 123-456-7890.",
    "Phone: (123) 456-7890."
]
# test_regex(r'\(\d{3}\) \d{3}-\d{4}', test24)

# 25. Match an email address
test25 = [
    "test@example.com",
    "Contact us at info@domain.org.",
    "Invalid email: user@@example.com."
]
# test_regex(r'\w+@[a-z]+\.[a-z]{2,3}', test25)

# 26. Match a URL
test26 = [
    "Visit http://www.example.com",
    "Secure site: https://secure.example.com.",
    "Invalid URL: www.example"
]
# test_regex(r'https?://\D+\.com', test26)

# 27. Match a date
test27 = [
    "Today's date is 12/31/2024.",
    "Event on 1/1/2024.",
    "Invalid date: 31/12/2024."
]
# test_regex(r'\d{1,2}/\d{1,2}/\d{4}', test27)

# 28. Match a hexadecimal color code
test28 = [
    "#ff5733 is a hex color.",
    "Background color: #abcdef.",
    "Invalid code: #123abz."
]
# test_regex(r'#[a-fA-F\d]{6}', test28)

# 29. Match a time format
test29 = [
    "The meeting is at 10:30 AM.",
    "Dinner at 6:45 PM.",
    "Invalid time: 25:00 PM."
]

# 30. Match a complex pattern
test30 = [
    "Hello World.",
    "Greetings, Earth!",
    "This is a test sentence."
]

test_regex(r'^[A-Z][a-z]*(?: [A-Z][a-z]*)*\.$', test30)

