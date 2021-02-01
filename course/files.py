import mimetypes
import os
from io import BytesIO, FileIO
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload, MediaFileUpload
from dateutil.parser import parse
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDriveStorage:
    GOOGLE_DRIVE_FOLDER_MIMETYPE = "application/vnd.google-apps.folder"
    UNKNOWN_MIMETYPE = "application/octet-stream"

    def __init__(self):
        self.json_keyfile_path = settings.GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.json_keyfile_path,
            scopes=["https://www.googleapis.com/auth/drive"],
        )

        self.drive_service = build('drive', 'v3', credentials=credentials, cache_discovery=False)

    def split_path(self, p):  # dzieli sciezke na liste poszczegolnych folderow i nazwe pliku
        p = p[1:] if p[0] == '/' else p
        a, b = os.path.split(p)
        return (self.split_path(a) if len(a) and len(b) else []) + [b]

    def check_file_exists(self, filename, parent_id=None):
        if len(filename) == 0:
            return self.drive_service.files().get(fileId='root').execute()
        else:
            split_filename = self.split_path(filename)
            if len(split_filename) > 1:
                q = "mimeType = '{0}' and name = '{1}'".format(self.GOOGLE_DRIVE_FOLDER_MIMETYPE,
                                                               split_filename[0])
                if parent_id is not None:
                    q = "{0} and '{1}' in parents".format(q, parent_id)
                results = self.drive_service.files().list(q=q, fields="nextPageToken, files(*)").execute()
                items = results.get('files', [])
                for item in items:
                    if item["name"] == split_filename[0]:
                        return self.check_file_exists(os.path.sep.join(split_filename[1:]), item["id"])
                return None
            else:
                q = "name = '{0}'".format(split_filename[0])
                if parent_id is not None:
                    q = "{0} and '{1}' in parents".format(q, parent_id)
                results = self.drive_service.files().list(q=q, fields="nextPageToken, files(*)").execute()
                items = results.get('files', [])
                if len(items) == 0:
                    q = "" if parent_id is None else "'{0}' in parents".format(parent_id)
                    results = self.drive_service.files().list(q=q, fields="nextPageToken, files(*)").execute()
                    items = results.get('files', [])
                    for item in items:
                        if split_filename[0] in item["name"]:
                            return item
                    return None
                else:
                    return items[0]

    def get_or_create_folder(self, path, parent_id=None):

        folder_data = self.check_file_exists(path, parent_id)
        if folder_data is None:

            split_path = self.split_path(path)

            if split_path[:-1]:
                parent_path = os.path.join(*split_path[:-1])
                current_folder_data = self.get_or_create_folder(parent_path, parent_id=parent_id)
            else:
                current_folder_data = None

            meta_data = {
                'name': split_path[-1],
                'mimeType': self.GOOGLE_DRIVE_FOLDER_MIMETYPE
            }
            if current_folder_data is not None:
                meta_data['parents'] = [current_folder_data['id']]
            else:
                if parent_id is not None:
                    meta_data['parents'] = [parent_id]
            current_folder_data = self.drive_service.files().create(body=meta_data).execute()
            return current_folder_data
        else:
            return folder_data

    def open(self, name, name2, mode='rb'):

        file_data = self.check_file_exists(name)

        if file_data is None:
            return "Nie ma!"
        if file_data['mimeType'] == self.GOOGLE_DRIVE_FOLDER_MIMETYPE:
            return "To folder!"
        request = self.drive_service.files().get_media(fileId=file_data['id'])
        # fh = BytesIO()
        fh2 = FileIO(name2, 'wb')
        downloader = MediaIoBaseDownload(fh2, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()
        fh2.seek(0)
        return File(fh2, name)

    def save(self, name, content, path):
        splited = self.split_path(path)
        file_name = splited[-1]
        folder_path = os.path.sep.join(self.split_path(name)[:-1])
        folder_data = self.get_or_create_folder(folder_path)
        parent_id = None if folder_data is None else folder_data['id']
        mime_type = mimetypes.guess_type(name)
        if mime_type[0] is None:
            mime_type = self.UNKNOWN_MIMETYPE
        media_body = MediaFileUpload(path, mimetype=mime_type[0])
        body = {
            'name': file_name,
            'mimeType': mime_type[0]
        }
        if parent_id:
            body['parents'] = [parent_id]
        file_data = self.drive_service.files().create(
            body=body,
            media_body=media_body).execute()

        return file_data.get(u'originalFilename', file_data.get(u'name'))

    def delete(self, name):

        file_data = self.check_file_exists(name)
        if file_data is not None:
            self.drive_service.files().delete(fileId=file_data['id']).execute()

    def exists(self, name):
        return self.check_file_exists(name) is not None

    def url(self, name):

        file_data = self.check_file_exists(name)
        if file_data is None:
            return None
        else:
            return file_data["webViewLink"]

    def listdir(self, path):

        directories, files = [], []
        if path == "/":
            folder_id = {"id": "root"}
        else:
            folder_id = self.check_file_exists(path)
        if folder_id:
            file_params = {
                'q': "'{0}' in parents and mimeType != '{1}'".format(folder_id["id"], self.GOOGLE_DRIVE_FOLDER_MIMETYPE),
            }
            dir_params = {
                'q': "'{0}' in parents and mimeType = '{1}'".format(folder_id["id"], self.GOOGLE_DRIVE_FOLDER_MIMETYPE),
            }
            files_results = self.drive_service.files().list(**file_params).execute()
            dir_results = self.drive_service.files().list(**dir_params).execute()
            files_list = files_results.get('files', [])
            dir_list = dir_results.get('files', [])
            for element in files_list:
                files.append(os.path.join(path, element["name"]))
            for element in dir_list:
                directories.append(os.path.join(path, element["name"]))
        return directories, files
