import arel

from . import content

hotreload = arel.HotReload("./content", on_reload=[content.load_content])
