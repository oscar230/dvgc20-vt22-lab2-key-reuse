from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

def predict(sentence: str, word_list: list[str]):
    word_scores = {}
    if not sentence or len(sentence) == 0 or sentence == ' ':
        print("Error! Input sentence is null or empty string")
    elif not word_list or len(word_list) == 0:
        print("Error! Input wordl ist is null or empty")
    else:
        # Initialize the model and tokenizer only once.
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

        # Extract the scores for each word in word_list by prepending a space and then checking its score.
        for word in word_list:
            # Consider the likelihood of the word being next after a space
            word_with_space = " " + word
            word_id = tokenizer.encode(word_with_space, add_special_tokens=False)[0]
            word_scores[word] = probabilities[0][word_id].item()

        # Consider the likelihood of a space being the next character
        space_id = tokenizer.encode(" ", add_special_tokens=False)[0]
        word_scores[" "] = probabilities[0][space_id].item()

    return word_scores
