from google import genai

client = genai.Client(api_key="AIzaSyDq6K2TW5HX-e_BcWbWWXvb7xSMaDyChSgY")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)