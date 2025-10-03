import reflex as rx
from app.state import AppState
from app.components.sidebar import sidebar
from app.components.file_browser import file_browser


def auth_landing() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Connect to Google Drive",
            class_name="text-2xl font-bold text-gray-800 mb-4 font-['Lora']",
        ),
        rx.el.p(
            "To view your files, please authenticate with your Google account.",
            class_name="text-gray-600 mb-8 max-w-md text-center",
        ),
        rx.el.button(
            rx.icon("link", class_name="mr-2"),
            "Connect to Google Drive",
            on_click=AppState.init_auth,
            is_loading=AppState.is_loading,
            class_name="bg-teal-600 text-white px-6 py-3 rounded-lg hover:bg-teal-700 transition-colors flex items-center font-medium shadow-sm",
        ),
        rx.cond(
            AppState.auth_error != "",
            rx.el.div(
                rx.el.p(
                    "Authentication Error:", class_name="font-semibold text-red-600"
                ),
                rx.el.p(AppState.auth_error, class_name="text-red-500 text-sm"),
                rx.el.p(
                    "Please make sure you have a `credentials.json` file in your project root and have enabled the Google Drive API.",
                    class_name="text-gray-500 text-xs mt-2",
                ),
                class_name="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg",
            ),
        ),
        class_name="flex flex-col items-center justify-center text-center p-8",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.cond(AppState.is_authenticated, file_browser(), auth_landing()),
                rx.cond(
                    AppState.is_loading,
                    rx.el.div(
                        rx.el.div(
                            class_name="animate-pulse bg-gray-200 h-12 w-full rounded-lg mb-6"
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="animate-pulse bg-gray-200 h-16 rounded-lg"
                            ),
                            rx.el.div(
                                class_name="animate-pulse bg-gray-200 h-16 rounded-lg"
                            ),
                            rx.el.div(
                                class_name="animate-pulse bg-gray-200 h-16 rounded-lg"
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
                        ),
                        class_name="w-full",
                    ),
                ),
                class_name="p-4 sm:p-6 md:p-8 w-full",
            ),
            class_name="flex-1 bg-gray-50 min-h-screen",
        ),
        class_name="flex flex-col md:flex-row min-h-screen bg-white font-['Lora']",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, title="Drive Explorer", on_load=AppState.on_load)