import pandas as pd
from sklearn.preprocessing import MinMaxScaler

### Load the raw data
def load_data(file_path):
    return pd.read_csv(file_path)

raw_file_path = "data/raw/automobileEDA_dirty_training.csv"    
dirty_df = load_data(raw_file_path)

def get_shape(df):
    return df.shape

(total_rows, total_columns) = get_shape(dirty_df)

def check_head(n):
    return dirty_df.head(n)

check_head(5)

### Clean
def null_value_check(df):
    null_counts = df.isnull().sum()
    dirty_df_nulls = null_counts.reset_index()
    dirty_df_nulls.columns = ['column_name', 'null_count']
    dirty_df_nulls = dirty_df_nulls[dirty_df_nulls['null_count'] > 0]

    dirty_df_nulls['data_type'] = dirty_df_nulls['column_name'].apply(lambda x: df[x].dtype)

    return dirty_df_nulls

null_value_check(dirty_df)

dirty_df = dirty_df.dropna()
null_value_check(dirty_df)

def duplicate_value_check(df):
    return df.duplicated().sum() / len(df)

duplicate_value_check(dirty_df)

dirty_df = dirty_df.drop_duplicates()
duplicate_value_check(dirty_df)

# Normalizing height column to meters
dirty_df['height'] = dirty_df['height'] / 100
dirty_df['height'].describe()

dirty_df['transaction_date'] = pd.to_datetime(dirty_df['transaction_date'], format='mixed')
dirty_df['transaction_date'].describe()

string_cols = dirty_df.select_dtypes(include='object').columns

def normalize_string_columns(df, string_cols):    
    for col in string_cols:
        df[col] = df[col].str.lower().str.strip()

normalize_string_columns(dirty_df, string_cols)

categories = {}

for col in string_cols:
    categories_list = pd.Categorical(dirty_df[col]).categories.tolist()
    if len(categories_list) > 10: continue
    categories[col] = categories_list

dirty_df['num-of-doors'] = dirty_df['num-of-doors'].map({'two': 0, 'four': 1})
dirty_df['num-of-doors'].describe()

dirty_df['num-of-cylinders'] = dirty_df['num-of-cylinders'].map({'four': 4, 'six': 6, 'five': 5, 'eight': 8, 'two': 2, 'three': 3, 'twelve': 12})
dirty_df['num-of-cylinders'].describe()

dirty_df['engine-location'] = dirty_df['engine-location'].map({'front': 0, 'rear': 1})
check_head(5)

dirty_df['horsepower_ordinal'] = dirty_df['horsepower-binned'].map({'low': 0, 'medium': 1, 'high': 2})
dirty_df.drop(columns=['horsepower-binned'], inplace=True)
dirty_df['horsepower_ordinal'].describe()

def encode_categorical_column(df, column):
    df = pd.get_dummies(df, columns=[column], dtype=int, prefix=column)
    return df

cols = ['body-style', 'drive-wheels', 'aspiration', 'engine-type', 'fuel-system']
for col in cols:
    dirty_df = encode_categorical_column(dirty_df, col)
    check_head(5)

def transform_features(df, columns):
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

dirty_df = transform_features(
    dirty_df, [
        'symboling', 
        'wheel-base', 
        'length', 
        'width', 
        'curb-weight', 
        'num-of-cylinders',
        'engine-size',
        'horsepower',
        'peak-rpm',
        'city-mpg',
        'highway-mpg',
        'price'
    ]
)

check_head(5)

dirty_df['make_frequency'] = dirty_df['make'].map(dirty_df['make'].value_counts(normalize=True))
dirty_df.drop(columns=['make'], inplace=True)
check_head(5)


def export(df, file_path):
    df.to_csv(file_path, index=False)

export(dirty_df, 'data/processed/automobile_cleaned_data.csv')