import boto3
import streamlit as st
import numpy as np
from PIL import Image


#   /------------------------------------------------/
#  /               Function Definitions             /
# /------------------------------------------------/

def s3_image_upload(file, file_name, bucket, client):
    """Uploads an image file object to Amazon S3.

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


# TODO: Make sure this does not break when there are more than 1000 images
def get_s3_object_filters(bucket, resource):
    """Scans all objects in an S3 bucket and returns lists of available
    years & locations.

    The list is used to generate filters for users to view an image set.

    Args:
        bucket: The S3 bucket to scan
        resource: A Boto3 S3 resource instance

    Returns:
        Two lists: Unique years and unique locations

    Raises:
        Boto3 error if the bucket name is not found on your AWS account
    """
    bucket_resource = resource.Bucket(bucket)
    bucket_objects = [s3_object.key for s3_object in bucket_resource.objects.all()]
    years = list({bucket_object.split("-")[0] for bucket_object in bucket_objects})
    locations = list({bucket_object.split("-")[1] for bucket_object in bucket_objects})
    return years, locations


def fetch_s3_objects(prefix, bucket, resource):
    """Fetches a list of S3 objects from a bucket based on a prefix.

    The list is used to load all images into memory and display them.

    Args:
        prefix: A string used to filter S3 objects
        bucket: The S3 bucket to fetch the objects from
        resource: A Boto3 S3 resource instance

    Returns:
        A list of S3 objects matching the filter in the selected bucket

    Raises:
        Boto3 error if the bucket name is not found on your AWS account
    """
    return [obj.key for obj in
            resource.Bucket(bucket).objects.filter(Prefix=prefix)]


def load_s3_image(s3_object, bucket, resource):
    """Loads an image file from S3 into memory.

    Args:
        s3_object: A S3 object to load
        bucket: The S3 bucket to load the image from
        resource: A Boto3 S3 resource instance

    Returns:
        np array: Image array

    Raises:
        # TODO: Identify proper error message(s)
        TypeError (probably) if s3_object is not an image file
    """
    s3_bucket = resource.Bucket(bucket)
    s3_image_object = s3_bucket.Object(s3_object)
    response = s3_image_object.get()
    file_stream = response["Body"]
    img = Image.open(file_stream)
    return np.array(img)


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
        # TODO: Add robustness against missing year/location
        if submitted and images:
            upload_bar = st.progress(0.0)
            to_upload = 0
            for image in images:
                to_upload += 1 / len(images)
                upload_bar.progress(to_upload)
                name_two_digits = f"{int(image.name.split('.')[0]):02d}.{image.name.split('.')[-1]}"
                filename = f"{year}-{location}-{name_two_digits}"
                s3_image_upload(image, filename, s3_bucket_raw, s3_client)

# Image view mode
if mode == "View Image(s)":

    # Boto3 Client
    s3_resource = boto3.resource("s3")

    # Get options for selector
    s3_years, s3_locations = get_s3_object_filters(s3_bucket_reframed, s3_resource)

    # Show selector
    selector_col_1, selector_col_2 = st.columns(2)

    # Select location
    with selector_col_1:
        s3_locs = st.selectbox("Location", s3_locations)

    # Select year
    with selector_col_2:
        s3_ys = st.selectbox("Year", s3_years)

    # Fetch and display images
    btn_go = st.button("GO!")

    # Activate if button is clicked
    if btn_go:

        # Fetch image names
        s3_images = fetch_s3_objects(f"{s3_ys}-{s3_locs}", s3_bucket_reframed, s3_resource)

        # "Gallery" layout
        cols = st.columns(4)
        loc = 0

        # Load images into memory and display
        for s3_image in s3_images:
            this_image = load_s3_image(s3_image, s3_bucket_reframed, s3_resource)
            with cols[loc % 4]:
                st.text(s3_image.split(".")[0])
                st.image(this_image)
                loc += 1


# Get statistics mode
if mode == "Export Statistics":
    st.header("UNDER CONSTRUCTION")
