e#To demine the api key create client structure as follows:
# client = OpenAI(
#      api_key=....
#)
#It takes intent file that is used by Zorro

import pandas as pd
from openai import OpenAI

index = 0

# Function to extract intent using OpenAI
def extract_intent(phrase):

   global index

   if not isinstance(phrase, str) or len(phrase) == 0 or phrase == "":
        return ""
   
   print("Inside extract with message: " + phrase)

   try:

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature = 0,
            #store=True,
            messages=[
                {"role": "system",
                 "content": """You will get English version of a phrase that a customer in US attempting to use in communication with a utliity company. Translate English version 
                 to Spanish but keeping it more realistic inline with how native Spanish speaker will communicate with the utility company delivering the same meaning 
                 as the phrase in English. Translate this phrase without providing any additional context. Only translation."""},
                {"role": "user",
                 "content": f"Translate this: '{phrase}'?"}
            ]
        )

        print("Got back: " + str(completion.choices[0].message.content))
        index += 1
        print("We are on: " + str(index))

        # Get usage information, including cached tokens
        usage_data = completion.usage

        if hasattr(usage_data, 'prompt_tokens_details') and hasattr(usage_data.prompt_tokens_details, 'cached_tokens'):
            cached_tokens = usage_data.prompt_tokens_details.cached_tokens
            print(f"Cached Tokens: {cached_tokens} / {usage_data.prompt_tokens}")
        else:
            print("Cached tokens data not available or caching not applied.")

        return completion.choices[0].message.content
   
   except Exception as e:
        print(f"Error processing phrase '{phrase}': {e}")
        return "Error"

# Input and output file paths
input_file = "swampfox_power_intents.csv"  # Replace with your file path
output_file = "output_translate.csv"  # Replace with desired output file path

# Read the input file in chunks to handle large files efficiently
df_chunks = pd.read_csv(input_file, sep=',', header=None, chunksize=1)

# Open the output file in write mode
with open(output_file, "w") as out_file:
    for chunk in df_chunks:
        # Process each row in the chunk
        row = chunk.iloc[0]
        phrase = row[0]  # Assuming the phrase is in column index 0
        intent = row[1]

        # Extract the intent
        translation = extract_intent(phrase)

        # Append the new data to the output file
        out_row =  [(f"\"{translation}\"")] + [(f"\"{intent}\"")]

        print(f"outraw: {out_row}")
        out_file.write(','.join(map(str, out_row)) + '\n') 

print(f"Updated file saved as {output_file}")
