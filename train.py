from rasa import train

def train_model():
    config = "config.yml"
    training_files = ["nlu.yml", "stories.yml"]
    domain = "domain.yml"
    output = "models/"

    model_path = train(domain, config, training_files, output)
    print(f"Model trained and saved at {model_path}")

train_model()
