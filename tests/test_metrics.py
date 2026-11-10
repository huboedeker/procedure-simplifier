import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

from procedure_simplifier import metrics

class MetricsTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.base=Path(t.name)
        self.source=self.base/'source.txt';self.output=self.base/'output.md'

    def test_same_method_on_abbreviations_and_numbers(self):
        self.source.write_text('IT P/S/S 70% member');self.output.write_text('IT P/S/S')
        result=metrics.compare(self.source,self.output)
        self.assertEqual((result['source_words'],result['output_words']),(6,4))
        self.assertEqual(result['reduction_percent'],33.3)

    def test_empty_baseline_does_not_invent_percentage(self):
        self.source.write_text('');self.output.write_text('New text')
        self.assertIsNone(metrics.compare(self.source,self.output)['reduction_percent'])

    def test_increase_is_negative_reduction(self):
        self.source.write_text('One');self.output.write_text('One two')
        self.assertEqual(metrics.compare(self.source,self.output)['reduction_percent'],-100.0)

    def test_evidence_hash_identifies_actual_file(self):
        self.source.write_text('Source');self.output.write_text('Output')
        result=metrics.compare(self.source,self.output)
        self.assertEqual(result['output_sha256'],hashlib.sha256(self.output.read_bytes()).hexdigest())
        self.output.write_text('Changed')
        self.assertNotEqual(result['output_sha256'],metrics.compare(self.source,self.output)['output_sha256'])
