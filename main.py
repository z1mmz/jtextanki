# python version 3.7.

from unicodedata import name
import nagisa
import regex as re
import requests
import random
import genanki
import sys
import os

card_data = {}

card_model = genanki.Model(
  random.randrange(1 << 30, 1 << 31),
  'Simple Model',
  fields=[
    {'name': 'meaning'},
    {'name': 'reading'},
  ],
  templates=[
    {
      'name': 'meaning to reading',
      'qfmt': '{{meaning}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{furigana:reading}}',
    },
    {
      'name': 'reading to meaning',
      'qfmt': '{{furigana:reading}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{meaning}}',
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


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        print(sys.argv[1])
        file_name = os.path.basename(sys.argv[1])
        title =os.path.splitext(file_name)[0]
        text = file.read()
        print(text)
        words = set()
        deck = genanki.Deck(
        random.randrange(1 << 30, 1 << 31),
        title)

        for word in filter(
                lambda w: not re.match(r'^\s*$', w) and not re.match(r'\W', w) and re.match(r'\p{Hiragana}|\p{Katakana}|\p{Han}', w), 
                nagisa.filter(text, filter_postags=['助詞', '助動詞']).words):
            words.add(word)
        for word in words:
            try:
                print(word)
                x = requests.get(f"https://jisho.org/api/v1/search/words?keyword={word}").json()['data'][0]
                # Get dict form, reading and meaning from jisho
                word = x['japanese'][0]['word']
                reading = f"{word}[{x['japanese'][0]['reading']}]"
                meaning = ', '.join(x['senses'][0]['english_definitions'])
                #Create card
                note = genanki.Note(
                    model=card_model,
                    fields=[meaning, reading])
                #Add card to deck
                deck.add_note(note)
            except Exception as e:
                print(e)

        genanki.Package(deck).write_to_file(f'{title}.apkg')