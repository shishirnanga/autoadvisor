
import openai, os
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyse_dashboard(text):
    prompt = f"""
    You are a senior product analyst. Summarise this dashboard:
    
    {text}
    
    1. Key trends or anomalies
    2. Possible root causes
    3. Concrete next-step recommendations (3-5 bullets)
    """
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are an expert product data analyst."},
            {"role":"user","content":prompt}
        ],
        temperature=0.7,
        max_tokens=450
    )
    return resp.choices[0].message.content.strip()
