import pandas as pd

# Load datasets
fake = pd.read_csv("data/Fake.csv")
true = pd.read_csv("data/True.csv")

# Add labels
fake['label'] = 1
true['label'] = 0

# Combine datasets
data = pd.concat([fake, true])

# Keep only required columns
data = data[['text', 'label']]

# Shuffle data
data = data.sample(frac=1).reset_index(drop=True)

# Save final dataset
data.to_csv("data/news.csv", index=False)

print("Dataset created successfully!")