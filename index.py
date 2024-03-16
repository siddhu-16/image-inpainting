import argparse
import streamlit as st
from skimage.io import imread, imsave
from inpainter import Inpainter
import io
        
prev_placeholder = None

def main():
    st.title('Image Completion')

    # Input file upload for the image
    image_upload = st.file_uploader("Upload the image containing objects to be removed", type=["jpg", "jpeg", "png"])
    mask_upload = st.file_uploader("Upload the mask of the region to be removed", type=["jpg", "jpeg", "png"])

    if image_upload is not None and mask_upload is not None:
        # Read uploaded files
        image = imread(image_upload)
        mask = imread(mask_upload, as_gray=True)

        # Inpainting parameters
        patch_size = 9  # Set your default patch size here

        if st.button('Start Process'):
            global prev_placeholder
            prev_placeholder = st.empty()
            # Create a spinner to indicate ongoing process
            with st.spinner('Inpainting in progress...'):
                inpainter = Inpainter(image, mask, patch_size=patch_size)
                output_image = inpainter.inpaint(progress_callback=update_progress)

            # Save the inpainted image to a BytesIO object
            output_buffer = io.BytesIO()
            imsave(output_buffer, output_image, format='JPEG', quality=100)

            # Create a download button for the inpainted image
            st.write('Inpainting complete. You can download the inpainted image below:')
            st.download_button(
                label='Download Inpainted Image',
                data=output_buffer,
                file_name='output.jpg',
                key='download-button'
            )   

def update_progress(image):
    global prev_placeholder
    if prev_placeholder is not None:
        prev_placeholder.image(image, caption='Inpainting Progress', use_column_width=True)

if __name__ == '__main__':
    main()
