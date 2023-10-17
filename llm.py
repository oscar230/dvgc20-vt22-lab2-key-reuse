from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
model = GPT2LMHeadModel.from_pretrained("gpt2-medium")
model.eval()
model.to('cuda')

def score_sentences(sentences: list[str]) -> list:
    return [score_sentence(s) for s in sentences]

def score_sentence(sentence: str) -> float:
    input_ids = tokenizer.encode(sentence, return_tensors="pt")
    with torch.no_grad():
        output = model(input_ids, labels=input_ids)
    loss = output.loss
    loss_score = -loss.item() # smaller loss i better
    return -loss_score # return inverted