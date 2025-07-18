import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_recommendation(summary):
    prompt = f"""
    You're a product strategist. Here's the summary of an A/B test:

    {summary}

    Based on this, what should the team do next?
    Give clear, actionable advice in 3-5 bullet points.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a senior product strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
