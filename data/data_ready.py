import pandas as pd

df = pd.read_csv("data/driving_data.csv")

print("Before:", df.shape)

df = df.drop_duplicates()

print("After:", df.shape)

df.to_csv("driving_data.csv", index=False)
print("Dataset shape:", df.shape)

print("\nSteering distribution:")
print(df["steering"].value_counts())

print("\nThrottle distribution:")
print(df["throttle"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())
