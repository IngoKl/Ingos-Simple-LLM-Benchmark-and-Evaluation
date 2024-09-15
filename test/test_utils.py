from ingollmbencheval.utils import sanitize_model_name


def test_sanitize_model_name():
    assert (
        sanitize_model_name(
            "lmstudio-community/Phi-3.1-mini-4k-instruct-GGUF/Phi-3.1-mini-4k-instruct-Q4_K_M.gguf"
        )
        == "lmstudio-community_Phi-3.1-mini-4k-instruct-GGUF_Phi-3.1-mini-4k-instruct-Q4_K_M.gguf"
    )
