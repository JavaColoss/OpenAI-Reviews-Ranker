import openai
import csv
import os

# set up OpenAI API
openai.api_key = "Your OpenAI API key"


# define function to evaluate sentiment of a review text
def evaluate_sentiment(review_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please rate the following review on a scale of 1-10, with 10 being the most enthusiastic and 1 being the most negative:\n\n{review_text}\n\nRating:",
        temperature=0,
        max_tokens=1,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0
    )

    rating = int(response.choices[0].text.strip())

    return rating


# set up file paths
input_file_path = "D:\Download\Welltory Test_Python Developer_App Reviews - Data.csv"
output_file_path = os.path.splitext(input_file_path)[0] + "_analyzed.csv"

# read in input file
with open(input_file_path, newline='') as input_file:
    reader = csv.DictReader(input_file)
    rows = list(reader)

# evaluate sentiment of each review and add to rows
for row in rows:
    row["rate"] = evaluate_sentiment(row["review text"])

# sort rows by rating in descending order
rows.sort(key=lambda row: row["rate"], reverse=True)

# write rows to output file
with open(output_file_path, 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Done!")
