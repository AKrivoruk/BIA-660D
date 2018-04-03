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
        self.name = name
        self.type = pet_type
        self.owner = owner

    def __repr__(self):
        return self.type

class Trip(object):
    def __init__(self, departs_to, traveler, departs_on=None):
        self.departs_on = departs_on
        self.departs_to = departs_to
        self.traveler = traveler

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

def add_to_likes(likee_token,liker_token):
    likee = add_person(likee_token.text)
    liker = add_person(liker_token.text)
    if likee.name not in liker.likes:
        liker.likes.append(likee.name)

def add_pet_to_person(pet_owner_token, pet_type_token, pet_name_string = None):
    owner = add_person(pet_owner_token.text)
    if pet_type_token.text not in owner.has:
        pet = add_pet(pet_type_token.text, pet_owner_token.text, pet_name_string)
        owner.has.append(pet_type_token.text)
    elif pet_type_token.text in owner.has:
        for animal in pets:
            owner = animal.owner
            if owner.name == pet_owner_token.text:
                animal.name = pet_name_string

def add_trip_to_person(location_token, departure_string, person_token):
    traveler = add_person(person_token.text)
    if location_token.text not in traveler.travels:
        trip = add_trip(location_token.text, person_token.text, departure_string)
    elif location_token.text in traveler.travels:
        for vacation in trips:
            if vacation.traveler == person_token.name:
                vacation.departs_on = departure_string

def select_pet(name, owner):
    for pet in pets:
        if pet.owner == owner:
            return pet

def select_pet_by_name(name):
    for pet in pets:
        if pet.name == name:
            return pet

def add_pet(type, owner_name, name=None):
    pet = None
    pet_owner = select_person(owner_name)
    if name:
        pet = select_pet(name, owner_name)
    if pet is None:
        pet = Pet(type, pet_owner, name)
        pets.append(pet)
    return pet

def select_trip(location_name, person):
    for place in trips:
        if place.traveler == person:
            return place

def add_trip(place, traveler, date = None):
    trip = None
    person = add_person(traveler)
    trip = select_trip(place, traveler)
    if not trip:
        person.travels.append(place)
        trip = Trip(place,traveler,date)
        trips.append(trip)
    return trip

def get_child_with_dep(token, dep):
    for child in token.children:
        if child.dep_ == dep:
            return child

def isLineEmpty(line):
    return len(line.strip()) == 0

def get_data_from_file(file_path='./assignment_01_data.txt'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if (not line.startswith(('$$$', '###', '===')) and not isLineEmpty(line))]
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

dictionary = {'leave':'leave', 'take':'leave', 'fly':'leave', 'go':'leave'}

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
            if child.dep_ == 'neg':
                negative = child
            elif (child.dep_ == 'nsubj' or child.dep_ == 'advmod') and child.pos_ == 'PROPN':
                subject = child
            elif child.dep_ == 'dobj' and child.pos_ == 'PROPN':
                object = child
        if subject and object:
            for pet in pets:
                if pet.name != subject.text and pet.name != object.text:
                    if (not find_compounds(subject) and not find_compounds(object)) and not negative:
                        add_to_likes(object,subject)


    elif verb.lemma_ == 'be':
        2+2
        attr = None
        object_two = None
        object_three = None
        for child in verb.children:

            if child.dep_ == 'nsubj' and child.text == 'name':
                pet_type = get_child_with_dep(child, 'poss')
                pet_owner = get_child_with_dep(pet_type, 'poss')

            elif child.dep_ == 'attr' and child.pos_ == 'PROPN':
                pet_name = child
                if find_compounds(pet_name):
                    prefix = get_child_with_dep(pet_name, 'compound')
                    full_pet_name = prefix.text + ' ' + pet_name.text

            elif child.dep_ == 'attr' and child.text == 'friends':
                attr = child
                with_token = get_child_with_dep(attr, 'prep')
                if with_token and with_token.text == 'with':
                    object = get_child_with_dep(with_token, 'pobj')
                    if get_child_with_dep(object, 'conj'):
                        object_two = get_child_with_dep(object, 'conj')
                        if object_two.pos_ != 'PROPN':
                            object_two = None
                        if get_child_with_dep(object_two, 'conj'):
                            object_three = get_child_with_dep(object_two, 'conj')
                            if object_three.pos_ != 'PROPN':
                                object_three = None
            elif child.dep_ == 'nsubj':
                subject = child
            elif child.dep_ == 'dobj' and child.pos_ == 'PROPN':
                object = child

        if attr and (subject and object and object_two and object_three) and (not find_compounds(subject) and not find_compounds(object) and not find_compounds(object_two) and not find_compounds(object_three)):
            add_to_likes(object, subject)
            add_to_likes(subject, object)
            add_to_likes(object_two, subject)
            add_to_likes(subject, object_two)
            add_to_likes(object_three, subject)
            add_to_likes(subject, object_three)

        elif attr and (subject and object and object_two) and (not find_compounds(subject) and not find_compounds(object) and not find_compounds(object_two)):
            add_to_likes(object, subject)
            add_to_likes(subject, object)
            add_to_likes(object_two, subject)
            add_to_likes(subject, object_two)

        elif attr and (subject and object) and (not find_compounds(subject) and not find_compounds(object)):
            for pet in pets:
                if pet.name == subject.text or pet.name == object.text:
                    break
                else:
                    add_to_likes(object, subject)
                    add_to_likes(subject, object)

        elif full_pet_name and pet_type and pet_owner:
            pet = add_pet_to_person(pet_owner, pet_type, full_pet_name)

        elif pet_name and pet_type and pet_owner:
            pet = add_pet_to_person(pet_owner, pet_type, pet_name.text)
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

        if (subject and object) and not full_pet_name and not pet_name:
            pet = add_pet_to_person(subject, object)

        elif (subject and object) and not full_pet_name:
            pet = add_pet_to_person(subject, object, pet_name.text)

        elif (subject and object) and full_pet_name:
            pet = add_pet_to_person(subject, object, full_pet_name)

        pass
    elif dictionary.get(verb.lemma_):
        2+2
        location = None
        month = None
        date = None
        departure = None
        prep = None
        subject_two = None
        for child in verb.children:
            if (child.dep_ == 'nsubj' or child.dep_ == 'advmod') and child.pos_ == 'PROPN':
                subject = child
                if get_child_with_dep(subject, 'conj'):
                    subject_two = get_child_with_dep(subject, 'conj')
            elif child.text == 'trip':
                to = get_child_with_dep(child, 'prep')
                location = get_child_with_dep(to, 'pobj')
            elif child.text == 'for' or child.text == 'to':
                location = get_child_with_dep(child, 'pobj')
            elif child.dep_ == 'npadvmod':
                departure = child.text
            elif child.dep_ == 'prep' and child.text == 'in':
                departure = get_child_with_dep(child, 'pobj')
            elif child.text == 'on':
                date = get_child_with_dep(child, 'pobj')
                month = get_child_with_dep(date, 'compound')
                departure = month.text + ' ' + date.text

        if subject and not subject_two and location:
            trip_one = add_trip_to_person(location, departure, subject)

        elif subject and subject_two and location:
            trip_one = add_trip_to_person(location, departure, subject)
            trip_two = add_trip_to_person(location, departure, subject_two)

        pass

    else:
        pass

def process_data_from_input_file(path):
    data = get_data_from_file(path)
    for sent in data:
        process_sentence(sent)

def answer_question(question_string):
    doc = nlp(unicode(question_string))
    verb = doc[:].root
    answer = None
    if verb.lemma_ == 'like':
        for child in verb.children:
            if child.dep_ == 'aux':
                aux = child
            elif child.dep_ == 'nsubj':
                subject = child
            elif child.dep_ == 'dobj' and child.pos_ == 'PROPN':
                object = child

        if subject.pos_ == 'PROPN' and object and aux:
            liker = add_person(subject.text)
            answer = liker.likes
            if answer:
                print(answer)

        elif subject.text == 'Who' and subject:
            target = add_person(object.text)
            for person in persons:
                if target.name in person.likes:
                    answer = person.name
                    print(answer)

        elif aux and subject.pos_ == 'PROPN' and object:
            liker = add_person(subject.text)
            likee = add_person(object.text)
            for person in persons:
                if likee.name in liker.likes:
                    answer = 'Yes'
                    print(answer)

    elif verb.lemma_ == 'have':
        for child in verb.children:
            if child.dep_ == 'dobj' and (child.text == 'dog' or child.text == 'cat'):
                object = child
                for pet in pets:
                    if object.text == pet.type:
                        answer = pet.owner
                        print(answer)

    elif dictionary[verb.lemma_] == 'leave':
        for child in verb.children:
            if child.dep_ == 'advmod':
                advmod = child
            elif child.dep_ == 'nsubj':
                subject = child
            elif child.dep_ == 'prep' and child.text == 'to':
                destination = get_child_with_dep(child, 'pobj')

        if subject.pos_ == 'PROPN' and destination and advmod:
            traveler = add_person(subject)
            for trip in trips:
                if trip.traveler == traveler.name and trip.departs_to == destination.text:
                    answer = trip.departs_on
                    print(answer)

        if subject.text == 'Who' and destination:
            for trip in trips:
                if trip.departs_to == destination.text:
                    answer = trip.traveler
                    print(answer)

    if not answer:
        print('I do not know.')

    pass

def main():
    process_data_from_input_file('assignment_01_data.txt')
    answer_question('Who likes Mary?')

if __name__ == '__main__':
    main()
