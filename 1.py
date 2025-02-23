from IPython.terminal.embed import InteractiveShellEmbed  # type: ignore # noqa
from traitlets.config import Config  # type: ignore


def create_ipshell() -> InteractiveShellEmbed:
    c = Config()
    c.InteractiveShellEmbed.colors = 'Linux'
    c.PrefilterManager.multi_line_specials = True
    ipshell = InteractiveShellEmbed(config=c)  # noqa
    ipshell.magic('load_ext autoreload')
    ipshell.magic('autoreload 2')
    ipshell.log.info('Ipython autoreload is included')
    return ipshell
