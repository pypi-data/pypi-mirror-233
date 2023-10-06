import logging
import pickle
from pathlib import Path

import numpy as np
from astropy.io import fits
from pkg_resources import resource_filename
from heinlein.dtypes import mask
from heinlein.dtypes.handlers.handler import Handler
from heinlein.locations import BASE_DATASET_CONFIG_DIR
import json

def setup(self, *args, **kwargs):
    self._regions = load_regions()


def load_regions():
    fname = resource_filename("heinlein_cfht", "regions.reg")
    with open(fname, "rb") as f:
        regions = pickle.load(f)
        return regions
def load_config():
    fname = resource_filename("heinlein_cfht", "config.json")
    with open(fname, "rb") as f:
        config = json.load(f)
    return config

class MaskHandler(Handler):
    def __init__(self, path: Path, config: dict, *args, **kwargs):
        super().__init__(path, config, "mask")

    def get_data(self, regions, *args, **kwargs):
        known_masks = self._project.list("data/mask")["files"]

        output = {}
        super_region_names = list(set([n.split("_")[0] for n in regions]))
        regions_ = {
            n: list(filter(lambda x: x.startswith(n), regions))
            for n in super_region_names
        }
        for name in super_region_names:
            matches = list(filter(lambda x: name in x, known_masks))
            if len(matches) > 1:
                logging.error(f"Error: Found more than one mask for region {name}")
                continue
            elif len(matches) == 0:
                logging.error(f"Found no masks for region {name}")
                continue

            path = self._project.get(f"data/mask/{matches[0]}")
            data = fits.open(path)
            out = np.empty(1, dtype="object")
            out[0] = data
            mask_obj = mask.Mask(out, pixarray=True, **self._config)
            output.update({n: mask_obj for n in regions_[name]})
        return output

    def get_data_object(self, data, *args, **kwargs):
        ids = [id(d) for d in data.values()]
        n_unique = len(set(ids))
        storage = np.empty(n_unique, dtype=object)
        found = []
        i = 0
        for value in data.values():
            if id(value) not in found:
                storage[i] = value
                found.append(id(value))
                i += 1
        return storage[0].append(storage[1:])
