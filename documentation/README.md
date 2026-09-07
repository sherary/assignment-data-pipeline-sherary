# Auto Mobile Data Processing 'Pipeline'

Input: 205 rows, 30 columns.
Output: 186 rows, 48 columns.

### Requirements: 
1. Python3 Version 3.14.7

## Running the pipeline
Requirements: `pandas`, `scikit-learn`.

```bash
pip3 install pandas scikit-learn
python3 src/pipeline.py
```

### Data Source:
| File | Rows | Columns 
| --- | --- | --- |
| `data/raw/automobileEDA_dirty_training.csv` | 205 | 30 | Raw Data 
| `data/processed/automobile_cleaned_data.csv` | 186 | 49 | Processed Data

### Folder Structure
root/
    data/
        |____ processed/
            |____ automovile_cleaned_data.csv
        |____ raw/
            |____ automobileEDA_dirty_training.csv
        documentation/
        |____ README.md (you are here)
        src/
        |____ eda.ipynb
        |____ pipeline.py
    .gitignore
    requirement.txt

### Dataset Preprocessed Condition
- Total Rows:       206
- Total Columns:    30

### Dataset Processed Condition
- Total Rows:       186
- Total Columns:    49

### Problems
1. Format inconsistencies in 'transaction_date' column and data type was in string.
2. Metrics measurement on column 'height' that does not match the 'width', and 'length'
3. Inconsistencies in capitalization on 'make' column: `BMW`, `Audi`, `ALFA-ROMERO`
4. Incorrect data type used for 'num-of-doors' and 'num-of-cylinders'
5. Whitespaces on some values: `'dodge  '`, `'porsche  '`, `'mercury  '`
6. Null values on crusial columns
    | Column | Nulls |
    | --- | --- |
    | `stroke` | 4 |
    | `horsepower` | 3 |
    | `price` | 3 |
    | `transaction_date` | 2 |
    | `make` | 2 |
    | `num-of-doors` | 2 |
    | `horsepower-binned` | 1 |

### Solutions:
1. Value for `transaction_date` parsed into date data type using strategy 'mixed', 
since the string format itself is not standardized.
2. I opt the value to be parsed following the `width` and `length`, but opt out,
because the reference is not requiring it. But if I may, I might do so to keep the 
data cleaner.
3. All lettering and wording are lowered to match the most commonly used terms.
4. Changed data type of `num-of-doors` and `num-of-cylinders` to int. 
5. Removing white spaces on some columns with string data type as a value.
6. Removing nulls on mentioned columns to make the data quantifiable in the future.
7. Data scaling and frequency encoding on columns (mentioned below) are needed 
to normalize the data to make it ingestable and less skew-prone in the process.

### Ordinal Encoding
Four columns are mapped to numbers by hand:

| Column | Mapping |
| --- | --- |
| `num-of-doors` | `two` to 0, `four` to 1 |
| `num-of-cylinders` | word to integer, 2 through 12 |
| `engine-location` | `front` to 0, `rear` to 1 |
| `horsepower-binned` | `low`, `medium`, `high` to 0, 1, 2 |

### One Hot encoding

Five columns are expanded into 23 indicator columns with `dtype=int`:

`body-style`, `drive-wheels`, `aspiration`, `engine-type`, `fuel-system`

### Min Max Scaling
Twelve numeric columns are scaled to the range 0 to 1:
`symboling`, `wheel-base`, `length`, `width`, `curb-weight`,
`num-of-cylinders`, `engine-size`, `horsepower`, `peak-rpm`,
`city-mpg`, `highway-mpg`, `price`

### Frequency Encoding

`make` is replaced by `make_frequency`, computed as the count of each make
divided by 186 rows. The original `make` column is dropped.

### Known Issues
#### Duplicate rows
There are 3 rows that detected as duplicate by pandas. In real world scenario, 
duplicates could be detected by serial number or ID. This dataframe does not
include both serial number or ID. Hence, it is kind of impossible to tell which one 
is a duplicate. So, dropping duplicate rows are a choice that should be 
predetermined.

#### Date column
As previously mentioned, the scaling for each column is purposedly to make the data 
to be easily ingestable. Though, I'm hesitating on date. Transaction date is a 
valuable data. Therefore, it would make more sense if it is transformed to UNIX.

#### Null rows
Null rows makes 8% of the total rows. However, it is hard to fill either the empty 
and null data with placeholder value. Both hesitated to add because of the importance
of the data and also domain knowledge limit on my part. 