set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# Prepare the historical Python/Qiskit environment and open the live demo.
start:
    #!/usr/bin/env bash
    set -euo pipefail

    if ! command -v uv >/dev/null 2>&1; then
        echo "uv is required. Install it with: brew install uv" >&2
        exit 1
    fi

    venv_python=".venv/bin/python"
    if [[ ! -x "$venv_python" ]]; then
        uv venv --seed --python 3.9 .venv
    fi

    requirements_hash="$(python3 -c 'import hashlib, pathlib; print(hashlib.sha256(pathlib.Path("requirements.txt").read_bytes()).hexdigest())')"
    marker=".venv/.quantum-bb84-requirements"
    installed_hash="$(test -f "$marker" && tr -d '\n' < "$marker" || true)"

    if [[ "$installed_hash" != "$requirements_hash" ]]; then
        uv pip install --python "$venv_python" \
            pip==21.3.1 setuptools==63.1.0 wheel==0.37.1

        if [[ "$(uname -s)" == "Darwin" && "$(uname -m)" == "arm64" ]]; then
            if ! "$venv_python" -c 'import tweedledum' >/dev/null 2>&1; then
                "$venv_python" -m pip install \
                    scikit-build==0.15.0 'cmake<4' ninja
                "$venv_python" -m pip install --no-build-isolation \
                    'git+https://github.com/boschmitt/tweedledum.git@v1.1.1'
            fi
        fi

        "$venv_python" -m pip install -r requirements.txt
        printf '%s\n' "$requirements_hash" > "$marker"
    fi

    if [[ "$(uname -s)" == "Darwin" && -d "/Applications/Brave Browser.app" ]]; then
        export BROWSER='open -a "Brave Browser" %s'
    fi

    extra_args=()
    if [[ -n "${JUPYTER_ARGS:-}" ]]; then
        read -r -a extra_args <<< "$JUPYTER_ARGS"
    fi

    exec .venv/bin/jupyter notebook demo.ipynb "${extra_args[@]}"
