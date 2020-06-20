import re
from textblob import TextBlob
from NegEx import negation_scope
 
class processor :
 
######################################################################
 
  def __init__(self,config) :
          self.target_phrases = config.get('target_phrases') or []
          self.skip_phrases = config.get('skip_phrases') or []
            
          #self.start_phrase = config.get('start_phrase') or ''
          #sb, 061320
          self.start_phrase = config.get('start_phrase') or []
          self.absolute_negative_phrases = config.get('absolute_negative_phrases') or []
          self.absolute_positive_phrases = config.get('absolute_positive_phrases') or []
 
          self.orig_text = ''
          self.final_answer = ''
          self.ambiguous = ''
 
          self.target_sentences = dict()
          self.negex_debug = dict()
 
######################################################################
 
  def process_text(self,text) :
          self.orig_text = text
          self.examine_text()
          return self.final_answer
 
  def examine_text(self) :
          text = self.orig_text
          if not text : return
          
          start_phrase = self.start_phrase
           
          for sp in start_phrase:
            regex = re.compile(re.escape(sp)+'\s+(\w.*)\Z',re.I)
            match = re.search(regex,str(text))
            if match : 
              #print('match')
              text = str(match.group(1))
              break  
        
          text = re.sub("\s+",' ',str(text)) # flattens all spaces to only one character
          #sb, 041520
          #text = re.sub(':','.',text) # treat colon ':' like a period '.'
 
          TB_obj = TextBlob(text)
          sentences = TB_obj.sentences if TB_obj else []
          for sentence in sentences :
            skip = 0
            for s_p  in self.skip_phrases :
              regex = re.compile(r'\b'+s_p+r'\b',re.I)
              if re.search(regex,str(sentence)) :
                skip = 1
                break
            if skip : continue # skip phrase matched, go to next sentence
 
            target_match = 0
            for t_p in self.target_phrases :
              regex = re.compile(r'\b'+t_p+r'\b',re.I)
              if re.search(regex,str(sentence)) :
                target_match = 1
                break
            if not target_match : continue # no target phrase matched, go to next sentence
 
            self.target_sentences[str(sentence)] = 'present'
            n_scope = negation_scope(sentence)
            if n_scope :
              self.negex_debug[str(sentence)] = str(n_scope[0])+' - '+str(n_scope[1])
              words = []
              for word in sentence.split() :
                word = re.sub("\W","",word)
                words.append(word)
 
              negated = 0
              for negation_index in range(n_scope[0],n_scope[1]+1) :
                if negation_index == len(words) : continue
                for t_p in self.target_phrases :
                  if len(t_p.split()) > 1 :
                  # target phrase has more than one word
                  # only use the first word for matching
                    t_p = t_p.split()[0]
                  regex = re.compile(r'\b'+t_p+r'\b',re.I)
                  if re.search(regex,words[negation_index]) :
                    self.target_sentences[str(sentence)] = 'absent'
                    negated = 1
                    break
                if negated > 0 : break
 
          if len(self.target_sentences) > 0 :
            final_answer = dict()
            for sentence, answer in self.target_sentences.items() :
              final_answer[answer] = final_answer[answer]+1 if final_answer.get(answer) else 1
              self.final_answer = answer
              if len(final_answer) > 1 :
                self.ambiguous = 1
                if not final_answer['absent'] :  final_answer['absent'] = 0
                if not final_answer['present'] : final_answer['present'] = 0
                if final_answer['absent'] > final_answer['present'] :
                  self.final_answer = 'absent'
                elif final_answer['present'] > final_answer['absent'] :
                  self.final_answer =  'present'
                else :
                  # There are an equal number of absent/present findings - defaulting to present
                  self.final_answer = 'present'
          else :
            self.final_answer = 'absent'
 
          for abs_positive in self.absolute_positive_phrases :
            regex = re.compile(r'\b'+abs_positive+r'\b',re.I)
            if re.search(regex,text) :
              if self.final_answer == 'absent' :
                self.ambiguous = 3
              self.final_answer = 'present'
 
          for abs_negative in self.absolute_negative_phrases :
            regex = re.compile(r'\b'+abs_negative+r'\b',re.I)
            if re.search(regex,text) :
              if self.final_answer == 'present' :
                self.ambiguous = 2
              self.final_answer = 'absent'
 
 
  def ambiguous_readable(self) :
    out = ''
    if self.ambiguous == 1 :
      out = 'Yes. Target phrase was present and absent in different sentences.'
    elif self.ambiguous == 2 :
      out = 'Absolute negative phrase matched but the answer was going to be present otherwise.'
    elif self.ambiguous == 3 :
      out = 'Absolute positive phrase matched but the answer was going to be absent otherwise.'
    else :
      out = 'No'
    return out
 
  def debug(self) :
          sentences = []
          negex = []
          for k,v in self.target_sentences.items() :
            sentences.append(str(k)+" : "+str(v))
          for k,v in self.negex_debug.items() :
            negex.append(str(k)+" : Negated between word indexes: "+str(v))
          return "Sentences with target phrase match:\r\n"+"\r\n".join(sentences)+"\r\n\r\nNegated Sentences:\r\n"+"\r\n".join(negex)
 
  def config(self) :
          out = 'Target Phrases: '+str(self.target_phrases)+"\r\n\r\n"
          out += 'Skip Phrases: '+str(self.skip_phrases)+"\r\n\r\n"
          out += 'Start Phrase: '+str(self.start_phrase)+"\r\n\r\n"
          out += 'Absolute Positive Phrases: '+str(self.absolute_positive_phrases)+"\r\n\r\n"
          out += 'Absolute Negative Phrases: '+str(self.absolute_negative_phrases)+"\r\n\r\n"
          return out
 
  def reset(self) :
          self.orig_text = ''
          self.target_sentences = dict()
          self.final_answer = ''
          self.ambiguous = ''
