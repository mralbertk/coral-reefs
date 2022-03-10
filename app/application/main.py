import streamlit as st
import requests


def cleanup(folder: str) -> dict:
    """
    Posts a request to the API to initiate
    a cleanup operation. All files in the
    specified directory will be deleted.

    Accepted folders: /preview or /export
    """
    req = requests.post(f"http://localhost:8000/cleanup/{folder}")
    return req.json()


@st.cache
def get_models() -> list:
    """
    Calls the backend to get a list of
    available filters. Returns a list of
    filters.
    """
    avail_models = requests.get("http://localhost:8000/models/")
    return avail_models.json()["models"]


@st.cache
def get_params(model: str) -> dict:
    """
    Calls the backend to get a list of
    parameters for a selected model.
    Returns a dictionary with params
    and default values.
    """
    params_res = requests.get(f"http://localhost:8000/{model}/params")
    return params_res.json()["params"]


@st.cache
def get_previews(files: dict) -> dict:
    """
    Sends an uploaded image to the backend and
    calls the generate_preview function. Returns
    a dictionary with the execution time and a
    list of preview thumbnails.
    """
    prev = requests.post("http://localhost:8000/previews", files=files)
    return prev.json()


# Config
st.set_page_config(
    page_title="Coral Image Processing",
    page_icon='🐠'
)

# Title
st.header("Coral Image Processor")

# Temporary: Confirm API is alive
if st.button("Poke API"):
    api_res = requests.get("http://localhost:8000")
    api_msg = api_res.json()
    st.write(api_msg["message"])

# Temporary: Clear export folder
if st.button("Clear exports"):
    clear_msg = cleanup("export")
    st.write(f'/exports cleared. Deleted {clear_msg["removed"]} '
             f'files in {clear_msg["time"]} seconds.')

# Temporary: Clear preview folder
if st.button("Clear preview"):
    clear_msg = cleanup("preview")
    st.write(f'/previews cleared. Deleted {clear_msg["removed"]} '
             f'files in {clear_msg["time"]} seconds.')
    st.legacy_caching.clear_cache()

# Upload image widget TODO: add state to be able to reset
image = st.file_uploader("Upload image")

# Retrieve available models from backend
available_models = get_models()

# Show image
if image:
    st.subheader("Original")
    st.image(image)

    # Serialize the image
    img = image.getvalue()

    # Assemble the request body
    files = {"file": img}

    # Generate preview images
    previews = get_previews(files)
    timing = previews["time"]
    thumbs = previews["thumbs"]

    # Report render time
    st.subheader("Filter previews")

    # Display preview images in 3xn grid
    cols = st.columns(3)
    loc = 0
    for thumb in thumbs:
        with cols[loc % 3]:
            st.text(thumb[0])
            st.image(thumb[1])
            loc += 1

    # Show compute time
    st.text(f"Preview images generated in {timing:.2f} seconds.")

    # Show model selector
    option = st.selectbox('Choose Filter', available_models)

    # Show param options
    if option:
        params = get_params(option)
        model_params = {}
        for param in params:

            match params[param]["type"]:

                case "slider":
                    model_params[param] = st.slider(param,
                                                    params[param]["min"],
                                                    params[param]["max"],
                                                    params[param]["default"],
                                                    params[param]["step"])

                case "selectbox":
                    model_params[param] = st.selectbox(param,
                                                       params[param]["options"],
                                                       params[param]["default"])

        # Temporary: Show params in frontend
        if model_params:
            st.write(f"Selected  params: {model_params}")

    # Upload image to API button
    if st.button("Apply filter") and option:
        # Send to API
        img_res = requests.post(f"http://localhost:8000/files/{option}", files=files)

        # Process response and display new image
        img_msg = img_res.json()
        new_img = img_msg["output"]
        st.image(new_img)
        st.text(f'Filtered image generated in {img_msg["time"]:.2f} seconds.')

        # Download file button
        with open(new_img, "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name=f"{new_img.split('/')[-1]}",
                mime="image/jpg"
            )
