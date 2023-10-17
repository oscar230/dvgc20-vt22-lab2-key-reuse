import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load pre-trained model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model.eval()

def could_be_valid_substring(substring):
    # Convert input string to token ids
    input_ids = tokenizer.encode(substring, return_tensors="pt")

    # Generate a continuation
    with torch.no_grad():
        output = model.generate(input_ids, max_length=50, num_return_sequences=1)

    # Decode the output ids to strings
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # If the generated text is much longer than the input, it means the model was able to generate a continuation
    if len(generated_text) > len(substring) + 5:  # added a threshold of 5 chars to avoid minor extensions
        return True
    else:
        return False

# Testing the function
test_strings = ["Hxyli", "ex"]
results = {s: could_be_valid_substring(s) for s in test_strings}
print(results)
