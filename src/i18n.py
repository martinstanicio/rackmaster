import gettext

localedir = "locales"
languages = ["es", "en"]


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
