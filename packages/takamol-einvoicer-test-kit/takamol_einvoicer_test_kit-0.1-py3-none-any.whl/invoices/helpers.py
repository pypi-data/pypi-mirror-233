import base64
import json
import urllib.parse

import qrcode


def convert_qr_code_into_image_url(qr_code):
    """
    This function will take the qr code as base 64 then convert it to image url
    @param qr_code: qr code data as base 64
    @return: image url data
    """

    # Decode the Base64 string into bytes
    tlv_bytes = base64.b64decode(qr_code)

    # Extract the value from the TLV data
    value = tlv_bytes[2:]

    # Encode the value as a URL
    url_encoded_value = urllib.parse.quote_plus(value)

    # Generate the QR code image
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url_encoded_value)
    qr.make(fit=True)

    return qr.make_image(fill_color='black', back_color='white').get_image_data()


def get_items(invoice):
    """
    Get the list of items associated with the given invoice and serialize them to a JSON-formatted string.

    @param invoice: The invoice object containing the items to be serialized.
    @return: A JSON-formatted string representing the list of items associated with the invoice.
    """
    items = []

    for item in invoice.items:
        serialized_obj = {
            'description_en': item.description_en,
            'description_ar': item.description_ar,
            'unit_price': item.unit_price,
            'quantity': item.quantity,
            'vat_amount': item.vat_amount,
            'vat_rate': item.vat_rate,
            'discount': item.discount,
            'subtotal_excluding_vat': item.subtotal_excluding_vat,
            'subtotal_including_vat': item.subtotal_including_vat,
        }
        items.append(serialized_obj)

    return json.dumps(items)


def convert_xml_str_to_encoded64(xml_string):
    """
    Converts an XML string to a base64 encoded string.

    @param @xml_string: The XML string to be encoded.
    @return: The base64 encoded representation of the XML string.
    """
    xml_bytes = xml_string.encode('utf-8')
    base64_encoded = base64.b64encode(xml_bytes).decode('utf-8')

    return base64_encoded
