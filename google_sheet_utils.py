import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient .discovery import build
from googleapiclient.errors import HttpError


credential_path = os.path.join(os.path.dirname(__file__), 'config', 'credential.json')
class GoogleSheetUtils:

    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        self.SPREADSHEET_ID = "1DoZMfiR7-OqDqPlfH61e41aXT4BzHuUZmjSFt1AWTxA"
        

    def sent_details_to_sheet(self,details,date):
        self.work_details = details
        self.date = date
        credentials = None

        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json",self.SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credential_path,self.SCOPES)
                credentials = flow.run_local_server(port=0)
            with open("token.json","w") as token:
                token.write(credentials.to_json())
        
        try:
            service =build("sheets", "v4", credentials=credentials)
            sheets = service.spreadsheets()

            # for work in self.work_details:
            #     print(work)

            result = service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, range=f"Sheet1!A:A").execute()

            starting_row_num = len(result.get("values", [])) + 1
            last_row = starting_row_num +  len(self.work_details)

            sum_range = f"B{starting_row_num}:B{last_row-1}"

            request_body = {"values": [["=SUM(" + sum_range + ")"]]}

            # work =self.work_details

            for i, (key, value) in enumerate(self.work_details.items(), start=starting_row_num):
                print(f"Processing {key}: {value}")

                sheets.values().update(spreadsheetId=self.SPREADSHEET_ID,range=f"Sheet1!A{i}",
                                        valueInputOption="USER_ENTERED",body={"values": [["home screen" if key == '' else key]]}).execute()
                time = self.seconds_to_hh_mm_ss(value)
                sheets.values().update(spreadsheetId=self.SPREADSHEET_ID,range=f"Sheet1!B{i}",
                                        valueInputOption="USER_ENTERED",body={"values": [[time]]}).execute()
                
            sheets.values().update(spreadsheetId=self.SPREADSHEET_ID,range=f"Sheet1!A{last_row}",
                                        valueInputOption="USER_ENTERED",body={"values": [["Total Hour"]]}).execute()
            sheets.values().update(spreadsheetId=self.SPREADSHEET_ID,range=f"Sheet1!B{last_row}",
                                        valueInputOption="USER_ENTERED",body=request_body).execute()
            sheets.values().update(spreadsheetId=self.SPREADSHEET_ID,range=f"Sheet1!C{last_row}",
                                        valueInputOption="USER_ENTERED",body={"values": [[self.date]]}).execute()
        
        except HttpError as error :
            print(error)
            pass

    def seconds_to_hh_mm_ss(self,seconds):
        # Calculate hours, minutes, and seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        # Format the result as HH:MM:SS
        time_format = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return time_format

