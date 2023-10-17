from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")

def score_sentences(sentences: list[str]) -> list:
    scores = []
    for sentence in sentences:
        input_ids = tokenizer.encode(sentence, return_tensors="pt")
        with torch.no_grad():
            output = model(input_ids, labels=input_ids)
        loss = output.loss
        scores.append(-loss.item())
    return scores
