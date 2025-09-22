import pandas as pd
import numpy as np
data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram"],
    "Age": [21, 22, 20, 23, 21],
    "Course": ["AI", "ML", "Data Science", "AI", "ML"],
    "Marks": [85, 90, 78, 88, 95]
}
df = pd.DataFrame(data)
print(df)

#selecting data
print(df["Name"])
print(df[["Name", "Marks"]])
print(df.iloc[0])
print(df.loc[2,"Marks"])

#Filter data
high_scorers = df[df["Marks"] > 85]
print(high_scorers)

#Adding and updating columns
df["Result"] = np.where(df["Marks"] >= 80, "Pass", "Fail")
print(df)

df.loc[df["Name"] == "Neha", "Marks"] = 92
print(df)

pip install matplotlib  
import matplotlib.pyplot as plt 
avg_marks = df.groupby("Course") ["Marks"].mean() 
avg_marks.plot(kind="bar", color = "skyblue", edgecolor= "red") 
plt.title("Average Marks")
plt.xlabel("Course")
plt.ylabel("Average Marks ")
plt.xticks(rotation = 45)
plt.show()




