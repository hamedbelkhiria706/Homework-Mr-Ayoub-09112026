from dotenv import load_dotenv
from openai import OpenAI,AuthenticationError,RateLimitError
from ai import AIServiceError,get_client
from models import SummarizeResponse

def generate_summarize(text,word_count):
    try:
        client = get_client()
        SYSTEM_PROMPT = f"""
        You are a summarize generator.
        Text is {text}
        Number of words is {word_count}
        """
  
        user_message = f"Generate {word_count} words about {text}"
        response = client.beta.chat.completions.parse(
            model = "openrouter/free",
            messages=[{
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":user_message
            }],
            response_format=SummarizeResponse 
        )
    except AuthenticationError as error:
        raise AIServiceError("auth","Invalid API key")
    except RateLimitError as error:
        raise AIServiceError("rate_limit","Rate limited by the provider")
    except Exception as e:
        raise AIServiceError("Unkown",str(e))
    event = response.choices[0].message.parsed
    return event
if __name__ == "__main__":
    print(generate_flashcard("math","4","4"))
