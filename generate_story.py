import os

from openai import OpenAI


def generate_bibr_story():
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    # Load prompt from text file
    prompt_file = os.path.join(os.path.dirname(__file__), "prompt.txt")
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_text = f.read()
    except FileNotFoundError:
        print(f"Error: Prompt file not found at {prompt_file}")
        return "Error generating story: prompt file not found."

    response = client.responses.create(
        model="gpt-4o",
        input=prompt_text,
        temperature=0.7,
        max_output_tokens=200,
    )

    return response.output_text


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
