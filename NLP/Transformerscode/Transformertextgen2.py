from transformers import pipeline
from accelerate import Accelerator
from transformers.pipelines.pt_utils import KeyDataset
import datasets

device = Accelerator().device

# KeyDataset is a utility that returns the item in the dict returned by the dataset
dataset = datasets.load_dataset("stanfordnlp/imdb", name="plain_text", split="unsupervised")
print(dataset[0:5])
# pipeline = pipeline(task="text-classification", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", device=device)
# for out in pipeline(KeyDataset(dataset, "text"), batch_size=8, truncation="only_first"):
#     print(out)



pipeline = pipeline(task ="audio-classification", model="", device=device)


# load the model into memory ( model - 10gb/  memory   20 GB)