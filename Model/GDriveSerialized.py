def get_model():
    import cloudpickle
    import requests

    url = 'https://drive.google.com/uc?id=1-MFsywHy0Ddcp8EH5z88CXARJoQFH8av'

    file = requests.get(url)

    with open('App/Model/trained_pipeline.pkl', 'wb') as f:
        f.write(file.content)

    with open('App/Model/trained_pipeline.pkl', 'rb') as f:
        model = cloudpickle.load(f)
        
    return model

if __name__ == '__main__':
    model = get_model()