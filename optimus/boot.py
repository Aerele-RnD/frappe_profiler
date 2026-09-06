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
	# One config read supplies both values. The "render durations in seconds
	# above (ms)" threshold lets Desk form scripts (the Optimus Session hot-path
	# picker) roll durations over to seconds at the same point the report does.
	# An explicit 0 (disable the rollover) is preserved; only a missing value
	# falls back to 1000ms. Fails open (widget visible, default threshold).
	try:
		from optimus.settings import get_config
		cfg = get_config()
		bootinfo.optimus_enabled = bool(cfg.enabled)
		_t = cfg.large_duration_threshold_ms
		bootinfo.optimus_large_duration_threshold_ms = float(1000.0 if _t is None else _t)
	except Exception:
		bootinfo.optimus_enabled = True
		bootinfo.optimus_large_duration_threshold_ms = 1000.0
