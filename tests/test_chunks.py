"""Synthetic plans; no real large-document or dispatch performance claim."""
import importlib.util
from pathlib import Path
import unittest

from procedure_simplifier import chunks

class ChunkTests(unittest.TestCase):
    def setUp(self):
        def chunk(cid,primary,deps=(),context=()):
            return dict(id=cid,source_ref='fixture-source-hash',task_ref='T1',shared_context_ref='G1',primary_ids=primary,read_only_ids=list(context),depends_on=list(deps),boundary_rationale='Synthetic coherent section',packet_estimated_tokens=200)
        self.plan=dict(run_id='fixture',task_ref='T1',shared_context_ref='G1',capacity_basis='Synthetic test capacity, not a real model limit',estimation_method='Synthetic packet sizes',context_budget=dict(window_tokens=1000,reserved_tokens=200,safety_tokens=100),strategy='chunked_parallel',max_parallel=2,host_parallel_capacity=2,source_element_ids=['D','A','B'],chunks=[chunk('C0',['D']),chunk('C1',['A'],['C0'],['D']),chunk('C2',['B'],['C0'],['D'])],waves=[['C0'],['C1','C2']],merges=[dict(id='M1',input_ids=['C0','C1','C2'],packet_estimated_tokens=400)],final_merge_id='M1',global_review_plan='Independent full-region and cross-boundary source review; synthetic fixture.')

    def test_valid_parallel_plan(self):self.assertEqual(chunks.validate(self.plan),[])

    def test_missing_source_ownership(self):
        self.plan['source_element_ids'].append('EXCEPTION')
        self.assertTrue(any('coverage is incomplete' in e for e in chunks.validate(self.plan)))

    def test_overlap_is_not_primary_duplicate(self):
        self.plan['chunks'][1]['primary_ids'].append('D')
        self.assertTrue(any('ownership must be unique' in e for e in chunks.validate(self.plan)))

    def test_capacity_reserves_apply(self):
        self.plan['chunks'][0]['packet_estimated_tokens']=850
        self.assertTrue(any('exceeds usable capacity' in e for e in chunks.validate(self.plan)))

    def test_synthesis_can_overflow_too(self):
        self.plan['merges'][0]['packet_estimated_tokens']=800
        self.assertTrue(any('exceeds usable capacity' in e for e in chunks.validate(self.plan)))

    def test_dependency_same_wave_rejected(self):
        self.plan['waves']=[['C0','C1'],['C2']]
        self.assertTrue(any('earlier wave' in e for e in chunks.validate(self.plan)))

    def test_cycle_rejected(self):
        self.plan['chunks'][0]['depends_on']=['C1']
        self.assertTrue(any('cycle or wrong sequence' in e for e in chunks.validate(self.plan)))

    def test_mixed_task_versions_rejected(self):
        self.plan['chunks'][1]['task_ref']='T2'
        self.assertTrue(any('version mismatch' in e for e in chunks.validate(self.plan)))

    def test_final_merge_must_cover_all(self):
        self.plan['merges'][0]['input_ids']=['C0','C1']
        self.assertTrue(any('does not cover all chunks' in e for e in chunks.validate(self.plan)))

    def test_host_concurrency_limit(self):
        self.plan['host_parallel_capacity']=1
        self.assertTrue(any('exceeds host capacity' in e for e in chunks.validate(self.plan)))

    def test_changed_definition_invalidates_consumers(self):
        self.assertEqual(chunks.invalidated_chunks(self.plan,['D']),['C0','C1','C2'])

    def test_local_change_preserves_independent_branch(self):
        self.assertEqual(chunks.invalidated_chunks(self.plan,['A']),['C1'])

    def test_global_context_change_invalidates_all(self):
        self.assertEqual(chunks.invalidated_chunks(self.plan,global_context_changed=True),['C0','C1','C2'])

    def test_sequential_fallback(self):
        self.plan.update(strategy='chunked_sequential',max_parallel=1,host_parallel_capacity=1,waves=[['C0'],['C1'],['C2']])
        self.assertEqual(chunks.validate(self.plan),[])

    def test_hierarchical_synthesis(self):
        self.plan['merges']=[dict(id='M0',input_ids=['C0','C1'],packet_estimated_tokens=300),dict(id='M1',input_ids=['M0','C2'],packet_estimated_tokens=300)]
        self.assertEqual(chunks.validate(self.plan),[])

    def test_single_packet_path(self):
        self.plan.update(strategy='single',max_parallel=1,chunks=[self.plan['chunks'][0]],source_element_ids=['D'],waves=[['C0']],merges=[],final_merge_id='C0')
        self.assertEqual(chunks.validate(self.plan),[])

    def test_zero_safety_margin_rejected(self):
        self.plan['context_budget']['safety_tokens']=0
        self.assertTrue(any('positive safety margin' in e for e in chunks.validate(self.plan)))

if __name__=='__main__':unittest.main()
