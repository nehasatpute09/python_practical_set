import csv

def calculate_average(filename, column_name):
    # Initialize variables
    total = 0
    count = 0

    # Open the CSV file and read data
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Try to convert the value in the specified column to float
                value = float(row[column_name])
                total += value
                count += 1
            except ValueError:
                print(f"Invalid value in column '{column_name}' for row: {row}")

    # Calculate the average
    if count > 0:
        average = total / count
        return average
    else:
        return None

# Test the function
filename = 'data.csv'
column_name = 'Score'
average_score = calculate_average(filename, column_name)
if average_score is not None:
    print(f"The average score in column '{column_name}' is: {average_score}")
else:
    print(f"No valid values found in column '{column_name}'")
