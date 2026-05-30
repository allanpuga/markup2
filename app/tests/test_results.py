import unittest
from unittest.mock import MagicMock, patch
from app.states.results_state import ResultsState


class TestResultsMarkup(unittest.IsolatedAsyncioTestCase):
    """Unit tests for the markup calculation logic."""

    async def test_recalculate_markup(self):
        """Verify the math logic of recalculate function."""
        state = ResultsState()
        profile = MagicMock()
        profile.km_dia = 150.0
        profile.dias_semana = 6
        profile.horas_dia = 8
        profile.veiculo_ativo_id = "test-vehicle"
        vehicle_state = MagicMock()
        vehicle_state.vehicles = [
            {
                "id": "test-vehicle",
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": "2023",
                "valor_fipe": "R$ 50.000,00",
                "tipo_posse": "Próprio",
            }
        ]
        costs = MagicMock()
        costs.has_active_vehicle = True
        costs.cf_ipva = 2000.0
        costs.cf_licenciamento = 160.0
        costs.cf_seguro_obrig = 0.0
        costs.cf_seguro_carro = 2500.0
        costs.cf_inss = 155.32
        costs.cf_internet = 60.0
        costs.cv_alim_dia = 30.0
        costs.cv_lavagem = 120.0
        costs.preco_comb = 5.8
        costs.consumo_comb = 10.0
        costs.cv_manut_mensal = 150.0
        costs.cv_oleo = 250.0
        costs.cv_pneu = 1600.0
        costs.cv_alinhamento = 100.0
        costs.cp_iss = 5.0
        costs.cp_icms = 0.0
        costs.cp_ipca = 4.62
        costs.margem_iss = 20.0
        costs.remuneracao_semanal = 1551.0

        def mock_parse_fipe(val_str):
            return 50000.0

        costs._parse_fipe = mock_parse_fipe

        async def mock_get_state(self_instance, cls):
            from app.states.profile_state import ProfileState
            from app.states.vehicle_state import VehicleState
            from app.states.costs_state import CostsState

            if cls == ProfileState:
                return profile
            if cls == VehicleState:
                return vehicle_state
            if cls == CostsState:
                return costs
            return None

        with patch.object(
            ResultsState, "get_state", autospec=True, side_effect=mock_get_state
        ):
            await state.recalculate()
        expected_monthly_km = 150 * 6 * 52 / 12
        self.assertEqual(expected_monthly_km, 3900.0)
        self.assertGreater(state.custo_por_km, 0)
        self.assertGreater(state.valor_ideal_km, state.custo_por_km)
        self.assertGreater(state.markup_sugerido, 0)
        self.assertGreater(state.markup_sugerido, 20.0)
        self.assertLess(state.markup_sugerido, 40.0)
        self.assertAlmostEqual(
            state.faturamento_bruto,
            state.valor_ideal_km * expected_monthly_km,
            places=0,
        )
        print(
            f"\n✓ Math Verified: Custo/km = R$ {state.custo_por_km:.2f}, Ideal/km = R$ {state.valor_ideal_km:.2f}, Markup = {state.markup_sugerido:.1f}%"
        )


if __name__ == "__main__":
    unittest.main()