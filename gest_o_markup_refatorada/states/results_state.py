import reflex as rx


class ResultsState(rx.State):
    custo_mensal_total: float = 0.0
    custo_por_km: float = 0.0
    custo_por_hora: float = 0.0
    markup_sugerido: float = 0.0
    custo_diario: float = 0.0
    custo_semanal: float = 0.0
    faturamento_bruto: float = 0.0
    bar_chart_data: list[dict[str, str | float]] = []
    pie_chart_data: list[dict[str, str | float]] = []

    @rx.event
    async def recalculate(self):
        from gest_o_markup_refatorada.states.profile_state import ProfileState
        from gest_o_markup_refatorada.states.vehicle_state import VehicleState
        from gest_o_markup_refatorada.states.costs_state import CostsState

        profile = await self.get_state(ProfileState)
        vehicle_state = await self.get_state(VehicleState)
        costs = await self.get_state(CostsState)
        if not costs.has_active_vehicle:
            return
        active_vehicle = next(
            (
                v
                for v in vehicle_state.vehicles
                if v["id"] == profile.veiculo_ativo_id
            ),
            None,
        )
        if not active_vehicle:
            return
        monthly_km = profile.km_dia * profile.dias_semana * 4.33
        if monthly_km <= 0:
            monthly_km = 1
        vehicle_monthly_cost = 0
        if active_vehicle["tipo_posse"] == "Aluguel":
            vehicle_monthly_cost = (
                active_vehicle.get("valor_aluguel_semana", 0) * 4.33
            )
        elif active_vehicle["tipo_posse"] == "Financiamento":
            vehicle_monthly_cost = active_vehicle.get("valor_parcela", 0)
        fixed_monthly = (
            vehicle_monthly_cost
            + costs.cf_ipva / 12
            + costs.cf_licenciamento / 12
            + costs.cf_seguro_obrig / 12
            + costs.cf_seguro_carro / 12
            + costs.cf_inss
            + costs.cf_internet
        )
        combustivel_mensal = monthly_km / costs.consumo_comb * costs.preco_comb
        oleo_mensal = (
            costs.cv_oleo / (10000 / monthly_km) if monthly_km > 0 else 0
        )
        pneu_mensal = (
            costs.cv_pneu / (40000 / monthly_km) if monthly_km > 0 else 0
        )
        variable_monthly = (
            costs.cv_alim_dia * profile.dias_semana * 4.33
            + costs.cv_lavagem
            + combustivel_mensal
            + costs.cv_manut_mensal
            + oleo_mensal
            + costs.cv_alinhamento / 3
            + pneu_mensal
        )
        self.custo_mensal_total = fixed_monthly + variable_monthly
        self.custo_por_km = self.custo_mensal_total / monthly_km
        monthly_hours = profile.horas_dia * profile.dias_semana * 4.33
        self.custo_por_hora = (
            self.custo_mensal_total / monthly_hours if monthly_hours > 0 else 0
        )
        self.custo_diario = (
            self.custo_mensal_total / (profile.dias_semana * 4.33)
            if profile.dias_semana > 0
            else 0
        )
        self.custo_semanal = self.custo_diario * profile.dias_semana
        tax_rate = (costs.cp_iss + costs.cp_icms) / 100
        if tax_rate >= 1:
            tax_rate = 0.99
        self.faturamento_bruto = self.custo_mensal_total / (1 - tax_rate)
        if self.custo_mensal_total > 0:
            self.markup_sugerido = (
                self.faturamento_bruto
                * (1 + costs.margem_iss / 100)
                / self.custo_mensal_total
                - 1
            ) * 100
        else:
            self.markup_sugerido = 0
        impostos_mensais = self.faturamento_bruto - self.custo_mensal_total
        self.bar_chart_data = [
            {"name": "Fixos", "valor": round(fixed_monthly, 2)},
            {"name": "Variáveis", "valor": round(variable_monthly, 2)},
            {"name": "Impostos", "valor": round(impostos_mensais, 2)},
        ]
        self.pie_chart_data = [
            {"name": "Veículo", "value": round(vehicle_monthly_cost, 2)},
            {"name": "Combustível", "value": round(combustivel_mensal, 2)},
            {
                "name": "Manutenção",
                "value": round(
                    costs.cv_manut_mensal
                    + oleo_mensal
                    + pneu_mensal
                    + costs.cv_alinhamento / 3,
                    2,
                ),
            },
            {
                "name": "Outros Fixos",
                "value": round(fixed_monthly - vehicle_monthly_cost, 2),
            },
            {
                "name": "Outros Vars",
                "value": round(
                    variable_monthly
                    - combustivel_mensal
                    - (
                        costs.cv_manut_mensal
                        + oleo_mensal
                        + pneu_mensal
                        + costs.cv_alinhamento / 3
                    ),
                    2,
                ),
            },
        ]