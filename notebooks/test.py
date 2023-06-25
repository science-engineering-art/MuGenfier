import pandas as pd

record = {
    'Name': ['Ankit', 'Swapnil', 'Aishwarya', 'Priyanka', 'Shivangi', 'Shaurya'],
    'Age': [22, 20, 21, 19, 18, 22],
    'Stream': ['Math', 'Commerce', 'Science', 'Math', 'Math', 'Science'],
    'Percentage': [90, 90, 96, 75, 70, 80]
}

dataframe = pd.DataFrame(record, columns=['Name', 'Age', 'Stream', 'Percentage'])
print("Given DataFrame:\n", dataframe)

filtered_dataframe = dataframe[dataframe['Stream'].apply(lambda v: v == 'Math')]
print("Filtered DataFrame:\n", filtered_dataframe)
