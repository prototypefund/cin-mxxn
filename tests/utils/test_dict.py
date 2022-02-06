"""Tests for the utils.dicts module."""
from mxxn.utils import dicts


class TestMerge():
    def test_merge(self):
        """Keys that only exist in the merge dict are ignored."""
        base_dict = {
            'test-key-1': 'test-value-1',
            'test-key-2': 'test-value-2',
            'level2': {
                'test-key-3': 'test-value-3',
                'test-key-4': 'test-value-4'
            }
        }

        merge_dict = {
            'test-key-2': 'test-value-2-new',
            'level2': {
                'test-key-3': 'test-value-3-new',
                'test-key-5': 'test-value-5'
            }
        }

        dicts.merge(base_dict, merge_dict)

        assert base_dict == {
            'test-key-1': 'test-value-1',
            'test-key-2': 'test-value-2-new',
            'level2': {
                'test-key-3': 'test-value-3-new',
                'test-key-4': 'test-value-4'
            }
        }
