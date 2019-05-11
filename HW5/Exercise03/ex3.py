import requests
from phe import paillier
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--part', action="store", dest="part")
args = parser.parse_args()
def do_a():
    return args.part in ['a', 'ab', 'ba', None]
def do_b():
    return args.part in ['b', 'ab', 'ba', None]


def main():
    if not do_a() and not do_b():
        print(f'Only part a and b are accepted')
        return

    email = 'gregoire.clement@epfl.ch'
    base_url = 'http://com402.epfl.ch/hw5/ex3/'

    public_key, private_key = paillier.generate_paillier_keypair()

    def predict(enc_x, model, public_key=public_key):
        url_predict = base_url + 'securehealth/prediction_service'
        payload_predict = {
            'email': email,
            'pk': public_key.n,
            'encrypted_input': enc_x,
            'model': model,
        }
        resp = requests.post(
            url = url_predict,
            json = payload_predict,
        )
        return resp.json()['encrypted_prediction']

    def encrypt(x, public_key=public_key):
        if type(x) is list:
            return [encrypt(e) for e in x]
        else:
            return public_key.encrypt(x).ciphertext()

    def decrypt(x, private_key=private_key):
        if type(x) is list:
            return [decrypt(e) for e in x]
        else:
            x = paillier.EncryptedNumber(public_key=public_key, ciphertext=x)
            return private_key.decrypt(x)

    def get_input(email=email):
        url_get_input = base_url + 'get_input'
        payload_get_inp = {
            'email': email,
        }
        resp = requests.post(
            url = url_get_input,
            json = payload_get_inp
        )
        return resp.json()['x']

    ## Part a
    if do_a():
        def get_token_a(prediction):
            url_token_a = base_url + 'get_token_1'
            payload_token_a = {
                'email': email,
                'prediction': prediction
            }
            resp = requests.post(
                url = url_token_a,
                json=payload_token_a,
            )
            if resp.status_code == 200:
                token = resp.json()['token']
                print(f'ex3a = "{token}"')
            else:
                print(f'ex3a token request failed with error_code {resp.stats_code}')

        x = get_input()
        pred_enc = predict(encrypt(x), model=1)
        pred = decrypt(pred_enc)
        get_token_a(pred)


    ## Part b
    if do_b():
        def find_bias():
            x = [0]*12
            pred_enc = predict(encrypt(x), model=2)
            pred = decrypt(pred_enc)
            return pred

        def find_weight(i, bias):
            x = [0]*12
            x[i] = 1
            pred_enc = predict(encrypt(x), model=2)
            pred = decrypt(pred_enc)
            return pred - bias
        
        def get_token_b(weights, bias):
            url_token_b = base_url + 'get_token_2'
            payload_token_b = {
                'email': email,
                'weights': weights,
                'bias': bias,
            }
            resp = requests.post(
                url = url_token_b,
                json=payload_token_b,
            )
            if resp.status_code == 200:
                token = resp.json()['token']
                print(f'ex3b = "{token}"')
            else:
                print(f'ex3b token request failed with error_code {resp.stats_code}')
        
        bias = find_bias()
        weights = [find_weight(i, bias) for i in range(12)]
        
        get_token_b(weights, bias)

main()