# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

__author__ = "Liyuan Liu"

__maintainer__ = "Liyuan Liu"
__email__ = "llychinalz@gmail.com"

from .sparsemixer import SparseMixer
from .switchgate import SwitchGate

router_map = {
    'sparsemixer': SparseMixer, 
    'switchgate': SwitchGate
}

def get_router(name):
    raise NotImplementedError("implementation under release review, will release asap, stay tuned!")
