import os

import openai


def generate_bibr_story():
    """
    Generate a short 50-word story in Russian
    about an orange plush beaver named Bibr
    wearing blue jeans jumpsuit, describing
    what he did today.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Feel free to adjust the prompt to your taste
    prompt_text = (
        "Составь короткую историю ровно на 50 слов по-русски о рыжем плюшевом бобре по имени Бибр "
        "в голубом джинсовом комбинезоне. Описывай, что Бибр сегодня сделал забавного и удивительного."
    )

    response = openai.Completion.create(
        model="gpt-4o-mini",  # or whatever model name you prefer
        prompt=prompt_text,
        max_tokens=200,  # Just enough for 50 words
        temperature=0.7,
    )

    # Extract text
    story = response.choices[0].text.strip()
    return story


def update_index_html(story_text):
    index_file = "index.html"

    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Identify the marker in HTML where we replace the story
    start_marker = '<div id="story">'
    end_marker = "</div>"

    # This is a simplistic approach: find the first <div id="story">
    start_index = content.find(start_marker)
    if start_index == -1:
        raise ValueError("start_marker not found in index.html")

    # We jump past the marker itself
    start_index += len(start_marker)

    end_index = content.find(end_marker, start_index)
    if end_index == -1:
        raise ValueError("end_marker not found in index.html")

    # Build new content
    new_content = (
        content[:start_index] + "\n<p>" + story_text + "</p>\n" + content[end_index:]
    )

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    story = generate_bibr_story()
    update_index_html(story)
