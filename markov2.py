from sys import argv
import random

class SimpleMarkovGenerator(object):

    def __init__(self, length = 300):
        self.length = length


    def combine_files(self, filenames_list):
        """Takes input arguments(file names) and returns a big long list"""

        combined_list = []
        
        for filename in filenames_list[1:]:
            corpus_file = open(filename).read().rstrip()
            cleaner_list = corpus_file.replace("\n", " ")
            even_cleaner_list = cleaner_list.replace("\r", "")
            corpus_list = even_cleaner_list.split(" ")
            combined_list.extend(corpus_list)

        return combined_list


    def make_chains(self, corpus_list):
        """Takes input text as a list; returns dictionary of markov chains."""
        
        corpus_dict = {}

        #define the end case (2nd to last, last)
        last_key = (corpus_list[-2], corpus_list[-1])
        corpus_dict[last_key] = [corpus_list[0]]

        #define the wraparound case (end to beginning)
        last_first_key = (corpus_list[-1], corpus_list[0])
        corpus_dict[last_first_key] = [corpus_list[1]]

        for i in range(len(corpus_list)-2):
            key = (corpus_list[i], corpus_list[i+1])
            if key not in corpus_dict:
                corpus_dict[key] = [corpus_list[i+2]]
            else:
                corpus_dict[key].append(corpus_list[i+2])
        
        #to print a test dictionary, uncomment the two lines bellow        
        # for key, value in corpus_dict.items():
        #     print key, value   

        return corpus_dict #returns a dictionary object


    def make_text(self, chains):
        """Takes dictionary of markov chains; returns random text."""
        output_text = ""
        random_key = random.choice(chains.keys())

        #populate the first tuple and make sure it's not empty
        random_word = random.choice(chains[random_key])
        

        if random_word == "":
            random_word = random.choice(chains[random_key])
        else:
            first_letter = random_word[0]

        while first_letter.islower():

            random_key = random.choice(chains.keys())
            random_word = random.choice(chains[random_key])        
            if random_word == "":
                random_word = random.choice(chains[random_key])
            else:
                first_letter = random_word[0]

        key_word_tuple = (random_key[0], random_key[1], random_word)
        output_text = "%s %s %s" %( key_word_tuple[0].title(), key_word_tuple[1], key_word_tuple[2])

        #until the tuple is empty, keep re-populating the three-word tuple
        while len(output_text) < self.length:
            new_key = (key_word_tuple[1], key_word_tuple[2])
            random_word = random.choice(chains[new_key])
            key_word_tuple = (new_key[0], new_key[1], random_word)
            output_text = "%s %s" %(output_text, random_word)

        return output_text #returns a string object

    def end_at_punct(self, markov_text):
        """Takes a string object and cleans up the end; returns a string"""
        output_text = markov_text
        #eats the end of the text until it reaches an acceptable char.
        output_text = output_text.rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:;()- \,\'')
        if len(output_text) > 140:
            output_text = output_text[:-1]
            output_text = output_text.rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:;()- \,\'')

        return output_text #returns a string object


###################################################
def create_markov():
    my_markov = SimpleMarkovGenerator(300)
    my_markov_list = my_markov.combine_files(argv)
    my_markov_diction = my_markov.make_chains(my_markov_list)
    my_markov_text = my_markov.make_text(my_markov_diction)
    return my_markov.end_at_punct(my_markov_text)

markov = create_markov()

while len(markov) <= 5:
    markov = create_markov()

print markov