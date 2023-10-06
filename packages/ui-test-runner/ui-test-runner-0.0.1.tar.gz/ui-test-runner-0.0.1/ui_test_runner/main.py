"""Semantic Smoke Tests for the Translator UI."""
from datetime import datetime
import jq
import json
import httpx
import time
import traceback

debug = False

urls = {
    "ci": "https://ui.ci.transltr.io/api",
    "test": "https://ui.test.transltr.io/api",
    "prod": "https://ui.transltr.io/api",
}
query_type_map = {
    "treats(creative)": {
        "type": "drug",
        "direction": "increased",
    },
}
output_map = {
    "TopAnswer": {
        "n_results": 10,
        "good": True,
    },
    "Acceptable": {
        "n_results": 50,
        "good": True,
    },
    "BadButForgivable": {
        "n_results": 50,
        "good": False,
    },
    "NeverShow": {
        "n_results": 100000,
        "good": False,
    },
}


def run_ui_test(
    env: str,
    predicate: str,
    expected_output: int,
    input_curie: str,
    output_curie: str,
):
    """Run UI Tests."""
    ui_url = urls[env]
    query_type = query_type_map.get(predicate)
    if query_type is None:
        return "Failed."
    # Send Query
    query_payload = {
        "type": query_type["type"],
        "curie": input_curie,
        "direction": query_type["direction"],
    }
    try:
        response = httpx.post(
            f"{ui_url}/creative_query",
            data=query_payload,
        )
        response.raise_for_status()
        response = response.json()
        if response["status"] == "success":
            query_id = {
                "qid": response["data"],
            }
        else:
            return
    except Exception:
        print(traceback.format_exc())
        return

    # Wait for query to finish
    wait_seconds = 60 * 10
    started = datetime.now()
    finished = False

    while not finished:
        try:
            response = httpx.post(
                f"{ui_url}/creative_status",
                headers={
                    "Content-Type": "application/json",
                },
                data=query_id,
            )
            response.raise_for_status()
            response = response.json()
            if response["status"] == "running":
                running_time = (datetime.now() - started).total_seconds()
                if running_time > wait_seconds:
                    print("Query ran out of time.")
                    return
                # retry after 10 seconds
                time.sleep(10)
            elif response["status"] == "error":
                finished = True
            elif response["status"] == "success":
                finished = True
        except Exception:
            print(traceback.format_exc())
            return

    # Get results
    try:
        response = httpx.post(
            f"{ui_url}/creative_result",
            headers={
                "Content-Type": "application/json",
            },
            data=query_id,
        )
        response.raise_for_status()
        response = response.json()
        results = response["data"]
    except Exception:
        print(traceback.format_exc())
        return

    output_check = output_map.get(expected_output)
    if output_check is None:
        return "Failed."
    # Create assertions list
    assertions = [
        f'.results[:{output_check["n_results"]}][] | .subject {"==" if output_check["good"] else "!="} "{output_curie}"'
    ]
    for assertion in assertions:
        values = jq.compile(assertion).input(results)
        if True in values:
            # test passed
            return "Passed!"
        else:
            return "Fail."
    if debug:
        now = datetime.now().isoformat()
        with open(f"results_{now}.json", "w") as f:
            json.dump(results, f)


if __name__ == "__main__":
    print(run_ui_test())
