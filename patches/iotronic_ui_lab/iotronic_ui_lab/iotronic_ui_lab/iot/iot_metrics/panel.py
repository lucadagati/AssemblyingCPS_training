# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

import horizon

from iotronic_ui.iot import dashboard


class IotMetrics(horizon.Panel):
    name = _("Metrics")
    slug = "iot_metrics"


_panels = list(dashboard.Iot.panels)
if "iot_metrics" not in _panels:
    try:
        idx = _panels.index("federated_learning") + 1
        _panels.insert(idx, "iot_metrics")
    except ValueError:
        try:
            idx = _panels.index("plugins") + 1
            _panels.insert(idx, "iot_metrics")
        except ValueError:
            _panels.append("iot_metrics")
    dashboard.Iot.panels = _panels

dashboard.Iot.register(IotMetrics)
