"""Test for the utils.modules module."""
import pytest
import importlib
import inspect
from mxxn.utils.modules import submodules, classes, classes_recursively


@pytest.fixture()
def modules_tree(mixxin_env):
    """Create a test directory with some Python modules."""
    content = """
        class Test1(object):
            pass

        class Test2(object):
            pass
    """
    (mixxin_env/'mxnone/__init__.py').write_text(inspect.cleandoc(content))
    (mixxin_env/'mxnone/module_1.py').write_text(inspect.cleandoc(content))
    (mixxin_env/'mxnone/module_2.py').touch()
    (mixxin_env/'mxnone/subpackage').mkdir()
    (mixxin_env/'mxnone/subpackage/__init__.py').touch()
    (mixxin_env/'mxnone/subpackage/module_3.py').write_text(
        inspect.cleandoc(content)
    )
    (mixxin_env/'mxnone/subpackage/module_4.py').touch()

    return mixxin_env


class TestSubmodules(object):
    """Test for submodule function."""

    def test_if_all_module_found(self, modules_tree):
        """Test if all modules were found."""
        modules = []

        submodules('mxnone', modules)

        assert modules == [
            'mxnone.module_1',
            'mxnone.module_2',
            'mxnone.subpackage.module_3',
            'mxnone.subpackage.module_4',
            'mxnone.subpackage'
        ]

    def test_raise_module_not_found_error(self):
        """Test if ModuleNotFoundError raised."""
        modules = []

        with pytest.raises(ModuleNotFoundError):
            submodules('xxxyyyzzz', modules)


class TestClasses(object):
    """Test for classes function."""

    def test_if_all_classes_found(self, modules_tree):
        """All classes were found."""
        import mxnone

        classes_list = classes(mxnone)

        assert len(classes_list) == 2
        assert classes_list[0].__name__ == 'Test1'
        assert classes_list[1].__name__ == 'Test2'


class TestCassesRecursively(object):
    """Test for classes_recursively function."""

    def test_if_all_classen_found_recursively(self, modules_tree):
        """Test if all classes were found recursively."""
        classes_list = classes_recursively('mxnone')

        assert len(classes_list) == 6
        assert classes_list[0].__module__ == 'mxnone'
        assert classes_list[0].__name__ == 'Test1'
        assert classes_list[1].__module__ == 'mxnone'
        assert classes_list[1].__name__ == 'Test2'
        assert classes_list[2].__module__ == 'mxnone.module_1'
        assert classes_list[2].__name__ == 'Test1'
        assert classes_list[3].__module__ == 'mxnone.module_1'
        assert classes_list[3].__name__ == 'Test2'
        assert classes_list[4].__module__ == \
            'mxnone.subpackage.module_3'
        assert classes_list[4].__name__ == 'Test1'
        assert classes_list[5].__module__ == \
            'mxnone.subpackage.module_3'
        assert classes_list[5].__name__ == 'Test2'
