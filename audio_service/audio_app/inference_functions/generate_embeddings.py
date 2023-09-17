import openai
import os 
from .. import secrets
import pandas as pd

openai.api_key = os.getenv(secrets.gpt_api_key)

def get_embeddings(array_of_texts):
    model = "text-embedding-ada-002"    
    response = openai.Embedding.create(
        model = model,
        input = array_of_texts
    )
    data_array = response["data"]
    embedding_arr = [data_obj["embedding"] for data_obj in data_array]
    return embedding_arr


def get_texts_from_directory(directory_path):
    texts = []
    filenames = []
    # Iterate over each file in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is a .txt file
        if filename.endswith('.txt'):
            filenames.append(filename)
            with open(os.path.join(directory_path, filename), 'r') as file:
                # Read the content of the file and append to the texts array
                texts.append(file.read())

    return texts, filenames


def generate_dataframe(text_descriptions, embeddings, filenames):
    df = pd.DataFrame({'filename':filenames, 'text':text_descriptions,'embedding':embeddings})
    return df 

def write_dataframe(dataframe, filename):
    dataframe.to_csv(filename, index=True)

if __name__ == "__main__":
    dir_path  = '/dummy_text'
    text_arr, filenames = get_texts_from_directory(directory_path=dir_path)
    embedding_arr = get_embeddings(text_arr)
    generate_dataframe(text_descriptions=text_arr,embeddings=embedding_arr, filenames=filenames)
    write_dataframe(filename='embedding_df.csv')