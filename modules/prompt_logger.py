import json
import os
from datetime import datetime


LOG_FILE = "output/prompt_log.json"


def save_prompt_log(
    page_number,
    prompt,
    issue,
    solution,
    iteration
):

    os.makedirs(
        "output",
        exist_ok=True
    )

    entry = {

        "timestamp":
            datetime.now().isoformat(),

        "page":
            page_number,

        "iteration":
            iteration,

        "prompt":
            prompt,

        "issue":
            issue,

        "solution":
            solution
    }

    logs = []

    if os.path.exists(LOG_FILE):

        try:

            with open(
                LOG_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                logs = json.load(file)

        except:

            logs = []

    logs.append(entry)

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            logs,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_prompt_logs():

    if not os.path.exists(
        LOG_FILE
    ):

        return []

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except:

        return []