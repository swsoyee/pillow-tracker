from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import argparse

print('Begin authentication')
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--folderId')
args = parser.parse_args()

file_list = drive.ListFile({
    'q':
    "'%s' in parents and trashed=false" % args.folderId
}).GetList()

for drive_file in file_list:
    if drive_file['title'] == 'PillowData.txt':
        file_local = drive.CreateFile({'id': drive_file['id']})
        file_local.GetContentFile('PillowData.txt')
        print('Download `PillowData.txt` to local has been successed.')
        break
