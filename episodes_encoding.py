from sentence_transformers import SentenceTransformer, util

def episodes_encoding(list_text):
    model_name = "all-mpnet-base-v2" # "multi-qa-MiniLM-L6-cos-v1" (smaller and faster, but less accurate)
    model = SentenceTransformer(model_name)
    sentence_encodings = model.encode(list_text)
    return sentence_encodings


text_1 = "How big is London"
text_2 = "London has 9,787,426 inhabitants at the 2011 census"
text_3 = "London is known for its finacial district"
list_text = [text_1, text_2, text_3]

sentence_encodings = episodes_encoding(list_text)

print("Similarity:", util.dot_score(sentence_encodings[0], sentence_encodings[1]))
print("Similarity:", util.dot_score(sentence_encodings[0], sentence_encodings[2]))