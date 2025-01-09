# SPDX-FileCopyrightText: © 2008-2022 Oprea Dan
# SPDX-FileCopyrightText: © 2008-2022 Bart de Koning
# SPDX-FileCopyrightText: © 2008-2022 Richard Bailey
# SPDX-FileCopyrightText: © 2008-2022 Germar Reitze
# SPDX-FileCopyrightText: © 2008-2022 Taylor Raak
# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2). See LICENSES directory or go to
# <https://spdx.org/licenses/GPL-2.0-or-later.html>.
from PyQt6.QtWidgets import (QDialog,
                             QGridLayout,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGroupBox,
                             QLabel,
                             QSpinBox,
                             QStyle,
                             QCheckBox,
                             QToolTip,
                             QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
import config
import qttools
from manageprofiles.combobox import BitComboBox
from manageprofiles.statebindcheckbox import StateBindCheckBox
from manageprofiles.spinboxunit import SpinBoxWithUnit


class AutoRemoveTab(QDialog):
    """The 'Auto-remove' tab in the Manage Profiles dialog."""

    _STRETCH_FX = (1, )

    def __init__(self, parent):
        super().__init__(parent=parent)

        self._parent_dialog = parent

        # Vertical main layout
        self._tab_layout = QVBoxLayout(self)
        self.setLayout(self._tab_layout)

        # Icon & Info label
        self._label_rule_execute_order()

        # ---
        self._tab_layout.addWidget(qttools.HLineWidget())

        # Keep named backups
        self.cbDontRemoveNamedSnapshots = self._checkbox_keep_named()

        # Remove older than N years/months/days
        self._checkbox_remove_older, self._spinunit_remove_older \
            = self._remove_older_than()

        # free space less than
        enabled, value, unit = self.config.minFreeSpace()

        self.spbFreeSpace = QSpinBox(self)
        self.spbFreeSpace.setRange(1, 1000)

        MIN_FREE_SPACE_UNITS = {
            config.Config.DISK_UNIT_MB: 'MiB',
            config.Config.DISK_UNIT_GB: 'GiB'
        }
        self.comboFreeSpaceUnit = BitComboBox(self, MIN_FREE_SPACE_UNITS)

        self.cbFreeSpace = StateBindCheckBox(_('If free space is less than:'), self)
        self.cbFreeSpace.bind(self.spbFreeSpace)
        self.cbFreeSpace.bind(self.comboFreeSpaceUnit)

        # min free inodes
        self.cbFreeInodes = QCheckBox(_('If free inodes is less than:'), self)

        self.spbFreeInodes = QSpinBox(self)
        self.spbFreeInodes.setSuffix(' %')
        self.spbFreeInodes.setSingleStep(1)
        self.spbFreeInodes.setRange(0, 15)

        enabled = lambda state: self.spbFreeInodes.setEnabled(state)
        enabled(False)
        self.cbFreeInodes.stateChanged.connect(enabled)

        grid = QGridLayout()

        self._tab_layout.addLayout(grid)

        grid.addWidget(self.cbFreeSpace, 1, 0)
        grid.addWidget(self.spbFreeSpace, 1, 1)
        grid.addWidget(self.comboFreeSpaceUnit, 1, 2)
        grid.addWidget(self.cbFreeInodes, 2, 0)
        grid.addWidget(self.spbFreeInodes, 2, 1)
        grid.setColumnStretch(3, 1)

        self._tab_layout.addSpacing(self._tab_layout.spacing()*2)

        # Smart removal: checkable GroupBox
        self.cbSmartRemove = QGroupBox(_('Smart removal:'), self)
        self.cbSmartRemove.setCheckable(True)
        smlayout = QGridLayout()
        smlayout.setColumnStretch(3, 1)
        self.cbSmartRemove.setLayout(smlayout)
        self._tab_layout.addWidget(self.cbSmartRemove)

        # Smart removal: the items...
        self.cbSmartRemoveRunRemoteInBackground = QCheckBox(
                _('Run in background on remote host.'), self)
        qttools.set_wrapped_tooltip(
            self.cbSmartRemoveRunRemoteInBackground,
            (
                _('The smart remove procedure will run directly on the remote '
                  'machine, not locally. The commands "bash", "screen", and '
                  '"flock" must be installed and available on the '
                  'remote machine.'),
                _('If selected, Back In Time will first test the '
                  'remote machine.')
            )
        )
        smlayout.addWidget(self.cbSmartRemoveRunRemoteInBackground, 0, 0, 1, 2)

        smlayout.addWidget(
            QLabel(_('Keep all snapshots for the last'), self), 1, 0)
        self.spbKeepAll = QSpinBox(self)
        self.spbKeepAll.setRange(1, 10000)
        smlayout.addWidget(self.spbKeepAll, 1, 1)
        smlayout.addWidget(QLabel(_('day(s).'), self), 1, 2)

        smlayout.addWidget(
            QLabel(_('Keep one snapshot per day for the last'), self), 2, 0)
        self.spbKeepOnePerDay = QSpinBox(self)
        self.spbKeepOnePerDay.setRange(1, 10000)
        smlayout.addWidget(self.spbKeepOnePerDay, 2, 1)
        smlayout.addWidget(QLabel(_('day(s).'), self), 2, 2)

        smlayout.addWidget(
            QLabel(_('Keep one snapshot per week for the last'), self), 3, 0)
        self.spbKeepOnePerWeek = QSpinBox(self)
        self.spbKeepOnePerWeek.setRange(1, 10000)
        smlayout.addWidget(self.spbKeepOnePerWeek, 3, 1)
        smlayout.addWidget(QLabel(_('week(s).'), self), 3, 2)

        smlayout.addWidget(
            QLabel(_('Keep one snapshot per month for the last'), self), 4, 0)
        self.spbKeepOnePerMonth = QSpinBox(self)
        self.spbKeepOnePerMonth.setRange(1, 1000)
        smlayout.addWidget(self.spbKeepOnePerMonth, 4, 1)
        smlayout.addWidget(QLabel(_('month(s).'), self), 4, 2)

        smlayout.addWidget(
            QLabel(_('Keep one snapshot per year for all years.'), self),
            5, 0, 1, 3)

        self._tab_layout.addStretch()

    @property
    def config(self) -> config.Config:
        return self._parent_dialog.config

    def load_values(self):
        # remove old snapshots
        enabled, value, unit = self.config.removeOldSnapshots()
        print(f'{enabled=} {value=} {unit=}')
        self._checkbox_remove_older.setChecked(enabled)
        self._spinunit_remove_older.set_value(value)
        self._spinunit_remove_older.select_unit(unit)

        # min free space
        enabled, value, unit = self.config.minFreeSpace()
        self.cbFreeSpace.setChecked(enabled)
        self.spbFreeSpace.setValue(value)
        self.comboFreeSpaceUnit.select_by_data(unit)

        # min free inodes
        self.cbFreeInodes.setChecked(self.config.minFreeInodesEnabled())
        self.spbFreeInodes.setValue(self.config.minFreeInodes())

        # smart remove
        smart_remove, keep_all, keep_one_per_day, keep_one_per_week, \
            keep_one_per_month = self.config.smartRemove()
        self.cbSmartRemove.setChecked(smart_remove)
        self.spbKeepAll.setValue(keep_all)
        self.spbKeepOnePerDay.setValue(keep_one_per_day)
        self.spbKeepOnePerWeek.setValue(keep_one_per_week)
        self.spbKeepOnePerMonth.setValue(keep_one_per_month)
        self.cbSmartRemoveRunRemoteInBackground.setChecked(
            self.config.smartRemoveRunRemoteInBackground())

        # don't remove named snapshots
        self.cbDontRemoveNamedSnapshots.setChecked(
            self.config.dontRemoveNamedSnapshots())

    def store_values(self):
        self.config.setRemoveOldSnapshots(
            self._checkbox_remove_older.isChecked(),
            self._spinunit_remove_older.value(),
            self._spinunit_remove_older.unit()
        )

        self.config.setMinFreeSpace(
            self.cbFreeSpace.isChecked(),
            self.spbFreeSpace.value(),
            self.comboFreeSpaceUnit.current_data)

        self.config.setMinFreeInodes(
            self.cbFreeInodes.isChecked(),
            self.spbFreeInodes.value())

        self.config.setDontRemoveNamedSnapshots(
            self.cbDontRemoveNamedSnapshots.isChecked())

        self.config.setSmartRemove(
            self.cbSmartRemove.isChecked(),
            self.spbKeepAll.value(),
            self.spbKeepOnePerDay.value(),
            self.spbKeepOnePerWeek.value(),
            self.spbKeepOnePerMonth.value())

        self.config.setSmartRemoveRunRemoteInBackground(
            self.cbSmartRemoveRunRemoteInBackground.isChecked())

    def update_items_state(self, enabled):
        self.cbSmartRemoveRunRemoteInBackground.setVisible(enabled)

    def _label_rule_execute_order(self) -> QWidget:
        # Icon
        icon = self.style().standardPixmap(
            QStyle.StandardPixmap.SP_MessageBoxInformation)
        icon = icon.scaled(
            icon.width()*2,
            icon.height()*2,
            Qt.AspectRatioMode.KeepAspectRatio)

        icon_label = QLabel(self)
        icon_label.setPixmap(icon)
        icon_label.setFixedSize(icon.size())

        # Info text
        txt = _(
            'The rules below are processed from top to buttom. Later rules '
            'override earlier ones and are not constrained by them. See the '
            '{manual} for details and examples.'
        ).format(
            manual='<a href="https://commingsoon">{}</a>'.format(
                _('user manual')))
        txt_label = QLabel(txt)
        txt_label.setWordWrap(True)
        txt_label.setOpenExternalLinks(True)

        # Show URL in tooltip without anoing http-protocol prefix.
        txt_label.linkHovered.connect(
            lambda url: QToolTip.showText(
                QCursor.pos(), url.replace('https://', ''))
        )

        wdg = QWidget()
        layout = QHBoxLayout(wdg)
        layout.addWidget(icon_label)
        layout.addWidget(txt_label)

        self._tab_layout.addWidget(wdg)

    def _checkbox_keep_named(self) -> QCheckBox:
        cb = QCheckBox(_('Keep named snapshots.'), self)
        cb.setToolTip(
            _('Snapshots that, in addition to the usual timestamp, have been '
              'given a name will not be deleted.'))

        self._tab_layout.addWidget(cb)

        return cb

    def _remove_older_than(self) -> QWidget:
        layout = QHBoxLayout()
        layout.setStretch(0, self._STRETCH_FX[0])

        # units
        units = {
            config.Config.DAY: _('Day(s)'),
            config.Config.WEEK: _('Week(s)'),
            config.Config.YEAR: _('Year(s)')
        }
        spin_unit = SpinBoxWithUnit(self, (1, 1000), units)

        # checkbox
        checkbox = StateBindCheckBox(_('Older than:'), self)
        checkbox.bind(spin_unit)

        layout.addWidget(checkbox)
        layout.addWidget(spin_unit)

        self._tab_layout.addLayout(layout)

        return checkbox, spin_unit
