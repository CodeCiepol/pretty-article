import os
from dotenv import load_dotenv
from openai import OpenAI


def get_article_from_file(name: str):
    with open(f"{name}", "r") as file:
        return file.read()


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

print(response.choices[0].message.content)
"""
<article>
    <h1>Sztuczna inteligencja: wpływ i wyzwania</h1>
    <p>Sztuczna inteligencja to dziedzina nauki i technologii zajmująca się tworzeniem maszyn i programów zdolnych do wykonywania zadań wymagających ludzkiej inteligencji, takich jak uczenie się, rozumienie języka naturalnego i podejmowanie decyzji. AI stała się integralną częścią naszego codziennego życia, od asystentów głosowych w smartfonach, jak Siri czy Google Assistant, po systemy rekomendacyjne na platformach streamingowych, takich jak Netflix czy Spotify. Wspiera nas w planowaniu tras, automatyzacji domowych urządzeń oraz w komunikacji. Obecnie jest o niej bardzo głośno chociażby za sprawą dużych modeli językowych, jak ChatGPT.</p>

    <h2>Rozwój uczenia maszynowego i głębokiego uczenia</h2>
    <p>Rozwój uczenia maszynowego i głębokiego uczenia umożliwił tworzenie zaawansowanych modeli, które potrafią samodzielnie rozwiązywać skomplikowane problemy. Sieci neuronowe analizują ogromne ilości danych w obszarach takich jak rozpoznawanie obrazów czy przetwarzanie języka naturalnego. Dzięki temu AI nie tylko przetwarza dane, ale także podejmuje decyzje, wcześniej zarezerwowane dla ludzi.</p>

    <h2>Wyzwania etyczne i społeczne</h2>
    <p>Kluczowym wyzwaniem jest zapewnienie etycznego i odpowiedzialnego rozwoju AI. Należy zwracać uwagę na uprzedzenia w danych treningowych, które mogą prowadzić do dyskryminacji, oraz na wpływ AI na prywatność i nierówności społeczne. Ważne jest opracowanie ram etycznych i mechanizmów nadzoru regulujących rozwój i wdrażanie AI, a także włączanie różnych grup społecznych w ten proces. Transparentność działań firm i instytucji może pomóc w budowaniu zaufania do technologii.</p>
    <figure>
        <img src="image_placeholder.jpg" alt="Ilustracja pokazująca różne aspekty etycznego rozwoju sztucznej inteligencji, z postaciami dyskutującymi nad komputerem.">
        <figcaption>Ilustracja omawiająca etyczne wyzwania związane z rozwojem sztucznej inteligencji.</figcaption>
    </figure>

    <p>Badacze pracują nad rozwiązaniami umożliwiającymi harmonijne współistnienie ludzi i AI, koncentrując się na tworzeniu systemów wspierających człowieka, a nie go zastępujących. Istotne jest opracowywanie mechanizmów współpracy między człowiekiem a maszyną, co sprzyja synergii i skutecznej komunikacji.</p>

    <h2>Automatyzacja i przyszłość rynku pracy</h2>
    <p>Automatyzacja procesów dzięki AI przynosi korzyści w postaci zwiększonej efektywności i redukcji kosztów. Jednak istnieją obawy dotyczące wpływu na rynek pracy i potencjalnego zastąpienia ludzi przez maszyny. Kluczowe jest przemyślane podejście do transformacji rynku pracy, inwestycja w edukację i przekwalifikowanie pracowników, aby mogli oni znaleźć nowe role w gospodarce przyszłości.</p>
    <figure>
        <img src="image_placeholder.jpg" alt="Wizualizacja przedstawiająca przyszłość rynku pracy z technologią AI, gdzie ludzie i roboty współpracują ze sobą.">
        <figcaption>Wizualizacja współpracy ludzi z maszynami w kontekście rynku pracy.</figcaption>
    </figure>

    <p>Specjaliści powinni być gotowi na ciągłe doskonalenie swoich umiejętności, ucząc się m.in. zasad działania algorytmów AI. Przyszłość pracy będzie wymagać nie tylko umiejętności technicznych, ale także kompetencji miękkich, takich jak kreatywność i zdolność rozwiązywania problemów.</p>

    <p>Nasza zdolność do adaptacji i innowacji zdecyduje o tym, jak AI wpłynie na przyszłość ludzkości. Wspólnie możemy kształtować tę przyszłość, wykorzystując AI dla dobra wszystkich.</p>

    <p><em>Tekst opracowany przez AI. W Oxido nie mamy aż tak cukierkowego spojrzenia na sztuczną inteligencję... ;)</em></p>
</article>
"""
