import reflex as rx
from app.states.auth_state import AuthState
from app.components.layout import base_layout


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
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
                            class_name="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all",
                        ),
                        class_name="mb-4",
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
                            class_name="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none transition-all",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.button(
                        "Entrar",
                        type="submit",
                        class_name="w-full bg-blue-600 text-white font-bold py-3 rounded-xl hover:bg-blue-700 transition-all shadow-lg hover:shadow-xl",
                    ),
                    on_submit=AuthState.handle_login,
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
                    class_name="mt-6 text-center",
                ),
                class_name="bg-white p-10 rounded-3xl shadow-xl border border-gray-100 w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-screen p-4 bg-gray-50",
        ),
        class_name="font-['Inter']",
    )


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
                    class_name="mt-6 text-center",
                ),
                class_name="bg-white p-10 rounded-3xl shadow-xl border border-gray-100 w-full max-w-md",
            ),
            class_name="flex items-center justify-center min-h-screen p-4 bg-gray-50",
        ),
        class_name="font-['Inter']",
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


from app.states.profile_state import ProfileState
from app.states.vehicle_state import VehicleState


def profile_page() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.h1(
                "Perfil do Motorista",
                class_name="text-2xl font-bold text-gray-900 mb-4",
            ),
            rx.el.div(
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Nome completo",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="nome",
                                default_value=ProfileState.nome,
                                placeholder="Seu nome",
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
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
                                default_value=ProfileState.email,
                                placeholder="seu@email.com",
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "WhatsApp",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="whatsapp",
                                default_value=ProfileState.whatsapp,
                                placeholder="(11) 99999-9999",
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Estado",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Selecione um estado", value=""
                                    ),
                                    rx.foreach(
                                        ProfileState.estados,
                                        lambda s: rx.el.option(
                                            s["nome"], value=s["sigla"]
                                        ),
                                    ),
                                    name="estado",
                                    value=ProfileState.estado,
                                    on_change=ProfileState.set_estado,
                                    class_name="w-full px-4 py-2 appearance-none border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Cidade",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Selecione uma cidade", value=""
                                    ),
                                    rx.foreach(
                                        ProfileState.cidades,
                                        lambda c: rx.el.option(c, value=c),
                                    ),
                                    name="cidade",
                                    value=ProfileState.cidade,
                                    on_change=ProfileState.set_cidade,
                                    class_name="w-full px-4 py-2 appearance-none border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none bg-white",
                                    disabled=ProfileState.estado == "",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Dias por semana",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="dias_semana",
                                type="number",
                                min="1",
                                max="7",
                                default_value=ProfileState.dias_semana.to_string(),
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Horas por dia",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="horas_dia",
                                type="number",
                                min="1",
                                max="24",
                                default_value=ProfileState.horas_dia.to_string(),
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Km rodado por dia",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="km_dia",
                                type="number",
                                step="0.1",
                                default_value=ProfileState.km_dia.to_string(),
                                class_name="w-full px-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.cond(
                                ProfileState.is_loading,
                                rx.icon(
                                    "loader", class_name="h-5 w-5 animate-spin"
                                ),
                                "Salvar Perfil",
                            ),
                            type="submit",
                            class_name="bg-blue-600 text-white font-bold py-3 px-8 rounded-xl hover:bg-blue-700 transition-all shadow-md flex items-center justify-center gap-2",
                            disabled=ProfileState.is_loading,
                        ),
                        class_name="mt-8 flex justify-end",
                    ),
                    on_submit=ProfileState.save_profile,
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
            ),
        ),
        "/app/perfil",
    )


def vehicle_card(v: dict):
    is_active = v["id"] == ProfileState.veiculo_ativo_id
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    f"{v['marca']} {v['modelo']}",
                    class_name="text-lg font-bold text-gray-900",
                ),
                rx.el.p(
                    f"Ano: {v['ano']} | FIPE: {v['valor_fipe']}",
                    class_name="text-sm text-gray-500",
                ),
                rx.el.span(
                    v["tipo_posse"],
                    class_name="mt-2 inline-block px-3 py-1 bg-gray-100 text-gray-700 text-xs font-medium rounded-full",
                ),
            ),
            rx.el.div(
                rx.cond(
                    is_active,
                    rx.el.span(
                        "Ativo",
                        class_name="px-3 py-1 bg-blue-100 text-blue-700 text-sm font-bold rounded-xl border border-blue-200 w-fit",
                    ),
                    rx.el.button(
                        "Tornar Ativo",
                        on_click=lambda: VehicleState.set_active_vehicle(
                            v["id"]
                        ),
                        class_name="px-3 py-1 bg-white text-gray-600 text-sm font-medium rounded-xl border border-gray-300 hover:bg-gray-50",
                    ),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: VehicleState.remove_vehicle(v["id"]),
                    class_name="p-2 text-red-500 hover:bg-red-50 rounded-xl",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-start",
        ),
        class_name=rx.cond(
            is_active,
            "bg-white p-6 rounded-2xl border-2 border-blue-500 shadow-md mb-4",
            "bg-white p-6 rounded-2xl border border-gray-200 shadow-sm mb-4",
        ),
    )


def vehicles_page() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.h1(
                "Meus Veículos",
                class_name="text-2xl font-bold text-gray-900 mb-6",
            ),
            rx.el.div(
                rx.foreach(VehicleState.vehicles, vehicle_card),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Adicionar Veículo",
                    class_name="text-xl font-bold text-gray-900 mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Marca (FIPE)",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Selecione", value=""),
                                    rx.foreach(
                                        VehicleState.brands,
                                        lambda b: rx.el.option(
                                            b["name"], value=b["code"]
                                        ),
                                    ),
                                    value=VehicleState.marca_code,
                                    on_change=VehicleState.set_marca,
                                    class_name="w-full px-4 py-2 appearance-none border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Modelo (FIPE)",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Selecione", value=""),
                                    rx.foreach(
                                        VehicleState.models,
                                        lambda m: rx.el.option(
                                            m["name"], value=m["code"]
                                        ),
                                    ),
                                    value=VehicleState.modelo_code,
                                    on_change=VehicleState.set_modelo,
                                    disabled=VehicleState.marca_code == "",
                                    class_name="w-full px-4 py-2 appearance-none border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Ano (FIPE)",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Selecione", value=""),
                                    rx.foreach(
                                        VehicleState.years,
                                        lambda y: rx.el.option(
                                            y["name"], value=y["code"]
                                        ),
                                    ),
                                    value=VehicleState.ano_code,
                                    on_change=VehicleState.set_ano,
                                    disabled=VehicleState.modelo_code == "",
                                    class_name="w-full px-4 py-2 appearance-none border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Valor FIPE",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                disabled=True,
                                class_name="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl text-gray-600",
                                default_value=VehicleState.valor_fipe,
                                key=VehicleState.valor_fipe,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Tipo de Posse",
                                class_name="block text-sm font-semibold text-gray-700 mb-1",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Próprio", value="Próprio"),
                                    rx.el.option(
                                        "Financiamento", value="Financiamento"
                                    ),
                                    rx.el.option("Aluguel", value="Aluguel"),
                                    value=VehicleState.tipo_posse,
                                    on_change=VehicleState.set_tipo_posse,
                                    class_name="w-full px-4 py-2 appearance-none border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-600 bg-white",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="absolute right-3 top-3 h-4 w-4 text-gray-400 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        rx.cond(
                            VehicleState.tipo_posse == "Aluguel",
                            rx.el.div(
                                rx.el.label(
                                    "Valor Aluguel (Semana)",
                                    class_name="block text-sm font-semibold text-gray-700 mb-1",
                                ),
                                rx.el.input(
                                    name="valor_aluguel_semana",
                                    type="number",
                                    step="0.01",
                                    default_value="0",
                                    class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                                ),
                            ),
                            rx.cond(
                                VehicleState.tipo_posse == "Financiamento",
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.label(
                                            "Valor Parcela (Mês)",
                                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                                        ),
                                        rx.el.input(
                                            name="valor_parcela",
                                            type="number",
                                            step="0.01",
                                            default_value="0",
                                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl mb-4",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "Parcelas Restantes",
                                            class_name="block text-sm font-semibold text-gray-700 mb-1",
                                        ),
                                        rx.el.input(
                                            name="parcelas_restantes",
                                            type="number",
                                            default_value="0",
                                            class_name="w-full px-4 py-2 border border-gray-200 rounded-xl",
                                        ),
                                    ),
                                ),
                                rx.el.div(),
                            ),
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.cond(
                                VehicleState.is_loading,
                                rx.icon(
                                    "loader", class_name="h-5 w-5 animate-spin"
                                ),
                                "Cadastrar Veículo",
                            ),
                            type="submit",
                            class_name="bg-blue-600 text-white font-bold py-3 px-8 rounded-xl hover:bg-blue-700 transition-all shadow-md flex items-center justify-center gap-2",
                            disabled=VehicleState.is_loading,
                        ),
                        class_name="mt-8 flex justify-end",
                    ),
                    on_submit=VehicleState.add_vehicle,
                ),
                class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
            ),
        ),
        "/app/veiculos",
    )


from app.states.costs_state import CostsState
from app.states.results_state import ResultsState


def costs_page() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.h1(
                "Custos Operacionais",
                class_name="text-2xl font-bold text-gray-900 mb-4",
            ),
            rx.cond(
                CostsState.has_active_vehicle,
                rx.el.form(
                    rx.el.div(
                        rx.el.h2(
                            "Custos Fixos",
                            class_name="text-lg font-semibold mb-4 text-gray-800 border-b pb-2",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "IPVA Anual",
                                    class_name="block text-sm font-semibold mb-1 text-gray-700",
                                ),
                                rx.el.input(
                                    name="cf_ipva",
                                    type="number",
                                    step="0.01",
                                    default_value=CostsState.cf_ipva.to_string(),
                                    key=CostsState.cf_ipva.to_string(),
                                    class_name="w-full p-2 border rounded-xl bg-gray-50 text-gray-500",
                                    disabled=True,
                                ),
                                rx.el.p(
                                    CostsState.info_ipva,
                                    class_name="text-xs text-blue-500 mt-1",
                                ),
                                rx.el.input(
                                    type="hidden",
                                    name="cf_ipva",
                                    value=CostsState.cf_ipva.to_string(),
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Licenciamento",
                                    class_name="block text-sm font-semibold mb-1 text-gray-700",
                                ),
                                rx.el.input(
                                    name="cf_licenciamento",
                                    type="number",
                                    step="0.01",
                                    default_value=CostsState.cf_licenciamento.to_string(),
                                    key=CostsState.cf_licenciamento.to_string(),
                                    class_name="w-full p-2 border rounded-xl bg-gray-50 text-gray-500",
                                    disabled=True,
                                ),
                                rx.el.p(
                                    CostsState.info_licenciamento,
                                    class_name="text-xs text-blue-500 mt-1",
                                ),
                                rx.el.input(
                                    type="hidden",
                                    name="cf_licenciamento",
                                    value=CostsState.cf_licenciamento.to_string(),
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "INSS Mensal",
                                    class_name="block text-sm font-semibold mb-1 text-gray-700",
                                ),
                                rx.el.input(
                                    name="cf_inss",
                                    type="number",
                                    step="0.01",
                                    default_value=CostsState.cf_inss.to_string(),
                                    class_name="w-full p-2 border rounded-xl",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6",
                        ),
                        rx.el.h2(
                            "Custos Variáveis",
                            class_name="text-lg font-semibold mb-4 text-gray-800 border-b pb-2",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Preço Combustível",
                                    class_name="block text-sm font-semibold mb-1 text-gray-700",
                                ),
                                rx.el.input(
                                    name="preco_comb",
                                    type="number",
                                    step="0.01",
                                    default_value=CostsState.preco_comb.to_string(),
                                    key=CostsState.preco_comb.to_string(),
                                    class_name="w-full p-2 border rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
                                ),
                                rx.el.p(
                                    CostsState.info_combustivel,
                                    class_name="text-xs text-gray-500 mt-1",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Consumo (km/l)",
                                    class_name="block text-sm font-semibold mb-1 text-gray-700",
                                ),
                                rx.el.input(
                                    name="consumo_comb",
                                    type="number",
                                    step="0.01",
                                    default_value=CostsState.consumo_comb.to_string(),
                                    key=CostsState.consumo_comb.to_string(),
                                    class_name="w-full p-2 border rounded-xl focus:ring-2 focus:ring-blue-600 outline-none",
                                ),
                                rx.el.p(
                                    CostsState.info_consumo,
                                    class_name="text-xs text-gray-500 mt-1",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Alimentação/Dia",
                                    class_name="block text-sm font-semibold mb-1 text-gray-700",
                                ),
                                rx.el.input(
                                    name="cv_alim_dia",
                                    type="number",
                                    step="0.01",
                                    default_value=CostsState.cv_alim_dia.to_string(),
                                    class_name="w-full p-2 border rounded-xl",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6",
                        ),
                        rx.el.h2(
                            "Impostos", class_name="text-lg font-semibold mb-4"
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "ISS (%)",
                                    class_name="block text-sm font-semibold mb-1",
                                ),
                                rx.el.input(
                                    name="cp_iss",
                                    type="number",
                                    step="0.1",
                                    default_value=CostsState.cp_iss.to_string(),
                                    class_name="w-full p-2 border rounded-xl",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Margem Lucro ISS (%)",
                                    class_name="block text-sm font-semibold mb-1",
                                ),
                                rx.el.input(
                                    name="margem_iss",
                                    type="number",
                                    step="0.1",
                                    default_value=CostsState.margem_iss.to_string(),
                                    class_name="w-full p-2 border rounded-xl",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6",
                        ),
                        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm",
                    ),
                    rx.el.button(
                        "Salvar Custos",
                        type="submit",
                        class_name="mt-4 bg-blue-600 text-white font-bold py-3 px-8 rounded-xl hover:bg-blue-700",
                    ),
                    on_submit=CostsState.save_costs,
                ),
                rx.el.div(
                    "Selecione um veículo ativo na página de Veículos",
                    class_name="bg-red-50 text-red-600 p-6 rounded-2xl border border-red-200 font-semibold",
                ),
            ),
        ),
        "/app/custos",
    )


def results_page() -> rx.Component:
    return base_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Resultados & Markup",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.button(
                    "Recalcular",
                    on_click=ResultsState.recalculate,
                    class_name="bg-blue-600 text-white px-4 py-2 rounded-xl font-bold",
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Custo Mensal"),
                    rx.el.p(
                        f"R$ {ResultsState.custo_mensal_total:.2f}",
                        class_name="text-2xl font-bold",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p("Custo por Km"),
                    rx.el.p(
                        f"R$ {ResultsState.custo_por_km:.2f}",
                        class_name="text-2xl font-bold",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p("Custo por Hora"),
                    rx.el.p(
                        f"R$ {ResultsState.custo_por_hora:.2f}",
                        class_name="text-2xl font-bold",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p("Markup Sugerido"),
                    rx.el.p(
                        f"{ResultsState.markup_sugerido:.1f}%",
                        class_name="text-2xl font-bold text-blue-600",
                    ),
                    class_name="bg-white p-6 rounded-2xl border-2 border-blue-500",
                ),
                class_name="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Custo Diário"),
                    rx.el.p(
                        f"R$ {ResultsState.custo_diario:.2f}",
                        class_name="text-xl font-bold",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p("Custo Semanal"),
                    rx.el.p(
                        f"R$ {ResultsState.custo_semanal:.2f}",
                        class_name="text-xl font-bold",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200",
                ),
                rx.el.div(
                    rx.el.p("Faturamento Bruto Necessário"),
                    rx.el.p(
                        f"R$ {ResultsState.faturamento_bruto:.2f}",
                        class_name="text-xl font-bold",
                    ),
                    class_name="bg-white p-6 rounded-2xl border border-gray-200",
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6",
            ),
        ),
        "/app/resultados",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(login_page, route="/")
app.add_page(register_page, route="/registrar")
app.add_page(recover_page, route="/recuperar-senha")
app.add_page(
    profile_page,
    route="/app/perfil",
    on_load=[AuthState.check_auth, ProfileState.load_profile],
)
app.add_page(
    vehicles_page,
    route="/app/veiculos",
    on_load=[
        AuthState.check_auth,
        ProfileState.load_profile,
        VehicleState.load_vehicles,
    ],
)
app.add_page(
    costs_page,
    route="/app/custos",
    on_load=[
        AuthState.check_auth,
        ProfileState.load_profile,
        CostsState.load_costs,
    ],
)
app.add_page(
    results_page,
    route="/app/resultados",
    on_load=[
        AuthState.check_auth,
        ProfileState.load_profile,
        CostsState.load_costs,
        ResultsState.recalculate,
    ],
)