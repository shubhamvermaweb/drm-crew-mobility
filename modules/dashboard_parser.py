import pandas as pd
import re


def make_unique(headers):

    counter = {}

    new_headers = []

    for idx,h in enumerate(headers):

        h = str(h).strip()

        if (
            h == ""
            or
            h.lower() == "nan"
        ):
            h = f"Column_{idx}"

        if h in counter:

            counter[h] += 1

            h = f"{h}_{counter[h]}"

        else:

            counter[h] = 0

        new_headers.append(h)

    return new_headers


def extract_dataframe(raw):

    if len(raw) < 5:
        return pd.DataFrame()

    headers = make_unique(raw[3])

    rows = raw[4:]

    return pd.DataFrame(
        rows,
        columns=headers
    )


def extract_kpis(raw):

    kpis = {

        "crew_required":0,

        "alp_lpg":0,

        "tm":0,

        "made_over":0,

        "on_run":0,

        "not_moved":0
    }

    try:

        text = " ".join([
            str(cell)
            for row in raw[:3]
            for cell in row
        ])

        numbers = re.findall(
            r'\d+',
            text
        )

        if len(numbers) >= 6:

            kpis["crew_required"] = numbers[0]
            kpis["alp_lpg"] = numbers[1]
            kpis["tm"] = numbers[2]
            kpis["made_over"] = numbers[3]
            kpis["on_run"] = numbers[4]
            kpis["not_moved"] = numbers[5]

    except Exception:
        pass

    return kpis