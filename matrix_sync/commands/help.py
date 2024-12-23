from mcdreforged.api.rtext import RTextList
from ..utils import tr

help_page = RTextList(
    tr("help.title", False) + "\n",
    tr("help.root", False) + "\n",
    tr("help.start", False) + "\n",
    tr("help.stop", False) + "\n",
    tr("help.send", False) + "\n",
    tr("help.status", False) + "\n",
    tr("help.reload.plugin", False) + "\n",
    tr("help.reload.subpack", False) + "\n"
)

help_message = tr("help.message", False)