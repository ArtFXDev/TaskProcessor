import random

def generate_random():

    word_options = ['cool', 'hype', 'dude', 'sick', 'awesome', 'wow', 'amazing', 'fantastic', 'superb']

    return random.choice(word_options)

if __name__ == '__main__':

    print(generate_random())