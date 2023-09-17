import pandas as pd
from scipy import spatial
import openai
import os 
import audio_app.secrets as secrets

openai.api_key = os.getenv(secrets.gpt_api_key)

class AnsweringAgent():
    def __init__(self):
        self.df = pd.read_csv('embedding_df.csv')
        self.model = "gpt-3.5-turbo"
    
    def ranked_by_relatedness(self, query: str, relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y), top_n: int = 3) -> tuple[list[str], list[float]]:
        query_embedding_response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=query,
        )
        query_embedding = query_embedding_response["data"][0]["embedding"]
        fname_text_similarity = [(row["filename"], row["text"], relatedness_fn(query_embedding, row["embedding"]))
                                for i, row in self.df.iterrows()]
        fname_text_similarity.sort(reverse=True, key = lambda x:x[2])
        
        top_n_results = fname_text_similarity[:top_n]
        filenames_top_n, texts_top_n, similarity_top_n = zip(*top_n_results)
        return filenames_top_n, texts_top_n, similarity_top_n

    def augment_query(self, query):
        top_filenames, top_texts, top_similarity = self.ranked_by_relatedness(query=query)
        print("top filenames:")
        print(top_filenames)

        introduction = 'Use the following information to answer the above question \n'
        + top_texts[0]

        final_query = query+'\n\n'+introduction

        return final_query
    
    def ask(self, query: str, print_message: bool = True) -> str:
        message = self.augment_query(query=query)
        if print_message:
            print(message)
        messages = [
            {"role": "system", "content": "You answer questions about a restaurant called Nikhilesh's pizzeria in Sydney, Australia"},
            {"role": "user", "content": message},
        ]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0
        )
        response_message = response["choices"][0]["message"]["content"]
        return response_message

if __name__ == "__main__":
    agent = AnsweringAgent()
    query = 'Hey. I have a query about a mozzarella pizza. How much would a mozzerela pizza cost?'
    response = agent.ask(query=query)
    print("Agent response:")
    print(response)