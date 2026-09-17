from pathlib import Path

root = Path(__file__).resolve().parents[2] / "manpage"
source = Path(__file__).resolve().parents[1] / "docs" / "manpage.src"
makefile_path = Path(__file__).with_name("Makefile")

root.write_text(source.read_text())
try:
    exec(compile((Path(__file__).with_name("setup_base.py")).read_text(), str(Path(__file__).with_name("setup_base.py")), "exec"))
finally:
    if root.exists():
        root.unlink()

text = makefile_path.read_text()
old = '''specs.1.gz: ../../manpage\n\tcp ../../manpage specs.1\n\tgzip specs.1'''
new = '''$(DOCS_DIR)/manpage: $(DOCS_DIR)/manpage.src $(EXE_DIR)/specs\n\t$(EXE_DIR)/specs -i $(DOCS_DIR)/manpage.src -o $(DOCS_DIR)/manpage -f $(DOCS_DIR)/resources/manpage_prepare\n\nspecs.1.gz: $(DOCS_DIR)/manpage\n\tcp $(DOCS_DIR)/manpage specs.1\n\tgzip specs.1'''
if old not in text:
    raise SystemExit("generated manpage rule not found")
text = text.replace(old, new)
text = text.replace('$(DOCS_DIR)/guidebook_tmp.md $(DOCS_DIR)/guidebook.pdf', '$(DOCS_DIR)/guidebook_tmp.md $(DOCS_DIR)/guidebook.pdf $(DOCS_DIR)/manpage')
makefile_path.write_text(text)
