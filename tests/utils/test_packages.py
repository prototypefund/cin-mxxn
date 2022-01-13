"""Tests for the packages module."""
import inspect


class TestCallerPackageName():
    """Tests for the caller_package_name function."""

    def test_direct_call(self, mxxn_env):
        """Test for direct call."""
        code = inspect.cleandoc(
            '''
            from mxxn.utils.packages import caller_package_name

            def test():
                return caller_package_name()
            '''
        )

        (mxxn_env/'mxnone/__init__.py').write_text(code)

        import mxnone

        assert mxnone.test() == 'mxnone'

    def test_call_with_depth(self, mxxn_env):
        """Test for call with depth argument."""
        code = inspect.cleandoc(
            '''
            from mxxn.utils.packages import caller_package_name

            def test():
                return caller_package_name(2)
            '''
        )

        (mxxn_env/'mxnone/__init__.py').write_text(code)

        import mxnone

        assert mxnone.test() == 'test_packages'
