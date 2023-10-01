class PluginNotFoundError(FileNotFoundError):
    ...

class PluginExistsError(FileExistsError):
    ...

class PluginInstallFailedError(RuntimeError):
    ...

class PluginUninstallFailedError(RuntimeError):
    ...