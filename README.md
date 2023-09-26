# iknowthatface

iknowthatface allows a user to see what other films or series an actor has appeared in.

## Usage

Hosted here: [https://iknowthatface.onrender.com/](https://iknowthatface.onrender.com/)
To run locally, install dependencies and execute the main file in python 3.10.

## Technologies

A Python server using Flask, HTML templates written with Jinja. Queries The Movie Database with API calls. CSS styling.

## Data Management

I made an interesting choice in the TMDB object in the file TMDB_access.py, to use a method to modify movie and tv show data, making it easier to use later.  
The `list_actors_with_images` method uses a list comprehension to modify the list of cast member objects returned by a query.  

```
return [{
            'id': cast_member['id'],
            'name': cast_member['name'],
            'character': cast_member['character'] if 'character' in cast_member.keys() else cast_member['roles'][0]['character'],
            'actor_image_url': f"{self.image_prefix}{cast_member['profile_path']}" if cast_member['profile_path'] else None

        } for cast_member in cast_list if cast_member['known_for_department'] == 'Acting']
```

The `list_works_by_name` method used for displaying movie and tv series information, however, processes the data for each movie through the organize_results method. The entire movie object supplied by TMDB is the first argument, followed by the desired property names with their corresponding names from TMDB.
```
  result['movie'] = [self.organize_results(
      movie,
      id='id',
      title='title',
      poster='poster_path',
      release_date='release_date',
      overview='overview') for movie in movie_response
```

The organize_results method finds the property name as supplied by TMDB, attempts to find the value given to this property by TMDB, and assigns the value None if it is not found.  Then, the desired keys are added to a new object, either with the values provided by TMDB, or, for images, image links derived from those values. Since organize_results creates a dictionary from an existing dictionary using keyword arguments, and is agnostic when it comes to any values other than key names for images, it can be used repeatedly, for all situations where information about movies and TV series is retrieved.

```
def organize_results(self, response_dict, **kwargs):
        # expects kwargs where the keyword is the desired key and the argument is the existing key
        return_dict = {}
        for key, value in kwargs.items():
            if value in response_dict.keys():
                if response_dict[value]:
                    if key == 'poster' or key == 'actor_image_url':
                        return_dict[key] = f"{self.image_prefix}{response_dict[value]}"
                    else:
                        return_dict[key] = response_dict[value]
                else:
                    return_dict[key] = None
            else:
                return_dict[key] = None
        return return_dict
```
Looking back, I think the long sequences of key word arguments in the call to organize_results seem lengthy, though they may be clearer to read than the conditionals used to create an object in list_actors_with_images. While organize_results gets the job done, the first and second conditional could be combined.

## Attribution

Gets film information from the [TMDB API](https://www.themoviedb.org/). 

