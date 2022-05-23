#Search, API

from flask import Flask, json, render_template
import requests

from pprint import pprint


app = Flask(__name__)

# @app.route('/home')
# @app.route("/")
# def home():
#     return render_template('home.html')

user_enters_movie = input("What movie do you want to search? ")


url = "https://api.themoviedb.org/3/search/movie?api_key=616b9b69d0327374c87a5514821907a5&language=en-US&query={}&page=1&include_adult=false".format(user_enters_movie)




##Recommend films based on movie id
# url = "https://api.themoviedb.org/3/movie/10625/recommendations?api_key=616b9b69d0327374c87a5514821907a5&language=en-US&page=1"

# # ## Fight Club and recommendations
# url = 'https://api.themoviedb.org/3/movie/680?api_key=616b9b69d0327374c87a5514821907a5&append_to_response=recommendations'

# pprint(url)
    # 'https://api.themoviedb.org/3/movie/550?api_key=616b9b69d0327374c87a5514821907a5'
response = requests.get(url)
moviedb = response.json()
pprint(moviedb)

# https://api.themoviedb.org/3/movie/550?api_key=616b9b69d0327374c87a5514821907a5&language=en-US


# moviedb_title_list = [x['original_title']for x in moviedb['results']]

# moviedb_title_list = [x['id'] for x in moviedb['results']]
moviedb_title_list = [x['title'] for x in moviedb['results']]
moviedb_id_list = [x['id'] for x in moviedb['results']]
# both_list = [x['id']['original_title'] for x in moviedb['results']]
# pprint(both_list)

output_title = "MOVIE TITLE: " + str(moviedb_title_list)
output_id = "MOVIE ID: " + str(moviedb_id_list)
output_both = output_title + output_id
output_title_and_id = "MOVIE TITLE: " + str(moviedb_title_list) + "MOVIE ID: " + str(moviedb_id_list)
output_2 = f"MOVIE ID: {str(moviedb_id_list)} MOVIE TITLE: {str(moviedb_title_list)}"
# pprint(output_2)
output_3 = str(moviedb_id_list), str(moviedb_title_list)
# pprint(output_3)

# pprint(moviedb_id_list[0])


# recommendations

id_for_recommendation = moviedb_id_list[0]

rec_url = 'https://api.themoviedb.org/3/movie/{}?api_key=616b9b69d0327374c87a5514821907a5&append_to_response=recommendations'.format(id_for_recommendation)
response = requests.get(rec_url)
rec_moviedb = response.json()
pprint(rec_moviedb)


# output = moviedb_id_list, moviedb_title_list
# pprint(output)


# pprint(output_title_and_id)
# pprint("BOTH LIST" + str(both_list))

# for x in moviedb_title_list:
#     moviedb_title_list.split(", ")
#     pprint("MOVIE TITLE: " + str(moviedb_title_list) + "ID: " + str(moviedb_id_list))

# x = txt.split(", ")

# moves_list = [x['move'] for x in pokemon['moves']]

# pokemon_number = input("What is the Pokemon's ID? ")
#
# url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number) # note how we manupulate the url to request data!
#
# response = requests.get(url)
# print(response)
#
# pokemon = response.json()
# pprint(pokemon)


app.config["DEBUG"] = True


# @app.route('/', methods=['GET'])
# def home():
#     return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()







if __name__ == '__main__':
    app.run(debug=True)