import asyncio
from typing import List

import requests
import zxing


class UserProfile:
    def __init__(self, allergies: List[str]):
        self.allergies = allergies


def get_barcode_data(_barcode: zxing.BarCode):
    response = requests.get(f'https://world.openfoodfacts.org/api/v3/product/{_barcode.parsed}.json')
    return response.json()


def get_allergens_from_barcode(_barcode: zxing.BarCode):
    data = get_barcode_data(_barcode)
    allergens = data['product']['allergens'].split(',')
    rtn = []
    for allergen_ in allergens:
        language, allergen = allergen_.strip().split(':')
        if language != 'en':
            print('allergen language is not english: {} {}'.format(language, allergen))
        rtn.append(allergen)
    return rtn


def get_allergy_risks(user_: UserProfile, _barcode: zxing.BarCode):
    allergens = get_allergens_from_barcode(_barcode)
    return list(set(user_.allergies) & set(allergens))


if __name__ == '__main__':
    reader = zxing.BarCodeReader()
    print(reader.zxing_version, reader.zxing_version_info)
    paths = [
        '/Users/andrew/Downloads/2024-04-12 21.40.08.jpg'
        # "/Users/andrew/Downloads/20240412_203645.jpg",
        # '/Users/andrew/Downloads/20240412_211741.jpg',
        # '/Users/andrew/Downloads/barcode-sample.jpeg'
    ]

    user = UserProfile(['peanuts'])

    for path in paths:
        print(f'Detecting in {path}...')
        barcode = reader.decode(path, try_harder=True)
        print(barcode)
        risks = get_allergy_risks(user, barcode)
        print(f'Possible allergy risks: {", ".join(risks)}')
