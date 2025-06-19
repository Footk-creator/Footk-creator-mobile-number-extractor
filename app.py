import streamlit as st
import pytesseract
from PIL import Image
import re
import io

st.title("📱 Mobile Number Extractor from Images")

uploaded_files = st.file_uploader("Upload image(s) to extract mobile numbers:", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    mobile_numbers = set()

    for file in uploaded_files:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)

        found = re.findall(r'(?:\+91[\s-]*|0)?[6-9]\d{9}', text)

        for num in found:
            clean_num = re.sub(r'\D', '', num)
            if clean_num.startswith("91"):
                clean_num = clean_num[2:]
            elif clean_num.startswith("0"):
                clean_num = clean_num[1:]
            if len(clean_num) == 10:
                mobile_numbers.add(clean_num)

    if mobile_numbers:
        st.success(f"✅ Found {len(mobile_numbers)} unique mobile numbers.")
        mobile_list = "\n".join(sorted(mobile_numbers))
        st.text_area("📋 Cleaned Mobile Numbers:", mobile_list, height=200)

        output = io.StringIO()
        output.write(mobile_list)
        output.seek(0)

        st.download_button("⬇ Download as .txt", data=output, file_name="mobile_numbers.txt", mime="text/plain")
    else:
        st.warning("No mobile numbers found.")
