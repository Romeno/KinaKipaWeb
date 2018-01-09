
meta_patterns = {
    'length': 'Працяглась*ць:*</strong>\s*:*\s*(.*?)<br'
}

patterns_header = {
    'name': [
        r'^([^/]+)\/' # from the beginning to "/"
    ],
    'name_origin': [
        r'/([^(/]+)\(',
        r'/([^/]+)\/'
    ],
    'year': [
        r'/\s*(\d{4})\s*/*', # / 2017 /, /2017, /2017/, etc.
        r'\d{4}-\d{4}', # / 2016-2017 /
        r'\[(\d{4}),', # [2015, blah-blah...]
        r'\((\d{4})\)' # (2015) blah
    ]
}

patterns_body = {
    'country': [
        r'Краіна:(.*)\n'
    ],
    'director': [
        r'Рэжыс[ёэ]р:(.*)\n'
    ],
    'stars' : [
        r'Ролі выконва\w+:(.*)\n',
        r'Акцёры:(.*)\n',
        r'У р[оа]лях:(.*)\n'
    ],
    'description': [
        r'Пра ф\w{4}:(.+)\n',
        r'Аб ф\w{5}:(.+)\n',
        r'Апісань*не:(.+)\n'
    ],
    'genres': [
        r'Жана*р:(.+)\n'
    ],
    # 'length': [
    #     r'Працяглась*ць:(.+)\n'
    # ]
        }

