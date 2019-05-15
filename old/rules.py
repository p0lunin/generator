import random


class Rule:
    def __init__(self):
        self.words = []
        self.next = []

    def add_word(self, word):
        self.words.append(word)

    def add_words(self, words):
        self.words += words

    def add_next(self, next):
        self.next.append(next)

    def run(self):
        return random.choice(self.words), random.choice(self.next)


class RuleGenerator:
    def __init__(self):
        self.rules = {}

    def add_word(self, rule, word):
        self.rules[rule].add_word(word)

    def add_words(self, rule, words):
        self.rules[rule].add_words(words)

    def add_next(self, rule, next):
        self.rules[rule].add_next(next)

    def add_rule(self, rule):
        self.rules[rule] = Rule()

    def generate(self, start_rule):
        result = ''
        rule = start_rule
        word, rule = self.rules[rule].run()
        while rule != '$end_of_mes$':
            result += word + ' '
            word, rule = self.rules[rule].run()
        result += word + '.'
        return result
