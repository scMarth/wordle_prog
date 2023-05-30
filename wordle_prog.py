# suggested first guesses: FLAME, BRICK, PODGY, SHUNT

import enchant, sys

# letters in the right spot
green_letters = {
    0 : 's',
    1 : '',
    2 : 'u',
    3 : '',
    4 : ''
}

# letters in the word but in the wrong location
orange_letters = {
    0 : 'bc',
    1 : 'au',
    2 : 'a',
    3 : 'cs',
    4 : ''
}

# letters not in the word
gray_letters = 'flmerikpodgyhntrkeliklideleeplmymrkyootyeldletffpohlthehoneydirydowry'

# validate green letters
for pos in green_letters:
    if len(green_letters[pos]) > 1:
        print('Position {} should only have 1 letter. Aborting.'.format(pos))
        sys.exit()

alphabet = 'abcdefghijklmnopqrstuvwxyz'

leftover_letters = [x for x in alphabet if x not in gray_letters]


word_template_list = []
word_template = ['', '', '', '', '']

for pos in green_letters:

    letter = green_letters[pos]
    if letter:
        word_template[pos] = letter


print('\nformats:')
for pos in orange_letters:
    letters = orange_letters[pos]
    if letters:

        for word_template_pos in orange_letters:
            if not word_template[word_template_pos] and pos != word_template_pos:

                for l in letters:

                    new_possible_word = list(word_template)
                    new_possible_word[word_template_pos] = l
                    print('\t{}'.format(new_possible_word))
                    word_template_list.append(new_possible_word)


possible_words = []

while word_template_list:
    word = word_template_list.pop()

    word_template_complete = True

    for i in range(0, len(word)):
        if not word[i]:

            word_template_complete = False

            for x in leftover_letters:

                push_word = list(word)
                push_word[i] = x

                word_template_list.append(push_word)

    if word_template_complete:
        possible_words.append(word)
    
dictionary = enchant.Dict("en_US")
results = []

# iterate over possible words and print it if it is in the dictionary
for word in possible_words:
    current_word = ''.join(word) # combine the word from the template that has the list of characters

    if dictionary.check(current_word):
        if current_word not in results:
            results.append(current_word)

print('\nsuggestions:')
# print results
for word in results:
    print('\t{}'.format(word))

print()






