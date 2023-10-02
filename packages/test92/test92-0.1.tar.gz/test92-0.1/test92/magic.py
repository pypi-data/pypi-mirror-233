import random

def tell_random_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you get when you cross a snowman and a vampire? Frostbite!",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        # Add more jokes here
    ]
    random_joke = random.choice(jokes)
    return random_joke


import random

def ask_me():
    answers = [
        "Yes",
        "No",
        "Maybe",
        "Ask again later",
        "Outlook not so good",
        "Absolutely!",
    ]
    return random.choice(answers)

