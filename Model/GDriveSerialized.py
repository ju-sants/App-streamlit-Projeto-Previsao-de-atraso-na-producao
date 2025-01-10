def get_model():
    import dill
    import requests

    url = 'https://drive.google.com/uc?id=1-MFsywHy0Ddcp8EH5z88CXARJoQFH8av'

    file = requests.get(url)

    with open('Model/trained_pipeline.pkl', 'wb') as f:
        f.write(file.content)

    with open('Model/trained_pipeline.pkl', 'rb') as f:
        model = dill.load(f)
        
    return model

if __name__ == '__main__':
    model = get_model()