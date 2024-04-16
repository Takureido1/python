import pandas as pd

SHEET_ID = 'https://docs.google.com/spreadsheets/d/1OAHj-sbg7FS1Q4YQDjdk8joePP7BKE6tgkqApaBVpAg'
affixes = pd.read_csv(f'{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Affixes')
roots = pd.read_csv(f'{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Roots')

consonants = [
  'p', 'b', 'pʰ', "p'", 'm', 'f', 'v', 't', 'd', 'tʰ', "t\'",
  'ţ', 'ḑ', 'n', 'c', 'ƶ', 'cʰ', "c\'", 's', 'z', 'ċ', 'ż', 'ċʰ',
  "ċ\'", 'ș', 'ᶎ', 'r', 'ŗ', 'č', 'j', "č\'", 'š', 'ž', 'ķ',
  'ǰ', 'ķʰ', "ķ\'", 'ç', "ç\'", 'y̌', 'k', 'g', 'ʰ', "ẓ", 'x\'',
  'x', 'ǧ', 'ņ', 'q', 'ġ', 'qʰ', "q\'", 'x̧\'', 'x̧', 'ř', 'ḩ',
  'h', 'q̌', 'ļ', 'l', 'ł', 'ń', 'ḿ', 'm̀', 'ĺ', 'ņ́', 'ǹ', 'ŗ̀', 'l̀', 'ŗ́'
  ' ̀', ' ́']
ambiguous = ['y', 'w', "\'"] 
vowels = [
  'î', 'ÿ', 'ü', 'ï', 'û', 'i', 'u', 'ê', 'ø', 'ë', 'ô', 'e', 'ö', 
  'o', 'ä', 'a', 'â', 'é', 'á', 'í', 'ó', 'ú', 'è', 'ì', 'ò', 'à', 'ù']
diph = ['ai', 'äi', 'ei', 'ëi', 'oi', 'öi', 
              'ui', 'au', 'äu', 'eu', 'ëu', 'iu', 
              'ou', 'öu', 'aï', 'eï', 'ëï', 'iï', 
              'oï', 'uï', 'äï', 'öï', 'üï', 'ae',
              'ài', 'èi', 'òi', 'ùi', 'àu', 'èu',
              'ìu', 'òu', 'àï', 'èï', 'ìï', 'òï',
              'ùï', 'àe', 'ái', 'éi', 'ói', 'úi', 
              'áu', 'éu', 'íu', 'óu', 'áï', 'éï', 
              'íï', 'óï', 'úï', 'áe']


def divide(word):
  groups = []
  current_group = ''
  group_type = word[0] in consonants
  letter_type = False
  for letter in word:
    if letter in ambiguous:
      current_group += letter
      continue
    elif letter in consonants:
      letter_type = True
    elif letter in vowels:
      letter_type = False
    if letter_type == group_type:
      current_group += letter
    else:
      groups.append(current_group)
      current_group = letter
      group_type = letter_type
  groups.append(current_group)
  return groups

def removeStress(v):
  accN = 'aeiou'
  accA = 'áéíóú'
  accG = 'àèìòù'
  vUns = []
  for i in v:
    if len(i) == 1 and i in accA:
      i = i.replace(i, accN[accA.index(i)])
    elif len(i) == 1 and i in accG:
      i = i.replace(i, accN[accG.index(i)])
    elif len(i) == 2 and i[0] in accA:
      i = i.replace(i[0], accN[accA.index(i[0])])
    elif len(i) == 2 and i[0] in accG:
      i = i.replace(i[0], accN[accG.index(i[0])])
    elif len(i) == 2 and i[1] in accA:
      t1 = i.replace(i[1], accN[accA.index(i[1])])
      t2 = i.replace(i[1], accG[accA.index(i[1])])
      i = t2 if t1 in diph else t1
    elif len(i) > 1 and i[0] == i[1]:
      i = i[1:]
    vUns.append(i)
  return vUns

def checkStress(word):
  components = divide(word)
  v = []
  stressType = []
  vowSyll = []

  for i in components:
    if i[0] in consonants:
      continue
    else:
      if len(i) > 1 and i[1] in ambiguous:
        iLeft , iRight = i.split(i[1])
        iLeft = ''.join(i for i in iLeft if i in vowels)
        v.append(iLeft)
        iRight = ''.join(i for i in iRight if i in vowels)
        v.append(iRight)
      elif len(i) > 2 and i[1] in vowels and i[2] in ambiguous:
        iLeft, iRight = i.split(i[2])
        iLeft = ''.join(i for i in iLeft if i in vowels)
        v.append(iLeft)
        iRight = ''.join(i for i in iRight if i in vowels)
        v.append(iRight)
      else:
        i = ''.join(i for i in i if i in vowels)
        v.append(i)
  v = [x for x in v if x != '']

  for i in v:
    if i in diph or (len(i) == 2 and i[0] == i[1]) or (len(i) > 2 and i[1:] in diph):
      vowSyll.append(i)
      if i in diph and i[0] in 'àèìòù':
        stressType.append(3)
      elif i in diph and i[0] in 'áéíóú':
        stressType.append(2)
      elif i in diph:
        stressType.append(1)
      else:
        stressType.append(2)
    elif len(i) > 2 and i[0] == i[1]:
      vowSyll.append(i[0]+i[1])
      stressType.append(2)
      vowSyll.append(i[2:])
      stressType.append(1)
    else:
      for j in i:
        vowSyll.append(j)
        if (len(i) == 2 and j in 'àèìòù' and i[-1] not in 'àèìòù') or (len(i) == 1 and 
                                                                         j in 'àèìòù'):
          stressType.append(3)
        elif j in 'áéíóú':
          stressType.append(2)
        else:
          stressType.append(1)

  stressType = stressType[-4:] if len(stressType) > 4 else stressType
  vowSyll = vowSyll[-4:] if len(vowSyll) > 4 else vowSyll
  n = stressType.count(3) + stressType.count(2)
  vow = removeStress(v)
  for num, i in enumerate(v):
    word = word.replace(i, vow[num])
  if n > 1:
    return None, None
  elif n == 0:
    return 'pen', word
  elif n == 1 and stressType.count(2) == 1:
    pos = len(stressType)-stressType.index(2)
    position_mapping = {
      4: 'pre',
      3: 'ant',
      2: 'pen',
      1: 'ult'
    }
    return position_mapping.get(pos), word
  elif n == 1 and stressType.count(3) == 1:
    if len(stressType) == 2 and stressType[0] == 3 or (len(stressType) > 2 
                                                         and stressType[-3] == 3):
      return 'ult', word
    elif len(stressType) == 3:
      return 'ant', word
    elif len(stressType) == 4:
      a = vowSyll[0]
      b = vowSyll[1]
      if a[0] in 'âêîôûäëïöüÿø':
        return 'pre', word
      elif b[0] in 'âêîôûäëïöüÿø':
        return 'ant', word
  return None, None

def convertMutation(file_path, C1):
  with open(file_path, 'r') as file:

      for line in file:
          elements = line.split()
          for index, el in enumerate(elements, 1): 
              if '-' in el:
                  el_before, el_after = el.split('-')
                  if el_before == C1 or el_after == C1:
                      return elements[0], index-1
              else:
                  if el == C1:
                      return elements[0], index-1
  return None, 0


def checkC1(c1):
  focus = False
  illocution = None
  configuration = None
  with open('mutations1.txt', 'r') as file:
    for line in file:
      elements = line.split()
      for el in elements:
        if '-' in el:
          el_before, el_after = el.split('-')
          if el_before == c1 or el_after == c1:
            illocution = 'ASR'
        elif el == c1:
          illocution = 'ASR'
          
  if illocution != 'ASR':
    focus = c1[-1] == 'w'
    c1 = c1[:-1] if focus else c1
    
  with open('mutations1.txt', 'r') as file:
    for line in file:
      elements = line.split()
      for el in elements:
        if '-' in el:
          el_before, el_after = el.split('-')
          if el_before == c1 or el_after == c1:
            illocution = 'ASR'
        elif el == c1:
          illocution = 'ASR'
          
  ill = c1[0]
  s_a = ['p', 't', 'k', 'ķ', 'q', 'c', 'ċ', 'č',
                    'b', 'd', 'ǰ', 'g', 'ƶ', 'ż', 'j']
  if illocution != 'ASR':
    c1 = c1[1:]
    if len(c1) == 1 and ill in s_a and ill == c1[0]:
      illocution = 'DIR'
    elif len(c1) == 2 and ill in s_a and c1[1] in ['ʰ', '\''] and ill == c1[0]:
      illocution = 'DIR'
    elif ill in ['n', 'r', 'ŗ'] and ill == 'm':
      illocution = 'CMV'
    elif ill == 'n' or ill == 'ņ':
      illocution = 'CMV'
    elif ill in ['f', 'z', 'ţ']:
      illocution = 'EXP'
    elif ill in ['ç', 'p', 't', 'k']:
      illocution = 'DEC'
    elif ill in ['r', 'n']:
      illocution = 'IRG'
    elif ill in ['l', 'ŗ', 'ļ']:
      illocution = 'ADM'
    else:
      c1 = None
  c1, index = convertMutation('mutations1.txt', c1)
  with open('mutations1.txt', 'r') as file:
    elements_fl = file.readline().split()
    configuration = elements_fl[index]
  return c1, illocution, configuration, focus

  
def checkInfix(infix):
  mode = None
  pattern = None
  form = None
  stem = None
  series = None
  with open('infixmutations.txt', 'r') as file:
    first_line_elements = file.readline().split()
    for line in file:
      elements = line.split()
      for index, el in enumerate(elements):
        if '-' in el:
          el_before, el_after = el.split('-') 
          if el_before == infix or el_after == infix:
            mode = elements[0]
            pattern = elements[1]
            form = elements[2]
            stem = elements[3]
            series = first_line_elements[index]
        elif el == infix:
          mode = elements[0]
          pattern = elements[1]
          form = elements[2]
          stem = elements[3]
          series = first_line_elements[index]
  return mode, pattern, form, stem, series


def getRoot(root, pattern, form, stem):
  stem = int(stem[-1])
  pattern = int(pattern[-1])
  form = int(form[-1])
  number = 9*(form-1)+3*(pattern-1)+stem
  for _, line in roots.iterrows():
    if root == line.iloc[0]:
      return line.iloc[number]
  return root


def checkPrefix(prefix):
  conflation = None
  affiliation = None
  extension = None
  illocution = None
  if prefix[-1] == '\'':
    illocution = True
    prefix = prefix[:-1]
  with open('conflations.txt', 'r') as file:
    first_line_elements = file.readline().split()
    for line in file:
      elements = line.split()
      for index, el in enumerate(elements, 1):
        if el == prefix:
          conflation = elements[0]
          affiliation = elements[1]
          extension = first_line_elements[index-1]
  return conflation, affiliation, extension, illocution

def checkC2(c2):
  check = None
  index = None
  affix = ''
  for _ in c2:
    check, index = convertMutation('mutations2.txt', c2)
    if check is None:
      affix = c2[-1] + affix
      c2 = c2[:-1]
    else:
      break
  return check, affix, index

def checkAffix(cns, vow):
  if vow[-1] == '\'':
    vow = vow[:-1]
    cns = '\''+cns
  degree = 0
  typestr = ''
  type = ''
  with open('affvow.txt', 'r') as file1:
    fl_el = file1.readline().split()
    for line in file1:
      elements = line.split()
      for i, el in enumerate(elements, 0):
        if '-' in el:
          el_before, el_after = el.split('-')
          if el_before == vow or el_after == vow:
            degree = elements[0]
            type = fl_el[i]
        elif vow == el:
          degree = elements[0]
          type = fl_el[i]
  if type == '1':
    typestr = '₁'
  elif type == '2':
    typestr = '₂'
  elif type == '3':
    typestr = '₃'
  affix2 = ''
  t = cns
  for _ in cns:
    for _, row in affixes.iterrows():
      if cns == row.iloc[0] and type in str(row.iloc[-1]):
          return '‘'+row.iloc[int(degree)]+'’'+typestr, affix2
    affix2 = cns[-1] + affix2
    cns = cns[:-1]
  return '**'+t+'**/'+str(degree)+typestr, ''

def checkTone(word):
  context = 'EXS'
  last = word[-1]
  if last == '/':
    context = 'RPS'
    word = word[:-1]
  elif last in '⁻-':
    context = 'FNC'
    word = word[:-1]
  elif last == '\\':
    context = 'AMG'
    word = word[:-1]
  return word, context   

def glossDefault(word, bias):
  persp, word = checkStress(word)
  if persp is None:
    return 'Error: invalid stress'
  persp_map = {
    'pre': 'A',
    'ant': 'N',
    'pen': 'M',
    'ult': 'U'
  }
  perspective = persp_map.get(persp)
  word, context = checkTone(word)
  #analyze first vocalic form
  gloss = ''
  components = divide(word)
  if bias != '':
    components.pop(0)
  first = components[0]
  prefix = first if first[0] in ambiguous or first[0] in vowels else 'a'
  conflation = None
  affiliation = None
  extension = None
  conflation, affiliation, extension, pr_ill = checkPrefix(prefix)
  if conflation is None:
    return 'Error: invalid slot I prefix'
  components.pop(0) if first[0] in ambiguous or first[0] in vowels else None
  #analyze first consonantal form, root's C1
  C1 = None
  C1 = components[0]
  illocution = None
  focus = None
  configuration = None
  C1, illocution, configuration, focus = checkC1(C1)
  if pr_ill and illocution == 'ASR':
    illocution = 'DIR'
  if C1 is None or illocution is None:
    return 'Error: invalid slot II root\'s C1'
  components.pop(0)
  #analyze root's infix
  infix = components[0]
  mode = None
  pattern = None
  form = None
  stem = None
  series = None
  mode, pattern, form, stem, series = checkInfix(infix)
  if mode is None or pattern is None or form is None or stem is None or series is None:
    return 'Error: invalid slot III infix'
  components.pop(0)
  #analyze second consonantal form, root's C2
  C2 = components[0]
  C2_index = None
  C2_affix = ''
  C2, C2_affix, C2_index = checkC2(C2)
  if C2 is None:
    return 'Error: invalid slot IV root\'s C2'
  with open('cases.txt', 'r') as cases:
    for i, line in enumerate(cases):
      if i == C2_index:
        c = line.split()
        case = c[int(series)-1]
  components.pop(0)
  #analyze affixes
  if C2_affix != '':
    components.insert(0, C2_affix)
    
  if len(components) > 0:
    newcomps = []
    for i in components:
      if 'y' in i:
        if i[-1] == 'y':
          vow_before = i[:-1]
          vow_after = 'a'
        else:
          vow_before, vow_after = i.split('y')
        if vow_before in vowels and vow_after in vowels:
          newcomps.append(vow_before)
          newcomps.append('y')
          newcomps.append(vow_after)
        else:
          newcomps.append(i)
      elif 'w' in i:
        if i[-1] == 'w':
          vow_before = i[:-1]
          vow_after = 'a'
        else:
          vow_before, vow_after = i.split('w')
        if vow_before in vowels and vow_after in vowels:
          newcomps.append(vow_before)
          newcomps.append('w')
          newcomps.append(vow_after)
        else:
          newcomps.append(i)
      elif '\'' in i:
        if i[-1] == '\'':
          vow_before = i[:-1]
          vow_after = 'a'
        else:
          vow_before, vow_after = i.split('\'')
        if vow_before in vowels and vow_after in vowels:
          newcomps.append(vow_before)
          newcomps.append('\'')
          newcomps.append(vow_after)
        else:
          newcomps.append(i)
      else:
        newcomps.append(i)
    components = newcomps
    components = list(filter(lambda x: x != "", components))
  if len(components) > 0:
    last = components[-1]
  if len(components) % 2 == 1 and last[0] not in vowels:
    components.append('a')
  i = 0
  glossAffixes = ''
  while len(components) > 1:
    a1 = components[0]
    a2 = components[1]
    affix2 = ''
    if a1[0] in ambiguous+consonants and a2[0] in vowels:
      if checkAffix(a1, a2) is None:
        return "Error: invalid affix"
      t, affix2 = checkAffix(a1, a2)
      glossAffixes += '-' + t 
    elif a1[0] in vowels and a2[0] in ambiguous+consonants:
      if checkAffix(a2, a1) is None:
        return "Error: invalid affix"
      t, affix2 = checkAffix(a2, a1)
      glossAffixes += '-' + t 
    components.pop(0)
    components.pop(0)
    if affix2 != '':
      components.insert(0, affix2)
    

  #parse string
  mod = 'NRM' if mode == 'm1' else 'RPV'
  foc = '+FC' if focus else ''
  root = C1 + '-' + C2
  root = getRoot(root, pattern, form, stem)
  if bias != '':
    gloss += bias + '.'
  gloss += '__'+stem+'__' + '-\"' + root + '\"-' + conflation + '.' + affiliation + '.'
  gloss += extension + '-' + illocution + '.' + configuration + '.' + mod + '-'
  gloss += case + '.' + context + '.' + perspective + foc
  gloss += glossAffixes
  return gloss

def getValence(valence):
  with open('valence.txt', 'r') as file:
    line1 = file.readline().split()
    for line in file:
      line = line.split()
      for num, i in enumerate(line, 0):
        if '-' in i:
          iLeft, iRight = i.split('-')
          if iLeft == valence or iRight == valence:
            return line[0], line1[num]
        elif i == valence:
          return line[0], line1[num]
  return None, None

def getFormat(format):
  vers_mapping = {
    'nń': 'DEF',
    'mḿ': 'SCH',
    'lĺ': 'ISR',
    'ņņ́': 'ATH',
    'nǹ': 'PRC',
    'ŗŗ̀': 'RSL',
    'mm̀': 'SBQ',
    'll̀': 'CCM',
    'ŗŗ́': 'OBJ'
  }
  return vers_mapping.get(format) if format in vers_mapping else None

def getDerivation(valCons):
  Cn = None
  with open('derivations.txt', 'r') as file:
    for line in file:
      line = line.split()
      if valCons in line:
        Cn = line.index(valCons)+1
  if Cn is None:
    return None
  else:
    dict = {1: '', 2: 'w', 3: 'y'}
    return dict.get(Cn)

def getModality(modality):
  modality_map = {
    'a': 'DES', 'ü': 'ASP', 'ï': 'EPC',
    'u': 'CRD', 'â': 'REQ', 'û': 'EXH', 
    'ai': 'OPR', 'ei': 'CPC', 'oi': 'PRM',
    'ëi': 'PTN', 'ui': 'CLS', 'iu': 'OBG',
    'au': 'IMS', 'ia': 'ADV', 'ou': 'ITV',
    'eu': 'ANT', 'äi': 'DSP', 'öi': 'PRE',
    'ëu': 'NEC', 'aï': 'DEC', 'eï': 'PTV',
    'iï': 'VOL', 'oï': 'ACC', 'öu': 'INC',
    'uï': 'CML', 'äu': 'DVR', 'ëï': 'DVT',
    'ua': 'PFT', 'üa': 'IPS', 'iù': 'PMS'
  }
  return modality_map.get(modality) if modality in modality_map else None


def glossValAdjunct(word):
  #check tone
  if word[-1] in '⁻-':
    level = 'EQU'
  elif word[-1] in '/':
    level = 'SUR'
  elif word[-1] in '\\':
    level = 'DFT'
  else:
    level = 'IDT'
  word = word[:-1] if level != 'IDT' else word
  components = divide(word)
  #check first vowel
  c = components[0]
  if c[0] in consonants:
    t = c
    c = getDerivation(c)
    components.pop(0)
    components[0] = c + components[0]
  focus = ''
  if c == '':
    derivation = 'CN1-\''+t+'\'.'
  elif c == 'w':
    derivation = 'CN2-\''+t+'\'.'
  elif c == 'y':
    derivation = 'CN3-\''+t+'\'.'
  else:
    derivation = ''
  c = components[0]
  if c[-1] == '\'':
    c = c[:-1]
    focus = '+FC'
  valence, version = getValence(c)
  if valence is None or version is None:
    return 'Error: invalid valence/version'
  components.pop(0)
  #check syllabic consonant
  format = getFormat(components[0])
  if format is None:
    return 'Error: invalid format'
  components.pop(0)
  #check vocalic suffix
  if len(components) == 0:
    components.append('a')
  modality = getModality(components[0])
  if modality is None:
    return 'Error: invalid modality'
  return derivation + valence + '.'+version+'-'+format+'.'+modality+'-'+level+focus

def getVPS(vps):
  with open('valphasan.txt', 'r') as file:
    line1 = file.readline().split()
    for line in file:
      line = line.split()
      for i in line:
        if i == vps:
          return line[0], line[1], line1[line.index(vps)]
  return None, None, None

def getAspect(aspect):
  with open('aspects.txt', 'r') as file:
    line1 = file.readline().split()
    for line in file:
      line = line.split()
      for i in line:
        if i == aspect:
          return line[0], line1[line.index(aspect)]
  return None, None

def glossAspAdjunct(word, bias):
  stress, word = checkStress(word)
  if stress not in ['ult', 'pen'] or word is None:
    return 'Error: invalid stress'
  #check tone
  if word[-1] in '⁻-':
    tone = 'high'
  elif word[-1] in '/':
    tone = 'rising'
  elif word[-1] in '\\':
    tone = 'broken'
  else:
    tone = 'falling'
  word = word[:-1] if tone != 'falling' else word
  components = divide(word)
  #check mood
  mood = ''
  if stress =='pen':
    if tone == 'falling':
      mood = 'FAC'
    elif tone == 'high':
      mood = 'ASM'
    elif tone == 'broken':
      mood = 'COU'
    elif tone == 'rising':
      mood = 'IPL'
  elif stress == 'ult':
    if tone == 'falling':
      mood = 'SUB'
    elif tone == 'high':
      mood = 'SPE'
    elif tone == 'broken':
      mood = 'HYP'
    elif tone == 'rising':
      mood = 'ASC'
  else:
    return 'Error: invalid stress'
  #check aspect 1
  aspect1, format = getAspect(components[0])
  if aspect1 is None or format is None:
    return 'Error: invalid aspect'
  if format == 'Vs':
    return 'Error: vocalic suffix for aspect in first position'
  components.pop(0)
  #check VSP
  validation, phase, sanction = getVPS(components[0])
  if validation is None or phase is None or sanction is None:
    return 'Error: invalid VSP'
  components.pop(0)
  #check aspect 2
  aspect2 = 'DEF'
  if len(components) > 0:
    components[0] = components[0] + '-'
    aspect2, i = getAspect(components[0])
    if aspect2 is None:
      return 'Error: invalid aspect suffix'
  gloss = ''
  if bias != '':
    gloss = bias + '-'
  gloss += aspect1 + '.' + format
  gloss += '-' + validation + '.' + phase + '.' + sanction
  gloss +=  '-' + aspect2 + '.' + mood
  return gloss

def getPRA(pra, tone):
  with open('PRAs.txt', 'r') as file:
    for line in file:
      line = line.split()
      for i in line:
        if i == pra and tone:
          return line[2]
        elif i == pra and not tone:
          return line[1]
  return None

def getPRAcase(case):
  with open('PRAcase.txt', 'r') as file:
    for line in file:
      line = line.split()
      for i in line:
        if i == case:
          return line[0]
  return None

def getPRAva(Va):
  with open('PRAva.txt', 'r') as file:
    line1 = file.readline().split()
    for line in file:
      line = line.split()
      for i in line:
        if i == Va:
          return line[0], line[1], line[2], line1[line.index(Va)]
  return None, None, None, None

def glossPRA(word):
  stress, word = checkStress(word)
  if stress is None or word is None:
    return 'Error: invalid stress'
  #check tone
  if word[-1] in '⁻-':
    tone = 'high'
  elif word[-1] in '/':
    tone = 'rising'
  elif word[-1] in '\\':
    tone = 'broken'
  else:
    tone = 'falling'
  word = word[:-1] if tone != 'falling' else word
  components = divide(word)
  c = components[0]
  if c[0] not in consonants:
    firstvow = True
    designation, focus, affiliation, configuration = getPRAva(c)
    if designation is None:
      return 'Error: invalid slot I Va prefix'

    components.pop(0)
  else:
    firstvow = False
    designation, focus, affiliation, configuration = getPRAva('a')
  focus = '' if focus == '-FC' else focus
  #type 1 and 2
  if len(components) == 2:
    type = tone in ['high', 'rising']
    essence = 'NRM' if tone in ['falling', 'high'] else 'RPV'
    pra = getPRA(components[0], type)
    if pra is None:
      return 'Error: invalid personal reference adjunct'
    components.pop(0)
    if 'w' in components[0]:
      Vc1, Vz = components[0].split('w')
      case = getPRAcase(Vc1+'w')
      if case is None:
        return 'Error: invalid case'
      context = ''
      if stress == 'ult':
        if Vz == 'a':
          context = 'RPS'
        elif Vz == 'u':
          context = 'AMG'
        else:
          return 'Error: invalid Vz slot for context'
      elif stress != 'ult':
        if Vz == 'a':
          context = 'EXS'
        elif Vz == 'u':
          context = 'FNC'
        else:
          return 'Error: invalid Vz slot for context'
      gloss = pra + '-' + designation + '.'+affiliation+'.'+configuration+'-'
      gloss += case+'.'+context+'-'+essence+focus
      return gloss
    elif 'y' in components[0]:
      Vc1, Vz = components[0].split('y')
      case = getPRAcase(Vc1+'y')
      if case is None:
        return 'Error: invalid case'
      context = ''
      if stress == 'ult':
        if Vz == 'a':
          context = 'RPS'
        elif Vz == 'u':
          context = 'AMG'
        else:
          return 'Error: invalid Vz slot for context'
      elif stress != 'ult':
        if Vz == 'a':
          context = 'EXS'
        elif Vz == 'u':
          context = 'FNC'
        else:
          return 'Error: invalid Vz slot for context'
      gloss = ''
      gloss = pra + '-' + designation + '.'+affiliation+'.'+configuration+'-'
      gloss += case+'.'+context+'-'+essence+focus
      return gloss
    elif firstvow == False:
      case = getPRAcase(components[0])
      if case is None:
        return 'Error: invalid case'
      return pra+'-'+case+'-'+essence
    else:
      return 'Error: invalid Type 1 personal reference adjunct'
  else:
    type = tone in ['high', 'rising']
    essence = 'NRM' if tone in ['falling', 'high'] else 'RPV'
    pra = getPRA(components[0], type)
    if pra is None:
      return 'Error: invalid personal reference adjunct'
    components.pop(0)
    if 'w' in components[0]:
      Vc1, Vd = components[0].split('w')
      Vc1 += 'w'
    elif 'y' in components[0]:
      Vc1, Vd = components[0].split('y')
      Vc1 += 'y'
    else:
      return 'Error: invalid Vc1 infix'
    case = getPRAcase(Vc1)
    Vd_map = {
      'ï': 1, 'u': 2, 'ë': 3, 'e': 4, 'a': 5, 'ö': 6, 'o': 7, 'ä': 8, 'i': 9 }
    degree = Vd_map.get(Vd)
    if degree is None:
      return 'Error: invalid Vd suffix'
    components.pop(0)
    if stress == 'pen':
      type = 1
    elif stress == 'ult':
      type = 2
    elif stress == 'ant':
      type = 3
    else:
      return 'Error: invalid stress'
    with open('affvow.txt', 'r') as file:
      for i, line in enumerate(file, 0):
        if i == degree:
          line = line.split()
          vow = line[type]
    if vow is not None and '-' in vow:
      vow, _ = vow.split('-')
    if vow is None:
      return 'Error: invalid Vd suffix'
    affix, _ = checkAffix(components[0], vow)
    if affix is None:
      return 'Error: invalid affix'
    components.pop(0)
    context = 'EXS'
    bias = ''
    if len(components) > 0:
      ctx_map = {'a': 'EXS', 'u': 'FNC', 'û': 'RPS', 'â': 'AMG'}
      context = ctx_map.get(components[0]) if components[0] in ctx_map else None
      if context is None:
        return 'Error: invalid Vw suffix for context'
      components.pop(0)
      if len(components) == 1:
        cons = components[0]+'\''
        bias = checkBias(cons)
        if bias == '':
          return 'Error: invalid bias suffix'
        else:
          bias = '-' + bias
      elif len(components) > 1:
        return 'Error: invalid personal reference adjunct'
    
    gloss = pra + '-' + designation + '.'+ affiliation +'.'+configuration+'-'
    gloss += case+'-'+affix+'-'+essence
    gloss += '.' + context + bias+focus
    return gloss

def checkBias(bias):
  bias = bias[:-1]
  bias_map = {
    'n': 'ASU', 'nn': 'ASU⁺',
    'm': 'HPB', 'mm': 'HPB⁺',
    'ņ': 'COI', 'ņņ': 'COI⁺',
    'h': 'ACP', 'hh': 'ACP⁺',
    'ç': 'RAC', 'çç': 'RAC⁺',
    's': 'STU', 'ss': 'STU⁺',
    'ș': 'CTV', 'șș': 'CTV⁺',
    'š': 'DPV', 'šš': 'DPV⁺',
    'l': 'RVL', 'll': 'RVL⁺',
    'ŗ': 'GRA', 'ŗŗ': 'GRA⁺',
    'ř': 'SOL', 'řř': 'SOL⁺',
    'ļ': 'SEL', 'ļļ': 'SEL⁺',
    'ł': 'IRO', 'łł': 'IRO⁺',
    'pł': 'EXA', 'płł': 'EXA⁺',
    'ḩ': 'LTL', 'ḩḩ': 'LTL⁺',
    'x': 'CRR', 'xx': 'CRR⁺',
    'x̧': 'EUP', 'x̧x̧': 'EUP⁺',
    'ks': 'SKP', 'kss': 'SKP⁺',
    'kș': 'CYN', 'kșș': 'CYN⁺',
    'kš': 'CTP', 'kšš': 'CTP⁺',
    'pç': 'DSM', 'pçç': 'DSM⁺',
    'pš': 'IDG', 'pšš': 'IDG⁺',
    'ps': 'SGS', 'pss': 'SGS⁺',
    'pș': 'PPV', 'pșș': 'PPV⁺'
  }
  return bias_map.get(bias) if bias in bias_map else ''

def hardGloss(word):
  components = divide(word)
  bias = ''
  c = components[0]
  if c[-1] == '\'' and checkBias(c) != '':
    bias = checkBias(c)
    components.pop(0)
    word = ''.join(components)
  formats = ['nń', 'mḿ', 'lĺ', 'ņņ́', 'nǹ', 'ŗŗ̀', 'mm̀', 'll̀', 'ŗŗ́']
  n = 0
  for i in components:
    n = n + 1 if i[0] in consonants else n
  if bias == '' and len(components) == 1 and getModality(components[0]) is not None:
    return getModality(components[0])
  if set(formats) & set(components):
    return glossValAdjunct(word)
  elif n == 1 and components[0] not in consonants:
    if 'Error:' not in glossAspAdjunct(word, bias).split():
      return glossAspAdjunct(word, bias)
  else:
    c = components[0]
    _, unsWord = checkStress(word)
    unsComponents = divide(unsWord)
    if len(components) == 2:
      return glossPRA(word)
    elif c[0] not in consonants and len(components) > 2:
      a, b, c, d, e = checkInfix(unsComponents[2])
      return glossPRA(word) if a is None else glossDefault(word, bias)
    elif c[0] in consonants and len(components) > 2:
      a, b, c, d, e = checkInfix(unsComponents[1])
      return glossPRA(word) if a is None else glossDefault(word, bias)
    else:
      return glossDefault(word, bias)
  return glossPRA(word)

defaultCategories = ['OPR', 'CSL', 'DEL', 'ASR', 'UNI', 'NRM', 'OBL', 'EXS', 'M',
                     'MNO', 'PRC', 'DEF', 'DES', 'IDT',
                     'NEU', 'SCH', 'CNF', 'CTX', 'PPS', 'FAC']

def removeDefCats(gloss):
  newBits = []
  bits = gloss.split('-')
  for i in bits:
    set = []
    cats = i.split('.')
    for j in cats:
      if j not in defaultCategories:
        set.append(j)
    newBits.append('.'.join(set))
  newBits = [i for i in newBits if i]
  return '-'.join(newBits)
  
def easyGloss(word):
  gloss = hardGloss(word)
  gloss = removeDefCats(gloss)
  return gloss

def printRootInfo(root):
  info = None
  message = ''
  for _, row in roots.iterrows():
    if root == row.iloc[0]:
      info = row
  if info is None:
    return 'Couldn\'t find the root.'
  else:
    message += '**' + root.upper() + ':** ' + str(info.iloc[-1]) + '\n'
    message += '__' + 'INFORMAL:'+ '__' + '\n'
    message += 'P1: 1. ' + info.iloc[1] + ', 2. ' + info.iloc[2] + ', 3. ' + info.iloc[3] + '\n'
    message += 'P2: 1. ' + info.iloc[4] + ', 2. ' + info.iloc[5] + ', 3. ' + info.iloc[6] + '\n'
    message += 'P3: 1. ' + info.iloc[7] + ', 2. ' + info.iloc[8] + ', 3. ' + info.iloc[9] + '\n'
    message += '__' + 'FORMAL:'+ '__' + '\n'
    message += 'P1: 1. ' + info.iloc[10] + ', 2. ' + info.iloc[11] + ', 3. ' + info.iloc[12] + '\n'
    message += 'P2: 1. ' + info.iloc[13] + ', 2. ' + info.iloc[14] + ', 3. ' + info.iloc[15] + '\n'
    message += 'P3: 1. ' + info.iloc[16] + ', 2. ' + info.iloc[17] + ', 3. ' + info.iloc[18] + '\n'
    return message

def printAffixInfo(affix):
  info = None
  message = ''
  for _, row in affixes.iterrows():
    if affix == row.iloc[0]:
      info = row
  if info is None:
    return 'Couldn\'t find the affix.'
  else:
    message += '**-'+affix.lower()+':** '+str(info.iloc[-3]) +' ('+info.iloc[-2]+') ' + '\n'
    for i in range(1, 10):
      message += str(i) + '. ' + info.iloc[i] + '\n'
  return message