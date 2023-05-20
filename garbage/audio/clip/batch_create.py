from garbage.audio.clip.youtube import create_clips

character_types = ['elf', 'orc', 'troll', 'dragon', 'gnome', 'vampire', 'werewolf', 'fairy', 'centaur', 'minotaur', 'demon']

urls = ['https://youtu.be/iozTg6Qps6s',
        'https://www.youtube.com/watch?v=DBnKjIVDdOw',
        'https://www.youtube.com/watch?v=YSd0UFJPpzw',
        'https://www.youtube.com/watch?v=QxYHkKLaFmY'
        'https://www.youtube.com/watch?v=yUrXrhWa0GA',
        'https://www.youtube.com/watch?v=uAISFiDCAa0',
        'https://www.youtube.com/watch?v=jIR8WFjuKio',
        'https://www.youtube.com/watch?v=iBf-mnslA3M',
        'https://www.youtube.com/watch?v=LaA-za0fxHI',
        'https://www.youtube.com/watch?v=aUQo2J7RZw0',
        'https://www.youtube.com/watch?v=MZh9iATzJ44'
        ]


def main():
    for name, url in zip(character_types, urls):

        create_clips(url, name)

if __name__ == '__main__':

    main()