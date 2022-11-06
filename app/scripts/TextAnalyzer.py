import torch
from transformers import AutoModel, AutoTokenizer


CHOSEN_MODEL = "sberbank-ai/sbert_large_nlu_ru"


class BertBasedTokenizer:
    def __init__(self, ):
        self.tokenizer = AutoTokenizer.from_pretrained(CHOSEN_MODEL)

    def get_tokens(self, data):
        tokenized = self.tokenizer(list(data), padding=True, truncation=True, max_length=24, return_tensors='pt')
        return tokenized


class BertBasedAnalyzer:
    def __init__(self, ):
        self.model_RuBERT = AutoModel.from_pretrained(CHOSEN_MODEL)

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def get_sentence_embeddings(self, tokenized):
        with torch.no_grad():
            model_output = self.model_RuBERT(**tokenized)
        return self.mean_pooling(model_output, tokenized['attention_mask'])
