import reflex as rx
import requests
import logging
import uuid

vehicles_db: dict[str, list[dict]] = {}


class VehicleState(rx.State):
    vehicles: list[dict] = []
    marca_code: str = ""
    marca_name: str = ""
    modelo_code: str = ""
    modelo_name: str = ""
    ano_code: str = ""
    ano_name: str = ""
    valor_fipe: str = ""
    tipo_posse: str = "Próprio"
    valor_aluguel_semana: float = 0.0
    valor_parcela: float = 0.0
    parcelas_restantes: int = 0
    brands: list[dict[str, str]] = []
    models: list[dict[str, str]] = []
    years: list[dict[str, str]] = []
    is_loading: bool = False

    @rx.event
    async def load_vehicles(self):
        from gest_o_markup_refatorada.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        if not auth.user_id:
            return
        self.vehicles = vehicles_db.get(auth.user_id, [])
        if not self.brands:
            yield VehicleState.fetch_brands

    @rx.event(background=True)
    async def fetch_brands(self):
        async with self:
            self.is_loading = True
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(
                "https://fipe.parallelum.com.br/api/v2/cars/brands",
                headers=headers,
                timeout=10,
            )
            if res.status_code == 200:
                data = res.json()
                async with self:
                    self.brands = [
                        {"code": str(b["code"]), "name": b["name"]}
                        for b in data
                    ]
        except Exception as e:
            logging.exception(f"Error fetching FIPE brands: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def set_marca(self, code: str):
        self.marca_code = code
        self.marca_name = next(
            (b["name"] for b in self.brands if b["code"] == code), ""
        )
        self.modelo_code = ""
        self.modelo_name = ""
        self.ano_code = ""
        self.ano_name = ""
        self.valor_fipe = ""
        self.models = []
        self.years = []
        if code:
            yield VehicleState.fetch_models

    @rx.event(background=True)
    async def fetch_models(self):
        async with self:
            if not self.marca_code:
                return
            self.is_loading = True
            code = self.marca_code
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(
                f"https://fipe.parallelum.com.br/api/v2/cars/brands/{code}/models",
                headers=headers,
                timeout=10,
            )
            if res.status_code == 200:
                data = res.json()
                async with self:
                    self.models = [
                        {"code": str(m["code"]), "name": m["name"]}
                        for m in data
                    ]
        except Exception as e:
            logging.exception(f"Error fetching FIPE models: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def set_modelo(self, code: str):
        self.modelo_code = code
        self.modelo_name = next(
            (m["name"] for m in self.models if m["code"] == code), ""
        )
        self.ano_code = ""
        self.ano_name = ""
        self.valor_fipe = ""
        self.years = []
        if code:
            yield VehicleState.fetch_years

    @rx.event(background=True)
    async def fetch_years(self):
        async with self:
            if not self.modelo_code:
                return
            self.is_loading = True
            b_code = self.marca_code
            m_code = self.modelo_code
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(
                f"https://fipe.parallelum.com.br/api/v2/cars/brands/{b_code}/models/{m_code}/years",
                headers=headers,
                timeout=10,
            )
            if res.status_code == 200:
                data = res.json()
                async with self:
                    self.years = [
                        {"code": str(y["code"]), "name": y["name"]}
                        for y in data
                    ]
        except Exception as e:
            logging.exception(f"Error fetching FIPE years: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def set_ano(self, code: str):
        self.ano_code = code
        self.ano_name = next(
            (y["name"] for y in self.years if y["code"] == code), ""
        )
        self.valor_fipe = ""
        if code:
            yield VehicleState.fetch_value

    @rx.event(background=True)
    async def fetch_value(self):
        async with self:
            if not self.ano_code:
                return
            self.is_loading = True
            b_code = self.marca_code
            m_code = self.modelo_code
            y_code = self.ano_code
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(
                f"https://fipe.parallelum.com.br/api/v2/cars/brands/{b_code}/models/{m_code}/years/{y_code}",
                headers=headers,
                timeout=10,
            )
            if res.status_code == 200:
                data = res.json()
                async with self:
                    self.valor_fipe = data.get("price", "")
        except Exception as e:
            logging.exception(f"Error fetching FIPE value: {e}")
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def set_tipo_posse(self, tipo: str):
        self.tipo_posse = tipo

    @rx.event
    async def add_vehicle(self, form_data: dict):
        if not self.marca_name or not self.modelo_name or (not self.ano_name):
            return rx.toast("Selecione marca, modelo e ano.")
        from gest_o_markup_refatorada.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        user_id = auth.user_id
        try:
            aluguel = float(form_data.get("valor_aluguel_semana", 0))
            parcela = float(form_data.get("valor_parcela", 0))
            restantes = int(form_data.get("parcelas_restantes", 0))
        except ValueError:
            return rx.toast("Valores numéricos inválidos.")
        new_v = {
            "id": str(uuid.uuid4()),
            "marca": self.marca_name,
            "modelo": self.modelo_name,
            "ano": self.ano_name,
            "valor_fipe": self.valor_fipe,
            "tipo_posse": self.tipo_posse,
            "valor_aluguel_semana": aluguel,
            "valor_parcela": parcela,
            "parcelas_restantes": restantes,
        }
        self.vehicles.append(new_v)
        vehicles_db[user_id] = self.vehicles
        self.marca_code = ""
        self.marca_name = ""
        self.modelo_code = ""
        self.modelo_name = ""
        self.ano_code = ""
        self.ano_name = ""
        self.valor_fipe = ""
        self.tipo_posse = "Próprio"
        return rx.toast("Veículo adicionado com sucesso!")

    @rx.event
    async def remove_vehicle(self, v_id: str):
        from gest_o_markup_refatorada.states.auth_state import AuthState

        auth = await self.get_state(AuthState)
        self.vehicles = [v for v in self.vehicles if v["id"] != v_id]
        vehicles_db[auth.user_id] = self.vehicles
        from gest_o_markup_refatorada.states.profile_state import ProfileState, profiles_db

        profile = await self.get_state(ProfileState)
        if profile.veiculo_ativo_id == v_id:
            profile.veiculo_ativo_id = ""
            if auth.user_id in profiles_db:
                profiles_db[auth.user_id]["veiculo_ativo_id"] = ""

    @rx.event
    async def set_active_vehicle(self, v_id: str):
        from gest_o_markup_refatorada.states.profile_state import ProfileState, profiles_db
        from gest_o_markup_refatorada.states.auth_state import AuthState

        profile = await self.get_state(ProfileState)
        auth = await self.get_state(AuthState)
        profile.veiculo_ativo_id = v_id
        if auth.user_id in profiles_db:
            profiles_db[auth.user_id]["veiculo_ativo_id"] = v_id
        else:
            profiles_db[auth.user_id] = {"veiculo_ativo_id": v_id}
        return rx.toast("Veículo ativo atualizado!")