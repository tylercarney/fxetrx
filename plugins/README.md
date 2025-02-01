Direcory with default plugin(s) for fxetrx.
Besides core functionality, everything is (or could be) a plugin.
Your imagination is the limit.
Plugins can access secrets stored with keyring (TODO: flesh out how to manage that when some things may be running as a service account and some things as your daily driver user account.
Most Plugins will probably be Python modules with an extra manifest file describing the plugin contents, its dependencies, where it came from, and whatever other metadata we decide on later.
