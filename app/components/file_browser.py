import reflex as rx
from app.state import AppState, GoogleFile


def file_card(file: GoogleFile) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(src=file["iconLink"], class_name="w-5 h-5"),
            rx.el.p(
                file["name"], class_name="text-sm font-medium text-gray-800 truncate"
            ),
            class_name="flex items-center gap-3",
        ),
        rx.el.p(
            f"Modified: {file['modifiedTime'].to_string().split('T')[0]}",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex items-center justify-between p-3 border border-gray-100 rounded-lg hover:bg-gray-50 hover:shadow-sm transition-all duration-200",
    )


def file_browser() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    AppState.get_tabs,
                    lambda tab: rx.el.button(
                        tab,
                        on_click=lambda: AppState.set_active_tab(tab),
                        class_name=rx.cond(
                            AppState.active_tab == tab,
                            "px-4 py-2 text-sm font-medium text-teal-700 bg-teal-50 border border-teal-200 rounded-lg",
                            "px-4 py-2 text-sm font-medium text-gray-600 border border-transparent rounded-lg hover:bg-gray-100",
                        ),
                    ),
                ),
                class_name="flex flex-wrap items-center gap-2 p-2 bg-gray-50 rounded-lg border border-gray-200",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.foreach(AppState.categorized_files[AppState.active_tab], file_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
        ),
        rx.cond(
            AppState.files.length() == 0,
            rx.el.div(
                rx.el.p(
                    "No files found in your Google Drive.", class_name="text-gray-500"
                ),
                class_name="flex items-center justify-center p-10 border-2 border-dashed border-gray-200 rounded-lg",
            ),
        ),
        class_name="w-full",
    )