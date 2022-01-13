"""Tests for the packages module."""
import inspect
from importlib import import_module


class TestCallerPackageName():
    """Tests for the caller_package_name function."""

    def test_direct_call(self, mixxin_env):
        """Test for direct call."""
        code = inspect.cleandoc(
            '''
            from mxxn.utils.packages import caller_package_name

            def test():
                return caller_package_name()
            '''
        )

        (mixxin_env/'mxnone/__init__.py').write_text(code)

        import mxnone

        assert mxnone.test() == 'mxnone'

    def test_call_with_depth(self, mixxin_env):
        """Test for call with depth argument."""
        code = inspect.cleandoc(
            '''
            from mxxn.utils.packages import caller_package_name

            def test():
                return caller_package_name(2)
            '''
        )

        (mixxin_env/'mxnone/__init__.py').write_text(code)

        import mxnone

        assert mxnone.test() == 'test_packages'
