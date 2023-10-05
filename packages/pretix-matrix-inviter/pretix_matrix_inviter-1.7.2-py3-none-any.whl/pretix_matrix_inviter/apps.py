from django.utils.translation import gettext_lazy

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    name = "pretix_matrix_inviter"
    verbose_name = "pretix Matrix inviter"

    class PretixPluginMeta:
        name = gettext_lazy("Matrix inviter")
        author = "Felix Schäfer"
        description = gettext_lazy("Invite participants to a Matrix Room or Space.")
        visible = True
        version = __version__
        category = "FEATURE"
        compatibility = "pretix>=2.7.0"

    def ready(self):
        from . import signals  # NOQA
