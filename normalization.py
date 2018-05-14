import re
import nltk
import string
from nltk.stem import WordNetLemmatizer
from pattern.en import tag
from nltk.corpus import wordnet as wn
# from nltk.tag.stanford import StanfordPOSTagger as POS_Tag

class Normalizer :

    stopword_list = open ('res/stop_words.txt','r').read().strip('\n')
    stemmer = nltk.ISRIStemmer()

    def tokenize_text(self,text):
        tokens = nltk.word_tokenize(text)
        tokens = [token.strip() for token in tokens]
        return tokens

    def stemming_text(self,text):
        tokens = self.tokenize_text(text)
        filtered_tokens = [self.stemmer.stem(token) for token in tokens]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    def remove_special_characters(self,text):
        def remove_conjunction(token):
            if token[0] == 'و' and len(token) > 4:
                t = token[1:len(token)]
                return t
            else:
                return token
        tokens = self.tokenize_text(text)
        pattern = re.compile(r'[?|.|:|;|,|"|\d|$|&|*|%|@|(|)|~]'.format(re.escape(string.punctuation)))
        filtered_tokens = filter(None, [pattern.sub('',remove_conjunction(token)) for token in tokens])
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    def remove_stopwords(self,text):
        tokens = self.tokenize_text(text)
        filtered_tokens = [token for token in tokens if token not in self.stopword_list]
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text

    def remove_repeated_characters(self,text):
        tokens = self.tokenize_text(text)
        repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
        match_substitution = r'\1\2\3'
        def replace(old_word):
            if wn.synsets(old_word):
                return old_word
            new_word = repeat_pattern.sub(match_substitution, old_word)
            return replace(new_word) if new_word != old_word else new_word

        correct_tokens = [replace(word) for word in tokens]
        filtered_text = ' '.join(correct_tokens)
        return filtered_text

    def normalize_corpus(self,corpus):
        normalized_corpus = []
        for text in corpus:
            text = self.remove_special_characters(text)
            text = self.remove_stopwords(text)
            text = self.remove_repeated_characters(text)
            text = self.stemming_text(text)
            text = self.remove_stopwords(text)
            normalized_corpus.append(text)
        return normalized_corpus

# #-----------------------------------------------
# # Annotate text tokens with POS tags
# def pos_tag_text(text):
#
#     def penn_to_wn_tags(pos_tag):
#         if pos_tag.startswith('J'):
#             return wn.ADJ
#         elif pos_tag.startswith('V'):
#             return wn.VERB
#         elif pos_tag.startswith('N'):
#             return wn.NOUN
#         elif pos_tag.startswith('R'):
#             return wn.ADV
#         else:
#             return None
#
#     tagged_text = tag(text)
#     tagged_lower_text = [(word.lower(), penn_to_wn_tags(pos_tag))
#                          for word, pos_tag in
#                          tagged_text]
#     return tagged_lower_text
#
# # lemmatize text based on POS tags
    # wnl = WordNetLemmatizer()
# def lemmatize_text(text):
#
#     pos_tagged_text = pos_tag_text(text)
#     lemmatized_tokens = [wnl.lemmatize(word, pos_tag) if pos_tag
#                          else word
#                          for word, pos_tag in pos_tagged_text]
#     lemmatized_text = ' '.join(lemmatized_tokens)
#     return lemmatized_text
# from contractions import CONTRACTION_MAP
# def expand_contractions(text, contraction_mapping):
#
#     contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
#                                       flags=re.IGNORECASE|re.DOTALL)
#     def expand_match(contraction):
#         match = contraction.group(0)
#         first_char = match[0]
#         expanded_contraction = contraction_mapping.get(match)\
#                                 if contraction_mapping.get(match)\
#                                 else contraction_mapping.get(match.lower())
#         expanded_contraction = first_char+expanded_contraction[1:]
#         return expanded_contraction
#
#     expanded_text = contractions_pattern.sub(expand_match, text)
#     expanded_text = re.sub("'", "", expanded_text)
#     return expanded_text
# #-----------------------------------------------
