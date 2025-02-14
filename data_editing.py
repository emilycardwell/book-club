import pandas as pd


# READ CSV FOR BOOK OPTIONS
def read_data(file_path):
    with open(file_path, 'r') as file_path:
        books_df = pd.read_csv(file_path)

    sorted_df = books_df.sort_values('Book').reset_index(drop=True)
    thin_df = sorted_df.loc[:, ['Book', 'Author']]

    items = []
    for key, data in thin_df.iterrows():
        items.append(f'{data[0]} - {data[1].split()[-1]}')

    return items
