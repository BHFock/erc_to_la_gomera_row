def eta(t1=None, t2=None, s1=None, s2=None, s3=None):
    "Estimate arrival time"

    import datetime as dt

    t12 = (t2-t1).total_seconds()
    v12 = (s2-s1) / t12

    # Assume to continue travel with average velocity
    v23 = v12
    t23 = (s3-s2)/v23

    t3 = t2 + dt.timedelta(seconds=t23)

    return t3
