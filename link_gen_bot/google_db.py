from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from private.data import CREDENTIALS_FILE, spreadsheet_id


credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# example of read of google spreadsheets
def read():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Sheet2!A1:A1',
        majorDimension='COLUMNS'
    ).execute()
    return values

# example of write to google spreadsheets
def write(num):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": "Sheet2!A1:A1",
                "majorDimension": "ROWS",
                "values": [[num]]},
        ]
        }
    ).execute()

def get_value():
    read_res = read()
    token = int(read_res["values"][0][0])
    write(token + 1)
    return token