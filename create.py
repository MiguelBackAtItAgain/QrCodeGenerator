import qrcode

def create_qr_code(data, color):

    qr = qrcode.QRCode(version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=20,
                        border=2)

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color='blue',
                        back_color="white")
    
    return img
