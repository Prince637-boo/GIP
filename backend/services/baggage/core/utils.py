import qrcode
import uuid
import os

def generate_qr_code(tag: str, output_dir="storage/qr_codes") -> str:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{tag}_{uuid.uuid4().hex}.png"
    file_path = os.path.join(output_dir, filename)

    img = qrcode.make(tag)
    img.save(file_path)

    return file_path
