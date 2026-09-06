# SWC2026 — Stack4Things lab demo scripts

Cartella operativa per sessioni live (conferenza / corso).  
Documentazione rete completa: [`../docs/LAB_NETWORK_ACCESS.md`](../docs/LAB_NETWORK_ACCESS.md).

## Credenziali

| Cosa | User / Pass |
|------|-------------|
| Horizon | `admin` / `s4t` |
| Lightning-Rod UI | `me` / `arancino` |
| SSH **dentro** LR (script `01`) | `root` / `arancino` (override `ROOT_PASS`) — **nessuna** porta SSH pubblicata sull'host |

## Ingress host (scegli il tuo)

| Ingress | Esempio |
|---------|---------|
| LAN | `192.168.100.11` |
| Tailscale primary | `100.74.114.23` |
| Tailscale secondary (`lab-secondary`) | `100.123.142.39` |

Imposta `vm-ip.txt` / `S4T_LAB_HOST` di conseguenza. Le demo WoT usano `http://<HOST>/lab-ws/<porta>/`.

## Porte LR (importante)

Dentro **ogni** container Lightning-Rod la dashboard ascolta sempre su **1474**.  
Sull’host ogni board ha una **porta diversa** mappata su quel 1474:

| Board | Container | Apri nel browser |
|-------|-----------|------------------|
| board-alpha | lightning-rod | `http://<HOST>:1474/` |
| board-beta | lightning-rod-2 | `http://<HOST>:1475/` |
| board-gamma | lightning-rod-3 | `http://<HOST>:1476/` |
| board-delta | lightning-rod-4 | `http://<HOST>:1477/` |
| board-epsilon | lightning-rod-5 | `http://<HOST>:1478/` |
| board-zeta | lightning-rod-6 | `http://<HOST>:1479/` |
| board manuali | `lightning-rod-<nome>` | `http://<HOST>:1482+` (assegnata da `01`) |

`:1474` sull’host = **solo alpha**. Per le altre board usa la tabella / `./04-list-lr-dashboards.sh`.

## Script

| Script | Cosa fa |
|--------|---------|
| `00-verify-demo.sh` | Health-check + ripara la demo |
| `01-run-manual-lr.sh` | Crea board IoTronic + avvia LR **senza** registrarla; installa `sshd` in-container |
| `02-destroy-manual-lr.sh` | Rimuove LR (+ `--delete-board`) |
| `03-print-lr-info.sh` | IP / porte / stato di un container |
| `04-list-lr-dashboards.sh` | Elenco board → URL dashboard corretto |
| `env.sh` | Default comuni |

```bash
cd swc2026   # oppure training/swc2026 nell'albero editoriale

./00-verify-demo.sh
./04-list-lr-dashboards.sh

BOARD_NAME=swc-edge-1 ./01-run-manual-lr.sh
# Apri l'URL stampato (es. http://<HOST>:1482/)
# Config: WAMP=wss://crossbar:8181  Code=<stampato>  Hostname=swc-edge-1

./02-destroy-manual-lr.sh --delete-board
```

## Registrazione manuale (dopo `01`)

1. Apri l’URL **host port** stampato dallo script (non usare sempre `:1474`)
2. First-boot Config:
   - **WAMP / urlwagent** = `wss://crossbar:8181` (solo se LR è un container sulla rete Docker)
   - **Code** = registration code stampato
   - **Hostname** = nome board
3. CONFIGURE → in Horizon la board diventa online

Per board **fisiche / esterne** su Tailscale: non usare l’hostname Docker `crossbar` senza `/etc/hosts` — vedi `docs/LAB_NETWORK_ACCESS.md` §5.

## SSH nel container (lab)

Dopo `01`, dalla lab host:

```bash
ssh root@<DOCKER_IP>          # password arancino
# oppure
docker exec -it <CONTAINER> bash
```

Nessun `-p 22:22` sull’host.

## Checklist pre-talk

1. `./00-verify-demo.sh` → `READY`
2. `./04-list-lr-dashboards.sh` → URL chiari per il tuo `<HOST>`
3. Demo WoT: `http://<HOST>/lab-ws/50006/` (ecc.)
4. Metrics / FL / Web Services come da demo
