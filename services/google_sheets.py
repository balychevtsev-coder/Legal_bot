import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

class GoogleSheetService:
    def __init__(self, creds_path, spreadsheet_id):
        # Настройка доступа
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        try:
            # Авторизация
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
            self.client = gspread.authorize(self.creds)
            # Открытие таблицы по ID
            self.spreadsheet = self.client.open_by_key(spreadsheet_id)
            print("✅ Успешное подключение к Google Sheets")
        except Exception as e:
            print(f"❌ Ошибка подключения к Google Sheets: {e}")
            raise e

    def log_to_sheets(self, user_data: list):
        """Записывает данные в первый лист (обычно это логи или записи)"""
        try:
            # .sheet1 — это самый первый (левый) лист в таблице
            sheet = self.spreadsheet.sheet1
            sheet.append_row(user_data)
        except Exception as e:
            print(f" Ошибка при записи лога: {e}")

    def get_faq_data(self):
        """Получает данные из листа с названием 'FAQ'"""
        try:
            worksheet = self.spreadsheet.worksheet("FAQ")
            # Возвращает список словарей, где ключи — это заголовки первой строки
            return worksheet.get_all_records()
        except gspread.exceptions.WorksheetNotFound:
            print("❌ Ошибка: Лист с названием 'FAQ' не найден в таблице!")
            return []
        except Exception as e:
            print(f"❌ Ошибка при получении FAQ: {e}")
            return []

def log_to_sheets(user_data: list):
    service = GoogleSheetService(config.GOOGLE_CREDS_PATH, config.SPREADSHEET_ID)
    service.log_to_sheets(user_data)