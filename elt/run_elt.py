from elt.extract_load.load_raw_to_mongodb import load_all_raw
from elt.transform.run_aggregations import run_all
from elt.metadata.elt_metadata import update_metadata

print("🚀 Running ELT Pipeline...")

load_all_raw()
run_all()
update_metadata()

print("✅ ELT selesai")
