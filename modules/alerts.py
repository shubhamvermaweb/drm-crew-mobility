def generate_alerts(df):

    alerts = []

    # ==================================
    # HIGH PRIORITY LOADS
    # ==================================

    if "Priority to improve mobility" in df.columns:

        high = df[
            df["Priority to improve mobility"]
            .astype(str)
            .str.contains(
                "HIGH",
                case=False,
                na=False
            )
        ]

        if len(high):

            alerts.append({
                "type":"high",
                "message":f"{len(high)} High Priority Loads"
            })

    # ==================================
    # LOADS NOT MOVED
    # ==================================

    if "Status of load" in df.columns:

        pending = df[
            ~df["Status of load"]
            .astype(str)
            .str.contains(
                "ON RUN|MADE OVER",
                case=False,
                na=False
            )
        ]

        if len(pending):

            alerts.append({
                "type":"critical",
                "message":f"{len(pending)} Loads Need Attention"
            })

    # ==================================
    # TM NOT PROVIDED
    # ==================================

    tm_cols = [

        c

        for c in df.columns

        if "TM" in c.upper()
    ]

    if tm_cols:

        no_tm = df[
            df[tm_cols[0]]
            .astype(str)
            .str.strip()
            .eq("")
        ]

        if len(no_tm):

            alerts.append({
                "type":"warning",
                "message":f"{len(no_tm)} Loads Without TM"
            })

    # ==================================
    # ALP NOT PROVIDED
    # ==================================

    alp_cols = [

        c

        for c in df.columns

        if "ALP" in c.upper()
    ]

    if alp_cols:

        no_alp = df[
            df[alp_cols[0]]
            .astype(str)
            .str.strip()
            .eq("")
        ]

        if len(no_alp):

            alerts.append({
                "type":"warning",
                "message":f"{len(no_alp)} Loads Without ALP"
            })

    # ==================================
    # LPG NOT PROVIDED
    # ==================================

    lpg_cols = [

        c

        for c in df.columns

        if "LPG" in c.upper()
    ]

    if lpg_cols:

        no_lpg = df[
            df[lpg_cols[0]]
            .astype(str)
            .str.strip()
            .eq("")
        ]

        if len(no_lpg):

            alerts.append({
                "type":"warning",
                "message":f"{len(no_lpg)} Loads Without LPG"
            })

    # ==================================
    # DUTY HOURS ALERT
    # ==================================

    duty_cols = [

        c

        for c in df.columns

        if "Duty" in c
    ]

    if duty_cols:

        try:

            duty_series = (
                df[duty_cols[0]]
                .astype(str)
                .str.extract(r'(\d+)')[0]
                .fillna(0)
                .astype(int)
            )

            over_limit = duty_series[
                duty_series > 10
            ]

            if len(over_limit):

                alerts.append({
                    "type":"critical",
                    "message":
                    f"{len(over_limit)} Crew Above 10 Duty Hours"
                })

        except Exception:
            pass

    # ==================================
    # NO ALERTS
    # ==================================

    if len(alerts) == 0:

        alerts.append({
            "type":"success",
            "message":"No Critical Alerts"
        })

    return alerts