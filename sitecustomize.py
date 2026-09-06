# Compatibility shim for the stable Streamlit 1.58 runtime.
# The UI was authored against newer layout helpers; keep the same app code
# while gracefully ignoring the later `wrap` keyword.
import streamlit as st
import streamlit.components.v1 as components

_columns_158 = st.columns

def _columns_compat(*args, **kwargs):
    kwargs.pop("wrap", None)
    return _columns_158(*args, **kwargs)

st.columns = _columns_compat

# Newer Streamlit accepts unsafe_allow_javascript on st.html. On 1.58,
# preserve the existing Copy/PDF controls through the components iframe.
_st_html_158 = getattr(st, "html", None)
_components_html_158 = components.html

def _html_compat(body, *args, unsafe_allow_javascript=False, **kwargs):
    if unsafe_allow_javascript:
        return _components_html_158(body, *args, **kwargs)
    if _st_html_158 is not None:
        return _st_html_158(body, *args, **kwargs)
    return _components_html_158(body, *args, **kwargs)

st.html = _html_compat
