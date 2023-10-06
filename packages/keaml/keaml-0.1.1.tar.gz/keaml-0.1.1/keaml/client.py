import requests
import joblib
import subprocess
import pkg_resources
import shutil
import os
import json

class KeaMLSDKClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def deploy(self, model, name, framework):
        version = self._get_model_version(name=name)
        self._save_model_as_joblib(model)
        self._package_model(name, version)
        self._upload_model(name, version)
        self._delete_files()

    def _get_model_version(self, name):
        url = f'https://api.keaml.com/models/{name}/next-version'
        headers = {
            'X-API-KEY': self.api_key
        }
        response = requests.get(url=url, headers=headers)
        return response.json()['next_version']

    def _save_model_as_joblib(self, model):
        with open('model.joblib', 'wb') as f:
            joblib.dump(model,f)
    
    def _delete_files(self):
        subprocess.run(['rm', 'model.joblib'])
    
    def _package_model(self, name, version):
        # Step 1: Get the path of inference.py from inside the SDK
        inference_path = pkg_resources.resource_filename(__name__, 'inference.py')
        
        # Step 2: Copy inference.py to the current directory
        shutil.copy(inference_path, './inference.py')
        
        # Step 3: Tar model.joblib and inference.py together
        bashCommand = f'tar -cvpzf {name}-{version}.tar.gz model.joblib inference.py'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        process.communicate()
        
        # Step 4: Clean up the copied inference.py (optional but recommended)
        os.remove('./inference.py')
    
    def _upload_model(self, name, version):
        url = f'https://api.keaml.com/models/deploy'
        headers = {
            'X-API-KEY': self.api_key
        }

        files=[('model',(f'{name}-{version}.tar.gz',open(f'{name}-{version}.tar.gz','rb'),'application/octet-stream'))]
        data = {
            "name": name,
            "version": version,
            "framework": "sklearn"
        }
        payload = {'data': json.dumps(data)}
        requests.post(url=url, headers=headers, data=payload, files=files)
        subprocess.run(['rm', f'{name}-{version}.tar.gz'])

def init(api_key):
    return KeaMLSDKClient(api_key)
