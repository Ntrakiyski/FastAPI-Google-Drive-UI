import reflex as rx


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("folder-kanban", class_name="w-8 h-8 text-teal-600"),
            rx.el.h1(
                "Drive Explorer",
                class_name="text-2xl font-bold text-gray-800 font-['Lora']",
            ),
            class_name="flex items-center gap-3 p-4",
        ),
        class_name="w-full md:w-64 bg-white border-r border-gray-200",
    )