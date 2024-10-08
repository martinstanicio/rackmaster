import gettext

# Run the following commansd to generate the translation files:
# python -c "import polib; polib.pofile('locales/es/LC_MESSAGES/base.po').save_as_mofile('locales/es/LC_MESSAGES/base.mo')"
# python -c "import polib; polib.pofile('locales/en/LC_MESSAGES/base.po').save_as_mofile('locales/en/LC_MESSAGES/base.mo')"

lang = gettext.translation("base", localedir="locales", languages=["es", "en"])
lang.install()
t = lang.gettext
