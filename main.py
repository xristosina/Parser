# Description: Программа, которая получает запрос от пользователя, выполняет поисковый запрос в Google, сохраняет текст содержимого всех выведенных сайтов в отдельно созданный html файл и отправляет его chatgpt вместе с запросом от пользователя
# возвращать результаты нужно в формате таблицы excel


from typing import List, Any
from bs4 import BeautifulSoup
import requests
import openai
import pandas as pd
try:
    from googlesearch import search
except ImportError: 
    print("No module named 'google' found")
# задаем ключ
openai.api_key = "sk-proj-ON5FvLckLLYHCuOxJNRIT3BlbkFJFcJ82ELKO3puUEGThLWN"

# получаем запрос от пользователя сайта для поиска в google
def get_search_query() -> str:
    return input("Введите запрос для поиска в Google: ")

#вводим запрос в google и возвращаем ссылки на сайты
proxy = 'http://185.117.154.164:80/'
def google(search_query: str) -> List[str]:
    search_results = []
    #удаляем повторяющиеся ссылки
    for j in search(search_query, proxy=proxy, num_results=30):
        if j not in search_results:
            search_results.append(j)
    return search_results

#получаем текст содержимого всех выведенных сайтов
def get_website_content(search_results: List[str]) -> List[str]:
    website_content = []
    for search_result in search_results:
        response = requests.get(search_result)
        soup = BeautifulSoup(response.text, "html.parser")
        website_content.append(soup.get_text())
    return website_content

#сохраняем текст содержимого всех выведенных сайтов в отдельно созданный html файл
def save_website_content(website_content: List[str]) -> None:
    with open("website_content.html", "w") as file:
        for content in website_content:
            file.write(content)

#получаем запрос от пользователя
def get_prompt() -> str:
    return input("Введите запрос для ChatGPT: ")

#передаем полученный файл с текстом и запрос от пользователя chatgpt
def get_chatgpt_response(file: str, prompt: str) -> List[str]:
    with open(file, "r") as file:
        file_content = file.read()[:10000]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt} {file_content}"},
        ]
    )
    return response["choices"][0]["message"]["content"]


#передаем полученные ссылки  и запрос от пользователя chatgpt
# def get_chatgpt_response(search_results: List[str], prompt: str) -> List[str]:
#     chatgpt_responses = []
#     for search_result in search_results:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": f"{prompt} {search_result}"},
#             ]
#         )
#         chatgpt_responses.append(response["choices"][0]["message"]["content"])
#     return chatgpt_responses
  
#получаем результаты в формате таблицы excel
def get_excel_results(search_results: List[str], chatgpt_responses: List[str]) -> Any:
    df = pd.DataFrame({"Search Results": search_results, "ChatGPT Responses": chatgpt_responses})
    df.to_excel("results.xlsx", index=False)

#запускаем программу
def main():
    search_query = get_search_query()
    search_results = google(search_query)
    print(search_results)
    website_content = get_website_content(search_results)
    save_website_content(website_content)
    prompt = get_prompt()
    chatgpt_responses = get_chatgpt_response("website_content.html", prompt)
    get_excel_results(search_results, chatgpt_responses)

    

if __name__ == "__main__":
    main()
