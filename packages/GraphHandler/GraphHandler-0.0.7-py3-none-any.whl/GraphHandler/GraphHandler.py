from typing import Union
import requests
import secrets, json

class FBGraphHandler():

    def __init__(self) -> None:
        self.AuthURL = "https://www.facebook.com/v{}/dialog/oauth?response_type&client_id={}&redirect_uri={}&scope={}&response_type=code&state={}"
        self.TokenURL = "https://graph.facebook.com/v{}/oauth/access_token?redirect_uri={}&scope={}&client_id={}&client_secret={}&code={}"
        self.FacebookMeURL = "https://graph.facebook.com/me?fields=id,name"
        self.FacebookImageURL = "https://graph.facebook.com/v{}/{}/picture/?access_token={}&type=normal&redirect=false"
        self.FacebookPageTokenURL = "https://graph.facebook.com/{}/accounts?access_token={}"
        self.FacebookLongLivedTokenURL = "https://graph.facebook.com/v{}/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}"
        self.FacebookRequestURL = "https://graph.facebook.com/{}/feed"
        self.FacebookVideoUploadURL = "https://graph.facebook.com/v{}/{}/videos"
        self.FacebookPhotoUploadURL = "https://graph.facebook.com/v{}/{}/photos"
        self.FacebookFeedURL = "https://graph.facebook.com/{}/feed"

    def Config(self, client_id : str, client_secret : str, version='14.0') -> None:
        """_summary_
                This method configure the GraphHandler library to use the provided credentials and version.
        Args:
            client_id (str): Facebook App client Id.
            client_secret (str): Facebook App client Secret.
            version (str, optional): Graph API version. Supported: [14.0, 15.0, 16.0, 17.0]. Defaults to '14.0'.
            NOTE::: Latest version is not always means it is better.
        """        
        self.client_id = client_id
        self.client_secret = client_secret
        self.version = version

    def GenerateAuthURL(self, redirect_uri : str, scopes : Union[list[str], str]) -> str:
        """_summary_
                This method generates auth url for users to complate auth process and get access code.
        Args:
            redirect_uri (str): your website url. example: www.example.com/linked-accounts/facebook/

            scopes (str or list[str]): permissions that you need from facebook to perform actions on Graph endpoints..example: public_profile,email,read_insights,pages_show_list,instagram_basic,instagram_manage_comments......and more..
        """
        if type(scopes) == list:
            scopes_ = ','.join(scopes)
        elif type(scopes) == str:
            scopes_ =  scopes.replace(' ', '')
        self.redirect_uri = redirect_uri
        self.scopes = scopes_
        self.state = secrets.token_hex(16)
        self.AuthURL_ = self.AuthURL.format(self.version, self.client_id, self.redirect_uri, self.scopes, self.state)
        
        return self.AuthURL_
    
    def ExchangeCodewithToken(self, code : str) -> str:
        """_summary_
                This method exchanges AuthCode with AccessToken
        Args:
            code (str): Facebook AuthCode.
        Returns:
            str: AccessToken as a string.
        """       
        self.code = code
        self.TokenURL_ = self.TokenURL.format(self.version, self.redirect_uri, self.scopes, self.client_id, self.client_secret, self.code)
        self.facebook_token_response = requests.get(self.TokenURL_)
        self.facebook_token = self.facebook_token_response.json()['access_token'] if self.facebook_token_response.json()['access_token'] else 'No Token Found. Please Try again.'
        return self.facebook_token
    
    def GetUserDetails(self, access_token='') -> dict:
        """_summary_
                This method uses Facebook AccessToken and returns Id, and Username of the user
        Args:
            access_token (str): Facebook AccessToken. Defaults empty string.
        Returns:
            dict: dict with userId, and Username. Example: {'id': <ID>, 'name': <USERNAME>}
        """        
        self.access_token = access_token if len(access_token) > 0 else self.facebook_token
        self.AccessTokenPayload = {
            "access_token": self.access_token
        }   
        self.facebook_me_response = requests.get(self.FacebookMeURL,  self.AccessTokenPayload)
        self.facebook_user_id = self.facebook_me_response.json()['id']
        self.facebook_name = self.facebook_me_response.json()['name']
        return {'id': self.facebook_user_id, 'name': self.facebook_name}
    
    def GetProfileImage(self, id : str, access_token='') -> dict:
        """_summary_
                This method uses Facebook AccessToken and returns a profile image url
        Args:
            id (str, required): The ID (ppage or User) you want to get profile image for.
            access_token (str, optional): The access token you want to get profile image for.
            defaults to instance access_token 
        Returns:
            str: Profile Image URL 
        """    
        self.access_token = access_token if len(access_token) > 0 else self.facebook_token
        self.ID = id 
        self.FacebookImageURL_ = self.FacebookImageURL.format(self.version, self.ID, self.access_token)
        self.facebook_image_response = requests.get(self.FacebookImageURL_)
        self.facebook_user_image = self.facebook_image_response.json()['data']['url']
        return {'profile_picture' : self.facebook_user_image}

    def GetLongLivedToken(self, access_token : str) -> str:
        """_summary_
                This method uses Facebook AccessToken and returns Long_Lived_Access_Token
        Args:
            access_token (str, required): The access token you want to exchange for long lived token with.
        Returns:
            str: long_lived_token 
        """        
        self.access_tokenforexchange = access_token
        self.FacebookLongLivedTokenURL_ = self.FacebookLongLivedTokenURL.format(self.version, self.client_id, self.client_secret, self.access_tokenforexchange)
        self.facebook_long_response = requests.get(self.FacebookLongLivedTokenURL_)
        self.long_token = self.facebook_long_response.json()['access_token']
        return self.long_token
    
    def FacebookPageAuth(self) -> list:
        """_summary_
                This method uses Facebook credentials generated for a particular instance and returns Page Long_Lived_Access_Token, PageId and PageName
        Returns:
            dict:   'access_token': <access_token>,
                    'page_id': <page_id>,
                    'page_name': <page_name>,
                    'id' : <id> 
        """        
        self.facebook_credentials = []
        self.FacebookPageTokenURL_ = self.FacebookPageTokenURL.format(self.facebook_user_id, self.facebook_token)
        self.facebook_page_responses = requests.get(self.FacebookPageTokenURL_)
        for response in self.facebook_page_responses.json()['data']:
            self.page_creds = {
                'access_token': self.GetLongLivedToken(response['access_token']),
                'page_id': response['id'],
                'page_name': response['name'],
            }
            self.page_creds.update(self.GetProfileImage(response['id']))
            self.facebook_credentials.append(self.page_creds)
        return self.facebook_credentials
    
    def PostTextFeed(self, text : str, id : str, access_token : str, accountType='page') -> str:
        """_summary_
                This method posts a feed to your account by using id and access_token.
                ##(If you have multiple pages or you want to post on multiple pages use PostTextToMutlipleFeeds)
        Args:
            text (str): The text you want to post on feed.
            id (str): pageId or UserId
            access_token (str): The access token you want to post the feed for.
            accountType (str, optional): page or user. Defaults to 'page'.
        Returns:
            str: PageId/UserId + _ + PostId
        """        
        self.FacebookRequestURL_ = self.FacebookRequestURL.format(id)
        # Facebook Request Payload
        facebook_post_payload = {
            'message': text,
            'access_token': access_token
        }
        self.facebook_resonse = requests.post(self.FacebookRequestURL_, data=facebook_post_payload)
        if self.facebook_resonse.json().get('error', False):
            return self.facebook_resonse.json()
        self.facebook_post_id = self.facebook_resonse.json()['id']
        return f"{id}_{self.facebook_post_id}"
    
    
    def PostVideoFeed(self, text : str, id : str, access_token : str, video_url : str, title='', accountType='page') -> str:
        """_summary_
                This method posts a video feed to your account by using id and access_token.
                ##(If you have multiple pages or you want to post on multiple pages use PostTextToMutlipleFeeds)
        Args:
            text (str): The text you want to post on feed.
            id (str): pageId or UserId
            access_token (str): The access token you want to post the feed for.
            video_url (str) : The video url must be accessible (available to public server) in order to be uploaded.
            title (str, optional) : The title for your video update. If not provided then your text (description) will be used as title for your video upto 250 characters.
            accountType (str, optional): page or user. Defaults to 'page'.
        Returns:
            str: PageId/UserId + _ + PostId
        """    
        self.FacebookVideoUploadURL_ = self.FacebookVideoUploadURL.format(self.version, id)
        facebook_upload_body = {
            'file_url': video_url,
            "description": text,
            "title": title[0:250] if len(title) > 0 else text[0:250],
            'access_token': access_token
        }
        self.facebook_video_resonse = requests.post(self.FacebookVideoUploadURL_, data=facebook_upload_body)
        if self.facebook_video_resonse.json().get('error', False):
            return self.facebook_video_resonse.json()
        facebook_post_id = self.facebook_video_resonse.json()['id']
        return f"{id}_{facebook_post_id}"
    
        
    @staticmethod
    def post_video_facebook(text, video_url, token, page_id, version, url, title) -> str:
        """
        This Function Posts the video to Facebook
        """
        url_ = url.format(version, page_id)
        facebook_upload_body = {
            'file_url': video_url,
            "description": text,
            "title": title[0:250] if len(title) > 0 else text[0:250],
            'access_token': token
        }
        facebook_resonse = requests.post(url_, data=facebook_upload_body)
        if facebook_resonse.json().get('error', False):
            print('-------Facebook Video Post-ERROR-------')
            print(facebook_resonse.json())
            return facebook_resonse.json()
        facebook_post_id = facebook_resonse.json()['id']
        print('-------Facebook Video Post-DONE-------')
        return facebook_post_id


    def PostToFacebook(self, text : str, media_urls : Union[list[str], str], access_token : str, id : str, isVideo : bool, title='') -> str:
        """_summary_

        Args:
            text (str): The text you want to post on feed.
            urls (Union[list[str], str]): The media url must be accessible (available to public server) in order to be uploaded.
            token (str): The access token you want to post the feed for.
            id (str): pageId or UserId
            isVideo (bool): If True the method will upload the media as Video (Can get an error if the media type is not video)
            title (str, optional) : The title for your video update. If not provided then your text (description) will be used as title for your video upto 250 characters.

        Returns:
            str: string of PostID
        """ 
        if type(media_urls) == str:
            if ',' not in media_urls:
                urls_ = []
                urls_.append(media_urls)
            else:
                media_urls = media_urls.replace(' ', '').split(',')   
                urls_ = []
                urls_.append(media_urls)   
        if isVideo:
            self.post_id = self.post_video_facebook(text, urls_[0], access_token, id, self.version, self.FacebookVideoUploadURL, title)
        else:
            medias = [{'media_fbid': self.facebook_upload(
                url, access_token, id, self.version, self.FacebookPhotoUploadURL)} for url in urls_]
            for media in medias:
                if type(media['media_fbid']) == dict:
                    return {'message': media['media_fbid'].get('error', {}).get('message', 'Some Error Occured')}
            self.post_id = self.post_facebook(text, medias, access_token, id, self.FacebookFeedURL)
        if type(self.post_id) == dict:
            return {'message': self.post_id.get('error', {}).get('message', 'Some Error Occured')}
        return f"{id}_{self.post_id}"

    @staticmethod
    def facebook_upload(img, token, id, version, photouploadUrl) -> str:
        url = photouploadUrl.format(version, id)
        facebook_upload_body = {
            'url': img,
            'published': 'false',
            'access_token': token
        }
        facebook_image_response = requests.post(url, data=facebook_upload_body)
        if facebook_image_response.json().get('error', False):
            return facebook_image_response.json()
        id = facebook_image_response.json()['id']
        return id
    
    @staticmethod
    def post_facebook(text, media, token, page_id, facebook_request_url) -> str:
        """
        This Function Posts the data to Facebook
        """
        url = facebook_request_url.format(page_id)
        facebook_post_payload = {
            'message': text,
            'access_token': token
        }
        if len(media) > 0:
            facebook_post_payload.update({
                'attached_media': json.dumps(media),
            })
        facebook_resonse = requests.post(url, data=facebook_post_payload)
        if facebook_resonse.json().get('error', False):
            return facebook_resonse.json()
        facebook_post_id = facebook_resonse.json()['id']
        return facebook_post_id