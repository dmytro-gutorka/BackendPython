from unittest import TestCase
from unittest.mock import patch, MagicMock
from pokemon_name_translator import PokemonNameTranslator
from pokemon_report import PokemonReport
from pokemon_service import PokemonService
from main import main
import pdfkit


class TestPokemonReport(TestCase):

	def test_create_html_report(self):
		report = PokemonReport()

		pokemon_info = {
			"height": 10,
			"weight": 100,
			"abilities": [
				{"ability": {"name": "static"}},
				{"ability": {"name": "lightning-rod"}}
			],
		}
		translated_name = "Pikachu Pikachu"

		html_path = report.create_html_report(pokemon_info, translated_name)

		with open(html_path, "r", encoding="utf-8") as f:
			content = f.read()

		self.assertIn("<strong>Abilities:</strong> static, lightning-rod", content)
		self.assertIn("<strong>Name:</strong> Pikachu Pikachu", content)
		self.assertIn("<strong>Height:</strong> 10 decimetres", content)
		self.assertIn("<strong>Weight:</strong> 100 hectograms", content)

	def test_create_html_report_empty_abilities(self):
		report = PokemonReport()

		pokemon_info = {
			"height": 10,
			"weight": 100,
			"abilities": []
		}
		translated_name = "Pikachu Pikachu"

		html_path = report.create_html_report(pokemon_info, translated_name)

		with open(html_path, "r", encoding="utf-8") as f:
			content = f.read()

		self.assertIn("<strong>Abilities:</strong> ", content)


class TestPokemonNameTranslator(TestCase):
	@patch("pokemon_name_translator.translate.TranslationServiceClient")
	def test_translate(self, MockTranslationServiceClient):
		mock_client = MagicMock()
		MockTranslationServiceClient.return_value = mock_client

		mock_response = MagicMock()
		mock_response.translations = [MagicMock(translated_text="Pikachu Pikachu")]
		mock_client.translate_text.return_value = mock_response

		translator = PokemonNameTranslator()

		result = translator.translate("Pikachu", target_language="it")

		self.assertEqual(result, "Pikachu Pikachu")

		mock_client.translate_text.assert_called_once_with(
			parent=mock_client.location_path("your-project-id", "global"),
			contents=["Pikachu"],
			target_language_code="it",
		)


class TestPokemonService(TestCase):

	@patch("pokemon_service.requests.get")
	def test_get_pokemon_info_success(self, mock_get):
		# Mock the response object
		mock_response = MagicMock()
		mock_response.status_code = 200
		mock_response.json.return_value = {
			"name": "pikachu",
			"height": 4,
			"weight": 60,
			"abilities": [
				{"ability": {"name": "static"}},
				{"ability": {"name": "lightning-rod"}}
			]
		}
		mock_get.return_value = mock_response

		service = PokemonService()

		pokemon_info = service.get_pokemon_info("pikachu")

		# Assertions
		self.assertEqual(pokemon_info["name"], "pikachu")
		self.assertEqual(pokemon_info["height"], 4)
		self.assertEqual(pokemon_info["weight"], 60)
		self.assertIn("static", [ability["ability"]["name"] for ability in pokemon_info["abilities"]])

		mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/pikachu")

	@patch("pokemon_service.requests.get")
	def test_get_pokemon_info_failure(self, mock_get):
		mock_response = MagicMock()
		mock_response.status_code = 404
		mock_get.return_value = mock_response
		service = PokemonService()

		pokemon_info = service.get_pokemon_info("nonexistentpokemon")
		self.assertIsNone(pokemon_info)
		mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/nonexistentpokemon")


class TestMain(TestCase):

	@patch("main.PokemonService")
	@patch("main.PokemonNameTranslator")
	@patch("main.PokemonReport")
	def test_main_success(self, MockPokemonReport, MockPokemonNameTranslator, MockPokemonService):

		mock_pokemon_service = MagicMock()
		mock_pokemon_name_translator = MagicMock()
		mock_pokemon_report = MagicMock()

		mock_pokemon_service.get_pokemon_info.return_value = {
			"name": "pikachu",
			"height": 4,
			"weight": 60,
			"abilities": [
				{"ability": {"name": "static"}},
				{"ability": {"name": "lightning-rod"}}
			]
		}

		mock_pokemon_name_translator.translate.return_value = "pickachu pika"

		mock_pokemon_report.generate_report.return_value = None

		MockPokemonService.return_value = mock_pokemon_service
		MockPokemonNameTranslator.return_value = mock_pokemon_name_translator
		MockPokemonReport.return_value = mock_pokemon_report

		with patch("builtins.print") as mock_print:
			main()

			mock_pokemon_service.get_pokemon_info.assert_called_once_with("pikachu")
			mock_pokemon_name_translator.translate.assert_called_once_with("pikachu", target_language="fr")
			mock_pokemon_report.generate_report.assert_called_once()

			mock_print.assert_called_with("PDF report saved as pokemon_report.pdf")

	@patch("main.PokemonService")
	@patch("main.PokemonNameTranslator")
	@patch("main.PokemonReport")
	def test_main_pokemon_not_found(self, MockPokemonReport, MockPokemonNameTranslator, MockPokemonService):

		mock_pokemon_service = MagicMock()
		mock_pokemon_name_translator = MagicMock()
		mock_pokemon_report = MagicMock()
		mock_pokemon_service.get_pokemon_info.return_value = None

		MockPokemonService.return_value = mock_pokemon_service
		MockPokemonNameTranslator.return_value = mock_pokemon_name_translator
		MockPokemonReport.return_value = mock_pokemon_report

		with patch("builtins.print") as mock_print:
			main()

			# Assertions
			mock_pokemon_service.get_pokemon_info.assert_called_once_with("pikachu")
			mock_pokemon_name_translator.translate.assert_not_called()
			mock_pokemon_report.generate_report.assert_not_called()

			mock_print.assert_called_with("Pokemon not found.")