check: test todo

test:
	nose2 --with-coverage

todo:
	@rgrep --include "*.py" "TODO" --exclude-dir "env" || true
	@rgrep --include "*.py" "REF" --exclude-dir "env" || true
