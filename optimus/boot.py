# Copyright (c) 2026, Optimus contributors
# For license information, please see license.txt

"""Boot-session hook.

Runs once per Desk session init (before any page renders) to attach
``optimus_enabled`` to ``frappe.boot``. The floating widget reads
this value synchronously to decide whether to mount itself so a
site admin toggling ``Optimus Settings ▸ Profiler Enabled`` off
hides the widget on the next Desk load, without needing a separate
HTTP round-trip to the settings endpoint.
"""


def boot_session(bootinfo):
	"""Attach profiler config to frappe.boot.

	Fails open on ANY error reading settings, we default the widget
	to visible. A misconfigured settings read should never hide the
	widget entirely (that would silently break the primary UI without
	explanation). The site admin can still disable via the DocType
	directly.
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
