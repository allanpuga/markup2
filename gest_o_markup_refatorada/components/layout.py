import reflex as rx
from gest_o_markup_refatorada.components.sidebar import sidebar
from gest_o_markup_refatorada.states.auth_state import AuthState


def base_layout(content: rx.Component, route: str) -> rx.Component:
    """Standard layout for authenticated pages."""
    return rx.el.div(
        sidebar(route),
        rx.el.main(
            rx.el.div(content, class_name="max-w-6xl mx-auto"),
            class_name="ml-64 p-8 min-h-screen bg-gray-50",
        ),
        class_name="min-h-screen font-['Inter']",
    )