import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder


input_path = (
    r"C:\Users\acer\Documents\data-pipeline-assignment\data\raw"
    r"\automobileEDA_dirty_training.csv"
)

output_path = (
    r"C:\Users\acer\Documents\data-pipeline-assignment\data\processed"
    r"\preprocessed_data.csv"
)


scaler = MinMaxScaler()

frequency_encoding = [
    "make",
    "engine-type",
    "fuel-system"
]

one_hot = [
    "body-style",
    "drive-wheels"
]

label_encoding = [
    "aspiration",
    "engine-location",
    "horsepower-binned"
]


def load_data(filename):
    data = pd.read_csv(filename)

    print(data.head())
    data.info()

    return data


def get_column_types(data):
    categorical_columns = list(
        data.select_dtypes(include="object").columns
    )

    categorical_columns += [
        "symboling",
        "diesel",
        "gas"
    ]

    numerical_columns = list(
        data.select_dtypes(include="number").columns
    )

    numerical_columns.remove("symboling")
    numerical_columns.remove("diesel")
    numerical_columns.remove("gas")

    print(
        "------------Categorical Columns------------"
    )
    print(categorical_columns)

    print(
        "-------------Numerical Columns-------------"
    )
    print(numerical_columns)

    return categorical_columns, numerical_columns


def check_data(data):
    inspect_data = [
        "symboling",
        "normalized-losses",
        "curb-weight",
        "engine-size",
        "city-mpg",
        "highway-mpg",
        "diesel",
        "gas"
    ]

    for ins in inspect_data:
        print(f"\nValue counts: {ins}")
        print(data[ins].value_counts())


def data_cleansing(data):
    data_raw = data.copy()

    categorical_columns, numerical_columns = (
        get_column_types(data_raw)
    )

    for category in categorical_columns:
        data_raw[category] = (
            data_raw[category]
            .astype("string")
            .str.lower()
            .str.strip()
        )

    data_raw["transaction_date"] = pd.to_datetime(
        data_raw["transaction_date"],
        dayfirst=True,
        format="mixed"
    )

    for category in categorical_columns:
        data_raw[category] = data_raw[category].fillna(
            data_raw[category].mode()[0]
        )

    data_raw["transaction_date"] = (
        data_raw["transaction_date"].fillna(
            data_raw["transaction_date"].mode()[0]
        )
    )

    data_raw["stroke"] = data_raw["stroke"].fillna(
        data_raw["stroke"].mean()
    )

    data_raw["horsepower"] = data_raw["horsepower"].fillna(
        data_raw["horsepower"].median()
    )

    data_raw["price"] = data_raw["price"].fillna(
        data_raw["price"].median()
    )

    return data_raw, numerical_columns


def data_transformation(data_raw, numerical_columns):
    data_raw = data_raw.copy()

    print("\nSebelum transformasi:")
    print(data_raw[numerical_columns].head())

    data_raw[numerical_columns] = scaler.fit_transform(
        data_raw[numerical_columns]
    )

    print("\nSesudah Min-Max Scaling:")
    print(data_raw[numerical_columns].head())

    categorical_columns = list(
        data_raw.select_dtypes(include="object").columns
    )

    categorical_columns += [
        "symboling",
        "diesel",
        "gas"
    ]

    if "transaction_date" in categorical_columns:
        categorical_columns.remove(
            "transaction_date"
        )

    for category in categorical_columns:
        print(f"\nValue counts: {category}")
        print(data_raw[category].value_counts())

    data_raw = pd.get_dummies(
        data_raw,
        columns=one_hot
    )

    for col in frequency_encoding:
        freq = data_raw[col].value_counts(
            normalize=True
        )

        data_raw[col] = data_raw[col].map(freq)

    for col in label_encoding:
        le = LabelEncoder()

        data_raw[col] = le.fit_transform(
            data_raw[col].astype(str)
        )

    data_raw["symboling"] = data_raw[
        "symboling"
    ].astype(int)

    data_raw["diesel"] = data_raw[
        "diesel"
    ].astype(int)

    data_raw["gas"] = data_raw[
        "gas"
    ].astype(int)

    data_raw = data_raw.drop(
        columns=["transaction_date"]
    )

    return data_raw


def save_data(data_raw):
    output_directory = (
        r"C:\Users\acer\Documents\data-pipeline-assignment"
        r"\data\processed"
    )

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    data_raw.to_csv(
        os.path.join(
            output_directory,
            "preprocessed_data.csv"
        ),
        index=False
    )

    print(
        "\nData berhasil disimpan di:"
    )
    print(output_path)


def pipelining_data(filename):
    data = load_data(filename)

    check_data(data)

    data_raw, numerical_columns = (
        data_cleansing(data)
    )

    data_raw = data_transformation(
        data_raw,
        numerical_columns
    )

    save_data(data_raw)


if __name__ == "__main__":
    pipelining_data(input_path)