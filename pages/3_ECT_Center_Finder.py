from pathlib import Path
import importlib.util

helper=Path(__file__).with_name("_oncology_center_finder.py")
spec=importlib.util.spec_from_file_location("oncology_center_finder",helper)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.render()
