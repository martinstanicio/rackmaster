import gettext
import sys
from os import path

languages = ["es", "en"]

try:
    bundledir = getattr(sys, "_MEIPASS")
except AttributeError:
    localedir = "locales"
else:
    localedir = path.abspath(path.join(bundledir, "locales"))


def main() -> None:
    import polib

    for language in languages:
        inpath = f"{localedir}/{language}/LC_MESSAGES/base.po"
        outpath = f"{localedir}/{language}/LC_MESSAGES/base.mo"

        polib.pofile(inpath).save_as_mofile(outpath)


if __name__ == "__main__":
    main()

lang = gettext.translation("base", localedir, languages)
lang.install()
t = lang.gettext
