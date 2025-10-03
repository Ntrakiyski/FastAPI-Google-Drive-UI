import reflex as rx
import os
import pickle
import logging
from typing import TypedDict, Literal
from collections import defaultdict
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


class GoogleFile(TypedDict):
    id: str
    name: str
    mimeType: str
    modifiedTime: str
    iconLink: str


class AppState(rx.State):
    files: list[GoogleFile] = []
    categorized_files: dict[str, list[GoogleFile]] = {"All Files": []}
    is_authenticated: bool = False
    is_loading: bool = False
    active_tab: str = "All Files"
    auth_url: str = ""
    auth_error: str = ""

    @rx.event
    def on_load(self):
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
            if creds and creds.valid:
                self.is_authenticated = True
                return AppState.fetch_files
            elif creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open("token.pickle", "wb") as token:
                    pickle.dump(creds, token)
                self.is_authenticated = True
                return AppState.fetch_files
        return AppState.init_auth

    @rx.event
    def init_auth(self):
        self.is_loading = True
        self.auth_error = ""
        try:
            if not os.path.exists("credentials.json"):
                self.auth_error = (
                    "credentials.json not found. Please follow the setup instructions."
                )
                self.is_loading = False
                return
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
            self.is_authenticated = True
            self.is_loading = False
            return AppState.fetch_files
        except Exception as e:
            logging.exception(f"Authentication failed: {e}")
            self.auth_error = f"Authentication failed: {e}"
            self.is_loading = False

    @rx.event(background=True)
    async def fetch_files(self):
        async with self:
            if not self.is_authenticated:
                return
            self.is_loading = True
            creds = None
            if os.path.exists("token.pickle"):
                with open("token.pickle", "rb") as token:
                    creds = pickle.load(token)
        if creds and creds.valid:
            try:
                service = build("drive", "v3", credentials=creds)
                results = (
                    service.files()
                    .list(
                        pageSize=100,
                        fields="nextPageToken, files(id, name, mimeType, modifiedTime, iconLink)",
                    )
                    .execute()
                )
                items = results.get("files", [])
                async with self:
                    self.files = [
                        GoogleFile(
                            id=item["id"],
                            name=item["name"],
                            mimeType=item.get("mimeType", "unknown"),
                            modifiedTime=item.get("modifiedTime", "unknown"),
                            iconLink=item.get("iconLink", ""),
                        )
                        for item in items
                    ]
                    self._categorize_files()
                    self.is_loading = False
            except Exception as e:
                logging.exception(f"Failed to fetch files: {e}")
                async with self:
                    self.auth_error = f"Failed to fetch files: {e}"
                    self.is_loading = False
        else:
            async with self:
                self.is_authenticated = False
                self.is_loading = False

    def _categorize_files(self):
        categories = defaultdict(list)
        mime_type_map = {
            "application/pdf": "PDFs",
            "image/jpeg": "Images",
            "image/png": "Images",
            "image/gif": "Images",
            "image/svg+xml": "Images",
            "application/vnd.google-apps.document": "Google Docs",
            "application/vnd.google-apps.spreadsheet": "Google Sheets",
            "application/vnd.google-apps.presentation": "Google Slides",
            "application/vnd.google-apps.form": "Google Forms",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Word",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "Excel",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": "PowerPoint",
            "video/mp4": "Videos",
            "video/quicktime": "Videos",
            "video/x-msvideo": "Videos",
            "audio/mpeg": "Audio",
            "audio/wav": "Audio",
            "text/plain": "Text",
            "application/zip": "Archives",
            "application/x-rar-compressed": "Archives",
        }
        for file in self.files:
            category = mime_type_map.get(file["mimeType"], "Other")
            categories[category].append(file)
        self.categorized_files = {
            "All Files": self.files,
            **dict(sorted(categories.items())),
        }

    @rx.var
    def get_tabs(self) -> list[str]:
        return list(self.categorized_files.keys())

    @rx.event
    def set_active_tab(self, tab: str):
        self.active_tab = tab