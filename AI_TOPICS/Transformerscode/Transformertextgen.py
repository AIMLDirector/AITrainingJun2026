# from transformers import pipeline

# pipeline = pipeline(task="text-generation", model="google/gemma-3-270m", max_new_tokens=50)
# pipeline("the secret to baking a really good cake is ")


from transformers import pipeline

generator = pipeline(
    task="text-generation", 
    model="google/gemma-3-270m",
    clean_up_tokenization_spaces=False
)

output = generator(
    "the secret to baking a really good cake is ", 
    max_new_tokens=50,
    do_sample=True,
    temperature=0.7
)

print(output)