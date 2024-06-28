import openai
import openai.error
import utills  # Ensure this is the correct import based on your actual utils module
import time
import random

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = utills.token

# Function to list available models
def list_models():
    models = openai.Model.list()
    available_models = [model['id'] for model in models['data']]
    return available_models

# Function to generate a response using OpenAI with error handling
def generate_response(prompt, model="text-embedding-ada-002", max_tokens=100, retry_limit=5):
    attempt = 0
    while attempt < retry_limit:
        try:
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except openai.error.InvalidRequestError as e:
            if "You are not allowed to sample from this model" in str(e):
                print(f"Model '{model}' is not available. Checking available models.")
                available_models = list_models()
                print("Available models:", available_models)
                if available_models:
                    model = available_models[0]  # Use the first available model
                    print(f"Switching to model '{model}'")
                else:
                    return "Error: No available models found."
            else:
                print(f"Invalid request error: {e}")
                break
        except openai.error.RateLimitError:
            attempt += 1
            sleep_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff with jitter
            print(f"Rate limit exceeded. Retrying in {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        except openai.error.OpenAIError as e:
            print(f"OpenAI error: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    return "Error: Unable to generate response after multiple attempts."

# Example usage
prompt = "Explain the theory of relativity in simple terms."

response = generate_response(prompt)
print(response)

# import pyttsx3

# import time 
# engine = pyttsx3.init()

# engine.setProperty('rate', 115)

# engine.setProperty('voice', "com.apple.eloquence.en-US.Grandma")


# def speak(text):
#     global engine
#     print("ASSISTANT -> " + text)
#     # try:
#     # engine.setProperty('voice', 'com.apple.ttsbundle.Maged-premium')
#     # engine.setProperty('rate', 185)
#     # text = "nigga ahmad was here playing some stuff "
#     engine.say(text)
#     engine.runAndWait()
#     time.sleep(2)
#     print("done ")

# if __name__ == "__main__":
#     text= "nigga ahmad was here and he doing some real shit "
#     speak(text)
 
 