from transformers import pipeline

def generate_unbiased_article(articles):
    """
    Generate an unbiased article using a simpler AI model (GPT-2) based on multiple news sources.
    """
    # Combine summaries from multiple articles
    combined_text = "\n\n".join([article['summary'] for article in articles])

    # Load GPT-2 model and tokenizer from Hugging Face
    generator = pipeline('text-generation', model='gpt2')

    try:
        # Generate text based on the combined summaries
        response = generator(f"Create an unbiased news article based on the following summaries:\n\n{combined_text}", max_length=300, num_return_sequences=1)

        # Extract generated text from the response
        generated_article = response[0]['generated_text']
        return generated_article

    except Exception as e:
        return f"Error during text generation: {e}"
