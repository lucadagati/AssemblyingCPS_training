#!/bin/bash
# Enable FL live dashboard reverse proxy then start Apache (lab overlay).
set -e
a2enmod proxy proxy_http 2>/dev/null || true
if [ -f /etc/apache2/conf-available/fl-live-proxy.conf ]; then
  ln -sf /etc/apache2/conf-available/fl-live-proxy.conf /etc/apache2/conf-enabled/fl-live-proxy.conf
fi
exec apache2ctl -D FOREGROUND
