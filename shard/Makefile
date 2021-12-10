check: test todo

test:
	nose2 --with-coverage

todo:
	@rgrep --include "*.py" "TODO" || True
	@rgrep --include "*.py" "REF" || True
