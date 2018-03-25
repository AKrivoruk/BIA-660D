import re
import spacy
nlp = spacy.load('en')
re_spaces = re.compile(r'\s+')

class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels

    def __repr__(self):
        return self.name


class Pet(object):
    def __init__(self, pet_type, name=None):
        self.name = name
        self.type = pet_type


class Trip(object):
    def __init__(self, location, date=None):
        self.departs_on = location
        self.departs_to = date

persons = []
pets = []
trips = []

def select_person(name):
    for person in persons:
        if person.name == name:
            return person

def add_person(name):
    person = select_person(name)
    if person is None:
        new_person = Person(name)
        persons.append(new_person)
        return new_person
    return person

def get_child_with_dep(token, dep):
    for child in token.children:
        if child.dep_ == dep:
            return child

def get_data_from_file(file_path='./assignment_01_data.txt'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if not line.startswith(('$$$', '###', '==='))]
        return cleaned_lines

def remove_articles(question):
    q_words = question.split(' ')
    for article in ('a', 'an', 'the'):
        try:
            q_words.remove(article)
        except:
            pass
    return re.sub(re_spaces, ' ', ' '.join(q_words))

def find_compounds(token):
    for child in token.children:
        if child.dep_ == 'compound':
            return True
    return False

def process_sentence(sentence):
    doc = nlp(unicode(sentence))
    verb = doc[:].root
    subject = None
    object = None

    if verb.lemma_ == 'like':
        2+2
        for child in verb.children:
            if child.dep_ == 'nsubj' and child.pos_ == 'PROPN':
                subject = child
            elif child.dep_ == 'dobj' and child.pos_ == 'PROPN':
                object = child

        if (subject and object) and (not find_compounds(subject) and not find_compounds(object)):
            liker = add_person(subject.text)
            likee = add_person(object.text)
            liker.likes.append(likee)

    elif verb.lemma_ == 'be':
        2+2
        attr = None
        for child in verb.children:
            if child.dep_ == 'attr' and child.text == 'friends':
                attr = child
                with_token = get_child_with_dep(attr, 'prep')
                if with_token and with_token.text == 'with':
                    object = get_child_with_dep(with_token, 'pobj')
            elif child.dep_ == 'nsubj':
                subject = child
            elif child.dep_ == 'dobj' and child.pos_ == 'PROPN':
                object = child


        if attr and (subject and object) and (not find_compounds(subject) and not find_compounds(object)):
            liker = add_person(subject.text)
            likee = add_person(object.text)
            liker.likes.append(likee)
            likee.likes.append(liker)

        elif subject.text == 'name':
            2+2
        pass
    elif verb.lemma_ == 'have':
        2+2
        pass
    elif verb.lemma_ == 'leave':
        2+2
        pass
    else:
        raise NotImplementedError

def process_data_from_input_file(path):
    data = get_data_from_file(path)
    for sent in data:
        process_sentence(sent)


def answer_question(question_string):
    pass

def main():
    process_data_from_input_file('assignment_01_data.txt')
    answer_question('Who likes Mary?')

if __name__ == '__main__':
    main()