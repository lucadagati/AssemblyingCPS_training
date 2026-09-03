#!/usr/bin/env bash
# Create shared FL client plugin and inject on online boards (Cap. 19 lab).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PLUGIN="${ROOT}/experiments/federated-learning/fl_client_plugin.py"
PLUGIN_NAME="${FL_SHARED_PLUGIN:-fl-client}"

if [[ ! -f "$PLUGIN" ]]; then
  echo "Missing plugin source: $PLUGIN" >&2
  exit 1
fi

echo "=== FL shared plugin (${PLUGIN_NAME}) ==="

docker exec iotronic-ui python2.7 -c "
import cPickle, json, urllib2
PLUGIN_PATH = '/opt/fl_lab/fl_client_plugin.py'
NAME = '${PLUGIN_NAME}'
CSV = {
    'board-alpha': '/opt/fl/machine_1.csv',
    'board-beta': '/opt/fl/machine_2.csv',
    'board-gamma': '/opt/fl/machine_3.csv',
}
body = json.dumps({'auth': {'identity': {'methods': ['password'], 'password': {'user': {'name': 'admin', 'domain': {'name': 'Default'}, 'password': 's4t'}}}, 'scope': {'project': {'name': 'admin', 'domain': {'name': 'Default'}}}}})
r = urllib2.urlopen(urllib2.Request('http://keystone:5000/v3/auth/tokens', body, {'Content-Type': 'application/json'}))
token = r.info().get('X-Subject-Token')
from iotronicclient.v1 import client
c = client.Client(token=token, endpoint='http://iotronic-conductor:8812/v1/')
code = open(PLUGIN_PATH).read().encode('ascii', 'replace').decode('ascii')
pickled = cPickle.dumps(str(code))
plugins = dict((p.name, p.uuid) for p in c.plugin.list(all_plugins=True))
if NAME in plugins:
    c.plugin.update(plugins[NAME], {'name': NAME, 'public': True, 'callable': False, 'code': pickled})
    plugin_id = plugins[NAME]
    print('[update]', NAME)
else:
    p = c.plugin.create(name=NAME, public=True, callable=False, code=code, parameters={})
    plugin_id = p.uuid
    print('[create]', NAME, plugin_id[:8])
boards = dict((b.name, b.uuid) for b in c.board.list() if b.status == 'online')
for board_name, board_id in sorted(boards.items()):
    try:
        c.plugin_injection.plugin_inject(board_id, plugin_id, False)
        print('[inject]', NAME, '->', board_name, '(csv', CSV.get(board_name, 'default') + ')')
    except Exception as exc:
        print('[inject-fail]', board_name, exc)
print('OK')
"
