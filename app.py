import qrcode
import streamlit as st
import base64
from io import BytesIO
from PIL import Image

# Streamlit app for generating QR codes
st.title("Enhanced QR Code Generator")
st.header("Enter the text or URL to generate a QR code:")

# Input data for QR code
data = st.text_input("QR Code Data")

# Color options
st.sidebar.header("Customize QR Code")
fill_color = st.sidebar.color_picker("Fill Color", "#000000")
back_color = st.sidebar.color_picker("Background Color", "#FFFFFF")

# File format options
file_format = st.sidebar.selectbox("Select File Format", ["PNG", "SVG"])

# QR Code size options
qr_size = st.sidebar.slider("QR Code Size", 1, 20, 10)
border_size = st.sidebar.slider("Border Size", 4, 10, 4)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """
    Generate HTML code for a download button
    """
    b64 = base64.b64encode(bin_file).decode()
    download_button = f'''
        <a href="data:application/octet-stream;base64,{b64}" download="qrcode.{file_format.lower()}">
            <button style="
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 12px 30px;
                cursor: pointer;
                font-size: 16px;
                border-radius: 4px;">
                Download {file_label}
            </button>
        </a>'''
    return download_button

# Generate QR Code
if st.button("Generate QR Code"):
    if not data:
        st.error("Please enter data to generate a QR code.")
    else:
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=qr_size,
                border=border_size,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create an image from the QR Code instance
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            # Convert to bytes for display and download
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_bytes = buffer.getvalue()

            # Display the QR code
            st.success("QR Code generated successfully! Here's your QR code:")
            st.image(img_bytes, use_column_width=True)

            # Download button
            st.markdown(get_binary_file_downloader_html(img_bytes, 'QR Code'), unsafe_allow_html=True)

            # Display QR code information
            st.info(f"""
            QR Code Information:
            - Content: {data}
            - Size: {qr_size}px
            - Border: {border_size}px
            - Fill Color: {fill_color}
            - Background Color: {back_color}
            """)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

