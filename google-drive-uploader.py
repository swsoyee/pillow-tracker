from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import argparse

print('Begin authentication')
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resultFolderId')
args = parser.parse_args()

file_list = drive.ListFile({
    'q':
    "'%s' in parents and trashed=false" % args.resultFolderId
}).GetList()

upload_file_list = ["sessions.csv", "stages.csv"]

# If there are not file `sessions.csv` and `stages.csv` in your folder,
# you could create an empty file for initiation.

for drive_file in file_list:
    for upload_file in upload_file_list:
        if drive_file['title'] == upload_file:
            file_local = drive.CreateFile({'id': drive_file['id']})
            file_local.SetContentFile(upload_file)
            file_local.Upload()
            print("`%s` has been updated." % upload_file)
            break
