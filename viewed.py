# class for listing movies and tv the user has seen
# adding basic functionality for both tv and movies, both might not be necessary.

class Viewed:
    def __init__(self):
        self.movies = [673, 1833]
        self.tv = [4087, 67198]

    def add_new(self, medium, work_id):
        if medium == 'movie' and work_id not in self.movies:
            self.movies.append(work_id)
        if medium == 'tv' and work_id not in self.tv:
            self.tv.append(work_id)

    def remove_work(self, medium, work_id):
        if medium == 'movie' and work_id in self.movies:
            self.movies.remove(work_id)
        if medium == 'tv' and work_id in self.tv:
            self.tv.remove(work_id)

    def prioritize(self, medium, work_list):
        print(f'prioritizing {medium}')
        if medium == 'movie':
            print(self.movies)
            print(work_list)
            part_1 = [work for work in work_list if work['id'] in self.movies]
            part_2 = [work for work in work_list if work['id'] not in self.movies]
            print(part_1)
            print(part_2)
            return part_1 + part_2
            # return [work for work in work_list if work['id'] in self.movies] + [work for work in work_list if work['id'] not in self.movies]
        if medium == 'tv':
            print(self.tv)
            # return [work for work in work_list if work['id'] in self.tv] + [work for work in work_list if work['id'] not in self.tv]
            print([work['id'] for work in work_list])
            part_1 = [work for work in work_list if work['id'] in self.tv]
            part_2 = [work for work in work_list if work['id'] not in self.tv]
            print(part_1)
            print(part_2)
            return part_1 + part_2


