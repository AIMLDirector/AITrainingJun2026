
from langchain_docling.loader import DoclingLoader

urls = [
    "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
    "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
    "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html",
]

loader = DoclingLoader(file_path=urls)

# Load all documents
documents = loader.load()

# For large datasets, lazily load documents
for document in loader.lazy_load():
    print(document)