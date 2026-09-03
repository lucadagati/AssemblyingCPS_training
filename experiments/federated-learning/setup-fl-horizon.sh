#!/usr/bin/env bash
# Enable native "Federated Learning" panel in Horizon IoT sidebar (Module G).
set -euo pipefail

CH13="$(cd "$(dirname "$0")/../../repos/ch13" && pwd)"

echo "=== Install Federated Learning Horizon panel ==="
echo "  Python panel: training/patches/iotronic_ui_lab/"
echo "  Enabled hook: training/patches/horizon-enabled/_6060_iot_federated_learning_panel.py"
echo "  Control API:  fl-control container (:8091)"
echo "  Live topology: /horizon/fl-live/ -> dashboard :8090"

cd "$CH13"
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d fl-control iotronic-ui
echo "Waiting for fl-control (pip install on first start may take 1-2 min)..."
for i in $(seq 1 24); do
  if curl -sf --connect-timeout 2 http://127.0.0.1:8091/health >/dev/null 2>&1; then
    echo "fl-control ready after $((i * 5))s"
    break
  fi
  sleep 5
done

if docker exec iotronic-ui test -f /usr/share/openstack-dashboard/openstack_dashboard/enabled/_6060_iot_federated_learning_panel.py; then
  echo "OK — panel enabled file mounted"
else
  echo "WARN — enabled file not found in container"
fi

if docker exec iotronic-ui test -f /usr/local/lib/python2.7/dist-packages/iotronic_ui_lab/iot/federated_learning/views.py; then
  echo "OK — iotronic_ui_lab panel code mounted"
else
  echo "WARN — panel Python package not mounted"
fi

echo ""
echo "Open Horizon -> IoT -> Federated Learning"
echo "  http://<VM_IP>/horizon/iot/federated_learning/"
echo ""
echo "Workflow: Lab parameters -> Create plugin fl-client -> Inject -> Start server -> Start all clients"
echo ""
echo "Optional — pre-create & inject fl-client on online boards (demo-ready):"
echo "  cd training && ./experiments/federated-learning/setup-fl-demo-plugins.sh"
echo ""
echo "CLI fallback: ./experiments/federated-learning/fl-server-ctl.sh start|stop|restart"
