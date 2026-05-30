import reflex as rx


def legal_header(title: str) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.el.div(
                rx.icon("arrow-left", class_name="h-4 w-4"),
                rx.el.span("Voltar para o Login", class_name="font-semibold"),
                class_name="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors mb-6",
            ),
            href="/",
        ),
        rx.el.h1(title, class_name="text-3xl font-bold text-gray-900 mb-2"),
        rx.el.p(
            "Última atualização: 20 de Maio de 2024",
            class_name="text-gray-500 text-sm mb-8",
        ),
    )


def legal_section(title: str, content: list[str]) -> rx.Component:
    return rx.el.section(
        rx.el.h2(title, class_name="text-xl font-bold text-gray-800 mb-4"),
        rx.el.div(
            rx.foreach(
                content,
                lambda p: rx.el.p(
                    p, class_name="text-gray-600 mb-4 leading-relaxed"
                ),
            )
        ),
        class_name="mb-10",
    )


def privacy_policy_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            legal_header("Política de Privacidade"),
            rx.el.div(
                legal_section(
                    "1. Coleta de Dados",
                    [
                        "O Gestão Markup coleta informações essenciais para o cálculo de rentabilidade do motorista de aplicativo. Ao utilizar nossa plataforma via login local ou Google OAuth, armazenamos seu nome, e-mail e identificadores únicos de sessão.",
                        "Coletamos dados de perfil (WhatsApp, Cidade, Estado) e rotina de trabalho (dias trabalhados, horas por dia, km rodados) para personalizar as métricas de desempenho.",
                    ],
                ),
                legal_section(
                    "2. Dados do Veículo e Custos",
                    [
                        "Para realizar os cálculos, processamos informações sobre seu veículo: marca, modelo, ano, valor de mercado (integrado à Tabela FIPE) e categoria de atuação (Uber X, Black, etc.).",
                        "Dados financeiros inseridos, como custos de combustível, manutenção, seguro e financiamento, são armazenados de forma privada para gerar seu histórico de resultados.",
                    ],
                ),
                legal_section(
                    "3. Uso de Serviços de Terceiros",
                    [
                        "Integramos com o Google OAuth para autenticação segura. O acesso é limitado aos dados básicos do perfil para criação de conta.",
                        "Utilizamos a API da Parallelum para consulta da Tabela FIPE e os serviços do IBGE para localização geográfica e índices de inflação (IPCA), garantindo que seus cálculos reflitam a realidade econômica atual.",
                    ],
                ),
                legal_section(
                    "4. Segurança e Retenção",
                    [
                        "Suas senhas são criptografadas utilizando algoritmos de hashing robustos (bcrypt). Mantemos seus dados enquanto sua conta estiver ativa.",
                        "Apenas administradores do sistema têm acesso consolidado a métricas de uso para monitoramento de saúde da plataforma e suporte técnico.",
                    ],
                ),
                rx.el.div(
                    rx.el.span(
                        "Dúvidas sobre sua privacidade? ",
                        class_name="text-gray-500",
                    ),
                    rx.el.a(
                        "Leia nossos Termos de Uso",
                        href="/termos",
                        class_name="text-blue-600 font-semibold hover:underline",
                    ),
                    class_name="mt-8 pt-8 border-t border-gray-100 text-center",
                ),
                class_name="bg-white p-8 md:p-12 rounded-3xl border border-gray-200 shadow-sm",
            ),
            class_name="max-w-4xl mx-auto py-12 px-4",
        ),
        class_name="bg-gray-50 min-h-screen font-['Inter']",
    )


def terms_of_service_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            legal_header("Termos de Uso"),
            rx.el.div(
                legal_section(
                    "1. Aceite dos Termos",
                    [
                        "Ao acessar o Gestão Markup, você concorda em cumprir estes termos de serviço. Esta ferramenta foi desenvolvida exclusivamente para auxiliar motoristas de aplicativo na gestão de seus custos operacionais."
                    ],
                ),
                legal_section(
                    "2. Isenção de Responsabilidade Financeira",
                    [
                        "Os cálculos de Markup, Custo por KM e Valor Ideal são ESTIMATIVAS baseadas nos dados fornecidos pelo usuário e em médias de mercado. O Gestão Markup não garante lucros específicos nem se responsabiliza por decisões financeiras tomadas com base nestas simulações.",
                        "É responsabilidade do motorista conferir a veracidade dos preços de combustível, seguros e taxas de impostos em sua região específica.",
                    ],
                ),
                legal_section(
                    "3. Uso da Conta",
                    [
                        "A conta é pessoal e intransferível. O uso indevido da plataforma para extração massiva de dados da Tabela FIPE ou outros serviços integrados resultará em suspensão imediata."
                    ],
                ),
                legal_section(
                    "4. Suporte e Contato",
                    [
                        "O suporte técnico é oferecido via e-mail para usuários cadastrados. Como ferramenta de apoio, o serviço é fornecido 'como está', sem garantias de disponibilidade ininterrupta."
                    ],
                ),
                rx.el.div(
                    rx.el.span(
                        "Como tratamos seus dados? ", class_name="text-gray-500"
                    ),
                    rx.el.a(
                        "Veja nossa Política de Privacidade",
                        href="/privacidade",
                        class_name="text-blue-600 font-semibold hover:underline",
                    ),
                    class_name="mt-8 pt-8 border-t border-gray-100 text-center",
                ),
                class_name="bg-white p-8 md:p-12 rounded-3xl border border-gray-200 shadow-sm",
            ),
            class_name="max-w-4xl mx-auto py-12 px-4",
        ),
        class_name="bg-gray-50 min-h-screen font-['Inter']",
    )