import boto3
import streamlit as st


#   /------------------------------------------------/
#  /               Function Definitions             /
# /------------------------------------------------/

def s3_image_upload(file, file_name, bucket, client):
    """Uploads an image file object to Amazon S3

    Args:
        file: The file object to upload to Amazon S3
        file_name: Name under which the file will be stored
        bucket: Amazon S3 bucket the file will be uploaded to
        client: A Boto3 S3 client instance.

    Returns:
        This function has no return statement

    Raises:
        TypeError: Only .jpg, .png, .tiff and .nef files are accepted
    """
    client.upload_fileobj(file, bucket, file_name)


#   /------------------------------------------------/
#  /                   Configuration                /
# /------------------------------------------------/

# TODO: Parameterize Bucket Names
# Image Upload Bucket
s3_bucket_raw = "criobe-images-raw"

# Image View Bucket TODO: Update with segmented bucket
s3_bucket_reframed = "criobe-images-reframed"

# Modes: To keep the UI simple, users will be able to select
#        a desired operation on top of the page. Operations
#        are: Upload Image(s), View Image(s), Export Stats
view_modes = ("Upload Image(s)", "View Image(s)", "Export Statistics")

#   /------------------------------------------------/
#  /                Streamlit Script                /
# /------------------------------------------------/


# Page Configuration
st.set_page_config(
    page_title="Coral Image Processor",
    page_icon='🐠'
)

# Page Header
st.header("Coral Image Processor")

# Select view mode
mode = st.selectbox("What would you like to do?", view_modes)

# Image upload mode
if mode == "Upload Image(s)":

    # Boto3 Client
    s3_client = boto3.client("s3")

    # Upload Form
    with st.form("s3_uploader"):
        st.subheader("Upload Image(s)")
        st.text("Note: Images will be stored as: [year]-[location]-[upload_filename]")
        location = st.text_input("Location",
                                 value="",
                                 help="Name of the Location the image(s) is/are from, i.e. Takapoto.")
        year = st.text_input("Year",
                             value="",
                             help="Year the image(s) was/were taken.")
        images = st.file_uploader("Upload File(s)", accept_multiple_files=True)
        submitted = st.form_submit_button("Upload to Amazon S3")

        # Image Upload Process
        if submitted and images:
            upload_bar = st.progress(0.0)
            to_upload = 0
            for image in images:
                to_upload += 1 / len(images)
                upload_bar.progress(to_upload)
                filename = f"{year}-{location}-{image.name}"
                s3_image_upload(image, filename, s3_bucket_raw, s3_client)

# Image view mode
if mode == "View Image(s)":
    pass

# Get statistics mode
if mode == "Export Statistics":
    pass
