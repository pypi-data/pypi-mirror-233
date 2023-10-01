import pandas as pd

def read_matrix(threshold, path_matrix):
    matrix = pd.read_excel(path_matrix, index_col = 0)
    # Create the dictionary with column names and the corresponding row indexes
    result = {}
    for col in matrix.columns:
        # Get the row indexes where the value is greater than threshold
        indexes = matrix[matrix[col] > threshold].index.tolist()
        if indexes:  # Only add to the dictionary if there's at least one index
            result[col] = indexes
    return result