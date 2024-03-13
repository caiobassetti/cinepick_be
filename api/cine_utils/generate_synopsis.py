# Import statements
import os
import openai

def generate_syn(title_1, title_2):
    # Load environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY')

    openai.api_key = openai_api_key
    prompt = f"Merge and rewrite the synopsis from '{title_1}' and '{title_2}'. Create a new synopsis incorporating elements from both."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Update model as necessary
        messages=[
            {"role": "system", "content": "You are a creative writer. Please merge the following movie synopses."},
            {"role": "user", "content": prompt}

        ],
        max_tokens=200
    )

    synopsis = response.choices[0].message.content
    return synopsis
