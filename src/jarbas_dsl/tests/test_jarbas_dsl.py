import pytest
import jarbas_dsl

def test_project_defines_author_and_version():
    assert hasattr(jarbas_dsl, '__author__')
    assert hasattr(jarbas_dsl, '__version__')

