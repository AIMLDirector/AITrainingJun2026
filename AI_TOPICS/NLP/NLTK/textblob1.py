from textblob import TextBlob
import openpyxl
import os

# Excel file name
file_name = "sentiment_results.xlsx"

# If file does not exist, create it with headers
if not os.path.exists(file_name):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(["User Input", "Polarity", "Sentiment"])
    workbook.save(file_name)

# Load the workbook
workbook = openpyxl.load_workbook(file_name)
sheet = workbook.active

# Get user input
user_text = input("Enter your text for sentiment analysis: ")
# # Save user input to a text file
# for i in open("user_text.txt", "a"):
#     x = i.readline().split("customer feedback: ")[-1]
#     textblob(x)
    

# Run sentiment analysis
blob = TextBlob(user_text)
print(blob)
polarity = blob.sentiment.polarity

# Decide sentiment label
if polarity > 0:
    sentiment = "Positive"
elif polarity < 0:
    sentiment = "Negative"
else:
    sentiment = "Neutral"

# Print results
print(f"Text: {user_text}")
print(f"Polarity: {polarity:.2f} → Sentiment: {sentiment}")

# Append results to Excel
sheet.append([user_text, polarity, sentiment])
workbook.save(file_name)

print(f"Result saved in {file_name}")
