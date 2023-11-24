import google.generativeai as palm

palm.configure(api_key="AIzaSyB5gh0evVf6e3Qwb5mKP-Krol3GEfxJU8k")

defaults = {
  'model': 'tunedModels/customer-support-1ljt7t7890as',
  'temperature': 0.7,
  'candidate_count': 5,
  'top_k': 40,
  'top_p': 0.95,
}
context = "My order cancel"
examples = []
messages = []
messages.append("NEXT REQUEST")
response = palm.chat(
  **defaults,
  context=context,
  examples=examples,
  messages=messages
)
print(response.last)