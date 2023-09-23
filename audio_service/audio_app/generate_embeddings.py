import openai
import os 
import mysecrets as secrets
import pickle 
import pprint 

openai.api_key = secrets.gpt_api_key

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


def generate_pickledump(filenames, text_descriptions, embeddings):
    zipper = list(zip(filenames, text_descriptions, embeddings))
    pickle_dictionary = [{'filename':fname,'text_description':txt,'embedding':embed} 
                         for fname, txt, embed in zipper]
    
    with open('embeddings.pkl', 'wb') as f:
        pickle.dump(pickle_dictionary, f)

if __name__ == "__main__":
    dir_path  = './dummy_text'
    text_arr, filenames = get_texts_from_directory(directory_path=dir_path)
    embedding_arr = get_embeddings(text_arr)
    generate_pickledump(text_descriptions=text_arr,embeddings=embedding_arr, filenames=filenames)
