# python version 3.7.

from unicodedata import name
import nagisa
import regex as re
import requests
import random
import genanki
import sys
import os
import wanakana


card_data = {}

card_model = genanki.Model(
  random.randrange(1 << 30, 1 << 31),
  'Simple Model',
  fields=[
    {'name': 'meaning'},
    {'name': 'reading'},
    {'name': 'reading_kana'},
  ],
  templates=[
    {
      'name': 'reading to meaning',
      'qfmt': '{{furigana:reading}}<br/>{{reading_kana}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{meaning}}',
    },
    {
      'name': 'meaning to reading',
      'qfmt': '{{meaning}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{furigana:reading}}<br/>{{reading_kana}}',
    }

  ],
  css=""".card {
 font-family: helvetica;
 font-size: 28px;
 text-align: center;
 color: black;
 background-color: white;
}
""")

def jankify(text):
    text = file.read()
    # text = "焦がす"
    # print(text)
    words = set()
    deck = genanki.Deck(
    random.randrange(1 << 30, 1 << 31),
    title)

    for word in filter(
            lambda w: not re.match(r'^\s*$', w) and not re.match(r'\W', w) and re.match(r'\p{Hiragana}|\p{Katakana}|\p{Han}', w), 
            nagisa.filter(text, filter_postags=['助詞', '助動詞']).words):
        words.add(word)
    for word in words:
        print('----------------------------------------------------')
        try:
        
            x = requests.get(f"https://jisho.org/api/v1/search/words?keyword={word}").json()['data'][0]
            # Get dict form, reading and meaning from jisho
            furi_word = ''
            word = x['japanese'][0]['word']
            w_p = 0
            r_p = 0
            reading = x['japanese'][0]['reading']
            meaning = ', '.join(x['senses'][0]['english_definitions'])
            furi_open = False
            
            print(f"word: {word}")
            print(f"reading: {reading}")

            while len(word) > w_p:
                # if non kanji add to str
                if not wanakana.is_kanji(word[w_p]):
                    furi_word +=word[w_p]
                    w_p+=1
                    r_p+=1
                else:
                    #if kanji find next non kanji and match it to reading 
                    s_p = w_p
                    next_nk = ''
                    kanj_c = 0
                    while len(word) > s_p and next_nk == '':
                        if not wanakana.is_kanji(word[s_p]):
                            next_nk = word[s_p]
                        else:
                            kanj_c += 1
                            furi_word += word[s_p]
                        s_p += 1
                    furigana = ""
                    print(kanj_c)
                    while True:
                        
                        if next_nk == reading[r_p] and len(furigana) >= kanj_c:
                                # furigana += reading[r_p]
                                break
                        furigana += reading[r_p]
                        if len(reading)-1 > r_p:
                            
                            r_p +=1
                        else: 
                            break

                    furi_word += f'[{furigana}]' 
                        
                    if next_nk != '':
                        furi_word +=next_nk
                    w_p = s_p
            print(f"Furiganad: {furi_word}")
                    


            #Create card
            note = genanki.Note(
                model=card_model,
                fields=[meaning, furi_word,reading])
            #Add card to deck
            deck.add_note(note)
        except Exception as e:
            print(e)
    return deck


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        print(sys.argv[1])
        file_name = os.path.basename(sys.argv[1])
        title =os.path.splitext(file_name)[0]
        text = file.read()
        deck = jankify(text)
        genanki.Package(deck).write_to_file(f'{title}.apkg')