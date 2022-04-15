"""
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
#print(sys.path)
"""

import nltk
from language.wikipage import WikiPage
from language.google_page import GooglePage
from actions import actions
from logic import logic_graph

current_concept = None

def branch(words):
  """
    This initial filter of our input sentence.
    It tokenizes the words and tags the words with parts of speech.
    It then passes the tokenized and tagged words to 1 of 3 functions.
    A sentence is either declarative() , interrogative() , or imperative()

    Args:
      words (String): The words inputted by the user
    Returns:
      String: response from one of the three functions that handle type of sentences.
  """
  parts_of_speech =  nltk.pos_tag(nltk.word_tokenize(words))
  leading_word = parts_of_speech[0][1][0]
  if leading_word == 'W':
    return interrogative(parts_of_speech[1:])
  elif leading_word == "V":
    return imperative(parts_of_speech)
  else:
    declarative(parts_of_speech)


def interrogative(remaining_words):
  """
    Function that handles interrogative senteces
  """
  global current_concept
  leading_word = remaining_words[0][1][0]
  while leading_word == "D" or leading_word == "V" and len(remaining_words) > 0:
    remaining_words.pop(0)
    leading_word = remaining_words[0][1][0]
  else:
    concept_list = [word[0] for word in remaining_words if word[1] != "."]
    concept = " ".join(concept_list)

    current_concept = GooglePage(concept)
    if current_concept.summary:
      return current_concept.summary

    current_concept = WikiPage(concept)
    if len(current_concept.summary) > 0 and "IN" not in dict(remaining_words).values():
      return current_concept.summary
    # The concept is a nested concept.
    elif "IN" in dict(remaining_words).values():
      return nested_concept(remaining_words)
    else:
      return "I don't know"


def imperative(words):
  """
    Handles imperative sentences.
  """
  return actions.pick_action(words[0][0], words)


def declarative(words):
  """
    Handles declarative sentences.
  """
  # Pick up an incorrectly tagged action
  if words[0][0] in actions.actions_dictionary.keys():
    return actions.pick_action(words[0][0], words)
  logic_graph.pos_insertion(words)


def nested_concept(remaining_words):
  remaining_words = remove_extraneous_words(remaining_words)
  in_found = False
  search_term = ""
  concept = ""
  for word in remaining_words:
    if word[1] == "IN":
      in_found = True
    else:
      if in_found:
        concept += word[0]
        concept += " "
      else:
        search_term += word[0]
        search_term += " "
  concept_base = WikiPage(concept)
  matching_sentences = " ".join(WikiPage(concept).search(search_term)[:4])
  return matching_sentences

def remove_extraneous_words(remaining_words):
  cleaned_words = []
  for word in remaining_words:
    if word[1][0] != "D":
      cleaned_words.append(word)
  return cleaned_words

def return_nouns(remaining_words):
  return [x for x in remaining_words if x[1][0] == "N"]


def action(remaining_words):
  print (remaining_words)
