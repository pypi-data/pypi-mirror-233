import requests
import json
from munch import DefaultMunch


class HavenClient:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json',
        }

    def completion(self, model, prompt, temperature=0.8, top_p=0.9, max_tokens=3000, stream=False):

        data = {
            'prompt': prompt,
            'temperature': temperature,
            'top_p': top_p,
            'max_tokens': max_tokens
        }

        if stream:
            url = f'https://{self.base_url}/v1/generate_stream/{model}'

            response = requests.post(url, headers=self.headers, json=data, stream=True)

            if response.status_code == 200:

                for r in response.iter_lines():
                    yield DefaultMunch.fromDict(json.loads(r))

            else:
                print(f"Request failed with status code {response.status_code}")
                print(response.text)

        else:
            url = f'https://{self.base_url}/v1/generate/{model}'
            response = requests.post(url, headers=self.headers, json=data, stream=True)

            if response.status_code == 200:
                return response.json()

            else:
                print(f"Request failed with status code {response.status_code}")
                print(response.text)
        
        

