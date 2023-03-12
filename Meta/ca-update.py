import configparser
import fileinput
from base64 import b64encode

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509.oid import NameOID

with open("cacert.pem", "rb") as source, open("certs.ini", "w", encoding="utf-8") as dest:
    certs = x509.load_pem_x509_certificates(source.read())
    output = configparser.RawConfigParser(allow_no_value=True)
    output.optionxform = lambda option: option

    for cert in certs:

        if not isinstance(cert.signature_hash_algorithm, hashes.SHA256):
            continue

        try:
            commonName = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        except IndexError:
            commonName = cert.subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value
        try:
            organizationName = cert.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
        except IndexError:
            organizationName = ""

        header = " ".join(commonName.split(" ")[:-1])
        certName = commonName.split(" ")[-1]
        raw_cert = b64encode(cert.public_bytes(Encoding.DER))
        if not output.has_section(organizationName):
            output.add_section(organizationName)
        if header:
            output.set(organizationName, header)
        output.set(organizationName, certName, raw_cert.decode("utf-8"))

    output.write(dest)

# This could be removed if it is ok to keep [DEFAULT] instead of [], configparser does not allow empty section names
with fileinput.FileInput("certs.ini", inplace=True) as file:
    for line in file:
        print(line.replace("[DEFAULT]", "[]"), end='')
