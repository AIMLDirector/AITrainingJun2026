from langchain_community.document_loaders import WebBaseLoader

urls = [
    "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html",
    "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html",
    "https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html",
]

loader = WebBaseLoader(web_paths=urls)

docs = loader.load()

print(f"Loaded {len(docs)} pages")
print(docs[0].page_content[:500])