"""
First process the log using the following command and then use this filter to clean it up.

grep Reportlog *.log* | awk -F'[ ,=]' '{
    # Remove filename prefix before processing
    split($0, parts, ":");
    log_content = substr($0, index($0, parts[2])); # Get everything after the first colon

    # Extract date and time from log_content
    split(log_content, date_time, "|");
    full_date_time = date_time[1]; # Full date and time (e.g., 2024-12-17 20:41:42)

    # Split full_date_time into date and time
    split(full_date_time, dt, " ");
    full_date = dt[1]; # Date (e.g., 2024-12-17)
    full_time = dt[2]; # Time (e.g., 20:41:42)

    # Extract process_id explicitly as the number
    for (i=1; i<=NF; i++) {
        if ($i == "process_id") {
            process_id = $(i+1);
        }
    }

    message_index = index($0, "message="); # Locate "message="
    message = substr($0, message_index + 8); # Extract message content
    split(message, fields, "|");           # Split the message content on "|"

    # Print the results in pipe-separated format
    printf "%s|%s|%s", full_date, full_time, process_id;  # Date, Time, Process ID
    for (i=2; i<=length(fields); i++) {                  # Skip "Reportlog"
        printf "|%s", fields[i];
    }
    printf "\n";
}'
"""

import os
import csv
import re
from datetime import datetime

def process_csv_files(input_directory, output_file, filter_date, exclude_words):
    """
    Processes CSV files in the specified directory and creates a combined output CSV file.
    
    :param input_directory: Directory containing the CSV files.
    :param output_file: Path to the final output CSV file.
    :param filter_date: A date string (e.g., '2024-12-15'). Rows with dates earlier than this will be excluded.
    :param exclude_words: Comma-separated string of words to exclude rows based on the 5th column.
    """
    filter_date = datetime.strptime(filter_date, "%Y-%m-%d")
    exclude_words = set(exclude_words.split(","))
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = None  # Writer object for the output file
        
        for filename in os.listdir(input_directory):

            if filename.endswith(".csv"):
                print("Working on: ", filename)

                filepath = os.path.join(input_directory, filename)
                
                with open(filepath, 'r', encoding='utf-8') as infile:
                    reader = csv.reader(infile, delimiter='|')
                    
                    for row in reader:
                        # Filter rows based on the date in the first column
                        row_date = datetime.strptime(row[0], "%Y-%m-%d")
                        if row_date >= filter_date:
                            # Remove rows with "entity" in the 4th column
                            if row[3].lower() == "entity":
                                continue
                            # Exclude default_fallback
                            if row[5].lower() == "default_fallback":
                                continue                            

                            # Skip rows where the 5th column contains numbers or excluded words
                            if re.search(r'\d', row[4]) or any(word in row[4] for word in exclude_words):
                                continue
                            
                            # Write the header row if writer is None
                            if writer is None:
                                writer = csv.writer(outfile, delimiter='|')
                                writer.writerow(["Date", "Time", "ID", "Type", "Content", "Tag", "Confidence"])
                            
                            writer.writerow(row)

    print(f"Processing complete. Filtered data saved to {output_file}.")

# Example usage
input_directory = "."  # Replace with the path to your directory
output_file = "filtered_output.csv"  # Replace with the desired output file name
filter_date = "2024-12-30"  # Replace with the cutoff date for filtering
exclude_words = "zero,one,two,three,four,five,six,seven,eight,nine,ten,0,1,2,3,4,5,6,7,8,9"  # Replace with your comma-separated words to exclude

process_csv_files(input_directory, output_file, filter_date, exclude_words)
