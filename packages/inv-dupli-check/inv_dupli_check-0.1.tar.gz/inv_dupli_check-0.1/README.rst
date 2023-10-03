Invoice Duplication Checker

Quick start
-----------

1. ``tesseract`` install like this

    ``sudo apt install tesseract-ocr -y``

2. create a virtual environment

3. install ``inv_dupli_check`` package like this

    ``pip3 install inv_dupli_check``
<!-- 
4. create a file with this code:
    ``from inv_dupli_check import convert_pdf_to_images, extract_text, calculate_txt_similarity

    if __name__ == "__main__":
        path = "/home/test.pdf
        images = convert_pdf_to_images(path)
        for index,img in images:
            text = extract_text(img)
        percent = calculate_txt_similarity(text1,text2)`` -->

5. Run ``python3 main.py`` to use this package.