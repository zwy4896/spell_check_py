#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spell.py
@Time    :   2020/04/30 11:35:04
@Author  :   zwy4896
@Version :   1.0
'''

# here put the import lib


# here put the import lib
import os
import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

def P(word): 
    "Probability of `word`."
    return WORDS[word] / sum(WORDS.values())

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz0123456789'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def correctTxt(txtFile):
    txt_dict = {}
    with open (txtFile, 'r' , encoding='utf8') as f:
        for line in f:
            txt_dict[line.split('$$$')[0]] = line.split('$$$')[1].strip()
    return txt_dict

def correctWords(coord, line):
    text_list = []
    # for word in text.lower().split(' '):
    #     print(word, correction(word))
    for word in line.lower().split(' '):
        text_list.append(correction(word))
        # print('{}$$${}'.format(coord, t))
    return text_list
if __name__ == '__main__':
    # File that you want to check
    txt_dir = ''
    WORDS = Counter(words(open('./big.txt').read()))
    # correct_txt = open('/algdata02/wuyang.zhang/spellCheck/A41_correct.txt', 'w', encoding='utf8')
    # print(correction('next apu'))
    # txt = '/algdata02/wuyang.zhang/det_rec_inference_tf/test/0424-test-final/txt/A41_0424_五楼调试.txt'
    for root, dirs, files in os.walk(txt_dir):
        for file in files:
            print(file)
            correct_txt = open(os.path.join('PATH_TO_CHECKED_TXT', file), 'w', encoding='utf8')
            txt = os.path.join(txt_dir, file)
            txt_dict = correctTxt(txt)
            for coord in txt_dict:
                correct_list = correctWords(coord, txt_dict[coord])
                correct_txt.write('{}$$${}\n'.format(coord, ' '.join(correct_list)))
                # print('{}$$${}'.format(coord, ' '.join(correct_list)))
            correct_txt.close()