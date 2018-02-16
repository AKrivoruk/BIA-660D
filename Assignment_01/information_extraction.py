from __future__ import print_function
import re
import spacy

from pyclausie import ClausIE


nlp = spacy.load('en')
re_spaces = re.compile(r'\s+')


class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels


class Pet(object):
    def __init__(self, pet_type, name=None):
        self.name = name
        self.type = pet_type


class Trip(object):
    def __init__(self):
        self.departs_on = None
        self.departs_to = None

persons = []
pets = []
trips = []

list_of_triples = []
def process_data_from_input_file(file_path):
    sents = get_data_from_file(file_path)
    cl = ClausIE.get_instance()
    triples = cl.extract_triples(sents)
    for t in triples:
        r = process_relation_triplet(t)

def get_data_from_file(file_path='chatbot_data.txt'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if not line.startswith(('$$$', '###', '==='))]

    return cleaned_lines


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


def add_pet(type, name=None):
    pet = None

    if name:
        pet = select_pet(name)

    if pet is None:
        pet = Pet(type, name)
        pets.append(pet)

    return pet


def get_persons_pet(person_name):

    person = select_person(person_name)

    for thing in person.has:
        if isinstance(thing, Pet):
            return thing



def process_relation_triplet(triplet):

    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object

    doc = nlp(unicode(sentence))

    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t

    # Process (PERSON, likes, PERSON) relations
    if root.lemma_ == 'like':
        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and triplet.object in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(triplet.object)
            s.likes.append(o)

    if root.lemma_ == 'be' and triplet.object.startswith('friends with'):
        fw_doc = nlp(unicode(triplet.object))
        with_token = [t for t in fw_doc if t.text == 'with'][0]
        fw_who = [t for t in with_token.children if t.dep_ == 'pobj'][0].text

        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and fw_who in [e.text for e in doc.ents if e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(fw_who)
            s.likes.append(o)
            o.likes.append(s)


    # Process (PET, has, NAME)
    if triplet.subject.endswith('name') and ('dog' in triplet.subject or 'cat' in triplet.subject):
        obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))

        # handle single names, but what about compound names? Noun chunks might help.
        if len(obj_span) == 1 and obj_span[0].pos_ == 'PROPN':
            name = triplet.object
            subj_start = sentence.find(triplet.subject)
            subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))

            s_people = [token.text for token in subj_doc if token.ent_type_ == 'PERSON']
            assert len(s_people) == 1
            s_person = select_person(s_people[0])

            s_pet_type = 'dog' if 'dog' in triplet.subject else 'cat'

            pet = add_pet(s_pet_type, name)

            s_person.has.append(pet)

        if len(obj_span) == 2 and obj_span[1].pos_ == 'PROPN':
            name = triplet.object
            subj_start = sentence.find(triplet.subject)
            subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))

            s_people = [token.text for token in subj_doc if token.ent_type_ == 'PERSON']
            assert len(s_people) == 1
            s_person = select_person(s_people[0])

            s_pet_type = 'dog' if 'dog' in triplet.subject else 'cat'

            pet = add_pet(s_pet_type, name)

            s_person.has.append(pet)


def preprocess_question(question):
    # remove articles: a, an, the

    q_words = question.split(' ')

    # when won't this work?
    for article in ('a', 'an', 'the'):
        try:
            q_words.remove(article)
        except:
            pass

    return re.sub(re_spaces, ' ', ' '.join(q_words))


def has_question_word(string):
    # note: there are other question words
    for qword in ('who', 'what'):
        if qword in string.lower():
            return True

    return False

def get_question():
    question = ' '
    while question[-1] != '?':
        question = raw_input("Please enter your question: ")
        return question
        if question[-1] != '?':
            print('This is not a question... please try again')

def answer_questions(string):
    sents = get_data_from_file()
    cl = ClausIE.get_instance()
    triples = cl.extract_triples(sents)
    q_trip = cl.extract_triples([preprocess_question(string)])[0]
    answers = []
    # (WHO, has, PET)
    # here's one just for dogs
    print(q_trip)

    if q_trip.subject.lower() == 'who' and q_trip.object == 'dog':
        answer = '{} has a dog.'

        for person in persons:
            pet = get_persons_pet(person.name)
            if pet and pet.type == 'dog':
                answer = (answer.format(person.name))
                answers.append(answer)

    if q_trip.subject.lower() == 'who' and q_trip.object == 'cat':
        answer = '{} has a cat.'

        for person in persons:
            pet = get_persons_pet(person.name)
            if pet and pet.type == 'cat':
                answer = (answer.format(person.name))
                answers.append(answer)


    if q_trip.subject.lower() == 'who'and q_trip.predicate == 'likes':
        target = q_trip.object
        answer = '{} likes {}'

        for people in persons:
            if people.likes == target:
                answer = answer.format(people.name, target)
                answers.append(answer)

    if  q_trip.subject.lower() == 'does'and q_trip.predicate == 'like':
        answer = '{} likes {}'
        for t in q_trip.subect:
            if t.pos_ == 'PERSON':
                Sender = t
                Receiver = q_trip.object
                if Sender.likes == Receiver:
                        answer = answer.format(Sender,Receiver)
                        answers.append(answer)

    if q_trip.subject.lower() == 'who' and (q_trip.predicate == 'going' or q_trip.predicate == 'flying' or q_trip.predicate == 'traveling' or q_trip.predicate == 'visiting'):
        destination = q_trip.obect
        answer = '{} is going on a trip to {}'
        for person in persons:
            if person.travels == destination
                answer = (answer.format(person.name),destination)
                answers.append(answer)

    for answer in answers:
        if answers != []:
            print(answer)
        else:
            print('I do not know')

def main():
    sents = get_data_from_file()

    cl = ClausIE.get_instance()

    triples = cl.extract_triples(sents)

    for t in triples:
        r = process_relation_triplet(t)

    process_data_from_input_file(file_path='chatbot_data.txt')
    answer_questions(get_question())

if __name__ == '__main__':
    main()
