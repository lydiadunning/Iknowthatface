# class for listing movies and tv the user has seen
# adding basic functionality for both tv and movies, both might not be necessary.

class Viewed:
    def __init__(self):
        self.movies = []
        self.tv = []

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
        if medium == 'movies':
            return [work for work in work_list if work['movie_id'] in self.movies] + [work for work in work_list if work['movie_id'] not in self.movies]
        if medium == 'tv':
            return [work for work in work_list if work['tv_id'] in self.tv] + [work for work in work_list if work['tv_id'] in self.tv]


