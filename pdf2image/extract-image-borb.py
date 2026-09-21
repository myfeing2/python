import typing

from PIL import ImageOps
from borb.pdf import Document
from borb.pdf import PDF
from borb.toolkit import ImageExtraction


def extract_images_from_pdf(filename: str, updated_number_dict: dict):
    l: ImageExtraction = ImageExtraction()

    # load
    doc: typing.Optional[Document] = None
    with open(filename, "rb") as in_file_handle:
        doc = PDF.loads(in_file_handle, [l])

    # check whether we have read a Document
    assert doc is not None

    index = 0
    for key, value in l.get_images().items():
        image = value[0]
        #image = ImageOps.mirror(image)  # 镜像反转
        card_id = updated_number_dict['card_id'][index]
        filename = f'imgs1/{card_id}.jpg'
        index += 1
        image.save(filename)


if __name__ == '__main__':
    extract_images_from_pdf('sl.pdf', {'card_id': list(range(1, 275))})
