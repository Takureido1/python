import re

consonants = {'p', 'b', 'm', 'f', 'v', 't', 
              'd', 'ŧ', 'đ', 'n', 'l', 'c',
              'ż', 's', 'z', 'r', 'č', 'j',
              'š', 'ž', 'ç', 'k', 'g', 'x', 
              'ň', 'ř', 'h'}
              
vowels = {'i', 'ï', 'ü', 'u', 'e', 
          'ö', 'ë', 'o', 'ä', 'a',
          'A', 'E', 'I', 'O', 'U'}
          
ambiguous = ['w', 'y', '\'']

diacritics_map = {char: repl for repl, chars in {
    'A': 'ạāàáăâ',
    'E': 'ẹēèéĕê',
    'I': 'ịīìíĭî',
    'O': 'ọōòóŏô',
    'U': 'ụūùúŭû'}.items() for char in chars}

tone1='ạẹịọụ'
tone2='āēīōū'
tone3='àèìòù'
tone4='áéíóú'
tone5='ăĕĭŏŭ'
tone6='âêîôû'

diphthongs = {"ai", "Ai", "äi", "äI", "ei", "Ei", "ëi", "ëI",
              "oi", "Oi", "öi", "öI", "ui", "Ui", "au", "Au", 
              "äu", "äU", "eu", "Eu", "ëu", "ëU", "iu", "Iu", 
              "ou", "Ou", "öu", "öU", 'äA', 'ëE', 'ïI', 'öO', 'üU'}

functions = [['OPR','DSP'],['STA','ATV'],['MNF','PSN'],['ICH','TNV']]
stress = ['ant', 'pen', 'ult']

def getStressTone(word):
    tone, transformed_word, division, vocalic_parts = [], [], [], []
    error = False

    for char in word:
        if char in diacritics_map:
            transformed_word.append(diacritics_map[char])
            tone.append(char)
        else:
            transformed_word.append(char)
    word = ''.join(transformed_word)
    
    pattern = f"({'|'.join(map(re.escape, sorted(diphthongs | vowels, key=len, reverse=True)))})"
    division = [i for i in re.split(pattern, word) if (len(i) > 0 and i[0] in vowels)]
    stress = [len(division)-i for i, s in enumerate(division) if any(c.isupper() for c in s)]

    if len(stress) > 1:
        error = True
    
    replacements = {'äA': 'ä', 'ëE': 'ë', 'ïI': 'ï', 'öO': 'ö', 'üU': 'ü'}  
    for old, new in replacements.items():
        word = word.replace(old, new).lower()
    
    if len(stress) == 0:
        stress = 1
    else:
        stress = stress[0]
    if stress > 3:
        error = True
    for i in range(1,7):
        tone_list = globals().get(f"tone{i}")
        if len(tone) > 0 and tone[0] in tone_list:
            tone = i
            break
    else:
        tone = 1

    return word, stress, tone, error

def divide(word):
  groups = []
  current_group = ''
  group_type = word[0] in consonants
  letter_type = False
  for letter in word:
    if letter in ambiguous and group_type:
        groups.append(current_group+letter)
        current_group = ''
        group_type = not group_type
        continue
    elif letter in ambiguous and not group_type:
        current_group += letter
        continue
    elif letter in ambiguous and not group_type:
        letter_type = True
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

def getInfo(filename, part, n):
    filename = 'v2_tables/'+filename
    info = []
    el_before, el_after = None, None
    with open(filename, 'r') as file:
        first_line_elements = file.readline().split()
        for line in file:
            elements = line.split()
            for index, el in enumerate(elements):
                if part == el:
                    for i in range(n):
                        info.append(elements[i])
                    info.append(first_line_elements[index])
    return info
    
def check(filename, part):
    filename = 'v2_tables/'+filename
    with open(filename, 'r') as file:
        for line in file:
            if part in line:
                return True
    return False

def glossFormative(word):
    word, stress, tone, error = getStressTone(word)
    if error:
        return "Error: invalid stress"
    
    stress_map = [2,1,3]
    stress = stress_map[stress-1]
    
    parts = divide(word)
    error = False
    gloss = ''
    
    isLevel = True
    level, illocution, bias = ['']*3
    w_format, aspect, context = ['a']*3
    vps = 'l'
    
    #case 1: illocution is y or w
    for char in ['w','y']:
        if char in parts[0] and parts[0][0] not in consonants:
            level, w_format = parts[0].split(char)
            illocution = char
            parts.pop(0)
    #case2: no presence of level
    if parts[0] in ['h','çw','hm','hn','ççw']:
        parts = ['a'] + parts
        isLevel = False
    #case3: presence of level
    if parts[1] in ['h','çw','hm','hn','ççw']:
        level = parts[0]
        illocution = parts[1]
        w_format = parts[2]
        del parts[:3]
        
    if not illocution and check('format.txt', parts[0].replace('\'','')):
        w_format = parts[0]
        del parts[:1]
    #phase sanction version aspect presence
    if '\'' in w_format:
        vps = parts[0]
        aspect = parts[1]
        del parts[:2]
    
    #root, case, Ca complex
    root_cns = parts[0]
    case = parts[1]
    ca_plex = parts[2]
    del parts[:3]
    
    #bias
    if len(parts) > 1 and parts[-2][-1] == '\'' and parts[-2][0] in vowels:
        bias = parts[-1]
        del parts[-1:]
        
    #suffixes
    suffixes = []
    while len(parts) > 1:
        suffixes.append(parts[0])
        suffixes.append(parts[1])
        del parts[:2]
        
    if len(parts) == 1:
        context = parts[0]
        del parts[:1]
    
    if isLevel and level:
        if check('level.txt', level):
            level = "".join(getInfo('level.txt', level, 1)[:2])
            gloss += level + '-'
        else:
            error, error_msg = True, "Error: invalid Vl level prefix"
            return error_msg, error

    if illocution:
        if check('illocution.txt', illocution):
            illocution = getInfo('illocution.txt', illocution, 1)[0]
            gloss += illocution + '-'
        else:
            error, error_msg = True, "Error: invalid Ci illocution affix"
            return error_msg, error
    else:
        gloss += 'ASR-'
    
    if w_format:
        if '\'' in w_format:
            if check('format.txt', w_format.replace('\'','')):
                w_format = w_format.replace('\'','')
            elif check('format.txt', w_format.replace('\'','-')):
                w_format = w_format.replace('\'','-')
        if check('format.txt', w_format):
            w_format = getInfo('format.txt', w_format, 3)
            designation = w_format[0]
            fnc_type = int(w_format[2])
            w_format = w_format[1]+'.'+w_format[3]
            gloss += w_format + '-'
        else:
            error, error_msg = True, "Error: invalid Vc portmanteau affix"
            return error_msg, error
        
    if vps:
        if check('verphasan.txt', vps):
            vps = ".".join(getInfo('verphasan.txt', vps, 2))
            gloss += vps + '-'
        else:
            error, error_msg = True, "Error: invalid Cx portmanteau affix"
            return error_msg, error
    
    if aspect:
        if check('aspect.txt', aspect):
            aspect = getInfo('aspect.txt', aspect, 1)[0]
            gloss += aspect + '-'
        else:
            error, error_msg = True, "Error: invalid Vp aspect affix"
            return error_msg, error
    
    if check('cmutation.txt',root_cns):
        root_cns = getInfo('cmutation.txt',root_cns,1)[0]
        function = '0'
    elif check('function.txt',root_cns):
        function = getInfo('function.txt',root_cns,1)
        root_cns = getInfo('cmutation.txt',function[0],1)[0]
        function = function[1]
    elif check('cmutation.txt',root_cns[1:]):
        function = root_cns[0]
        root_cns = getInfo('cmutation.txt',root_cns[1:],1)[0]
    elif check('cmutation.txt',root_cns[:-1]):
        function = root_cns[-1]
        root_cns = getInfo('cmutation.txt',root_cns[:-1],1)[0]
    else:
        error, error_msg = True, "Error: invalid Cr root mutation"
        return error_msg, error

    function_map = {'': 0, 'l': 1, 'r': 2, 'm': 3, 'n': 3, 'ň': 3}
    function = int(function_map.get(function, function))
    if not (function in {0,1,2,3}):
        error, error_msg = True, "Error: invalid Cm function affix"
        return error_msg, error
    else:
        function = functions[int(function)][fnc_type-1]

    if check('vmutation.txt',case):
        case = getInfo('vmutation.txt', case, 1)
        root_vow = case[0]
        case = case[1]
    else:
        error, error_msg = True, "Error: invalid Vr case affix"
        return error_msg, error
    
    vow_map = ['a','e','i','o','u']
    vow_index = vow_map.index(root_vow)
    tone_list = globals().get(f"tone{tone}")
    root_vow = tone_list[vow_index]
    gloss += function + '.'
    gloss += '__S'+str(stress)+'__-'
    gloss += '\"'+root_cns+root_vow+"\"-"
    gloss += case + '-'
    
    if check('cacomplex.txt', ca_plex):
        ca_plex = ".".join(getInfo('cacomplex.txt', ca_plex, 3))
        gloss += ca_plex + '-'
    else:
        error, error_msg = True, "Error: invalid Ca complex affix"
        return error_msg, error
        
    while len(suffixes) > 0:
        if check('suffix.txt',suffixes[0]):
            sufvow = getInfo('suffix.txt',suffixes[0],1)
            s_degree = sufvow[0]
            s_type = sufvow[1]
            suffix = '\"'+suffixes[1]+'\"'
            gloss += suffix+s_type+'-'
            del suffixes[:2]
        else:
            error, error_msg = True, "Error: invalid Vx suffix"
        
    if context:
        context = context.replace('\'','')
        if check('context.txt', context):
            context = ".".join(getInfo('context.txt', context, 1))
            gloss += context
        else:
            error, error_msg = True, "Error: invalid Vf suffix"
            return error_msg, error
    
    if bias:
        if check('bias.txt', bias):
            bias = getInfo('bias.txt',bias,1)
            if bias[1] == '⁺':
                bias = bias[0]+bias[1]
            else:
                bias = bias[0]
            gloss += '-'+bias
        else:
            error, error_msg = True, "Error: invalid Cb bias suffix"
            return error_msg, error
    
    return gloss, error

default = ['ASR','NRM','SCH','PRC',
           'CTX','PPS','NEU','OBL',
           'DEL','M','CSL','UNI',
           'EXS','FAC','OPR']
           
def removeDefCats2(gloss):
    newBits = []
    bits = gloss.split('-')
    for i in bits:
        set = []
        cats = i.split('.')
        for j in cats:
            if j not in default:
                set.append(j)
        newBits.append('.'.join(set))
    newBits = [i for i in newBits if i]
    return '-'.join(newBits)

def glossLong2(word):
    try:
        gloss, error = glossFormative(word)
    except Exception as e:
        print(e)
        return "Error: couldn\'t parse word."
    if error:
        return gloss
    else:
        return gloss
