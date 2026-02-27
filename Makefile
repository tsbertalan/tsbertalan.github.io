all:
	cp ../Job\ Search/Resume/artifacts/TomBertalan-Resume-NA-F75B0A9.pdf ./resume_TomBertalan.pdf
	bash make.sh

clean-generated:
	@if [ -f .generated_dirs ]; then \
		echo "Cleaning previously generated directories..."; \
		while IFS= read -r dir; do \
			if [ -d "$$dir" ]; then \
				echo "Removing $$dir"; \
				rm -rf "$$dir"; \
			fi \
		done < .generated_dirs; \
		rm -f .generated_dirs; \
	else \
		echo "No .generated_dirs file found, skipping clean."; \
	fi

list-generated:
	@if [ -f .generated_dirs ]; then \
		echo "Generated directories:"; \
		cat .generated_dirs; \
	else \
		echo "No .generated_dirs file found. Run 'make' first."; \
	fi

view:
	xdg-open index.html

.PHONY: all clean-generated list-generated view
