# If qrcode is not installed, use pip install qrcode
import qrcode

parameters = {
    "qr transform": "https://www2.acom.ucar.edu/modeling/tropospheric-ultraviolet-and-visible-tuv-radiation-model",
    "graphics path": "../Graphics/",
    "output name": "qr",
}

qr = qrcode.make(parameters["qr transform"])
qr_image = open("{}{}.png".format(parameters["graphics path"],
                                  parameters["output name"]),
                "wb")
qr.save(qr_image)
qr.close()
