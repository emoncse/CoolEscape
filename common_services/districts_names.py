import json
import logging

logger = logging.getLogger(__name__)

def district_names_for_swagger():
    with open("bd-districts.json", "r") as f:
        logger.info("Loading district names from bd-districts.json")
        districts_data = json.load(f)["districts"]
    district_names = [d["name"] for d in districts_data]
    logger.info(f"District names loaded: {district_names}")
    return district_names


def processed_json_data():
    with open("bd-districts.json", "r") as f:
        districts = json.load(f)["districts"]

    logger.info(f"Processed JSON data loaded, {districts}")
    return districts