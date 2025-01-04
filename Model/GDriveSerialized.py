def get_model():
    import cloudpickle
    import requests

    url = url = 'https://drive.google.com/uc?id=1-MFsywHy0Ddcp8EH5z88CXARJoQFH8av'

    file = requests.get(url)

    with open('model.pkl', 'wb') as f:
        f.write(file.content)

    with open('model.pkl', 'rb') as f:
        model = cloudpickle.load(f)
        
    return model