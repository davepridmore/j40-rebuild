# Engine Electrical Inputs Reconciliation - 2026-05-17

Evidence source: Google Photos picker run `20260517T230711`.

This intake belongs to the electrical refit. The aim is not to reuse the old engine wiring blindly; it is to identify every engine-side input, reconcile it with the existing wiring master, repair the connector/terminal condition, and only then close the loom.

## Working Rule

No unknown connector gets reconnected by color or memory. Every engine-side wire needs a label, a component endpoint, a dash/relay/fuse endpoint, and a continuity or live-function result before final wrap.

## Identified Inputs

| Input | Photos | Identification | Confidence | Reconcile To |
| --- | --- | --- | --- | --- |
| `EEI-001` | `20260517_204429_gp_yEAcUHBg` | Starter motor main feed, solenoid trigger region, and ground return evidence | High | `HD1`, ignition/start path, WP03B starter interrupt, engine/chassis ground |
| `EEI-002` | `20260517_204740_gp_yI8f8DQw`, `20260517_204756_gp_xdOm3erw` | Alternator charge output/regulator/exciter/sense wiring | High | Main charge lead, charge warning/excite, voltage sense if fitted, regulator wiring |
| `EEI-003` | `20260517_204504_gp_46p1VNCg`, `20260517_204550_gp_kDsqLZQg`, `20260517_204711_gp_jZ4tm3uQ`, `20260517_204725_gp_y7P6qvhQ` | Injection-pump/throttle-linkage electrical input; possible fuel-stop, idle-up, or engine-control function | Medium | WP03B diesel cutoff only after device function is proven |
| `EEI-004` | `20260517_204615_gp_wsn4bN8g`, `20260517_204711_gp_jZ4tm3uQ` | Engine sender branch, probably gauge or warning-lamp related | Medium | WP03 gauges/warning branch and dash cluster wiring |
| `EEI-005` | `20260517_204445_gp_oaQKzDrA` | Unidentified two-wire inline connector | Medium | Hold as `U-01` until continuity and endpoint are known |
| `EEI-006` | `20260517_204538_gp_9CERKvYA`, `20260517_204550_gp_kDsqLZQg` | Loose unassigned engine-side connector | Medium | Hold as `U-02` until continuity and endpoint are known |
| `EEI-007` | `20260517_204550_gp_kDsqLZQg`, `20260517_204711_gp_jZ4tm3uQ`, `20260517_204725_gp_y7P6qvhQ` | Engine input branch route and protection context | Medium | Electrical Master final protection, clips, sleeving, grommets, and strain relief |

The machine-readable reconciliation sheet is `data/manual/engine_electrical_inputs_reconciliation_20260517.csv`.

## Refit Decisions

- Starter: keep as a controlled high-current circuit. Clean the B+ lug path, label the solenoid trigger, prove the starter-interrupt path, and voltage-drop-test both feed and ground during cranking.
- Alternator: read the actual terminal markings before assigning output, excite/warning, sense, regulator, or ground functions. Replace taped or weak terminals and confirm charging voltage and warning-lamp behavior live.
- Injection pump/throttle-linked input: do not assign it to the new diesel cutoff until the device is identified and key-on/key-off behavior is proven. The manual cutoff cable remains the fallback.
- Sender branch: identify the sender by component and behavior, not by wire color. Gauge senders need resistance checks; warning switches need ground-switch behavior checks.
- Unknown connectors: tag as `U-01` and `U-02`, trace both ends, then decide retain/repair/delete.
- Routing: final wrap is blocked until the branch has proper clips, sleeving, heat/oil protection, grommets, and movement clearance from linkage, injector lines, alternator, starter, steering, and exhaust heat.

## Verification Checklist

- Photograph each connector with a temporary label before disturbing it.
- Record terminal markings on the starter solenoid, alternator, and any sender or pump-linked device.
- Continuity-test each lead from engine endpoint to dash, relay, fuse, or loom connector.
- Check key-state voltage in OFF, ACC, RUN, and START for unknown connectors before connection.
- Run starter cranking voltage-drop tests on B+ and ground.
- Run alternator charging voltage and warning-lamp/excite tests after start.
- Confirm diesel key-off shutdown if EEI-003 becomes fuel-stop related.
- Confirm dash gauge or warning-lamp response for EEI-004.
- Update the Electrical Master connector/pin map before final loom wrap.
- Take final labelled photos after repaired terminals, clips, sleeves, and grommets are installed.
