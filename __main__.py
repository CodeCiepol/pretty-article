import os
import json
from dotenv import load_dotenv
from openai import OpenAI


def get_article_from_file(name: str):
    with open(f"{name}", "r") as file:
        return file.read()


def save_article(content: str, filename: str):
    with open(f"{filename}", "w") as file:
        file.write(content)


load_dotenv()
API_KEY = os.getenv("API_KEY")

output_language = "Polish"
model = "gpt-4o-mini"
number_of_responses = 1

article_str = get_article_from_file("artykul.txt")

prompt = f'Use appropriate HTML tags to structure given article content. Follow these guidelines:\n \
1. Use semantic HTML tags such as <h1>, <h2>, <p>, <ul>, <ol> to properly organize the content.\n\
2. Indicate places where images should be included by using the <img> tag with the attribute src="image_placeholder.jpg".\n\
3. Add an alt attribute to each <img> tag that provides a detailed prompt for generating the image.\n\
4. Include captions under the images using the <figcaption> tag, wrapping <img> and <figcaption> within a <figure> tag.\n\
5. Exclude CSS and JavaScript code – only include content meant to go between <body> and </body>.\n\
6. Use {output_language} language.'


client = OpenAI(api_key=API_KEY)

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
    n=number_of_responses,
)

response_dict = json.loads(response.choices[0].message.content)
save_article(response_dict["article"], "artykul.html")
