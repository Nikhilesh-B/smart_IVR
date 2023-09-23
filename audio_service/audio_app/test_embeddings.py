import openai
import os 
import mysecrets as secrets
import pickle 
import pprint 
from scipy import spatial
openai.api_key = secrets.gpt_api_key

EMBEDDING_MODEL = "text-embedding-ada-002" 

def get_embeddings() -> list[dict()]:
    with open('/Users/nikhileshbelulkar/Documents/smart_IVR/audio_service/audio_app/embeddings.pkl', 'rb') as f:
        data_table = pickle.load(f)
    return data_table

def strings_ranked_by_relatedness(
    query: str,
    table: list(dict()),
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
) -> list[tuple[str, str, float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]

    zipper = [(dictionary['filename'], dictionary['text_description'], relatedness_fn(dictionary['embedding'],query_embedding)) 
               for dictionary in table]
    zipper.sort(key=lambda x: x[2], reverse=True)
    return zipper

if __name__ == "__main__":
    data_table = get_embeddings()
    question = input("Please input your query about Nikhilesh's restaruant? ")
    zipped_embeddings = strings_ranked_by_relatedness(question, data_table)
    for tup in zipped_embeddings[0:10]:
        print(tup[0])
    







