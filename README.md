# Famly app image download

The Famly app does not provide download functionality for images. A third party paid browser extension is available which allows downloads.

The Python script within this repo demonstrates how it is possible to use the Python requests library to download images from a Famly app feed.

Running the script requires the user to:

* extract a HTTP request value using browser development tools
* launch a Docker container from VS Code
* step through Python code sections in VS Code

### Python setup

In order to access the Famly app web functionality, you will need to store a text file named `famly_access_token.txt` in the same directory as the `download.py` script. This text file should only contain the value of the `x-famly-accesstoken` header sent in requests to the Famly app. This header value can be found using the development tools in a web browser which can be typically accessed via the F12 key.

Developed in Visual Studio Code using the [Remote-Containers](https://code.visualstudio.com/docs/devcontainers/containers) extension. 

To start the container, open `docker-compose.yml` and select `Docker: Compose Up`. Then find the `famly-download` container and right-click it, choose `Attach Visual Studio Code`. This will open a new window within the container. The first time you run the container you will need to install the Python extension, and choose the Python interpreter at `/usr/local/bin/python`.

You should then be able to step through the code sections in [the Python notebook](download.py) to see how it is possible to download images.

Key Python libraries used are:

* [Requests](https://requests.readthedocs.io/en/latest/) - for getting data from URLs
