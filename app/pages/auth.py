import reflex as rx
from app.states.auth_state import AuthState
from app.states.legal_state import LegalState


def legal_card(title: str, content_component: rx.Component) -> rx.Component:
    """Standard layout for legal views."""
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.icon("arrow-left", class_name="h-4 w-4"),
                    rx.el.span(
                        "Voltar para o Login", class_name="font-semibold"
                    ),
                    class_name="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors mb-6",
                ),
                on_click=LegalState.show_login,
            ),
            rx.el.h1(title, class_name="text-3xl font-bold text-gray-900 mb-2"),
            rx.el.p(
                "Última atualização: 20 de Maio de 2024",
                class_name="text-gray-500 text-sm mb-8",
            ),
            content_component,
            class_name="bg-white p-8 md:p-12 rounded-3xl border border-gray-100 shadow-sm w-full max-w-4xl",
        ),
        class_name="flex items-center justify-center min-h-screen p-4 bg-gray-50",
    )


def privacy_content() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            rx.el.h2(
                "1. Coleta de Dados",
                class_name="text-xl font-bold text-gray-800 mb-4",
            ),
            rx.el.p(
                "O Gestão Markup coleta informações essenciais para o cálculo de rentabilidade do motorista de aplicativo. Ao utilizar nossa plataforma via login local ou Google OAuth, armazenamos seu nome, e-mail e identificadores únicos de sessão.",
                class_name="text-gray-600 mb-4",
            ),
            class_name="mb-10",
        ),
        rx.el.section(
            rx.el.h2(
                "2. Security",
                class_name="text-xl font-bold text-gray-800 mb-4",
            ),
            rx.el.p(
                "Suas senhas são criptografadas utilizando algoritmos de hashing robustos (bcrypt). Mantemos seus dados enquanto sua conta estiver ativa.",
                class_name="text-gray-600 mb-4",
            ),
            class_name="mb-10",
        ),
    )


def terms_content() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            rx.el.h2(
                "1. Aceite dos Termos",
                class_name="text-xl font-bold text-gray-800 mb-4",
            ),
            rx.el.p(
                "Ao acessar o Gestão Markup, você concorda em cumprir estes termos de serviço. Esta ferramenta foi desenvolvida exclusivamente para auxiliar motoristas de aplicativo na gestão de seus custos operacionais.",
                class_name="text-gray-600 mb-4",
            ),
            class_name="mb-10",
        ),
        rx.el.section(
            rx.el.h2(
                "2. Isenção de Responsabilidade",
                class_name="text-xl font-bold text-gray-800 mb-4",
            ),
            rx.el.p(
                "Os cálculos de Markup são estimativas baseadas nos dados fornecidos pelo usuário. O Gestão Markup não garante lucros específicos.",
                class_name="text-gray-600 mb-4",
            ),
            class_name="mb-10",
        ),
    )


def login_form() -> rx.Component:
    """The standard login card component."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "trending-up", class_name="h-10 w-10 text-blue-600 mb-2"
                ),
                rx.el.h1(
                    "Gestão Markup",
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.el.p(
                    "Entre para gerenciar sua lucratividade",
                    class_name="text-gray-500 mt-2",
                ),
                class_name="text-center mb-8",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Usuário",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="username",
                        placeholder="Seu usuário",
                        class_name="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all mb-4",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Senha",
                        class_name="block text-sm font-semibold text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        type="password",
                        name="password",
                        placeholder="••••••••",
                        class_name="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all mb-6",
                    ),
                ),
                rx.el.button(
                    "Entrar",
                    type="submit",
                    class_name="w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl",
                ),
                on_submit=AuthState.handle_login,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "ou",
                        class_name="px-2 bg-white text-gray-500 font-medium",
                    ),
                    class_name="relative flex justify-center text-sm mt-8 mb-8 before:absolute before:inset-0 before:top-1/2 before:h-px before:w-full before:bg-gray-200 before:z-[-1]",
                ),
                rx.el.button(
                    rx.icon("omega", class_name="h-5 w-5"),
                    rx.el.span(
                        "Entrar com Google",
                        class_name="text-gray-700 font-bold",
                    ),
                    on_click=AuthState.init_google_oauth,
                    class_name="w-full bg-white border border-gray-200 py-3 rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all shadow-sm flex items-center justify-center gap-2",
                ),
            ),
            rx.el.div(
                rx.el.a(
                    "Esqueceu a senha?",
                    href="/recuperar-senha",
                    class_name="text-sm text-blue-600 hover:underline",
                ),
                rx.el.div(
                    rx.el.span(
                        "Não tem uma conta? ",
                        class_name="text-sm text-gray-500",
                    ),
                    rx.el.a(
                        "Cadastre-se",
                        href="/registrar",
                        class_name="text-sm text-blue-600 font-semibold hover:underline",
                    ),
                    class_name="mt-4",
                ),
                rx.el.div(
                    rx.el.a(
                        "Termos",
                        href="/termos",
                        class_name="text-xs text-gray-400 hover:text-blue-600 transition-colors",
                    ),
                    rx.el.span(" • ", class_name="text-gray-300"),
                    rx.el.a(
                        "Privacidade",
                        href="/privacidade",
                        class_name="text-xs text-gray-400 hover:text-blue-600 transition-colors",
                    ),
                    class_name="mt-8 flex justify-center gap-2",
                ),
                class_name="mt-6 text-center",
            ),
            class_name="bg-white p-10 rounded-3xl shadow-xl border border-gray-100 w-full max-w-md",
        ),
        class_name="flex items-center justify-center min-h-screen p-4 bg-gray-50",
    )


def login_page() -> rx.Component:
    """Public entry page that handles safe legal views."""
    return rx.el.div(
        rx.match(
            LegalState.current_view,
            ("terms", legal_card("Termos de Uso", terms_content())),
            (
                "privacy",
                legal_card("Política de Privacidade", privacy_content()),
            ),
            login_form(),
        ),
        class_name="font-['Inter']",
    )


# Legacy direct pages as fallback
def privacy_policy_page() -> rx.Component:
    return legal_card("Política de Privacidade", privacy_content())


def terms_of_service_page() -> rx.Component:
    return legal_card("Termos de Uso", terms_content())


def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Criar Conta",
                    class_name="text-2xl font-bold text-gray-900 text-center mb-8",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Nome de Usuário",
                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="username",
                            placeholder="Escolha um usuário",
                            class_name="w-full px-4 py-3 border border-gray-200 rounded-xl mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "E-mail",
                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="email",
                            type="email",
                            placeholder="seu@email.com",
                            class_name="w-full px-4 py-3 border border-gray-200 rounded-xl mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Senha",
                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="password",
                            type="password",
                            placeholder="Mínimo 6 caracteres",
                            class_name="w-full px-4 py-3 border border-gray-200 rounded-xl mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Confirmar Senha",
                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="confirm_password",
                            type="password",
                            placeholder="Repita a senha",
                            class_name="w-full px-4 py-3 border border-gray-200 rounded-xl mb-6",
                        ),
                    ),
                    rx.el.button(
                        "Registrar",
                        type="submit",
                        class_name="w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition-all shadow-md",
                    ),
                    on_submit=AuthState.handle_register,
                ),
                rx.el.div(
                    rx.el.a(
                        "Voltar para login",
                        href="/",
                        class_name="text-sm text-blue-600 font-semibold hover:underline",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Ao registrar, você concorda com nossos ",
                            class_name="text-xs text-gray-400",
                        ),
                        rx.el.a(
                            "Termos",
                            href="/termos",
                            class_name="text-xs text-blue-500 hover:underline",
                        ),
                        rx.el.span(" e ", class_name="text-xs text-gray-400"),
                        rx.el.a(
                            "Privacidade",
                            href="/privacidade",
                            class_name="text-xs text-blue-500 hover:underline",
                        ),
                        class_name="mt-8",
                    ),
                    class_name="mt-6 text-center",
                ),
                class_name="bg-white p-10 rounded-3xl shadow-xl border border-gray-100 w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-screen p-4 bg-gray-50",
        ),
        class_name="font-['Inter']",
    )


def google_callback_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "loader", class_name="h-10 w-10 text-blue-600 animate-spin mb-4"
            ),
            rx.el.h2(
                "Processando login com Google...",
                class_name="text-xl font-bold text-gray-900",
            ),
            class_name="flex flex-col items-center justify-center bg-white p-10 rounded-3xl shadow-xl border border-gray-100",
        ),
        class_name="flex items-center justify-center min-h-screen p-4 bg-gray-50 font-['Inter']",
    )


def recover_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Recuperar Senha",
                    class_name="text-2xl font-bold text-gray-900 mb-4",
                ),
                rx.el.div(
                    rx.icon(
                        "info",
                        class_name="h-12 w-12 text-blue-500 mb-4 mx-auto",
                    ),
                    rx.el.p(
                        "A recuperação de senha estará disponível em breve.",
                        class_name="text-gray-600 mb-6 text-center",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Voltar para Login",
                            class_name="w-full bg-gray-100 text-gray-700 font-bold py-3 rounded-xl hover:bg-gray-200 transition-all",
                        ),
                        href="/",
                    ),
                    class_name="text-center",
                ),
                class_name="bg-white p-10 rounded-3xl shadow-xl border border-gray-100 w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-screen p-4 bg-gray-50",
        ),
        class_name="font-['Inter']",
    )