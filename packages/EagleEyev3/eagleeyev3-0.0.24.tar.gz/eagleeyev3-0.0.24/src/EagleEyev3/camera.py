
import json
import logging
import requests

from datetime import datetime, timedelta
from pytz import timezone

from io import BytesIO

logging.basicConfig(level=logging.INFO)


from EagleEyev3.device import Device



class Camera(Device):

    def __init__(self, id=None, name=None, status=dict(), account_id=None, bridge_id=None, user_base_url=None, een_instance=None):
        super().__init__(id=id, name=name, status=status, account_id=account_id, user_base_url=user_base_url, een_instance=een_instance)
        self.bridge_id = bridge_id
        self.previews = []
        self.videos = []
        self.events = {
                'status': [],
                'motion': []
                }
        
    def get_list_of_events(self, start_timestamp=None, end_timestamp=None):
        """
        Obtains the list of events.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """

        if start_timestamp == None or end_timestamp == None:
            logging.warn(f"get_list_of_events called without timestamp")
            return {
                "success": False,
                "response_http_status": None,
                "data": { 'msg': 'get_list_of_events called without required args, needs start_timestamp, end_timestamp' }
            }

        url = f"https://{self.user_base_url}/api/v3.0/events?pageSize=100&include=een.deviceCloudStatusUpdate.v1&startTimestamp__gte={start_timestamp}&endTimestamp__lte={end_timestamp}&actor=camera%3A{self.id}&type__in=een.deviceCloudStatusUpdateEvent.v1"

        headers = { 
                    "Authorization": f"Bearer {self.een_instance.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self.een_instance._get_timeout_values('list_of_events'))
            response_json = response.json()

            logging.debug(f"{response.status_code} returned from {url} with {headers} and {response.text}")
            logging.info(f"{response.status_code} in get_list_of_events")

            if response.status_code == 200:
                success = True
                # filter events by type
                [self.events['status'].append(i) for i in response.json()['results'] if i['type'] == 'een.deviceCloudStatusUpdateEvent.v1']
                [self.events['motion'].append(i) for i in response.json()['results'] if i['type'] == 'een.motionDetectionEvent.v1']

                # remove duplicates
                seen = set()
                self.events['status'] = [event for event in self.events['status'] if event['id'] not in seen and not seen.add(event['id'])]

                seen = set()
                self.events['motion'] = [event for event in self.events['motion'] if event['id'] not in seen and not seen.add(event['id'])]

                # sort by event startTimestamp descending
                self.events['status'] = sorted(self.events['status'], key=lambda x: x['startTimestamp'], reverse=True)
                self.events['motion'] = sorted(self.events['motion'], key=lambda x: x['startTimestamp'], reverse=True)
            else:
                success = False

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {self.id} get_list_of_events()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }
            

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_live_preview(self):

        url = f"https://{self.user_base_url}/api/v3.0/media/liveImage.jpeg?deviceId={self.id}&type=preview"

        headers = { 
                    "Authorization": f"Bearer {self.een_instance.access_token}", 
                    "Accept": "image/jpeg"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self.een_instance._get_timeout_values('live_preview'))
            logging.info(f"{response.status_code} in get_live_preview")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {self.id} get_live_preview()")
            response = None
        
        except requests.exceptions.RequestException as e:
            logging.warn(e)
            response = None
        
        return response

    def get_list_of_videos(self, start_timestamp=None, end_timestamp=None, stream_type='main', media_type='video', coalesce='true', include=['mp4Url']):
        """
        Obtains the list of videos.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        nextPageToken = None
        include_str = ','.join(include)

        if start_timestamp == None or end_timestamp == None:
            logging.warn(f"get_list_of_videos called without timestamps")
            return {
                "success": False,
                "response_http_status": None,
                "data": { 'msg': 'get_list_of_videos called without required args, needs start_timestamp, end_timestamp' }
            }

        # emulating a do while toop in order to handle pagination, remember to break out of this loop
        while True:

            if nextPageToken:
                url = f"https://{self.user_base_url}/api/v3.0/media?deviceId={self.id}&type={stream_type}&mediaType={media_type}&startTimestamp__gte={start_timestamp}&coalesce={coalesce}&include={include_str}&pageToken={nextPageToken}"
            else:
                url = f"https://{self.user_base_url}/api/v3.0/media?deviceId={self.id}&type={stream_type}&mediaType={media_type}&startTimestamp__gte={start_timestamp}&coalesce={coalesce}&include={include_str}"


            headers = { 
                        "Authorization": f"Bearer {self.een_instance.access_token}", 
                        "Accept": "application/json"
                    }

            response = self.een_instance._make_get_request(url=url, headers=headers, timeout='list_of_videos')

            if response:
                response_json = response.json()

                logging.info(f"{response.status_code} in get_list_of_videos")

            else:
                return {
                    "success": False,
                    "response_http_status": 0,
                    "data": None
                }


            if response.status_code == 200:
                success = True
                self.videos = [i for i in response_json['results'] if i['startTimestamp'] not in [j['startTimestamp'] for j in self.videos]] + self.videos

                # sort by event startTimestamp descending
                self.videos = sorted(self.videos, key=lambda x: x['startTimestamp'], reverse=True)

                if 'nextPageToken' in response_json and len(response_json['nextPageToken']) > 0:
                    nextPageToken = response_json['nextPageToken']
                else:
                    break

            else:
                success = False
                break


        dups = {}
        for video in self.videos:
            if video['endTimestamp'] in dups:
                dups[video['endTimestamp']] = dups[video['endTimestamp']] + 1
                logging.debug(f"found duplicate endTimestamp: { video['endTimestamp'] }")
            else:
                dups[video['endTimestamp']] = 1

        logging.debug(dups)

        self.videos = [i for i in self.videos if dups[i['endTimestamp']] == 1]
        self.videos = sorted(self.videos, key=lambda x: x['startTimestamp'], reverse=True)

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": self.videos
        }

    def save_video_to_file(self, url=None, filename=None):

        success = False
        status_code = None
        data = {}

        if url == None or filename == None:
            logging.warn("save_video_to_file called without url and/or filename")
            
            data = { 'message': 'save_video_to_file called without url and/or filename' }

            return {
                "success": success,
                "response_http_status": status_code,
                "data": data
            }

        
        headers = { 
                    "Authorization": f"Bearer {self.een_instance.access_token}"
                }

        try:
            with requests.get(url, stream=True, headers=headers, timeout=self.een_instance._get_timeout_values('recorded_video')) as response:
                status_code = response.status_code
                logging.info(f"{response.status_code} in save_video_to_file")
                with open(filename, 'wb') as fname:
                    for chunk in response.iter_content(chunk_size=8192):
                        fname.write(chunk)

                    success = True
                    data = { 'message': f"video saved as {fname}" }


        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {url} save_video_to_file")
            data = { 'message': f"timeout expired for {url} save_video_to_file" }
        
        except requests.exceptions.RequestException as e:
            logging.warn(e)
            data = { 'message': "Exception {e} in save_video_to_file" }
        
        return {
            "success": success,
            "response_http_status": status_code,
            "data": data
        }













