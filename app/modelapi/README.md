# App
This is the backend application. Refer to the top level ```README.md``` for
installation and run instructions.

## Structure
- `main.py` contains the actual code for the backend, written in Python using
[FastAPI](https://fastapi.tiangolo.com/)
- `config.py` contains configuration variables such as file paths and a list of
models imported to the backend
- `models/` contains the various models users can execute via the frontend.
Currently, only underwater image enhancement and underwater image color restoration
filters are implemented.

## Credit
- Underwater Image Enhancement & Restoration Filters: Yan Wang, Wei Song, Giancarlo
Fortino, Lizhe Qi, Wenqiang Zhang, Antonio Liotta via
[Single-Underwater-Image-Enhancement-and-Color-Restoration](https://github.com/wangyanckxx/Single-Underwater-Image-Enhancement-and-Color-Restoration)
