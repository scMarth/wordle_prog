# suggested first guesses: FLAME, BRICK, PODGY, SHUNT

import enchant, sys

'''
    {'word': 'flame', 'green': '', 'orange': ''},
    {'word': 'brick', 'green': '', 'orange': ''},
    {'word': 'podgy', 'green': '', 'orange': ''},
    {'word': 'shunt', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''}


'''

word_guesses = [
    # green and orange store the position of the letters (1 being the first letter)
    {'word': 'flame', 'green': '5', 'orange': ''},
    {'word': 'brick', 'green': '', 'orange': '1'},
    {'word': 'podgy', 'green': '', 'orange': '2'},
    {'word': 'shunt', 'green': '', 'orange': '1'},
    {'word': 'dwelt', 'green': '3', 'orange': ''},
    {'word': 'tabby', 'green': '', 'orange': '3'},
    {'word': 'party', 'green': '', 'orange': ''},
    {'word': 'usurp', 'green': '', 'orange': '2'},
    {'word': 'undue', 'green': '5', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''},
    {'word': '', 'green': '', 'orange': ''}
]

word_template = ['', '', '', '', '']

known_letters = {}

alphabet = 'abcdefghijklmnopqrstuvwxyz'

possible_letters_template = [alphabet, alphabet, alphabet, alphabet, alphabet]

known_letters = {}

for guess in word_guesses:
    word = guess['word']
    greens = guess['green']
    oranges = guess['orange']

    if not word:
        continue

    print(word.upper())
    found_letters = {}

    if greens:
        for green in greens:
            position = int(green) - 1
            letter = word[position]

            possible_letters_template[position] = letter

            if letter not in found_letters:
                found_letters[letter] = 0
            found_letters[letter] += 1
        
    if oranges:
        for orange in oranges:
            position = int(orange) - 1

            letter = word[position]
            possible_letters_template[position] = possible_letters_template[position].replace(letter, '')

            if letter not in found_letters:
                found_letters[letter] = 0
            found_letters[letter] += 1
    
    for i in range(0, len(word)):
        if str(i+1) not in greens and str(i+1) not in oranges: # gray letter found
            
            letter = word[i]

            for j in range(0, len(possible_letters_template)):
                possible_letters_template[j] = possible_letters_template[j].replace(letter, '')
    
    for letter in found_letters:
        if letter in known_letters:
            known_letters[letter] = max(known_letters[letter], found_letters[letter])
        else:
            known_letters[letter] = found_letters[letter]

print('\npossible letters template: {}\n'.format(possible_letters_template))
print('\nknown letters: {}\n'.format(known_letters))

for letters in possible_letters_template:
    # if there is only one possible letter for that position, we know the position for the letter in known_letters
    if len(letters) == 1:
        known_letters[letters] -= 1
        if known_letters[letters] == 0:
            del known_letters[letters]

# by now, known_letters should only store letters whose letters we know are in the word but do not know the position of
print('known letters with unknown positions: {}'.format(known_letters))
print('processing combinations from templates...')

complete_combinations = 0
stack = [[possible_letters_template, known_letters]]

while len(stack) != complete_combinations:
    template, knowns = stack.pop(0)
    # print('popping:')
    # print('\ttemplate: {}'.format(template))
    # print('\tknowns: {}'.format(knowns))
    # print('')

    if knowns == {}:
        complete_combinations += 1
        # print('complete combination: {}'.format(complete_combinations))
        
        stack.append([list(template), dict(knowns)])
        # print('pushing:')
        # print('\t{}'.format(template))
        # print('\t{}'.format(knowns))
        # print('')
        continue
    
    for i in range(0, len(template)):
        for known in knowns:
            if known in template[i]:
                # if it's possible that the known letter can be in this position

                # create a copy of knowns to push to the staack
                push_knowns = dict(knowns)
                push_knowns[known] -= 1
                if push_knowns[known] == 0:
                    del push_knowns[known]
                
                push_template = list(template)
                push_template[i] = known

                stack.append([push_template, push_knowns])
                # print('pushing:')
                # print('\t{}'.format(push_template))
                # print('\t{}'.format(push_knowns))
                # print('')

print('completed combinations with known letters, reducing templates...')

# reduce templates to a single letter for every position
reduced_templates = 0

while len(stack) != reduced_templates:
    template, knowns = stack.pop(0)
    
    if knowns != {}:
        print('failed to simplify template with known letters:')
        print('\ttemplate: {}'.format(template))
        print('\tknowns: {}'.format(knowns))
        sys.exit()
    
    # check if any position in the template still has more than 1 possibility, if so, we need to iterate over all possibilities and push it back into the list. if all positions only have 1 letter, then mark it as complete

    all_letters_simplified = True

    for i in range(0, len(template)):
        letters = template[i]

        if len(letters) > 1:
            all_letters_simplified = False
            for j in range(0, len(letters)):
                push_template = list(template)
                push_template[i] = letters[j]
                stack.append([push_template, {}])
            
    if all_letters_simplified:
        reduced_templates += 1
        stack.append([list(template), {}])
    
dictionary = enchant.Dict("en_US")
results = []


# iterate over the fully simplified templates, if the word is an English word, put it in the list of results
# print('all letters simplified:')
for template, _ in stack:

    current_word = ''.join(template)

    if dictionary.check(current_word):
        if current_word not in results:
            results.append(current_word)

print('\nsuggestions:')
# print results
for word in results:
    print('\t{}'.format(word))
print('')