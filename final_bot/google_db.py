from pprint import pprint
from private.data import CREDENTIALS_FILE, spreadsheet_id

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

def get_data():
    # Auth and getting service
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A:E',
        majorDimension='ROWS'
    ).execute()
    return values["values"][1:]

# MAIN: Append to google spreadsheets
def append(values):
    # Auth and getting service
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

    # needed arguments
    RANGE_ARG = "Sheet1!A2:B2"
    VALUE_I_OPTION = "USER_ENTERED"
    INSERT_D_OPTION = "INSERT_ROWS"
    BODY_ARG = {"values": values} # argument in append function

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, 
            range=RANGE_ARG, valueInputOption=VALUE_I_OPTION, 
            insertDataOption=INSERT_D_OPTION, body=BODY_ARG).execute()