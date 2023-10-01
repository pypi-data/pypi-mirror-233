import os
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from movva_tools.constants import GoogleSheets


# If modifying these scopes, delete the file token.json.
SCOPES = GoogleSheets.READ_ONLY_SCOPE


class GoogleSheetsIntegration:

    def __init__(self, link, spreadsheet_page, creds_path):
        self.__link = link
        self.spreadsheet_page = spreadsheet_page
        self.__creds_path = creds_path
        self.service = None
        self.__spreadsheet_id = None

    def check_data(self):
        """
            Verifica se as informações necessárias para a classe
            foram informadas.
        """
        if not self.__link or not self.__spreadsheet_id or not self.spreadsheet_page:
            raise Exception('The spreadsheet link, name and id must be informed')

    def __extract_id_from_google_sheets_link(self):
        """
            Extrai o id do link da planilha do Google através do
            padrão de expressão regular
        """

        pattern = r'/d/([a-zA-Z0-9-_]+)'

        # Procura pelo padrão no link fornecido
        match = re.search(pattern, self.__link)

        # Se houver uma correspondência, retorna o ID encontrado, caso contrário, retorna None
        if match:
            return match.group(1)
        else:
            raise Exception('Planilha não encontrada.')

    def __authorize_google_sheets(self):
        """
            Cria/carrega credenciais de acesso da API do Google Sheets
            e inicia a conexão com a API.
        """
        creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        token_path = os.environ.get('TOKEN_PRODUCTION_PATH', '')
        if not token_path:
            token_path = os.environ.get('TOKEN_LOCAL_PATH', '')

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__creds_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            print('Openning token.json file...')
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Create Google Sheets connection
        service = build('sheets', 'v4', credentials=creds)

        return service

    def read_sheet_data(self, end_selection: str = None) -> list:
        """
            Lê e armazena em uma estrutura de listas o conteúdo da planilha.
        """

        self.__spreadsheet_id = self.__extract_id_from_google_sheets_link()

        self.check_data()

        self.service = self.__authorize_google_sheets()

        # Call the Sheets API
        end_selection = end_selection if end_selection else 'BZ'
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.__spreadsheet_id,
            range=f'{self.spreadsheet_page}!A1:{end_selection}'
        ).execute()

        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        return values
