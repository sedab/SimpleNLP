# NegEx

import re

####################################################################################

def negation_scope(sentence) :
  sentence = sentence.lower()
  sentence = re.sub("\s+",' ',str(sentence))
  words = []
  for word in sentence.split() :
    word = re.sub('\W','',word) # get rid of non [Aa-Zz0-9] characters
    words.append(word)
  return word_iterator(words,0)

####################################################################################

def word_iterator(string,index) :
  word_length = len(string)
  if index < word_length :
    for i in range(index,word_length) :
      #print('pseudo')
      pseudo_index = contains_at_index(string,phrase['pseudo'],i)
      if pseudo_index :
        return word_iterator(string,pseudo_index)
      else :
        #print('negation')
        negation_index = contains_at_index(string,phrase['negation'],i)
        if negation_index :
          conjunction_index = 0
          for j in range(negation_index,word_length) :
            #print('conjunctions')
            conjunction_index = contains_at_index(string,phrase['conjunctions'],j)
            if conjunction_index : break
          if conjunction_index :
            return [negation_index,conjunction_index]
          elif negation_index >= word_length-1 :
            return [0,word_length-1]
          else :
            return [negation_index,word_length-1]
        else :
          #print('post')
          post_index = contains_at_index(string,phrase['post'],i)
          if post_index :
            return [0,post_index]
  return 0
  
def contains_at_index(string,phrase_list,index) :
  word_count = len(string)
  for phrase in phrase_list :
    phrase_words = []
    for i in phrase.split() :
      i.replace("\W","")
      phrase_words.append(i)
    if len(phrase_words) == 1 :
      if string[index] == phrase_words[0] :
        return index+1
    else :
      if word_count - index >= len(phrase_words) and string[index] == phrase_words[0] :
        counts = 1
        for i in range(1,len(phrase_words)) :
          if string[index+i] == phrase_words[i] :
            counts+= 1
          else :
            counts = 0
            break
          if counts == len(phrase_words) :
            return index+i+1
  return 0

####################################################################################

phrase = {
  'pseudo' : [
    'no increase',
    'no change',
    'no suspicious change',
    'no significant change',
    'no interval change',
    'no definite change',
    'not extend',
    'not cause',
    'not drain',
    'not significant interval change',
    'not certain if',
    'not certain whether',
    'gram negative',
    'without difficulty',
    'not necessarily',
    'not only',
  ],
  'post' : [
    'should be ruled out for',
    'ought to be ruled out for',
    'may be ruled out for',
    'might be ruled out for',
    'could be ruled out for',
    'will be ruled out for',
    'can be ruled out for',
    'must be ruled out for',
    'is to be ruled out for',
    'be ruled out for',
    'unlikely',
    'free',
    'was ruled out',
    'is ruled out',
    'are ruled out',
    'have been ruled out',
    'has been ruled out',
    'being ruled out',
    'should be ruled out',
    'ought to be ruled out',
    'may be ruled out',
    'might be ruled out',
    'could be ruled out',
    'will be ruled out',
    'can be ruled out',
    'must be ruled out',
    'is to be ruled out',
    'be ruled out',
  ],
  'conjunctions' : [
    'but',
    'however',
    'nevertheless',
    'yet',
    'though',
    'although',
    'still',
    'aside from',
    'except',
    'apart from',
    'secondary to',
    'as the cause of',
    'as the source of',
    'as the reason of',
    'as the etiology of',
    'as the origin of',
    'as the cause for',
    'as the source for',
    'as the reason for',
    'as the etiology for',
    'as the origin for',
    'as the secondary cause of',
    'as the secondary source of',
    'as the secondary reason of',
    'as the secondary etiology of',
    'as the secondary origin of',
    'as the secondary cause for',
    'as the secondary source for',
    'as the secondary reason for',
    'as the secondary etiology for',
    'as the secondary origin for',
    'as a cause of',
    'as a source of',
    'as a reason of',
    'as a etiology of',
    'as a cause for',
    'as a source for',
    'as a reason for',
    'as a etiology for',
    'as a secondary cause of',
    'as a secondary source of',
    'as a secondary reason of',
    'as a secondary etiology of',
    'as a secondary origin of',
    'as a secondary cause for',
    'as a secondary source for',
    'as a secondary reason for',
    'as a secondary etiology for',
    'as a secondary origin for',
    'cause of',
    'cause for',
    'causes of',
    'causes for',
    'source of',
    'source for',
    'sources of',
    'sources for',
    'reason of',
    'reason for',
    'reasons of',
    'reasons for',
    'etiology of',
    'etiology for',
    'trigger event for',
    'origin of',
    'origin for',
    'origins of',
    'origins for',
    'other possibilities of',
  ],
  'negation' : [
    'absence of',
    'cannot see',
    'cannot',
    'checked for',
    'declined',
    'declines',
    'denied',
    'denies',
    'denying',
    'evaluate for',
    'fails to reveal',
    'free of',
    'negative for',
    'never developed',
    'never had',
    'no',
    'no abnormal',
    'no cause of',
    'no complaints of',
    'no evidence',
    'no new evidence',
    'no other evidence',
    'no evidence to suggest',
    'no findings of',
    'no findings to indicate',
    'no mammographic evidence of',
    'no new',
    'no radiographic evidence of',
    'no sign of',
    'no significant',
    'no signs of',
    'no suggestion of',
    'no suspicious',
    'not',
    'not appear',
    'not appreciate',
    'not associated with',
    'not complain of',
    'not demonstrate',
    'not exhibit',
    'not feel',
    'not had',
    'not have',
    'not know of',
    'not known to have',
    'not reveal',
    'not see',
    'not to be',
    'patient was not',
    'rather than',
    'resolved',
    'test for',
    'to exclude',
    'unremarkable for',
    'with no',
    'without any evidence of',
    'without evidence',
    'without indication of',
    'without sign of',
    'without',
    'rule out for',
    'rule him out for',
    'rule her out for',
    'rule the patient out for',
    'rule him out',
    'rule her out',
    'rule out',
    'r/o',
    'ro',
    'rule the patient out',
    'rules out',
    'rules him out',
    'rules her out',
    'ruled the patient out for',
    'rules the patient out',
    'ruled him out against',
    'ruled her out against',
    'ruled him out',
    'ruled her out',
    'ruled out against',
    'ruled the patient out against',
    'did rule out for',
    'did rule out against',
    'did rule out',
    'did rule him out for',
    'did rule him out against',
    'did rule him out',
    'did rule her out for',
    'did rule her out against',
    'did rule her out',
    'did rule the patient out against',
    'did rule the patient out for',
    'did rule the patient out',
    'can rule out for',
    'can rule out against',
    'can rule out',
    'can rule him out for',
    'can rule him out against',
    'can rule him out',
    'can rule her out for',
    'can rule her out against',
    'can rule her out',
    'can rule the patient out for',
    'can rule the patient out against',
    'can rule the patient out',
    'adequate to rule out for',
    'adequate to rule out',
    'adequate to rule him out for',
    'adequate to rule him out',
    'adequate to rule her out for',
    'adequate to rule her out',
    'adequate to rule the patient out for',
    'adequate to rule the patient out against',
    'adequate to rule the patient out',
    'sufficient to rule out for',
    'sufficient to rule out against',
    'sufficient to rule out',
    'sufficient to rule him out for',
    'sufficient to rule him out against',
    'sufficient to rule him out',
    'sufficient to rule her out for',
    'sufficient to rule her out against',
    'sufficient to rule her out',
    'sufficient to rule the patient out for',
    'sufficient to rule the patient out against',
    'sufficient to rule the patient out',
    'what must be ruled out is',
  ],
}
