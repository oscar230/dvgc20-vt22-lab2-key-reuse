from transformers import GPT2LMHeadModel, GPT2Tokenizer

def complete(sentence: str, word_list: list[str]) -> str:
    max_length: int = len(sentence) + len(max(word_list, key=len)) + 1
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
    model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
    
    input_ids = tokenizer.encode(sentence, return_tensors='pt')

    # Generate predictions
    output = model.generate(input_ids, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)

    predicted_sentence = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Tokenize the predicted sentence and the original sentence
    predicted_tokens = tokenizer.tokenize(predicted_sentence)
    input_tokens = tokenizer.tokenize(sentence)
    
    # Identify the word immediately following the original sentence
    if len(predicted_tokens) > len(input_tokens):
        next_word = predicted_tokens[len(input_tokens)]
        # Check if the word is in the word_list
        if next_word not in word_list:
            # If not, choose the most probable word from the word_list
            next_word = word_list[0]  # This is a basic selection; in reality, you might want a more refined approach
    
        return sentence + " " + next_word
    else:
        # If the model did not generate any additional tokens, return the original sentence
        return sentence