import openai
import mysecrets as secrets
import pickle 
import tiktoken
from scipy import spatial
openai.api_key = secrets.gpt_api_key

EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_COMPLETION_MODEL = "gpt-3.5-turbo" 

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

def num_tokens(text: str, model: str = CHAT_COMPLETION_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def query_message(
    query: str,
    zipper,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings = [z[1] for z in zipper]
    introduction = 'Use the below paragraphs about Nikhilesh Down Under Pizzerria to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer."'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'New section:\n"""\n{string}\n"""'
        if (
            num_tokens(message + next_article + question, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
    return message + question

def ask(
    query: str,
    zipper,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, zipper, model=CHAT_COMPLETION_MODEL, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "You answer questions about Nikhilesh's Down Under Pizzeria"},
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        model=CHAT_COMPLETION_MODEL,
        messages=messages,
        temperature=0
    )
    response_message = response["choices"][0]["message"]["content"]
    return response_message

if __name__ == "__main__":
    data_table = get_embeddings()
    question = input("Please input your query about Nikhilesh's restaruant? ")
    zipped_embeddings = strings_ranked_by_relatedness(question, data_table)
    response_message = ask(query=question,zipper=zipped_embeddings)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("The response provided is :", response_message)