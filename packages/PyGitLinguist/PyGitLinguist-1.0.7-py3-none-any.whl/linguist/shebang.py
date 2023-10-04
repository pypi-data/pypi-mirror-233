import re
from linguist.language import Language


class Shebang:
    @staticmethod
    def call(blob, candidates):
        if blob.symlink:
            return []
        interpreter = Shebang.interpreter(blob.data)
        languages = Language.find_by_interpreter(interpreter)
        return list(set(candidates) & set(languages)) if candidates else languages

    @staticmethod
    def interpreter(data):
        lines = data.split("\n")
        if not lines:
            return None

        first_line = lines[0]

        if not first_line.startswith("#!"):
            return None

        shebang = first_line[2:].strip()

        # Split shebang line into parts and handle cases like '/usr/bin/env python3 -u'
        parts = re.split(r'\s+', shebang)
        script = parts[0]

        if script == '/usr/bin/env':
            # Handle '/usr/bin/env python3 -u' case
            if len(parts) > 1:
                script = parts[1]

        # Remove version suffix like 'python3.8' -> 'python3'
        script = re.sub(r'\.\d+$', '', script)
        return script
