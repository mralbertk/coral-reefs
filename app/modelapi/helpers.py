def param_types(params: dict) -> dict:
    """
    Converts dictionary values of parameters to the
    correct data types for filters to process.
    """
    for param in params:
        match param:
            case "omega" | "t0" | "percent":
                params[param] = float(params[param])
            case "blockSize":
                params[param] = int(params[param])
            case "meanMode":
                params[param] = bool(params[param])
    return params
