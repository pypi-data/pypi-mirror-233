import click
import os
import requests
from sieve.api.constants import API_URL, API_BASE
import uuid
import yaml

from traitlets import default
@click.command()
@click.option('--command', default='upload', help='commands using models')
@click.option('--retrain', default=False, help='retrain model')
@click.option('--version', default=None, help='new model version')

def model(command, retrain, version):
	if command == "upload":
		build_command(retrain=retrain, version=version)

def build_command(retrain=False, version=None, API_KEY=None):
	if API_KEY is not None:
		api_key = API_KEY
	else:
		api_key = os.environ.get('SIEVE_API_KEY')
		if not api_key:
			print("Please set environment variable SIEVE_API_KEY with your API key")
			return

	if version is not None:
		# Open sieve.yaml and set version
		print("Setting version to " + version)
		with open('sieve.yaml', 'r') as stream:
			sieve_yaml = yaml.safe_load(stream)
		sieve_yaml['model_version'] = version
		with open('sieve.yaml', 'w') as stream:
			yaml.dump(sieve_yaml, stream)
		


	os.system('zip dir * -r > zipout')

	upload_url_url = f'{API_URL}/{API_BASE}/create_local_upload_url'
	headers = {
		'X-API-KEY': api_key,
		'Content-Type': 'application/json',
	}
	payload = {"file_name": str(uuid.uuid4())}

	upload_response = requests.request("POST", upload_url_url, headers=headers, json=payload)

	upload_url_json = upload_response.json()
	upload_url = upload_url_json['upload_url']
	headers = {
		'x-goog-content-length-range': '0,10000000000'
	}
	file_upload_response = requests.request("PUT", upload_url, headers=headers, data=open('dir.zip', 'rb'))

	url = f'{API_URL}/{API_BASE}/upload_model'
	payload = {"dir_url": upload_url_json['get_url'], "retrain": "true" if retrain else "false"}
	headers = {
		'X-API-KEY': api_key,
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	os.remove("dir.zip")
	os.remove("zipout")

	if 200 <= response.status_code < 300:
		# Get user info
		out = requests.get(f'{API_URL}/{API_BASE}/user', headers=headers)
		if 200 <= out.status_code < 300:
			user_info = out.json()
			name = user_info['name']
			print("Your model is being built. Your model id is " + response.text + ". You can check the status of your model at https://sievedata.com/app/" + name + "/models")
		else:
			print(f"There was an issue retrieving your user info, but your model with id {response.text} should be processing:" + out.text)
		return
	if 400 <= response.status_code < 500:
		print("There was an issue processing your model. " + response.text)
		return

	print("Response text: " + response.text)
	print("There was an internal error while processing your model. If this problem persists, please contact sieve support")

