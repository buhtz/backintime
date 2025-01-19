<!--
SPDX-FileCopyrightText: © 2025 Christian Buhtz <c.buhtz@posteo.jp>

SPDX-License-Identifier: GPL-2.0-or-later

This file is part of the program "Back In Time" which is released under GNU
General Public License v2 (GPLv2). See LICENSES directory or go to
<https://spdx.org/licenses/GPL-2.0-or-later.html>
-->
# Remove & Retention

Bestehende Backups können, gesteuert durch Regeln, automatisch entfernt bzw.
behalten werden. Die Regeln erlauben eine feingranuliertes Ausdünnen des Backup
Archivs und reduzieren damit den Verbrauch an Speicherplatz. Die Funktion wird
am Ende jedes Backup-Durchlaufs (JEDER oder nur bei Änderungen!???) ausgeführt.

- Year: Calculation is based on 12 months. Current months is ignored. Older
than two years, at date 2025-04-17, result in removing backups before (or
older than) 2023-04-01.
- Week: Calculation is based on calendar weeks with Monday as first day of a
week. Current week is ignored. Older than two weeks, at Friday 2025-08-29,
result in removing backups before (or older than) Monday 2025-08-11.
- Day: Calculation is based on full days ignoring time at day. Current day is
ignored. Older than 3 days, at date 2025-01-10, result in removing backups
before (or older than) 2025-01-07.

!!! note
    The feature was also known as _Auto-remove_ or _Smart Remove_ in erlier
    versions of _Back In Time_ (prior to 1.6.0).

# Notizen
- Remove_retention auch ausgeführt, wenn kein neues Backup (wegen
  fehlender Änderungen) angelegt wird.
- Das gerade angefertigte Backup (`new_snaphshot`) wird ignoriert und nicht
  gelöscht. Siehe `listSnapshots()` und den default Wert `False` für
  `includeNewSnapshot`.
- _Remove snapshots older than_ : Ist nur ein Backups in der Liste wird er
  nicht gelöscht. In Verbindung mit dem vorherigen Punkt
  (`includeNewSnapshot=False`) bleiben also immer mind. zwei Backups erhalten.
