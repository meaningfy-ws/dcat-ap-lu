SHELL=/bin/bash -o pipefail

BUILD_PRINT = \e[1;34m
END_BUILD_PRINT = \e[0m

ICON_DONE = [✔]
ICON_ERROR = [x]
ICON_WARNING = [!]
ICON_PROGRESS = [-]

TEST_DIR = tests

#-----------------------------------------------------------------------------
# Dev commands
#-----------------------------------------------------------------------------
install: check-uv
	@ echo "Installing dependencies using uv..."
	@ uv sync

check-uv:
	@ command -v uv >/dev/null 2>&1 || { \
		echo "uv not found. Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}

test:
	@ echo "Running tests..."
	@ uv run pytest $(TEST_DIR)
