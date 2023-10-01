# Makefile for automating release tasks

# Get project name from pyproject.toml
PROJECT_NAME=$(shell grep name pyproject.toml | head -n 1 | awk -F= '{print $$2}' | xargs)
# Get the current version using `rye version`
NEW_VERSION=v$(shell rye version)

# Step 1: Create PR
release-step1: gen-docs gen-changelog commit create-pr

gen-docs:
	pdoc --html --output-dir=docs --force $(PROJECT_NAME)
	mv docs/$(PROJECT_NAME)/* docs
	rmdir docs/$(PROJECT_NAME)

gen-changelog:
	git cliff --tag $(NEW_VERSION) -o CHANGELOG.md

commit:
	git add --all
	git commit -m "chore: 🚀 new release setup $(NEW_VERSION)"

create-pr:
	gh pr create --title "$(PROJECT_NAME): New release $(NEW_VERSION)" --body "Release version $(NEW_VERSION)"
	gh pr list --json number,title | jq -r --arg title "$(PROJECT_NAME): New release $(NEW_VERSION)" 'map(select(.title == $$title)) | .[0].number' > pr_id.txt


# Step 2: Merge PR, tag, and cleanup
release-step2: merge-pr pull-main tag-version publish create-dev-branch

merge-pr:
	gh pr merge $(shell cat pr_id.txt) --merge --delete-branch

pull-main:
	@if [ -f pr_id.txt ]; then \
		echo "Removing pr_id.txt"; \
		rm pr_id.txt; \
	fi
	git checkout main
	git pull origin main

tag-version:
	git tag $(NEW_VERSION)
	git push origin $(NEW_VERSION)

publish:
	rye build -c && rye publish

create-dev-branch:
	$(eval NEW_DEV_BRANCH := dev-after-$(NEW_VERSION))
	git checkout -b $(NEW_DEV_BRANCH)
