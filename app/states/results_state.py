import reflex as rx


class ResultsState(rx.State):
    custo_operacional_mensal: float = 0.0
    custo_mensal_total: float = 0.0
    custo_por_km: float = 0.0
    custo_por_hora: float = 0.0
    valor_ideal_km: float = 0.0
    valor_ideal_hora: float = 0.0
    salario_base_dieese: float = 7200.0
    markup_sugerido: float = 0.0
    custo_diario: float = 0.0
    custo_semanal: float = 0.0
    faturamento_bruto: float = 0.0
    bar_chart_data: list[dict[str, str | float]] = []
    pie_chart_data: list[dict[str, str | float]] = []
    total_cf: float = 0.0
    total_cv: float = 0.0
    total_cp_iss: float = 0.0
    total_cp_icms: float = 0.0
    markup_iss: float = 0.0
    markup_icms: float = 0.0
    saved_results: list[dict] = []
    is_saving: bool = False

    @rx.event
    async def recalculate(self):
        from app.states.profile_state import ProfileState
        from app.states.vehicle_state import VehicleState
        from app.states.costs_state import CostsState

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
        km_dia = profile.km_dia
        dias_semana = profile.dias_semana
        horas_dia = profile.horas_dia
        annual_km = km_dia * dias_semana * 52
        monthly_km = annual_km / 12
        monthly_hours = horas_dia * dias_semana * 4.33
        vehicle_monthly_cost = 0
        if active_vehicle["tipo_posse"] == "Aluguel":
            vehicle_monthly_cost = (
                active_vehicle.get("valor_aluguel_semana", 0) * 4.33
            )
        elif active_vehicle["tipo_posse"] == "Financiamento":
            vehicle_monthly_cost = active_vehicle.get("valor_parcela", 0)
        fipe_val = costs._parse_fipe(active_vehicle["valor_fipe"])
        cf_depreciacao_anual = fipe_val * 0.24
        cf_ipva_anual = costs.cf_ipva
        cf_licenciamento_anual = costs.cf_licenciamento
        cf_seguro_obrig_anual = costs.cf_seguro_obrig
        cf_seguro_carro_anual = costs.cf_seguro_carro
        cf_financiamento_anual = vehicle_monthly_cost * 12
        cf_inss_anual = costs.cf_inss * 12
        cf_internet_anual = costs.cf_internet * 12
        total_cf_anual = (
            cf_depreciacao_anual
            + cf_ipva_anual
            + cf_licenciamento_anual
            + cf_seguro_obrig_anual
            + cf_seguro_carro_anual
            + cf_financiamento_anual
            + cf_inss_anual
            + cf_internet_anual
        )
        cv_alimentacao_anual = costs.cv_alim_dia * dias_semana * 52
        daily_fuel = km_dia / max(costs.consumo_comb, 0.1) * costs.preco_comb
        cv_combustivel_anual = daily_fuel * dias_semana * 52
        cv_oleo_anual = annual_km / 10000 * costs.cv_oleo
        cv_pneu_anual = annual_km / 60000 * costs.cv_pneu
        cv_manut_anual = costs.cv_manut_mensal * 12
        cv_lavagem_anual = costs.cv_lavagem * 12
        cv_alinhamento_anual = (
            annual_km / 10000 * costs.cv_alinhamento
            if costs.cv_alinhamento > 0
            else 0
        )
        total_cv_anual = (
            cv_alimentacao_anual
            + cv_combustivel_anual
            + cv_oleo_anual
            + cv_pneu_anual
            + cv_manut_anual
            + cv_lavagem_anual
            + cv_alinhamento_anual
        )
        custo_operacional_anual = total_cf_anual + total_cv_anual
        cp_ipca_anual = custo_operacional_anual * (costs.cp_ipca / 100)
        cp_iss_anual = costs.remuneracao_semanal * (costs.cp_iss / 100) * 52
        cp_icms_anual = costs.remuneracao_semanal * (costs.cp_icms / 100) * 52
        total_costs_with_taxes_iss = (
            custo_operacional_anual + cp_ipca_anual + cp_iss_anual
        )
        profit_margin_iss = total_costs_with_taxes_iss * (
            costs.margem_iss / 100
        )
        markup_iss_anual = total_costs_with_taxes_iss + profit_margin_iss
        total_costs_with_taxes_icms = (
            custo_operacional_anual + cp_ipca_anual + cp_icms_anual
        )
        profit_margin_icms = total_costs_with_taxes_icms * (
            costs.margem_icms / 100
        )
        markup_icms_anual = total_costs_with_taxes_icms + profit_margin_icms
        total_cp_iss_anual = cp_iss_anual + cp_ipca_anual
        total_cp_icms_anual = cp_icms_anual + cp_ipca_anual
        custo_operacional_mensal = custo_operacional_anual / 12
        if monthly_km > 0:
            self.custo_por_km = custo_operacional_mensal / monthly_km
        else:
            self.custo_por_km = 0
        if monthly_hours > 0:
            self.custo_por_hora = custo_operacional_mensal / monthly_hours
        else:
            self.custo_por_hora = 0
        self.custo_operacional_mensal = custo_operacional_mensal
        markup_iss_mensal = markup_iss_anual / 12
        if monthly_km > 0:
            self.valor_ideal_km = markup_iss_mensal / monthly_km
        else:
            self.valor_ideal_km = 0
        if monthly_hours > 0:
            self.valor_ideal_hora = markup_iss_mensal / monthly_hours
        else:
            self.valor_ideal_hora = 0
        self.total_cf = total_cf_anual / 12
        self.total_cv = total_cv_anual / 12
        self.total_cp_iss = total_cp_iss_anual / 12
        self.total_cp_icms = total_cp_icms_anual / 12
        self.custo_mensal_total = custo_operacional_mensal
        self.markup_iss = (
            (markup_iss_anual / custo_operacional_anual - 1) * 100
            if custo_operacional_anual > 0
            else 0
        )
        self.markup_icms = (
            (markup_icms_anual / custo_operacional_anual - 1) * 100
            if custo_operacional_anual > 0
            else 0
        )
        self.markup_sugerido = self.markup_iss
        self.faturamento_bruto = markup_iss_mensal
        days_per_month = dias_semana * 4.33
        self.custo_diario = (
            custo_operacional_mensal / days_per_month
            if days_per_month > 0
            else 0
        )
        self.custo_semanal = self.custo_diario * dias_semana
        impostos_mensais = total_cp_iss_anual / 12
        self.bar_chart_data = [
            {"name": "Fixos", "valor": round(self.total_cf, 2)},
            {"name": "Variáveis", "valor": round(self.total_cv, 2)},
            {"name": "Impostos", "valor": round(impostos_mensais, 2)},
        ]
        combustivel_mensal = cv_combustivel_anual / 12
        oleo_mensal = cv_oleo_anual / 12
        pneu_mensal = cv_pneu_anual / 12
        vehicle_monthly = cf_financiamento_anual / 12
        self.pie_chart_data = [
            {"name": "Veículo", "value": round(vehicle_monthly, 2)},
            {"name": "Combustível", "value": round(combustivel_mensal, 2)},
            {
                "name": "Manutenção",
                "value": round(
                    (
                        cv_manut_anual
                        + cv_oleo_anual
                        + cv_pneu_anual
                        + cv_alinhamento_anual
                    )
                    / 12,
                    2,
                ),
            },
            {
                "name": "Outros Fixos",
                "value": round(
                    (total_cf_anual - cf_financiamento_anual) / 12, 2
                ),
            },
            {
                "name": "Outros Vars",
                "value": round(
                    (
                        total_cv_anual
                        - cv_combustivel_anual
                        - cv_oleo_anual
                        - cv_pneu_anual
                        - cv_manut_anual
                        - cv_alinhamento_anual
                    )
                    / 12,
                    2,
                ),
            },
        ]

    @rx.event
    async def save_result(self):
        """Save the current calculation result to the database."""
        from app.states.auth_state import AuthState
        from app.states.profile_state import ProfileState
        from app.states.vehicle_state import VehicleState
        from app.states.costs_state import CostsState
        from sqlalchemy import text
        import uuid

        auth = await self.get_state(AuthState)
        profile = await self.get_state(ProfileState)
        vehicle_state = await self.get_state(VehicleState)
        costs = await self.get_state(CostsState)
        if not auth.user_id or not profile.veiculo_ativo_id:
            yield rx.toast("Nenhum veículo ativo selecionado.")
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
            yield rx.toast("Veículo não encontrado.")
            return
        self.is_saving = True
        result_id = str(uuid.uuid4())
        veiculo_nome = f"{active_vehicle['marca']} {active_vehicle['modelo']} {active_vehicle['ano']}"
        try:
            async with rx.asession() as session:
                await session.execute(
                    text("""
                    INSERT INTO saved_results (
                        id, user_id, vehicle_id, veiculo_nome, valor_fipe, tipo_posse,
                        dias_semana, horas_dia, km_dia, remuneracao_semanal,
                        margem_iss, margem_icms, cp_iss, cp_icms, cp_ipca,
                        custo_por_km, custo_por_hora, valor_ideal_km, valor_ideal_hora,
                        custo_mensal_total, custo_diario, custo_semanal,
                        markup_sugerido, faturamento_bruto, total_cf, total_cv
                    ) VALUES (
                        :id, :uid, :vid, :vname, :fipe, :posse,
                        :dias, :horas, :km, :remun,
                        :miss, :micms, :iss, :icms, :ipca,
                        :ckm, :chora, :vikm, :vihora,
                        :cmensal, :cdiario, :csemanal,
                        :markup, :fat, :tcf, :tcv
                    )
                """),
                    {
                        "id": result_id,
                        "uid": auth.user_id,
                        "vid": profile.veiculo_ativo_id,
                        "vname": veiculo_nome,
                        "fipe": active_vehicle["valor_fipe"],
                        "posse": active_vehicle["tipo_posse"],
                        "dias": profile.dias_semana,
                        "horas": profile.horas_dia,
                        "km": profile.km_dia,
                        "remun": costs.remuneracao_semanal,
                        "miss": costs.margem_iss,
                        "micms": costs.margem_icms,
                        "iss": costs.cp_iss,
                        "icms": costs.cp_icms,
                        "ipca": costs.cp_ipca,
                        "ckm": self.custo_por_km,
                        "chora": self.custo_por_hora,
                        "vikm": self.valor_ideal_km,
                        "vihora": self.valor_ideal_hora,
                        "cmensal": self.custo_mensal_total,
                        "cdiario": self.custo_diario,
                        "csemanal": self.custo_semanal,
                        "markup": self.markup_sugerido,
                        "fat": self.faturamento_bruto,
                        "tcf": self.total_cf,
                        "tcv": self.total_cv,
                    },
                )
                await session.commit()
            yield rx.toast("Resultado salvo com sucesso!")
            yield ResultsState.load_saved_results
        except Exception as e:
            import logging

            logging.exception(f"Error saving result: {e}")
            yield rx.toast("Erro ao salvar resultado.")
        finally:
            self.is_saving = False

    @rx.event
    async def auto_save_result(self):
        """Auto-save result on page load. Only saves if values changed from last saved."""
        if self.custo_por_km <= 0:
            return
        if self.saved_results:
            last = self.saved_results[0]
            if (
                abs(float(last.get("custo_por_km", 0)) - self.custo_por_km)
                < 0.01
                and abs(
                    float(last.get("valor_ideal_km", 0)) - self.valor_ideal_km
                )
                < 0.01
            ):
                return
        yield ResultsState.save_result

    @rx.event
    async def load_saved_results(self):
        """Load all previously saved results for this user."""
        from app.states.auth_state import AuthState
        from sqlalchemy import text

        auth = await self.get_state(AuthState)
        if not auth.user_id:
            return
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text("""
                    SELECT id, veiculo_nome, valor_fipe, tipo_posse,
                        dias_semana, horas_dia, km_dia, remuneracao_semanal,
                        margem_iss, cp_iss, cp_ipca,
                        custo_por_km, custo_por_hora, valor_ideal_km, valor_ideal_hora,
                        custo_mensal_total, markup_sugerido, created_at
                    FROM saved_results
                    WHERE user_id = :uid
                    ORDER BY created_at DESC
                    LIMIT 20
                """),
                    {"uid": auth.user_id},
                )
                rows = result.all()
                self.saved_results = [
                    {
                        "id": row[0],
                        "veiculo_nome": row[1] or "",
                        "valor_fipe": row[2] or "",
                        "tipo_posse": row[3] or "",
                        "dias_semana": int(row[4] or 6),
                        "horas_dia": int(row[5] or 8),
                        "km_dia": float(row[6] or 150),
                        "remuneracao_semanal": float(row[7] or 1551),
                        "margem_iss": float(row[8] or 20),
                        "cp_iss": float(row[9] or 5),
                        "cp_ipca": float(row[10] or 4.62),
                        "custo_por_km": float(row[11] or 0),
                        "custo_por_hora": float(row[12] or 0),
                        "valor_ideal_km": float(row[13] or 0),
                        "valor_ideal_hora": float(row[14] or 0),
                        "custo_mensal_total": float(row[15] or 0),
                        "markup_sugerido": float(row[16] or 0),
                        "created_at": str(row[17].strftime("%d/%m/%Y %H:%M"))
                        if row[17]
                        else "",
                    }
                    for row in rows
                ]
        except Exception as e:
            import logging

            logging.exception(f"Error loading saved results: {e}")

    @rx.event
    async def delete_saved_result(self, result_id: str):
        """Delete a saved result by ID."""
        from app.states.auth_state import AuthState
        from sqlalchemy import text

        auth = await self.get_state(AuthState)
        try:
            async with rx.asession() as session:
                await session.execute(
                    text(
                        "DELETE FROM saved_results WHERE id = :id AND user_id = :uid"
                    ),
                    {"id": result_id, "uid": auth.user_id},
                )
                await session.commit()
            self.saved_results = [
                r for r in self.saved_results if r["id"] != result_id
            ]
            yield rx.toast("Resultado removido.")
        except Exception as e:
            import logging

            logging.exception(f"Error deleting result: {e}")
            yield rx.toast("Erro ao remover resultado.")