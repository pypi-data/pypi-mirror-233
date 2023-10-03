import os
import re


class MdDB:
    def __init__(self, path=None):
        self.path = path or os.path.join(os.getcwd(), "mdb")
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def create(self, dictionary, filename, level=1):
        md = self._dict_to_md(dictionary, level)
        try:
            with open(os.path.join(self.path, filename), "w") as f:
                f.write(md)
        except Exception as e:
            print(f"An error occurred: {e}")
        return md

    def _dict_to_md(self, dictionary, level):
        md = ""
        for key, value in dictionary.items():
            md += level * "#" + " " + str(key) + "\n"
            if isinstance(value, dict):
                md += self._dict_to_md(value, level + 1)
            else:
                md += str(value) + "\n"
        return md

    def read(self, filename):
        with open(os.path.join(self.path, filename), "r") as f:
            lines = f.readlines()
        return self._md_to_dict(lines)

    def _md_to_dict(self, lines):
        d = {}
        key = None
        value = []
        for line in lines:
            match = re.match(r"(#+) (.*)", line)
            if match:
                if key is not None:
                    d[key] = (
                        "\n".join(value).strip()
                        if "\n" not in value
                        else self._md_to_dict(value)
                    )
                level, key = len(match.group(1)), match.group(2)
                value = []
            else:
                value.append(line.strip())
        if key is not None:
            d[key] = (
                "\n".join(value).strip()
                if "\n" not in value
                else self._md_to_dict(value)
            )
        return d
