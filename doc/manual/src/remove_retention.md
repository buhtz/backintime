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

!!! note
    The feature was also known as _Auto-remove_ or _Smart Remove_ in erlier
    versions of _Back In Time_ (prior to 1.6.0).

