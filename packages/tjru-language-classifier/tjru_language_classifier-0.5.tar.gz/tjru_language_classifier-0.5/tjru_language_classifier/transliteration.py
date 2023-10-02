
# Create mapping
translit_dict = {
    'yo': 'ё',
    'yu': 'ю',
    'ya': 'я',
    'sh': 'ш',
    'ch': 'ч',
    'gh': 'ғ',
    'zh': 'ж',
    'q': 'қ',
    'j': 'ҷ',
    'h': 'ҳ',
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 
    'z': 'з', 'i': 'и', 'y': 'й', 'k': 'к',
    'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 
    's': 'с', 't': 'т', 'u': 'у', 'f': 'ф', 'c': 'к', 
    'y': 'й', 'e': 'е', 
}

# Special cases must be replaced before single characters
special_cases = [k for k in translit_dict.keys() if len(k) > 1]

def transliterate(text: str):
    text = text.lower()
    for special in special_cases:
        if special in text:
            text = text.replace(special, translit_dict[special])

    transliterated_text = ''
    for char in text:
        if char in translit_dict:
            transliterated_text += translit_dict[char]
        else:
            transliterated_text += char
    return transliterated_text


if __name__ == '__main__':
    tr = transliterate('Pochemu transakciya cherez prilozhenie uzhe 2 ')
    # tr = transliterate('салом! korti manba pul gzaron')
    print(tr)