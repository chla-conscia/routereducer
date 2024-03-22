import csv
from datetime import datetime
import subprocess
import pandas as pd
from ipaddress import ip_network
#chla2

def sort_subnets(subnets):
    return sorted(subnets, key=lambda subnet: (ip_network(subnet).network_address, ip_network(subnet).prefixlen))

# Load the subnets from 'subnets.txt'
with open('subnets.txt') as file:
    subnets = [line.strip() for line in file if line.strip()]

# Sort the subnets
sorted_subnets = sort_subnets(subnets)

# Prepare the input for aggregate6, which should be a string of subnets separated by newlines
subnets_str = "\n".join(sorted_subnets)

# Run aggregate6 and capture the output
result = subprocess.run(['aggregate6', '-4'], input=subnets_str, text=True, capture_output=True)
summarized_subnets_str = result.stdout.strip()

# Split the summarized subnets into a list
summarized_subnets = summarized_subnets_str.split('\n')

# Convert subnets to ip_network objects for comparison.
original_networks = [ip_network(subnet) for subnet in sorted_subnets]

# Get the current date and time for the filename
current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_file_path = f'summarization_report_{current_datetime}.csv'

# Write the data to a CSV file using semicolon as the delimiter
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(["Summarized Subnet", "Original Subnets", "Comments"])  # Writing the header row
    
    for summarized_subnet in summarized_subnets:
        # Find which original subnets are within the summarized subnet range
        summarized_network = ip_network(summarized_subnet)
        contributing_subnets = [str(net) for net in original_networks if net.subnet_of(summarized_network)]

        # Determine the comment based on the number of contributing subnets
        if len(contributing_subnets) == 1 and contributing_subnets[0] == summarized_subnet:
            comments = "Single Subnet"
        else:
            comments = "Summarization Possible"
        
        # Write the summarized subnet and contributing original subnets to the CSV
        writer.writerow([summarized_subnet, "\n".join(contributing_subnets), comments])

print(f"Report generated: {csv_file_path}")

# Create xlsx table report

# Load the newly created CSV data
df = pd.read_csv(csv_file_path, delimiter=';', quotechar='"')

# Convert CSV to Excel file with a table format
xlsx_file_path = csv_file_path.replace('.csv', '.xlsx')
with pd.ExcelWriter(xlsx_file_path, engine='xlsxwriter') as writer:
    # Load the CSV data into a DataFrame
    df = pd.read_csv(csv_file_path, delimiter=';')
    
    # Clean up the Original Subnets column by removing trailing semicolons
    df['Original Subnets'] = df['Original Subnets'].str.rstrip(';')
    
    # Convert the cleaned DataFrame to an Excel file
    df.to_excel(writer, index=False, sheet_name='Report', header=False, startrow=1)
    
    workbook = writer.book
    worksheet = writer.sheets['Report']

    # Format settings for text wrap and font settings
    combined_format = workbook.add_format({
        'text_wrap': True, 
        'font_name': 'IBM Plex Mono', 
        'font_size': 11, 
        'valign': 'top'
    })

    
    # Add a format. Light red fill with dark red text.
    format1 = workbook.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006"})

    # Add a format. Green fill with dark green text.
    format2 = workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100"})

    # Add a format. Yellow fill with dark yellow text.
    format3 = workbook.add_format({'bg_color':   '#FFEB9C','font_color': '#9C6500'})

    # Apply the combined format to all data columns
    worksheet.set_column('A:A', 22.5, combined_format)
    worksheet.set_column('B:B', 22.5, combined_format)
    worksheet.set_column('C:C', 32, combined_format)

    # Apply conditional formatting to column C
    worksheet.conditional_format('C1:C1048576', {
    'type': 'text', 
    'criteria': 'containing', 
    'value': 'Summarization Possible', 
    'format': format2
    })

    # Manually writing headers with formatting
    header_format = workbook.add_format({
        'bold': True,
        'font_name': 'IBM Plex Mono', 
        'font_size': 12
    })

    for col_num, column_title in enumerate(df.columns):
        worksheet.write(0, col_num, column_title, header_format)

    # Add a table to the worksheet
    (max_row, max_col) = df.shape
    column_settings = [{'header': column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {
        'columns': column_settings,
        'style': 'Table Style Medium 16'
    })
    