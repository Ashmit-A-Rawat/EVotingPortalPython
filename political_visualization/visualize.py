import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file
df = pd.read_csv("parties_data.csv")

# Set plot style
sns.set_theme(style="whitegrid")

# 1️⃣ Bar Plot: Total Wins by Party
plt.figure(figsize=(8, 5))
sns.barplot(x="Party", y="Total_Wins", data=df, palette="viridis")
plt.xticks(rotation=45)
plt.title("Total Wins by Political Party")
plt.xlabel("Party")
plt.ylabel("Total Wins")
plt.show()

# 2️⃣ Pie Chart: Vote Share Percentage
plt.figure(figsize=(7, 7))
plt.pie(df["Vote_Share"], labels=df["Party"], autopct="%1.1f%%", colors=sns.color_palette("pastel"))
plt.title("Vote Share Distribution")
plt.show()

# 3️⃣ Line Plot: Party Popularity Over Time
plt.figure(figsize=(8, 5))
sns.lineplot(x="Founded", y="Leader_Popularity", hue="Party", marker="o", data=df, palette="tab10")
plt.title("Leader Popularity Over Years")
plt.xlabel("Year Founded")
plt.ylabel("Leader Popularity (Out of 100)")
plt.show()
