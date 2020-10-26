from locust import HttpLocust, TaskSet, task, between
import random

# proxies = {
#   'http': 'http://cors-anywhere.herokuapp.com/"',
#   'https': 'https://cors-anywhere.herokuapp.com/"',
# }

# with self.client.get(get_web_url(), proxies=proxies) as response:
#     pass

class UserBehaviourAPI(TaskSet):
    root_url = "https://fncflnxl03.execute-api.eu-west-2.amazonaws.com/testing/"
    proxyurl = "https://cors-anywhere.herokuapp.com/"

    base_query = "/testing/fetch-venues?query=&pricemin=0&pricemax=3&latitude=51.4988&longitude=-0.1749&radius=2&restaurants=true&bars=true&cafes=true"
    filters_query = "/testing/fetch-venues?query=&pricemin=1&pricemax=2&latitude=51.4988&longitude=-0.1749&radius=2&restaurants=true&bars=false&cafes=true"
    search_word_query = "/testing/fetch-venues?query=chicken&pricemin=0&pricemax=3&latitude=51.4988&longitude=-0.1749&radius=2&restaurants=true&bars=true&cafes=true"
    queries = [[base_query, "base_query"], [filters_query, "filters_query"], [search_word_query, "search_word_query"]]

    menu_query = "/testing/get-menu?venueid=1&typeid=1"

    postcode_query = "https://api.postcodes.io/postcodes/SW72AZ"


    @task(2)
    def get_venues(self):
        query = UserBehaviour.queries[random.randint(0,2)]
        self.client.get(f"{query[0]}", name=query[1])

    @task(1)
    def get_menu(self):
        self.client.get(f"{UserBehaviour.menu_query}", name="get_menu")

    # @task(1)
    # def get_coords(self):
    #     self.client.get(f"{UserBehaviour.postcode_query}")

class UserBehaviourBase(TaskSet):
  @task
  def page_load(self):
    self.client.get('/', name="load")

class WebsiteUser(HttpLocust):
    task_set = UserBehaviourBase
    wait_time = between(5, 9)
