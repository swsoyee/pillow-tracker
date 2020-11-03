pip3 install setuptools
pip3 install -r requirements.txt
echo $CREDENTIALS >> credentials.json
echo client_config:'\n  'client_id: $CLIENT_ID'\n  'client_secret: $CLIENT_SECRET >> settings.yaml
python3 google-drive-downloader.py -i $SOURCE_FOLDER_ID
python3 parser.py
python3 google-drive-uploader.py -r $RESULT_FOLDER_ID
