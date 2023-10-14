from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

def complete(sentence: str, word_list: list[str]):
    word_scores = {}
    if len(sentence) > 0:
        # Initialize the model and tokenizer
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
        model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
        model.eval()

        # Tokenize the input sentence
        inputs = tokenizer.encode(sentence, return_tensors="pt")

        # Get the model's raw logits for the last word
        with torch.no_grad():
            outputs = model(inputs)
            logits = outputs.logits[:, -1, :]

        # Convert logits to probabilities
        probabilities = torch.nn.functional.softmax(logits, dim=-1)

        # Extract the scores for each word in word_list
        for word in word_list:
            word_id = tokenizer.encode(word, add_special_tokens=False)[0]
            word_scores[word] = probabilities[0][word_id].item()

    return word_scores