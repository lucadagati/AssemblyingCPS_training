# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

import horizon

from iotronic_ui.iot import dashboard


class IotWot(horizon.Panel):
    name = _("Web Services")
    slug = "iot_wot"


_panels = list(dashboard.Iot.panels)

# Drop the empty upstream webservices panel slug
if "webservices" in _panels:
    _panels.remove("webservices")

# Insert iot_wot in place of webservices (after 'services')
if "iot_wot" not in _panels:
    try:
        idx = _panels.index("services") + 1
        _panels.insert(idx, "iot_wot")
    except ValueError:
        _panels.append("iot_wot")

dashboard.Iot.panels = tuple(_panels)
dashboard.Iot.register(IotWot)
