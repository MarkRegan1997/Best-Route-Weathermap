import requests
import json
from itertools import permutations

API_KEY = "054ff6c4bb4734f4242bf89a6732144f"
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"


class City:

    def __init__(self, name, temperatures):
        self.name = name
        self.temps = temperatures

    def get_temp(self, day):
        return self.temps[day]

    def __str__(self):
        return self.name

class Route:

    def __init__(self, path, temp):
        self.path = path
        self.avg_temp = temp

    def get_path(self):
        return list(self.path)

    def get_temp(self):
        return self.avg_temp

    def __str__(self):
        return self.path

def fetch_weather(id):
    """
    finds the average temperature for the next 5 days of the city id that is passed to it
    :param id:
    :return:
    """

    temp_list = []

    # request parameter(s): Start with '?'
    # separate name and value with '='
    # multiple parameter name value pairs are separate with '&'
    # encode space ' ' with '%20'
    query_string = "?id={}&US&units=imperial&APIKEY={}".format(id, API_KEY)
    request_url = WS_URL + query_string
    # print("Request URL: ",request_url)
    response = requests.get(request_url)

    if response.status_code == 200:

        # get the info for the city
        d = response.json()
        city_name = (d["city"]["name"])

        tem_lst = d['list']

        for i in range (len(tem_lst) // 8):
            li = (x for x in range(len(tem_lst)) if x // 8 == i)
            # get max temp for every day
            temp_list.append(max([tem_lst[j]["main"]["temp_max"] for j in li] ))

        return City(city_name, temp_list)

    else:
        print("\nHow should I know?")

if __name__ == "__main__":

    try:
        id_list = json.loads(open("cities.json").read())
    except:
        print("Oops, where is the file")

    # get the temperatures for all the cities
    cities_list = []
    for id in id_list:
        cities_list.append(fetch_weather(id))

    # create the permutations for the cities
    perm_list = list(permutations(cities_list))

    # initialize the value to keep track of the lowest average temp among routes
    lowest_avg = 1000

    for perm in perm_list:
        # reset the avgerage temp for this permutation
        avg_temp = 0
        for city in perm:
            avg_temp += (city.get_temp(perm.index(city)))

        # calculate the average temperature for this permuutaion
        avg_temp /= len(cities_list)

        # calculate if the avg temp for this permutation is the lowest so far, if so update the best route object
        if avg_temp < lowest_avg:
            lowest_avg = avg_temp
            best_route = Route(perm, avg_temp)

    # print out the information for the best route
    print("Best Route: " )
    for city in best_route.get_path():
        print("\tDay {}: {:<20} {}".format(str(best_route.get_path().index(city) + 1), city.name, "Temp: " + str(city.get_temp(best_route.get_path().index(city)))))

    print("Average Temperature: " + str(best_route.get_temp()))