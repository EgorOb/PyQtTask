import importlib.util


def load_main():
    spec = importlib.util.spec_from_file_location("c_weatherapi_widget", "c_weatherapi_widget.py")
    load_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(load_module)
    return load_module


if __name__ == "__main__":
    load_main().main()
