import pandas as pd


'''
Write CSV file from a list of dictionaries.
'''
def write_csv(file_path, data, fieldnames):
    df = pd.DataFrame(data, columns=fieldnames)

    df.to_csv(file_path, index=False, encoding='utf-8')



'''
    Read CSV file and return a list of dictionaries.
'''
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')

        return df.to_dict(orient='records')
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []





