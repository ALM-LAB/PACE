import cohere
from sentence_transformers import SentenceTransformer, util
import numpy as np

cohere_api_key = 'c8ES1KWN9nd8uObqxiBvBWEQ450asuAkoF61EYCg'
co = cohere.Client(cohere_api_key)

texts = [
    "Political elections in USA",
    "New Icelandic study shows COVID reinfection rate rises with number of vaccine doses. Joe Biden just got off his second round of COVID and quadruple vaccinated. U.S. Defense Secretary Lloyd Austin is infected with COVID for the second time this year.",
    "Republican voters headed to the polls for primary elections in Alaska and Wyoming. Alaska had senator Lisa Murkowski facing opposition from Donald Trump's endorsed Kelly Tischbacha. Rep. Liz Cheney she's going against Trump endorsed Harriet Hagman check your states for results today.",
    "A California church that was fined over $200,000 for defined COVID-19 restrictions has had its fines dropped after a nearly two year battle. California Court of Appeals reversed the injunction, contempt orders and fines on Monday. Be praying there's more going on in that case.",
    "President Biden signed the Inflation Reduction Act into law on Tuesday. Said with this law, the American people won and special interests lost. At the same time slams GOP for voting against the tax and climate deal. Judge declines to block Georgia's fetal fetal heartbeat law.",
]

response = co.embed(
  texts=texts,
  model="small",
)
embeddings = response.embeddings
print (len(embeddings[0]))
# convert list to numpy array
embeddings = np.array(embeddings)
print (type(embeddings[0]))
query = embeddings[0]

for i, embedding in enumerate(embeddings):
    print(f"Similarity between query and text {i}: {util.cos_sim(query, embedding)}")
    print ()
