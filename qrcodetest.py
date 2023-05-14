"""testing creation of arbitrary QR codes with the qrcode module"""

import numpy
import qrcode


def make_code(text: str):
    img = qrcode.make(text)
    type(img)
    img.save(f'_qr_{text}.png')


def make_code_fiddly(text: str):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    type(img)
    img.save(f'_qr_{numpy.random.randint(1000, 9999)}.png')
    print(f'size: {qr.modules_count}')


qrtext = "This is just to say" \
         "" \
         "I have eaten" \
         "the plums" \
         "that were in" \
         "the icebox" \
         "" \
         "and which" \
         "you were probably" \
         "saving" \
         "for breakfast" \
         "" \
         "forgive me" \
         "they were delicious" \
         "so sweet" \
         "and so cold"

make_code_fiddly(qrtext)
