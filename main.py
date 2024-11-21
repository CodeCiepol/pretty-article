import os
import json
import openai
from openai import OpenAI
from dotenv import load_dotenv
from bs4 import BeautifulSoup


def get_file(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        file_str = file.read()
    return file_str


def save_file(content: str, filename: str):
    with open(f"{filename}", "w", encoding="utf-8") as file:
        file.write(content)


def generate_view_from_template(article_html, template_name="szablon.html"):
    template_html = get_file(template_name)

    template_soup = BeautifulSoup(template_html, "html.parser")

    if template_soup.body:
        template_soup.body.clear()
        template_soup.body.append(article_html)
        save_file(str(template_soup.prettify()), "podglad.html")


load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise EnvironmentError(
        "Missing API key. Ensure that the .env file contains the correct API_KEY variable."
    )

output_language = "Polish"
model = "gpt-4o-mini"

article_str = get_file("artykul.txt")

prompt = f'Use appropriate HTML tags to structure given article content. Follow these guidelines:\n \
1. Use semantic HTML tags such as <article>, <h1>, <h2>, <p>, <ul>, <ol> to properly organize the content.\n\
2. Indicate places where images should be included by using the <img> tag with the attribute src="image_placeholder.jpg".\n\
3. Add an alt attribute to each <img> tag that provides a detailed prompt for generating the image.\n\
4. Include captions under the images using the <figcaption> tag, wrapping <img> and <figcaption> within a <figure> tag.\n\
5. Exclude CSS and JavaScript code – only include content meant to go between <body> and </body>.\n\
6. Use {output_language} language.'


# prepare the message
def get_response_from_openai():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {"role": "user", "content": article_str},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "article_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "article": {
                            "description": "The formatted article that appears in the input",
                            "type": "string",
                        },
                        "additionalProperties": False,
                    },
                },
            },
        },
        n=1,
    )
    return response


# get the response
client = OpenAI(api_key=API_KEY)

response = get_response_from_openai()

# Handle the response data
if not response.choices:
    raise IndexError("No data in openai response.")

message_content = response.choices[0].message.content
response_dict = json.loads(message_content)
formatted_article_str = response_dict["article"]

save_file(formatted_article_str, "artykul.html")

generate_view_from_template(BeautifulSoup(formatted_article_str, "html.parser"))
