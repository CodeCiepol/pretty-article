import os
import requests
from dotenv import load_dotenv
from openai import OpenAI


def get_article_from_URL(url: str, encoding="utf-8"):
    r = requests.get(url)
    r.encoding = encoding
    return r.text


number_of_responses = 1
model = "gpt-4o-mini"
article_str = get_article_from_URL(
    "https://cdn.oxido.pl/hr/Zadanie%20dla%20JJunior%20AI%20Developera%20-%20tresc%20artykulu.txt"
)

load_dotenv()
API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "Write what this article is about (in Polish language, max 3 sentences) into JSON data.",
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
                        "description": "The description of article that appears in the input",
                        "type": "string",
                    },
                    "additionalProperties": False,
                },
            },
        },
    },
    n=number_of_responses,
)

print(response.choices[0].message.content)
"""
response:
{
"article":
"Artykuł omawia wpływ sztucznej inteligencji (AI) na codzienne życie, 
podkreślając jej zastosowania oraz wyzwania etyczne i społeczne związane z jej rozwojem. 
Zawiera analizę automatyzacji procesów dzięki AI oraz jej potencjalnego wpływu na rynek pracy, wskazując na konieczność przemyślanej transformacji i edukacji pracowników. 
Podkreśla również znaczenie współpracy między ludźmi a AI oraz rozwijania umiejętności, aby móc sprostać przyszłym wymaganiom rynku."
}

"""
