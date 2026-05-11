import reflex as rx
import requests
import logging

profiles_db: dict[str, dict] = {}


class ProfileState(rx.State):
    nome: str = ""
    email: str = ""
    estado: str = ""
    cidade: str = ""
    whatsapp: str = ""
    dias_semana: int = 6
    horas_dia: int = 8
    km_dia: float = 150.0
    veiculo_ativo_id: str = ""
    estados: list[dict[str, str]] = []
    cidades: list[str] = []
    is_loading: bool = False

    @rx.event
    async def load_profile(self):
        from gest_o_markup_refatorada.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        if not auth.user_id:
            return
        profile = profiles_db.get(auth.user_id, {})
        self.nome = profile.get("nome", auth.username)
        self.email = profile.get("email", auth.email)
        self.estado = profile.get("estado", "")
        self.cidade = profile.get("cidade", "")
        self.whatsapp = profile.get("whatsapp", "")
        self.dias_semana = profile.get("dias_semana", 6)
        self.horas_dia = profile.get("horas_dia", 8)
        self.km_dia = float(profile.get("km_dia", 150.0))
        self.veiculo_ativo_id = profile.get("veiculo_ativo_id", "")
        if not self.estados:
            yield ProfileState.fetch_estados
        if self.estado:
            yield ProfileState.fetch_cidades

    @rx.event(background=True)
    async def fetch_estados(self):
        async with self:
            self.is_loading = True
        try:
            res = requests.get(
                "https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome",
                timeout=10,
            )
            if res.status_code == 200:
                estados_data = res.json()
                async with self:
                    self.estados = [
                        {"sigla": s["sigla"], "nome": s["nome"]}
                        for s in estados_data
                    ]
        except Exception as e:
            logging.exception(f"Error fetching estados: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def set_estado_cidade(self, form_data: dict):
        self.estado = form_data.get("estado", "")
        self.cidade = form_data.get("cidade", "")
        if self.estado:
            yield ProfileState.fetch_cidades

    @rx.event
    def set_estado(self, estado: str):
        self.estado = estado
        self.cidade = ""
        yield ProfileState.fetch_cidades

    @rx.event
    def set_cidade(self, cidade: str):
        self.cidade = cidade

    @rx.event(background=True)
    async def fetch_cidades(self):
        async with self:
            if not self.estado:
                self.cidades = []
                return
            self.is_loading = True
            estado = self.estado
        try:
            res = requests.get(
                f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estado}/municipios",
                timeout=10,
            )
            if res.status_code == 200:
                cidades_data = res.json()
                async with self:
                    self.cidades = [c["nome"] for c in cidades_data]
        except Exception as e:
            logging.exception(f"Error fetching cidades: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    async def save_profile(self, form_data: dict):
        nome = form_data.get("nome", "").strip()
        email = form_data.get("email", "").strip()
        if not nome or not email:
            return rx.toast("Nome e E-mail são obrigatórios.")
        from gest_o_markup_refatorada.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        self.nome = nome
        self.email = email
        self.whatsapp = form_data.get("whatsapp", "")
        try:
            self.dias_semana = int(form_data.get("dias_semana", 6))
            self.horas_dia = int(form_data.get("horas_dia", 8))
            self.km_dia = float(form_data.get("km_dia", 150.0))
        except ValueError:
            return rx.toast("Valores numéricos inválidos.")
        profiles_db[auth.user_id] = {
            "nome": self.nome,
            "email": self.email,
            "estado": self.estado,
            "cidade": self.cidade,
            "whatsapp": self.whatsapp,
            "dias_semana": self.dias_semana,
            "horas_dia": self.horas_dia,
            "km_dia": self.km_dia,
            "veiculo_ativo_id": self.veiculo_ativo_id,
        }
        return rx.toast("Perfil salvo com sucesso!")