import reflex as rx

costs_db: dict[tuple[str, str], dict] = {}


class CostsState(rx.State):
    has_active_vehicle: bool = False
    cf_ipva: float = 0.0
    cf_licenciamento: float = 0.0
    cf_seguro_obrig: float = 0.0
    cf_seguro_carro: float = 0.0
    cf_inss: float = 155.32
    cf_internet: float = 60.0
    cv_alim_dia: float = 30.0
    cv_lavagem: float = 120.0
    preco_comb: float = 5.8
    consumo_comb: float = 10.0
    tipo_comb: str = "Gasolina"
    cv_manut_mensal: float = 150.0
    cv_oleo: float = 250.0
    cv_alinhamento: float = 0.0
    cv_pneu: float = 1600.0
    cp_iss: float = 5.0
    cp_icms: float = 0.0
    margem_iss: float = 30.0
    is_auto_filled: bool = False
    vehicle_is_rental: bool = False
    info_ipva: str = ""
    info_licenciamento: str = ""
    info_combustivel: str = ""
    info_consumo: str = ""

    def _get_ipva_rate(self, estado: str) -> float:
        rates = {
            "AC": 2.0,
            "AL": 3.0,
            "AP": 3.0,
            "AM": 3.0,
            "BA": 2.5,
            "CE": 3.0,
            "DF": 3.5,
            "ES": 2.0,
            "GO": 3.75,
            "MA": 2.5,
            "MT": 3.0,
            "MS": 3.0,
            "MG": 4.0,
            "PA": 2.5,
            "PB": 2.5,
            "PR": 3.5,
            "PE": 3.0,
            "PI": 2.5,
            "RJ": 4.0,
            "RN": 3.0,
            "RS": 3.0,
            "RO": 3.0,
            "RR": 3.0,
            "SC": 2.0,
            "SP": 4.0,
            "SE": 2.5,
            "TO": 2.0,
        }
        return rates.get(estado, 0.0)

    def _get_licenciamento_fee(self, estado: str) -> float:
        fees = {
            "AC": 120.0,
            "AL": 140.0,
            "AP": 130.0,
            "AM": 140.0,
            "BA": 165.35,
            "CE": 201.23,
            "DF": 180.0,
            "ES": 110.0,
            "GO": 160.0,
            "MA": 120.0,
            "MT": 160.0,
            "MS": 150.0,
            "MG": 39.36,
            "PA": 140.0,
            "PB": 130.0,
            "PR": 90.94,
            "PE": 140.0,
            "PI": 120.0,
            "RJ": 268.65,
            "RN": 130.0,
            "RS": 160.0,
            "RO": 130.0,
            "RR": 120.0,
            "SC": 120.0,
            "SP": 160.22,
            "SE": 130.0,
            "TO": 120.0,
        }
        return fees.get(estado, 0.0)

    def _get_avg_fuel_price(self, estado: str) -> float:
        prices = {
            "AC": 6.8,
            "AL": 6.3,
            "AP": 6.7,
            "AM": 6.5,
            "BA": 6.2,
            "CE": 6.4,
            "DF": 6.1,
            "ES": 5.9,
            "GO": 5.8,
            "MA": 6.5,
            "MT": 5.9,
            "MS": 5.85,
            "MG": 5.95,
            "PA": 6.6,
            "PB": 6.3,
            "PR": 5.8,
            "PE": 6.3,
            "PI": 6.4,
            "RJ": 6.5,
            "RN": 6.35,
            "RS": 6.0,
            "RO": 6.4,
            "RR": 6.8,
            "SC": 5.85,
            "SP": 5.8,
            "SE": 6.2,
            "TO": 6.3,
        }
        return prices.get(estado, 5.8)

    def _estimate_consumption(self, model: str) -> float:
        model_up = model.upper()
        segments = {
            "Hatch": [
                "UNO",
                "MOBI",
                "HB20",
                "ONIX",
                "GOL",
                "POLO",
                "ARGO",
                "SANDERO",
                "KA",
            ],
            "Sedan": ["CRONOS", "VIRTUS", "VOYAGE", "VERSA", "YARIS", "CITY"],
            "SUV Compact": [
                "T-CROSS",
                "CRETA",
                "TRACKER",
                "RENEGADE",
                "KICKS",
                "HR-V",
                "PULSE",
            ],
            "SUV Med": [
                "COMPASS",
                "TUCSON",
                "SPORTAGE",
                "RAV4",
                "COROLLA CROSS",
                "TIGGO",
            ],
            "Pickup": [
                "HILUX",
                "S10",
                "RANGER",
                "AMAROK",
                "STRADA",
                "TORO",
                "SAVEIRO",
            ],
            "Luxury": ["COROLLA", "CIVIC", "CRUZE", "SENTRA", "JETTA"],
        }
        for seg, keywords in segments.items():
            if any((k in model_up for k in keywords)):
                if seg == "Hatch":
                    return 12.0
                if seg == "Sedan":
                    return 11.5
                if seg == "SUV Compact":
                    return 10.5
                if seg == "SUV Med":
                    return 9.5
                if seg == "Pickup":
                    return 8.5
                if seg == "Luxury":
                    return 11.0
        return 10.0

    def _parse_fipe(self, val_str: str) -> float:
        if not val_str:
            return 0.0
        clean = (
            val_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
        )
        try:
            return float(clean)
        except ValueError:
            return 0.0

    @rx.event
    async def load_costs(self):
        from app.states.auth_state import AuthState
        from app.states.profile_state import ProfileState
        from app.states.vehicle_state import VehicleState

        auth = await self.get_state(AuthState)
        profile = await self.get_state(ProfileState)
        vehicle_state = await self.get_state(VehicleState)
        if not auth.user_id or not profile.veiculo_ativo_id:
            self.has_active_vehicle = False
            return
        self.has_active_vehicle = True
        key = (auth.user_id, profile.veiculo_ativo_id)
        v_data = next(
            (
                v
                for v in vehicle_state.vehicles
                if v["id"] == profile.veiculo_ativo_id
            ),
            None,
        )
        self.vehicle_is_rental = (
            v_data["tipo_posse"] == "Aluguel" if v_data else False
        )
        if key in costs_db:
            data = costs_db[key]
            for k, v in data.items():
                if hasattr(self, k):
                    setattr(self, k, v)
            self.is_auto_filled = False
        else:
            self.is_auto_filled = True
            estado = profile.estado or "SP"
            if self.vehicle_is_rental:
                self.cf_ipva = 0.0
                self.cf_licenciamento = 0.0
            else:
                fipe_val = (
                    self._parse_fipe(v_data["valor_fipe"]) if v_data else 0.0
                )
                rate = self._get_ipva_rate(estado)
                self.cf_ipva = fipe_val * rate / 100
                self.cf_licenciamento = self._get_licenciamento_fee(estado)
            self.preco_comb = self._get_avg_fuel_price(estado)
            self.consumo_comb = (
                self._estimate_consumption(v_data["modelo"]) if v_data else 10.0
            )
        if self.vehicle_is_rental:
            self.info_ipva = "Incluído no aluguel"
            self.info_licenciamento = "Incluído no aluguel"
        else:
            self.info_ipva = (
                "Calculado automaticamente com base no valor FIPE e estado"
            )
            self.info_licenciamento = (
                "Calculado automaticamente com base no estado"
            )
        self.info_combustivel = f"Média do estado ({profile.estado}): R$ {self._get_avg_fuel_price(profile.estado or 'SP'):.2f}"
        model_name = v_data["modelo"] if v_data else "veículo"
        self.info_consumo = f"Estimativa para {model_name}: {self._estimate_consumption(model_name):.1f} km/l"

    @rx.event
    async def save_costs(self, form_data: dict):
        from app.states.auth_state import AuthState
        from app.states.profile_state import ProfileState

        auth = await self.get_state(AuthState)
        profile = await self.get_state(ProfileState)
        if not auth.user_id or not profile.veiculo_ativo_id:
            return rx.toast("Nenhum veículo ativo selecionado.")
        try:
            self.cf_ipva = float(form_data.get("cf_ipva", 0))
            self.cf_licenciamento = float(form_data.get("cf_licenciamento", 0))
            self.cf_seguro_obrig = float(form_data.get("cf_seguro_obrig", 0))
            self.cf_seguro_carro = float(form_data.get("cf_seguro_carro", 0))
            self.cf_inss = float(form_data.get("cf_inss", 0))
            self.cf_internet = float(form_data.get("cf_internet", 0))
            self.cv_alim_dia = float(form_data.get("cv_alim_dia", 0))
            self.cv_lavagem = float(form_data.get("cv_lavagem", 0))
            self.preco_comb = float(form_data.get("preco_comb", 0))
            self.consumo_comb = float(form_data.get("consumo_comb", 1))
            if self.consumo_comb <= 0:
                self.consumo_comb = 1
            self.tipo_comb = form_data.get("tipo_comb", "Gasolina")
            self.cv_manut_mensal = float(form_data.get("cv_manut_mensal", 0))
            self.cv_oleo = float(form_data.get("cv_oleo", 0))
            self.cv_alinhamento = float(form_data.get("cv_alinhamento", 0))
            self.cv_pneu = float(form_data.get("cv_pneu", 0))
            self.cp_iss = float(form_data.get("cp_iss", 0))
            self.cp_icms = float(form_data.get("cp_icms", 0))
            self.margem_iss = float(form_data.get("margem_iss", 0))
            key = (auth.user_id, profile.veiculo_ativo_id)
            costs_db[key] = {
                "cf_ipva": self.cf_ipva,
                "cf_licenciamento": self.cf_licenciamento,
                "cf_seguro_obrig": self.cf_seguro_obrig,
                "cf_seguro_carro": self.cf_seguro_carro,
                "cf_inss": self.cf_inss,
                "cf_internet": self.cf_internet,
                "cv_alim_dia": self.cv_alim_dia,
                "cv_lavagem": self.cv_lavagem,
                "preco_comb": self.preco_comb,
                "consumo_comb": self.consumo_comb,
                "tipo_comb": self.tipo_comb,
                "cv_manut_mensal": self.cv_manut_mensal,
                "cv_oleo": self.cv_oleo,
                "cv_alinhamento": self.cv_alinhamento,
                "cv_pneu": self.cv_pneu,
                "cp_iss": self.cp_iss,
                "cp_icms": self.cp_icms,
                "margem_iss": self.margem_iss,
            }
            return rx.toast("Custos salvos com sucesso!")
        except ValueError:
            return rx.toast("Por favor, insira valores numéricos válidos.")