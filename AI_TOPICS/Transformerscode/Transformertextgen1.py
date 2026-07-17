from transformers import pipeline
from accelerate import Accelerator

device = Accelerator().device   # CPU or GPU / load the model on the appropriate device/run the code 

pipeline = pipeline(task="text-generation", model="google/gemma-2-2b", device=device)
pipeline(["the secret to baking a really good cake is ", "a baguette is "])