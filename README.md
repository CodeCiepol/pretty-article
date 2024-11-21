# pretty-article

Interacts with OpenAI's API to process a text article and generate a structured HTML output. The application is designed to transform a plain text article into an HTML file with semantic tags and placeholders for images, making it ready for further styling and enhancement.

## Prerequisites

Before running this program, ensure the following dependencies are installed:

- Python 3.7 or higher
- `openai` library
- `beautifulsoup4`
- `python-dotenv`

## Setup

1. Create a `.env` file in the project root directory and add your OpenAI API key:
   API_KEY=your_api_key_here

2. Prepare the following files:
   - `artykul.txt` - your input article text 
   - `szablon.html` - HTML template file (optional)

## Usage

1. Place your article text in `artykul.txt`

2. Run the script:
   `python main.py`

3. The script will generate two files:
   - `artykul.html` - contains the formatted HTML article
   - `podglad.html` - preview file with the article inserted into the template

## Configuration

You can modify these variables in the script:
output_language = "Polish"  # Change the output language
model = "gpt-4o-mini"      # Change the GPT model

## Output Format

The generated HTML will include:
- Semantic HTML tags (`<article>`, `<h1>`, `<h2>`, `<p>`, etc.)
- Image placeholders with descriptive alt text
- Proper content hierarchy
- Clean, formatted HTML structure"""