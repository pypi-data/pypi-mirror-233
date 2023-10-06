# GraphHandler
## FBGraphHandler

FBGraphHandler is a Python library that simplifies the process of interacting with Facebook's Graph API. It provides methods for authenticating users, retrieving user details, posting text and video feeds, and more.

## Installation

You can install FBGraphHandler using pip:

```bash
pip install FBGraphHandler
```
## Usage

### Importing FBGraphHandler
```python
from FBGraphHandler import FBGraphHandler
```

### Initializing FBGraphHandler
```python
# Create an instance of FBGraphHandler
graph_handler = FBGraphHandler()

# Configure FBGraphHandler with your Facebook App credentials
graph_handler.Config(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET", version="14.0")
```
### Generating an Authorization URL
```python
# Generate an authorization URL for users to complete the authentication process
auth_url = graph_handler.GenerateAuthURL(redirect_uri="YOUR_REDIRECT_URI", scopes=["public_profile", "email"])
```
### Exchanging Authorization Code for Access Token
```python
# Exchange the authorization code for an access token
access_token = graph_handler.ExchangeCodewithToken(code="AUTHORIZATION_CODE")
```
### Getting User Details
```python
# Get user details using the access token
user_details = graph_handler.GetUserDetails(access_token="ACCESS_TOKEN")
```
### Posting a Text Feed
```python
# Post a text feed to a user or page
post_id = graph_handler.PostTextFeed(text="Hello, Facebook!", id="PAGE_OR_USER_ID", access_token="ACCESS_TOKEN")
```
### Posting a Video Feed
```python
# Post a video feed to a user or page
post_id = graph_handler.PostVideoFeed(text="Check out this video!", id="PAGE_OR_USER_ID", access_token="ACCESS_TOKEN", video_url="VIDEO_URL")
```
### Posting Media (Text, Photos, or Videos)
```python
# Post text, photos, or videos to a user or page
media_urls = ["PHOTO_URL_1", "PHOTO_URL_2"]
post_id = graph_handler.PostToFacebook(text="My Facebook post", media_urls=media_urls, access_token="ACCESS_TOKEN", id="PAGE_OR_USER_ID", isVideo=False)
```
## Documentation
For detailed documentation and more information about available methods and parameters, please refer to the <a href='https://github.com/Ambar-06/python-graph-handler'>official documentation</a>.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
