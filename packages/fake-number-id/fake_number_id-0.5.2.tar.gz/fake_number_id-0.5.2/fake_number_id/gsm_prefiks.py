#! pustaka/alat/bin/python3

from faker import Faker
import phonenumbers


def telepon(operator: str) -> str:
    fake = Faker(locale="id_iD")
    nomor = '{0}{1}'.format(operator.value, fake.msisdn()[5:])
    nomor_seri = phonenumbers.parse(nomor, "ID")
    return phonenumbers.format_number(nomor_seri, phonenumbers.PhoneNumberFormat.NATIONAL)

def layanan_operator(operator: str) -> str:
    return str(operator).split('.')[0]

