# def get_model():
#     import cloudpickle
#     import requests

#     url = 'https://drive.google.com/uc?id=1-MFsywHy0Ddcp8EH5z88CXARJoQFH8av'

#     file = requests.get(url)

#     with open('Model/trained_model.pkl', 'wb') as f:
#         f.write(file.content)

#     with open('Model/trained_pipeline.pkl', 'rb') as f:
#         model = cloudpickle.load(f)
        
#     return model

# if __name__ == '__main__':
#     model = get_model()
#     print(model.predict([[1, 2, 3, 4]]))


import cloudpickle
import requests

def get_model():
    url = 'https://drive.google.com/uc?id=1-MFsywHy0Ddcp8EH5z88CXARJoQFH8av'

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file: status code {response.status_code}")

    with open('Model/trained_pipeline.pkl', 'wb') as f:
        f.write(response.content)

    try:
        with open('Model/trained_pipeline.pkl', 'rb') as f:
            model = cloudpickle.load(f)
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

    return model

if __name__ == '__main__':
    try:
        model = get_model()
        print(model.predict([[1, 2, 3, 4]]))
    except Exception as e:
        print(f"An error occurred: {e}")