import configparser

config = configparser.ConfigParser()

config["database"] = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "admin123",
}
with open("config.ini", "w") as configfile:
    config.write(configfile)

config.read("api.ini")
print(config["database"]["host"])
