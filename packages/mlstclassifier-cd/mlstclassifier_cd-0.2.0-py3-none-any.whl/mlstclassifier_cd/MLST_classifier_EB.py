#!/usr/bin/env python3

import pandas as pd
import sys
import joblib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import argparse
import re


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print("Error: Number of argument must be 4")
        print("Usage: MLSTclassifier_cd input_path output_path input_type")
        sys.exit(1)


    # Extract the command-line arguments
    parser = argparse.ArgumentParser(description='input, output and input type')
    parser.add_argument('input_file', type=str, action='store', help='intput should be a path to the input file')
    parser.add_argument('output_file', type=str, action='store', help='output should be a path to the output file')
    parser.add_argument('input_type', type=str, action='store', default='csv' , help='type "fastmlst" if the file is the output from fastmlst, "csv" is the file is a table and "pubmlst" if the file is a text file downloaded from pubmlst. Default is "csv".')
    args = parser.parse_args()


    def extract_number(v):    
        match = re.search(r'\(~?(\d+)\)', v)# Use regular expression to find the number within brackets and avoid ~ if present
        # If a match is found, return the extracted number as an integer
        if match:
            return int(match.group(1))
        else:
            return None
    

    def fastmlst_to_df(f):
        df = pd.read_csv(f, header=None)
        modified_columns = df.iloc[:, 3:10]# Select mlst columns (3rd to 10th column) from the DataFrame
        modified_columns = modified_columns.map(extract_number)# Apply the 'extract_number' function to each element in the selected columns
        df.rename(columns={3: 'adk',4: 'atpA',5: 'dxr',6: 'glyA',7: 'recA',8: 'sodA',9: 'tpi'}, inplace=True)# Modify the column names to be recognized for the prediction
        df.iloc[:, 3:10] = modified_columns
        return df
    

    try:
        if args.input_file.endswith('.txt'):  # Check if the file extension is '.txt'
            # If it's a '.txt' file, check the specified input type
            if args.input_type == "pubmlst":
                df = pd.read_table(args.input_file)  # Read the '.txt' file
            else:
                # Raise an error for an invalid input type when the file is a '.txt'
                raise ValueError('Error: Make sure the input type is "pubmlst" for a .txt file.')
        elif args.input_file.endswith('.csv'):  # Check if the file extension is '.csv'
            # If it's a '.csv' file, check the specified input type
            if args.input_type == "csv":
                df = pd.read_csv(args.input_file)  # Read the '.csv' file
            else:
                # Raise an error for an invalid input type when the file is a '.csv'
                raise ValueError('Error: Make sure the input type is "csv" for a .csv file.')
        elif args.input_type == "fastmlst":
            df = fastmlst_to_df(args.input_file)
        else:
        # Raise an error for an invalid file format
            raise ValueError("Error: Make sure the input file is in format .txt, .csv, or comes from fastMLST and that you write the argument correctly.")
    except FileNotFoundError:# Handle the case where the input file is not found
        print("Error: Input file not found.")
        sys.exit(1)
    except ValueError as ve:# Handle other value-related errors and print the error message
        print(ve)
        sys.exit(1)
    

    #Load the pre-trained model
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_directory, "KNN_model_080923.sav")
        model = joblib.load(model_path)
    except FileNotFoundError:
        print("Error: Model file not found.")
        sys.exit(1)


    # Extract features (X) from the DataFrame and make predictions
    df = df.dropna() # Drop missing values if some are present
    X = df[['adk', 'atpA', 'dxr', 'glyA', 'recA', 'sodA', 'tpi']]   # Extract columns corresponding to the 7 genes as features 'X'
    df['predicted_clade'] = model.predict(X)   # Make predictions using the pre-trained model and add them as a new column 'predicted_clade' in the DataFrame 'df'
    

    # Save the raw count in a separated file called count.csv:
    output_dir = os.path.dirname(args.output_file)
    count = df['predicted_clade'].value_counts() # Extract value count
    count_df = pd.DataFrame(count) # Create a df with value count
    with open(os.path.join(output_dir, "count.csv"), "w") as f: # Create the file count.csv with the value count df
        count_df.to_csv(f, index=True)
    

    # Create a pie chart with the value counts:
    fig = make_subplots(1, 1, specs=[[{"type": "pie"}]])
    fig.add_trace(
        go.Pie(
            labels=df['predicted_clade'].value_counts().index,
            values=df['predicted_clade'].value_counts().values,
            textinfo="label+percent",
            showlegend=False,
        ),
        row=1, col=1
    )

    fig.update_layout(title_text="Predicted Clade Distribution")
    # Save the pie chart as an HTML file:
    fig.write_html(os.path.join(output_dir, "pie_chart.html"))
    

    # Write the DataFrame with the added column of predictions to the output CSV file:
    try:
        with open(args.output_file, 'w') as f:   # Open the output CSV file
            df.to_csv(f, index=False)   # Write the DataFrame 'df' to the CSV file 'f', excluding the index column
    except PermissionError:
        print("Error: Unable to write to output CSV file.")
        sys.exit(1)


if __name__ == "__main__":
    main()   # Call the main function if the script is run as the main program (not imported as a module)


