import pandas as pd

def ipaV4(word):
    ipa = ''
    word += '£'
    i = 0
    setV = ['a', 'ä', 'e', 'ë', 'i', 'o', 'ö', 'u', 'ü']
    ipaDict = { 'ä': 'æ', 'e': 'ɛ', 'ë': 'ə', 'o': 'ɔ', 'ö': 'œ', 'u': 'ʊ',
                'ü': 'y', 't': 't̪', 'd': 'd̪', '\'': 'Ɂ', 'ţ': 'θ', 'đ': 'ð',
                'š': 'ʃ', 'ž': 'ʒ', 'l': 'l̪', 'ḷ': 'ɬ', 'c': 'ʦ', 'ẓ': 'ʣ',
                'č': 'ʧ', 'j': 'ʤ', 'ň': 'ŋ', 'r': 'ɾ', 'ř': 'ʁ', 'y': 'j',
                'ì': 'iː', 'ù': 'w', '-': '-'}
    #remove stress and correct
    newWord = ''
    while i < len(word):
        correctDict = {'ṭ': 'ţ', 'ŧ': 'ţ', 
                       'ḍ': 'đ', 'ḑ': 'đ', 
                       'n͕': 'ň', 'ṇ': 'ň',
                       'r͕': 'ř', 'ṛ': 'ř',
                       'ł': 'ḷ', 'l͕': 'ḷ'}
        newWord += correctDict.get(word[i], '') if word[i] in correctDict else ''
        stressDict = {'á': '%a', 'â': '%ä', 'é': '%e',
                    'ê': '%ë', 'í': '%i', 'ó': '%o',
                    'ô': '%ö', 'ú': '%u', 'û': '%ü'}
        newWord += stressDict.get(word[i], '') if word[i] in stressDict else word[i]
        i += 1
    word = newWord
    i = 0

    while i < len(word)-1:
        i += 1
        l1 = word[i-1]
        l2 = word[i]
        #vowel exceptions
        if l1 == '%':
            ipa += '\''
        elif l1 in 'eioöu' and l2 in setV:
            biconj = {'e': 'e', 'i': 'i', 'o': 'o', 'ö': 'ø', 'u': 'u'}
            if l1 in biconj:
                ipa += biconj.get(l1, '')
        elif l1 in 'yw' and l2 == 'ü':
            ipa += l1 + 'ʉ'
            i += 1
        elif l1 == 'y' and l2 == 'i':
            ipa += 'jɪ'
            i += 1
        elif l1 == 'i' and l2 == 'y':
            ipa += 'ɪj'
            i += 1
        #consonant exceptions
        elif l1 in 'ptkcč' and l2 == 'h':
            ipa += l1 + 'ʰ'
            i += 1
        elif l1 == 'r' and l2 == 'r':
            ipa += 'r'
            i += 1
        elif l1 == 'n' and l2 in 'kgx':
            ipa += 'ŋ' + l2
            i += 1
        elif l1 == 'h' and l2 in 'lrmn':
            i += 1
            if l2 == 'l':
                ipa += 'ɬ'
            if l2 == 'r':
                ipa += 'ɾ̥'
            if l2 == 'm':
                ipa += 'm̥'
            if l2 == 'n':
                ipa += 'n̥'
        #expected vow/cons
        elif l1 in ipaDict:
            ipa += ipaDict.get(l1, '')
        elif l1 in 'aipkgbfmsvwzçxnh':
            ipa += l1
    #check geminates
    ipaNew = ''
    i = 0
    ipa += '£'
    while i < len(ipa)-1:
        i += 1
        l1 = ipa[i-1]
        l2 = ipa[i]
        ipaNew += l1 + 'ː' if l1 == l2 else l1
        i += 1 if l1 == l2 else 0

    return ipaNew

SHEET_ID = 'https://docs.google.com/spreadsheets/d/1OAHj-sbg7FS1Q4YQDjdk8joePP7BKE6tgkqApaBVpAg'
categories = pd.read_csv(f'{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Categories')

def getCategory(abbrev):
  text = ''
  for _, line in categories.iterrows():
    if abbrev == line.iloc[0] or abbrev.lower() == line.iloc[1].lower():
      text += '**' + line.iloc[0] + '**: ' + line.iloc[1] + '\n'
      text += line.iloc[3]
      return text 
  return 'Couldn\'t find the category.'