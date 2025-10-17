import pandas as pd

def load_and_preview_data(file_path):
    print(f"✅ Loading data from: {file_path}")
    data = pd.read_csv(file_path)

    print("\n📊 Dataset Preview:")
    print(data.head())

    print("\n📈 Dataset Info:")
    print(data.info())

    print("\n🔢 Dataset Shape:", data.shape)
    return data

if __name__ == "__main__":
    data_path = "data/raw/kdd_train.csv"
    dataset = load_and_preview_data(data_path)

