def parse_time(duration: int) -> str:
    """
    Converts a duration in seconds to hours (if more than 1), minutes, and seconds.

    Parameters
    ----------
    duration : int
        The amount of time in seconds.


    Returns
    -------
    str
        The amount of time in to hours (if more than 1), minutes, and seconds.
    """
    h = str(duration // 3600)
    m = str((duration % 3600) // 60)
    s = str(duration - (int(h) * 3600 + int(m) * 60))

    h = f"0{h}" if not len(h)-1 else h
    m = f"0{m}" if not len(m)-1 else m
    s = f"0{s}" if not len(s)-1 else s

    return f"{h}:{m}:{s}" if duration % 3600 != 0 else f"{m}:{s}"


def parse_size(size: int) -> str:
    """
    Converts filesize in bytes to megabytes.

    Parameters
    ----------
    size : int
        The size of the file bytes.


    Returns
    -------
    str
        The size in megabytes, with the "MB" suffix.   
    """
    return f"{round(size / 1000000, 2)} MB" if size % 1000000 == 0 else f"{round(size / 1000000000, 2)} GB"