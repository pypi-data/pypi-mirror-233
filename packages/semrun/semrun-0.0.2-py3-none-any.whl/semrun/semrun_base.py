from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import torch

class SemRun:
    def __init__(self, function_topic_dict, model_name='thenlper/gte-small'):
        self.functions = list(function_topic_dict.keys())
        self.topics = list(function_topic_dict.values())
        self.model = SentenceTransformer(model_name)
        self.topic_embeddings = self.model.encode(self.topics)
        
    def execute(self, user_input):
        user_embedding = self.model.encode([user_input])
        similarities = [cos_sim(topic_embedding, user_embedding) for topic_embedding in self.topic_embeddings]
        max_sim_index = torch.argmax(torch.Tensor(similarities))
        return self.functions[max_sim_index]()  # Notice the parentheses here

