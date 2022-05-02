import logging as log
import re

from utils.caller import call


def load(name, config, separator="_", **kw):

    prefix = f"{name}{separator}"

    mod_fn = getattr(config, f"{prefix}fn")
    log.info(f"Building {name} from config")
    for k, v in vars(config).items():
        if k.startswith(f"{prefix}") and k != f"{prefix}fn":
            k = re.sub(f"{prefix}", "", k)
            if k not in kw:
                kw[k] = v

    mod = call(mod_fn)

    for k, v in kw.items():
        if isinstance(v, list):
            log.info(f" >> {k} is a list with len({k})= {len(v)}")
            log.info("  >> [")
            for vv in v[:10]:  # just print the first few elements
                log.info(f"    {vv},")
            if len(v) > 10:
                log.info("    ...")
            log.info(" ]")
        elif isinstance(v, dict):
            log.info(f" >> {k} is a dict with len({k})= {len(v)}")
            log.info("  >> {")
            for kk, vv in list(v.items())[:10]:  # just print a few elements
                log.info(f"    {kk}= {vv},")
            if len(v.items()) > 10:
                log.info("    ...")
            log.info(" }")
        else:
            log.info(f" >> {k}= {v}")

    return mod(**kw)


# import logging as log
# import re
# import inspect

# from utils.caller import call


# def load(name, config, **kw):

#   mod = call(getattr(config, f"{name}_fn"))

#   log.info(f"Building {name} from config")
#   for k, v in vars(config).items():
#     if k.startswith(f"{name}") and not k.endswith("_fn"):
#       k = re.sub(f"{name}_", "", k)
#       if k not in kw:
#         kw[k] = v

#   valid = list(inspect.signature(mod).parameters)
#   log.info(f"valid= {valid}")
#   invalid = [k for k in kw if k not in valid]

#   if len(invalid) > 0:
#     raise ValueError(f"invalid keywords found {invalid}")

#   return mod(**kw)
