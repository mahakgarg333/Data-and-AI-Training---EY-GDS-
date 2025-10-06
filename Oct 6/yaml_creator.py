import yaml


#Python dictionary
config = {
    "model": "RandomForest",
    "params":{
        "n_estimators": 100,
        "max_depth": 5,
    },
    "dataset" : "students.yaml"
}
#write to a json file
with open("config.yaml", "w") as f:
    yaml.dump(config, f)

with open("student.json", "r") as f:
    data = yaml.safe_load(f)

print(data["params"]["n_estimators"])
