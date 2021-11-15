# Frontend
This is the front end application. Refer to the top level ```README.md``` for
installation and run instructions.

## Usage
The following actions are supported:

- Upload an image
- Generate previews
- Select a filter
- Apply a filter to a full-size image
- Download the modified image

### Clean-up
All preview and export files are currently stored in the file system. It may
be necessary to run periodical clean-ups to avoid filling the available disk
space.

Until automated clean-up (or a proper DBMS) are implemented, users can manually
clean their `preview/` and `export/` directories using UI buttons at the top of
the `streamlit` application.

## References
The frontend application is written in Python 3.10 and built with the [Streamlit](https://streamlit.io/)
library. Refer to the [documentation](https://docs.streamlit.io/) for more information.
