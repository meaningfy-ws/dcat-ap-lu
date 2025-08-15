ifeq ($(OS),Windows_NT)
    SHELL := powershell.exe
    .SHELLFLAGS := -NoProfile -Command
    CHECK_UV := if (!(Get-Command uv -ErrorAction SilentlyContinue)) { \
        Write-Host "uv not found. Installing uv..."; \
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"; \
        $$env:Path = "C:\Users\$$env:USERNAME\.local\bin;$$env:Path"; \
    }
else
    SHELL := /bin/bash -o pipefail
    CHECK_UV := command -v uv >/dev/null 2>&1 || { \
        echo "uv not found. Installing uv..."; \
        curl -LsSf https://astral.sh/uv/install.sh | sh; \
    }
endif

TEST_DIR = tests

#-----------------------------------------------------------------------------
# Dev commands
#-----------------------------------------------------------------------------
install: check-uv
	@ echo "Installing dependencies using uv..."
	@ uv sync

check-uv:
	@ $(CHECK_UV)

test:
	@ echo "Running tests..."
	@ uv run pytest $(TEST_DIR)
