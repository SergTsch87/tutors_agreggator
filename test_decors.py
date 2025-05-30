import unittest
from decors import registry, register, register_parser


def dummy_parser(html):
    return "I parsed something!"


class TestParserRegistry(unittest.TestCase):
    def setup(self):
        registry.clear()
    
    def test_register_parser_adds_function_to_registry(self):
        register('buki', dummy_parser)
        self.assertIn('buki', registry)
        self.assertEqual(registry['buki']('test html'), 'I parsed something!')

    def test_register_multiple_sites(self):
        def parser1(html):
            return 'A'
        
        def parser2(html):
            return 'B'

        register('buki', parser1)
        register('profrep', parser2)
        
        self.assertEqual(registry['buki']('test'), 'A')
        self.assertEqual(registry['profrep']('test'), 'B')

    def test_decorator_registers_function(self):
        @register_parser('buki')
        def parse_buki(html):
            return 'Parsed Buki'

        self.assertIn('buki', registry)
        self.assertEqual(registry['buki']('html...'), 'Parsed Buki')

    def test_invalid_site_name_type(self):
        with self.assertRaises(TypeError):
            @register_parser(123)
            def invalid_parser(html):
                return 'Should not register'

    def test_overwriting_existing_key(self):
        @register_parser('buki')
        def parse_v1(html): return 'v1'

        @register_parser('buki')  # second definition should overwrite
        def parse_v2(html): return 'v2'

        self.assertEqual(registry['buki']('dummy'), 'v2')