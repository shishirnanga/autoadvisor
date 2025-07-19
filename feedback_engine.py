import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_feedback_insights(text):
    prompt = f"""
    You're a product UX researcher. Analyze the following customer feedback:

    {text}

    Identify the top 3-5 most common themes (bugs, praise, suggestions, complaints).
    Then provide actionable recommendations.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert product feedback analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
