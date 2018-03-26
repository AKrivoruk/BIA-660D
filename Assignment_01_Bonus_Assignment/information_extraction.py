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
    def __init__(self, pet_type, owner, name=None):
        self.name = name = [] if name is None else name
        self.type = pet_type
        self.owner = owner

    def __repr__(self):
        return self.type

class Trip(object):
    def __init__(self, location, date=None):
        self.departs_on = location
        self.departs_to = date

    def __repr__(self):
        return self.location

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

def select_pet(name):
    for person in persons:
        if person.name == name:
            return person

def add_pet(type, owner, name=None):
    pet = None
    if name:
        pet = select_pet(name)
    if owner:
        pet_owner = select_person(owner)
    if pet is None:
        pet = Pet(type, pet_owner, pet)
        pets.append(pet)
    return pet

def select_trip(name):
    for place in trips:
        if place.name == name:
            return place

def add_trip(place):
    trip = select_trip(place)
    if trip is None:
        new_trip = Trip(place)
        trips.append(new_trip)
        return new_trip
    return trip

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
    full_pet_name = None
    pet_name = None
    negative = None

    if verb.lemma_ == 'like':
        2+2
        for child in verb.children:
            if  child.dep_ == 'neg':
                doesNT = child
            elif child.dep_ == 'nsubj' and child.pos_ == 'PROPN':
                subject = child
            elif child.dep_ == 'dobj' and child.pos_ == 'PROPN':
                object = child

        if (subject and object) and (not find_compounds(subject) and not find_compounds(object)) and not negative:
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
            pet_type = get_child_with_dep(subject, 'poss')
            pet_name = get_child_with_dep(verb, 'attr')
            owner_token = get_child_with_dep(pet_type, 'poss')
            pet_owner = add_person(owner_token.text)
            pet_owner.has.append(pet_type.text)
            pet = add_pet(pet_type.text, pet_owner, pet_name.text)

        pass
    elif verb.lemma_ == 'have':
        named = None
        2+2
        for child in verb.children:
            if child.dep_ == 'nsubj' and child.pos_ == 'PROPN':
                subject = child
            elif child.dep_ == 'dobj' and (child.text == 'dog' or child.text == 'cat'):
                object = child
                named = get_child_with_dep(object, 'acl')
                if named and named.text == 'named':
                    pet_name = get_child_with_dep(named,'oprd')
                    if find_compounds(pet_name):
                        prefix = get_child_with_dep(pet_name, 'compound')
                        full_pet_name = prefix.text + ' ' + pet_name.text

        pet_owner = add_person(subject.text)
        pet_owner.has.append(object.text)
        if (subject and object) and not full_pet_name and not pet_name:
            pet = add_pet(object.text, pet_owner)

        elif (subject and object) and not full_pet_name:
            pet = add_pet(object.text, pet_owner, pet_name.text)

        elif (subject and object) and full_pet_name:
            pet = add_pet(object.text, pet_owner, full_pet_name)

        pass
    elif verb.lemma_ == 'leave':
        2+2
        location = None
        month = None
        date = None
        departure = None
        prep = None
        for child in verb.children:
            if child.dep_ == 'nsubj' and child.pos_ == 'PROPN':
                subject = child
            elif child.dep_ == 'prep' and (child.text == 'for' or child.text == 'to'):
                prep = child
                location = get_child_with_dep(object, 'pobj')
            elif child.dep_ == 'prep' and (child.text == 'on' or child.text == 'in'):
                prep = child
                date = get_child_with_dep(object, 'pobj')
                month = get_child_with_dep(date, 'compound')
                departure = month.text + ' ' + date.text

        if subject and location and not departure:
            pass
        elif subject and location and departure:
            pass
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