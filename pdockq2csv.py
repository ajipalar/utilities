import re
import csv
import sys

def parse_output_to_csv(input_stream, output_csv):
    # Define regular expressions for parsing pDockQ and PPV lines
    pdockq_pattern = r'pDockQ = ([\d\.]+) for (.+\.pdb)'
    ppv_pattern = r'This corresponds to a PPV of at least ([\d\.]+)'

    # Initialize list to store parsed data
    parsed_data = []
    # Read the input stream line by line
    for line in input_stream:
        # Match pDockQ line
        pdockq_match = re.search(pdockq_pattern, line)
        if pdockq_match:
            pdockq = float(pdockq_match.group(1))
            pdbfile = pdockq_match.group(2)
            
            # Get the next line for PPV value
            ppv_line = next(input_stream, None)
            ppv_match = re.search(ppv_pattern, ppv_line) if ppv_line else None
            ppv = float(ppv_match.group(1)) if ppv_match else None
            
            # Append the parsed information
            if ppv is not None:
                parsed_data.append([pdbfile, pdockq, ppv])
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['pdbfile', 'pDockQ', 'PPV'])  # Header row
        csv_writer.writerows(parsed_data)

if __name__ == "__main__":
    # Example usage: python parse_script.py input.txt output.csv
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    with open(input_filename, 'r') as infile:
        parse_output_to_csv(infile, output_filename)
        print(f"Parsed data has been saved to {output_filename}")
