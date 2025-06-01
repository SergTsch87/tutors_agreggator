import unittest
from decors import registry, register#, register_parser


site_parsers = {}


def warn_overwrite(site, logger=print):
    logger(f'[WARN] Overwriting existing parser for site: "{site}"')


def register_site_parser(site, func, logger=print):
    if site in site_parsers:
        logger(f'[WARN] Overwriting existing parser for site: "{site}"')
    site_parsers[site] = func


def parser(site, debug=False, logger=print):
    if not isinstance(site, str):
        raise TypeError(f'Expected site to be str, got {type(site).__name__}')
        
    def decorator(func):
        decorated_func = func

        if debug:
            def wrapper(html):
                logger(f"[LOG] BEFORE {func.__name__}")
                result = func(html)
                logger(f"[LOG] AFTER {func.__name__}")
                return result
            decorated_func = wrapper
        
        register_site_parser(site, decorated_func, logger=logger)
        return decorated_func
    
    return decorator


class TestFullParserDecorator(unittest.TestCase):
    def setUp(self):
        site_parsers.clear()  # Reset the registry before each test
        self.logs = []

    def fake_log(self, message):
        self.logs.append(message)

    def test_parser_registers_and_logs(self):
        @parser(site="buki", debug=True, logger=self.fake_log)
        def parse_buki(html):
            return f"Parsed: {html}"

        result = site_parsers["buki"]("Hello")

        self.assertEqual(result, "Parsed: Hello")
        self.assertEqual(self.logs, [
            "[LOG] BEFORE parse_buki",
            "[LOG] AFTER parse_buki"
        ])

# ----------------------------------------------------------

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
        log = []

        def fake_log(msg):
            log.append(msg)

        @parser('buki', debug=True, logger=fake_log)
        def parse_buki(html):
            return 'Parsed Buki'

        self.assertIn('buki', registry)
        self.assertEqual(registry['buki']('html...'), 'Parsed Buki')

    def test_invalid_site_name_type(self):
        log = []

        def fake_log(msg):
            log.append(msg)

        with self.assertRaises(TypeError):
            @parser(123, debug=True, logger=fake_log)
            def invalid_parser(html):
                return 'Should not register'

    def test_overwriting_existing_key(self):
        log = []

        def fake_log(msg):
            log.append(msg)

        @parser('buki', debug=True, logger=fake_log)
        def parse_v1(html): return 'v1'

        @parser('buki', debug=True, logger=fake_log)  # second definition should overwrite
        def parse_v2(html): return 'v2'

        self.assertEqual(registry['buki']('dummy'), 'v2')


class TestPrePostProcessing(unittest.TestCase):
    def test_log_before_and_after_parse(self):
        log = []

        def fake_log(msg):
            log.append(msg)

        # Create a dummy decorator for test; we'll replace this with the real one later.
        def log_decorator(func):
            def wrapper(html):
                fake_log('BEFORE parsing')
                result = func(html)
                fake_log('AFTER parsing')
                return result
            return wrapper
        
        @log_decorator
        def dummy_parser(html):
            return f'parsed({html})'
        
        result = dummy_parser('test_html')

        self.assertEqual(result, "parsed(test_html)")
        self.assertEqual(log, ["BEFORE parsing", "AFTER parsing"])


    def test_log_on_exception(self):
        log = []

        def fake_log(msg):
            log.append(msg)

        def log_decorator(func):
            def wrapper(html):
                try:
                    fake_log("BEFORE parsing")
                    result = func(html)
                    fake_log("AFTER parsing")
                    return result
                except Exception as e:
                    fake_log(f"ERROR: {e}")
                    raise
            return wrapper

        @log_decorator
        def failing_parser(html):
            raise ValueError("Parse failed")

        with self.assertRaises(ValueError):
            failing_parser("bad html")

        self.assertEqual(log, ["BEFORE parsing", "ERROR: Parse failed"])


def conditional_log(enabled=True, logger=print):
    def decorator(func):
        def wrapper(html):
            if enabled:
                logger(f"[LOG] BEFORE {func.__name__}")
            result = func(html)
            if enabled:
                logger(f"[LOG] AFTER {func.__name__}")
            return result
        return wrapper
    return decorator


class TestConditionalLog(unittest.TestCase):
    def setUp(self):
        self.logs = []

    def fake_log(self, message):
        self.logs.append(message)

    def test_logs_when_enabled(self):
        log = []

        def fake_log(msg):
            log.append(msg)
        
        # Assume this decorator exists
        @conditional_log(enabled=True, logger=fake_log)
        def dummy_parser(html):
            return f"parsed({html})"

        result = dummy_parser("hello")

        self.assertEqual(result, "parsed(hello)")
        self.assertEqual(log, ["[LOG] BEFORE dummy_parser", "[LOG] AFTER dummy_parser"])

    
    def test_does_not_log_when_disabled(self):
        log = []

        def fake_log(msg):
            log.append(msg)

        @conditional_log(enabled=False, logger=fake_log)
        def dummy_parser(html):
            return f"parsed({html})"

        result = dummy_parser("hello")

        self.assertEqual(result, "parsed(hello)")
        self.assertEqual(log, [])  # nothing should have been logged


    def test_parser_silent_when_debug_false(self):
        @parser(site="profrep", debug=False, logger=self.fake_log)
        def parse_profrep(html):
            return f"Parsed: {html}"

        result = site_parsers["profrep"]("Data")

        self.assertEqual(result, "Parsed: Data")
        self.assertEqual(self.logs, [])  # No logs should be captured


    def test_warns_on_overwrite(self):
        @parser(site="buki", debug=False, logger=self.fake_log)
        def first(html):
            return "1"

        @parser(site="buki", debug=False, logger=self.fake_log)
        def second(html):
            return "2"

        self.assertIn('buki', site_parsers)
        self.assertEqual(self.logs[-1], '[WARN] Overwriting existing parser for site: "buki"')


# 2-й варіант тесту для перевірки типу
class TestInputValidation(unittest.TestCase):
    def setUp(self):
        self.logs = []

    def fake_log(self, message):
        self.logs.append(message)

    def test_invalid_site_type(self):
        with self.assertRaises(TypeError):
            @parser(site=None, debug=True, logger=self.fake_log)
            def bad_parser(html):
                return "Should fail"