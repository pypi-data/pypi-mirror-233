import os
import json
from base64 import b64encode, b64decode
from configparser import ConfigParser
import boto3
import requests as r
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import pickle
from datetime import datetime as dt
from zoneinfo import ZoneInfo
urllib3.disable_warnings(InsecureRequestWarning)


def request(method, url, headers, data=None, params=None, _json=None, timeout=5, verify=False, allow_redirects=True):
	res = r.request(method, url, data=data, headers=headers, json=_json, params=params,
					verify=verify, allow_redirects=allow_redirects, timeout=timeout, proxies=None)

	try:
		return json.loads(res.content.decode('utf8'))
	except json.decoder.JSONDecodeError:
		return res.content


def base(price, rounder=0.05, precision=2):
	return round(rounder * round(float(price) / rounder), precision)


def get_details(config_name, data_dir):
	config = ConfigParser()
	config.read(os.path.join(data_dir, 'config.ini'))
	z = config[config_name]
	api_key, api_secret, access_token = decrypt(z['api_key']), decrypt(z['api_secret']), decrypt(z['access_token'])

	return api_key, api_secret, access_token


def decrypt(text, key_id='alias/kite_api_key'):
	kms = boto3.client('kms')
	return kms.decrypt(KeyId=key_id, CiphertextBlob=bytes(b64decode(text)))['Plaintext'].decode('utf8')


def encrypt(text, key_id='alias/kite_api_key'):
	kms = boto3.client('kms')
	return b64encode(kms.encrypt(KeyId=key_id, Plaintext=bytes(text, encoding='utf8'))['CiphertextBlob']).decode('utf8')


def get_trade_number(orders):
	trade_num = 0

	if not orders:
		return trade_num

	for order in orders:
		if order['transaction_type'] == 'SELL':
			trade_num += 1

	return trade_num


def check_global_loss(o, global_stop_loss):
	margin = o.get_cash_details(verbose=True)
	pnl = margin['utilised']['m2m_realised']

	if pnl < 0:
		cash = margin['available']
		total_cash = cash['opening_balance'] + cash['intraday_payin'] + cash['collateral']

		return False if abs(pnl) > (total_cash * global_stop_loss) else margin['net']

	return margin['net']


def get_total_cash(o):
	margin = o.get_cash_details(verbose=True)
	cash = margin['available']

	return cash['opening_balance'] + cash['intraday_payin'] + cash['collateral']


def get_oms_session():
	s3 = boto3.client('s3')
	file_obj = s3.get_object(Bucket=os.environ['SESSION_BUCKET'], Key='session.json')

	return file_obj['Body'].read().decode('utf-8')


def ticker_transform(ticker):
	months = {'1': 'JAN', '2': 'FEB', '3': 'MAR', '4': 'APR', '5': 'MAY', '6': 'JUN', '7': 'JUL', '8': 'AUG',
	          '9': 'SEP', 'O': 'OCT', 'N': 'NOV', 'D': 'DEC'}
	date_modifier = {'01': 'st', '02': 'nd', '03': 'rd', '21': 'st', '22': 'nd', '23': 'rd'}
	
	today = dt.now(tz=ZoneInfo('Asia/Kolkata'))
	cur_month, cur_year = today.strftime('%b').upper(), today.strftime('%y')
	ticker, data = ticker.split(cur_year)
	month, date, strike = months[data[0]], data[1:3], data[3:]
	date_modified = date_modifier.get(date, 'th')
	
	return f'{ticker} {date}{date_modified}{month} {strike}'


def round_down(x, nearest_num=50):
	return x if x % nearest_num == 0 else x - (x % nearest_num)


def round_up(x, nearest_num=50):
	return x if x % nearest_num == 0 else x + (nearest_num - (x % nearest_num))


def get_from_s3(bucket, file_path):
	s3 = boto3.client('s3')
	file_obj = s3.get_object(Bucket=bucket, Key=file_path)

	return file_obj['Body'].read().decode('utf-8')


def upload_to_s3(bucket, file, key):
	s3 = boto3.client('s3')
	s3.put_object(Body=file, Bucket=bucket, Key=key)


def text_to_pickle(text, direc):
	with open(direc, 'wb') as f:
		pickle.dump(text, f)


def pickle_to_text(direc):
	with open(direc, 'rb') as f:
		return pickle.load(f)


def colourise(text, colour, decorate=None, end_='\n'):
	_c = {'pink': '\033[95m', 'blue': '\033[94m', 'green': '\033[92m', 'yellow': '\033[93m', 'grey': '\033[97m',
		  'cyan': '\033[96m', 'end': '\033[0m', 'red': '\033[91m', 'underline': '\033[4m', 'bold': '\033[1m'}
	colour, end = _c[colour], _c['end']

	if decorate is not None:
		print(f'{_c[decorate]}{colour}{text}{end}', end=end_)
	else:
		print(f'{colour}{text}{end}', end=end_)
