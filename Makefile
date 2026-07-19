.PHONY: verify verify-external verify-native paper

verify:
	.venv/bin/pytest -q
	.venv/bin/ruff check src tests scripts
	.venv/bin/mypy src
	.venv/bin/python -c "from pathlib import Path; from rule_carryover.artifact_verify import verify_repository_artifacts; print(verify_repository_artifacts(Path.cwd()))"

verify-external:
	.venv/bin/python -c "from pathlib import Path; from rule_carryover.artifact_verify import verify_repository_artifacts; print(verify_repository_artifacts(Path.cwd(), require_external_artifacts=True))"

verify-native:
	.venv-mlx/bin/python -m pytest -q

paper:
	.venv/bin/python scripts/build_working_note_pdf.py \
		--source paper/working-note-v1.md \
		--output output/pdf/context-carryover-feasibility-note-v1.pdf
