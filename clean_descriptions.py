from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch.nn.functional as F
import torch
import spacy

# Load model, tokenizer and spacy nlp: to be initialized in the main script
# model = AutoModelForSequenceClassification.from_pretrained('morenolq/spotify-podcast-advertising-classification')
# tokenizer = AutoTokenizer.from_pretrained('morenolq/spotify-podcast-advertising-classification')
# nlp = spacy.load("en_core_web_sm")

#sentence = "On their first episode, Kate and Doree talk about some of their personal rituals, including vision boards and makeup routines. Plus, they discuss peeing on planes, sleeping away from your phone, and their favorite mascaras! To learn more about Forever35 and get a list of the products mentioned on the show, visit www.forever35podcast.com. And you can email Kate and Doree at forever35podcast@gmail.com, and follow them on Instagram at @forever35podcast.Special thanks to launch sponsor Tripping.com! Visit tripping.com/forever35 to find your perfect vacation rental.Theme music by Riot. Hosted on Acast. See acast.com/privacy for more information."

def description_cleaner(model, tokenizer, nlp, sentence):
    desc_sentences = nlp(sentence)
    desc_sentences = [str(s) for s in desc_sentences.sents]

    new_desc = []
    for i, s in enumerate(desc_sentences): 
        if i==0:
            context = "__START__"
        else:
            context = desc_sentences[i-1] 
        out = tokenizer(context, s, padding = "max_length",
                            max_length = 256,
                            truncation=True,
                            return_attention_mask=True,
                            return_tensors = 'pt')
        outputs = model(**out)
        outputs = F.softmax(outputs.logits, dim=1)
        predicted_label = torch.argmax(outputs, dim=1)

        if predicted_label == 0:
            new_desc.append(s)

    new_desc = " ".join(new_desc)
    return new_desc

# new_desc = description_cleaner(model, tokenizer, nlp, sentence)
# print(new_desc)
