e#To demine the api key create client structure as follows:
# client = OpenAI(
#      api_key=....
#)
#It takes output from zorro_reportlog.py

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
                 "content": """Callers are calling into a phone system for utility company, and what they are saying is reflected in the input.
You goal is to extract the intent tag (only the tag) using your natural language understanding capabilities.
The tags are defined below and for each provided phrase you need to respond with the tag only.
get_transfer_service - caller wants to transfer service including explicit message such as transfer service or I want to transfer service. It also can be requests to transfer service to a new address because customer is moving, etc.
get_no - caller responds as "no" or related response to questions that could be negation or negative. Example is "No", "No I don't want it"
get_yes - caller response as "yes" or related response to questions that could be positive. So "Yes" or related such as "Yes please", etc.
get_greeting - greeting of the caller as hello or related.
payment_arrangements - caller is attempting to request for payment arrangement, has a difficultly paying the bill and need help. Any reference of an arrangement such as "arrangement"
get_agent - caller would like to speak to a person, representative, human, operator, customer service etc.
stop_service - caller would like to stop, cancel the service. For example "I would like to stop my service", "stop service", "disconnect service"
get_repeat - caller would like to repeat what they've heard
new_service - caller would like to setup a new service
get_something_else - caller would like to do something else as a response to some question
get_business - caller is requesting to talk about business account or business property that has an account
get_billing_question - caller has questions about the bill, billing, etc. 
pay_bill - caller would like to pay the bill
get_goback - caller would like to go back in the menu
use_credit_card - caller would like to pay with the credit card
get_ways_to_pay - caller would like to understand how they can pay the bill
get_power_outage - caller would like to report an outage
get_gas_emergency - caller has a gas related emergency 
get_channel_sms - caller would like to get notified via sms
get_rent - caller is calling about the account for a rental therefore may have corresponding questions
get_electric_emergency - caller reporting electrical emergency such as hanging wires or related
get_residence_type - caller is referring to a type of residence they have 
get_own - caller indicates that they own the property where the account is
restart_service - caller would like to restart the service
Not Recognized - use if you can not match any of the provided intents."""},
                {"role": "user",
                 "content": f"What is the intent tag for this phrase: '{phrase}'?"}
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
input_file = "filtered_output.csv"  # Replace with your file path
output_file = "output_en.csv"  # Replace with desired output file path

# Read the input file in chunks to handle large files efficiently
df_chunks = pd.read_csv(input_file, sep='|', header=None, chunksize=1)

# Open the output file in write mode
with open(output_file, "w") as out_file:
    for chunk in df_chunks:
        # Process each row in the chunk
        row = chunk.iloc[0]
        phrase = row[4]  # Assuming the phrase is in column index 4

        # Extract the intent
        intent = extract_intent(phrase)

        # Compare the intent with the original last column
        comparison = int(row.iloc[-2] == intent)  # Convert to 1 (True) or 0 (False)

        # Append the new data to the output file
        out_row = list(row) + [intent, comparison]

        print(f"outraw: {out_row}")
        out_file.write('|'.join(map(str, out_row)) + '\n')

print(f"Updated file saved as {output_file}")
