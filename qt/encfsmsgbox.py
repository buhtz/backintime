# SPDX-FileCopyrightText: © 2024 Christian BUHTZ <c.buhtz@posteo.jp>
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This file is part of the program "Back In Time" which is released under GNU
# General Public License v2 (GPLv2). See LICENSES directory or go to
# <https://spdx.org/licenses/GPL-2.0-or-later.html>.
"""Message box warning about EncFS deprecation.

See #1734 and #1735 for details
"""
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QLabel, QToolTip, QMessageBox
from bitbase import URL_ENCRYPT_TRANSITION


class _EncfsWarningBase(QMessageBox):
    """Base clase for Warning boxes in context of EncFS decprecation.
    """

    def __init__(self, parent, text, informative_text):
        super().__init__(parent)

        self.setWindowTitle(_('Warning'))
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText(text)
        self.setInformativeText(informative_text)

        # Set link tooltips (via hovering) on the QLabels
        for label in self.findChildren(QLabel):
            label.linkHovered.connect(
                lambda url: QToolTip.showText(
                    QCursor.pos(), url.replace('https://', '')))


class EncfsCreateWarning(_EncfsWarningBase):
    """Warning box when using EncFS encrypting while creating a new profile
    or modify an existing one.
    """

    def __init__(self, parent):
        text = _('EncFS profile creation will be removed in the next minor '
                 'release (1.7), scheduled for 2026.')
        text = text + ' ' + _('It is not recommended to use that '
                              'mode for a profile furthermore.')
        whitepaper = f'<a href="{URL_ENCRYPT_TRANSITION}">' \
            + _('whitepaper') + '</a>'

        informative_text = _('Support for EncFS is being discontinued due '
                             'to security vulnerabilities.')
        informative_text = informative_text + ' ' + _(
            'For more details, including potential alternatives, please refer '
            'to this {whitepaper}.').format(
                whitepaper=whitepaper)

        super().__init__(parent, text, informative_text)


class EncfsExistsWarning(_EncfsWarningBase):
    """Warning box when encrypted profiles exists.
    """

    def __init__(self, parent, profiles):
        # DevNote: Code looks ugly because we need to take the needs of
        # translators into account. Also the limitations of Qt's RichText
        # feature need to be considered.
        text = ' '.join([
            _('EncFS profile creation will be removed in the next minor '
              'release (1.7), scheduled for 2026.'),
            _('It is not recommended to use that mode for a '
              'profile furthermore.')
        ])

        profiles = '<ul>' \
            + ''.join(f'<li>{profile}</li>' for profile in profiles) \
            + '</ul>'

        whitepaper = f'<a href="{URL_ENCRYPT_TRANSITION}">' \
            + _('whitepaper') + '</a>'

        info_paragraphs = (
            _('The following profile(s) use encryption with EncFS:'),
            profiles,
            ' '.join([
                _('Support for EncFS is being discontinued due '
                  'to security vulnerabilities.'),
                _('A replacement is planned, but it cannot be guaranteed that '
                  'it will arrive on time.')]),
            _('Users are invited to join this discussion. Updated details '
              'on the next steps are available in this {whitepaper}.').format(
                  whitepaper=whitepaper),
            _('This message will not be shown again. This dialog is '
              'available at any time via the help menu.'),
            _('Your Back In Time Team')
        )

        informative_text = ''.join(
            [f'<p>{par}</p>' for par in info_paragraphs])

        super().__init__(parent, text, informative_text)
