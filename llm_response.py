from transformers import pipeline

chatbot = pipeline(
    "text-generation",
    model="distilgpt2"
)

def generate_ai_response(user_message):

    prompt = f"Question: {user_message}\nAnswer:"

    response = chatbot(
        prompt,
        max_new_tokens=50,
        temperature=0.7,
        do_sample=True,
        num_return_sequences=1,
        pad_token_id=50256
    )

    generated_text = response[0]["generated_text"]

    # Extract only answer part
    if "Answer:" in generated_text:
        generated_text = generated_text.split("Answer:")[-1]

    return generated_text.strip()