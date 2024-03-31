import os
import configparser


def create_config():
    """Initializes a config with defaults."""
    datapath = f"{os.getenv('HOME')}/.local/share/modo/hours.parquet"
    os.makedirs(os.path.dirname(datapath), exist_ok=True)
    configpath = f"{os.getenv('HOME')}/.config/modo/modo.ini"
    os.makedirs(os.path.dirname(configpath), exist_ok=True)
    config = configparser.ConfigParser()
    config["settings.data"] = {
        "path": datapath,
        "type": "arrow",
    }
    config["settings.preferences"] = {"colors": "green"}
    with open(configpath, "w") as configfile:
        config.write(configfile)
        configfile.close()

    return


def load_config():
    config = configparser.ConfigParser()
    config.read(f"{os.getenv('HOME')}/.config/modo/modo.ini")


if __name__ == "__main__":
    create_config()
