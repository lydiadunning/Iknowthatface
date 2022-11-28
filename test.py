from pprint import pprint

movie = {
        'adult': False,
        'backdrop_path': '/xK28lhRlypVf1sE3sNZNfcsPKPA.jpg',
         'genre_ids': [28, 35, 27],
         'id': 10206,
         'original_language': 'en',
         'original_title': 'Buffy the Vampire Slayer',
         'overview': 'Blonde, bouncy Buffy is your typical high school cheerleader. '
                     "But all that changes when a strange man informs her she's been "
                     'chosen by fate to kill vampires.',
         'popularity': 12.503,
         'poster_path': '/tcF3S4UdFpuoZEWovMDq5AXazNF.jpg',
         'release_date': '1992-07-24',
         'title': 'Buffy the Vampire Slayer',
         'video': False,
         'vote_average': 5.6,
         'vote_count': 632
    }

tv = {
        'backdrop_path': '/q4CbisNArigphVn608Faxijdw8N.jpg',
         'first_air_date': '1997-03-10',
         'genre_ids': [10765, 35, 18, 10759],
         'id': 95,
         'name': 'Buffy the Vampire Slayer',
         'origin_country': ['US'],
         'original_language': 'en',
         'original_name': 'Buffy the Vampire Slayer',
         'overview': 'Into every generation a slayer is born: one girl in all the '
                     'world, a chosen one. She alone will wield the strength and skill '
                     'to fight the vampires, demons, and the forces of darkness; to '
                     'stop the spread of their evil and the swell of their number. She '
                     'is the Slayer.',
         'popularity': 67.997,
         'poster_path': '/y7fVZkyheCEQHDUEHwNmYENGfT2.jpg',
         'vote_average': 8.2,
         'vote_count': 1257
    }

def error_insertion(work_dict):
    work_list = []
    for key in work_dict.keys():
        if key != 'id' and key != 'title':
            temporary_dict = work_dict.copy()
            del temporary_dict[key]
            work_list.append(temporary_dict)
    return work_list

error_movie_list = error_insertion(movie)
error_tv_list = error_insertion(tv)