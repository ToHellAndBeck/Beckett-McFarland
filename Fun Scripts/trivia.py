import requests
from typing import Literal
from random import choice

API_URL = "https://opentdb.com/api.php?amount=1"

def hit_api(url, method: Literal["get", "post"] = "get", return_type: Literal["json", "content"] | None = "json"):
    hit_method = requests.get if method == 'get' else requests.post
    return hit_method(url).json() if return_type == 'json' else hit_method(url).content.decode()

def get_random_trivia_question():
    response = hit_api(API_URL)
    if response and 'results' in response:
        trivia_data = response['results'][0]
        return trivia_data
    else:
        return None

def main():
    # Get a random trivia question
    trivia_question = get_random_trivia_question()

    if trivia_question:
        print("Random Trivia Question:")
        print("Category:", trivia_question['category'])
        print("Question:", trivia_question['question'])
        print("Correct Answer:", trivia_question['correct_answer'])
        print("Incorrect Answers:", trivia_question['incorrect_answers'])
    else:
        print("Failed to retrieve a trivia question.")

if __name__ == "__main__":
    main()
