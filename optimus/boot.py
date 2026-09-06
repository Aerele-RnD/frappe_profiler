# Copyright (c) 2026, Optimus contributors
# For license information, please see license.txt

"""Boot-session hook: attach ``optimus_enabled`` to ``frappe.boot`` once per
Desk session init. The floating widget reads it synchronously to decide whether
to mount, so toggling ``Profiler Enabled`` off hides the widget on the next
Desk load without a separate settings request.
"""


def boot_session(bootinfo):
	"""Attach profiler config to frappe.boot. Fails open (widget visible) on any
	error reading settings, so a misconfigured read never hides the widget
	entirely; the admin can still disable it via the DocType.
	"""
	try:
		from optimus.settings import is_enabled
		bootinfo.optimus_enabled = bool(is_enabled())
	except Exception:
		bootinfo.optimus_enabled = True
	# The "render durations in seconds above (ms)" threshold, so Desk form
	# scripts (the Optimus Session hot-path picker) roll durations over to
	# seconds at the same point the report does. Fails open to 1000ms.
	try:
		from optimus.settings import get_config
		bootinfo.optimus_large_duration_threshold_ms = float(
			get_config().large_duration_threshold_ms or 1000.0
		)
	except Exception:
		bootinfo.optimus_large_duration_threshold_ms = 1000.0
