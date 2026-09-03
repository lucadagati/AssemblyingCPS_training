# -*- coding: utf-8 -*-
# Licensed under the Apache License, Version 2.0 (the "License").

from django.utils.translation import ugettext_lazy as _

import horizon

from iotronic_ui.iot import dashboard


class FederatedLearning(horizon.Panel):
    name = _("Federated Learning")
    slug = "federated_learning"


_panels = list(dashboard.Iot.panels)
if "federated_learning" not in _panels:
    try:
        idx = _panels.index("plugins") + 1
        _panels.insert(idx, "federated_learning")
    except ValueError:
        _panels.append("federated_learning")
    dashboard.Iot.panels = _panels

dashboard.Iot.register(FederatedLearning)
