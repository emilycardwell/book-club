# PACKAGES
reinstall_package:
	@pip uninstall -y bookclub || :
	@pip install -e .


# COMMANDS
run_api_get_results:
	python -c 'from book-club.app import api_get_results; api_get_results()'

build_docker_local_dev:
	docker build --tag={GCR_IMAGE}:dev .

build_docker_gcp_dev:
	docker build --tag {GCR_MULTI_REGION}/{GCP_PROJECT}/{GCR_IMAGE}:dev .

run_docker_local_dev:
	docker run -it -e PORT=8000 -p 8000:8000 {GCR_IMAGE}:dev

push_docker_gcp_dev:
	docker push {GCR_MULTI_REGION}/{GCP_PROJECT}/{GCR_IMAGE}:dev .


# TESTS
test_gcp_setup:
	@TEST_ENV=development pytest \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_key_env \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_key_path \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_code_get_project

test_gcp_project:
	@TEST_ENV=development pytest \
	tests/setup/test_gcp_setup.py::TestGcpSetup::test_setup_project_id

test_api: test_api_root test_api_get_results

test_api_root:
	TEST_ENV=development pytest tests/api -k 'test_root' --asyncio-mode=strict -W "ignore"

test_api_get_results:
	TEST_ENV=development pytest tests/api -k 'test_get_results' --asyncio-mode=strict -W "ignore"


# LOCAL ENVIRONMENT
show_env:
		@echo "\nEnvironment variables used by the \`bookclub\` package loaded by \`direnv\` from your \`.env\` located at:"
	@echo ${DIRENV_DIR}

	@echo "\n$(ccgreen)local storage:$(ccreset)"
	@env | grep -E "LOCAL_DATA_PATH" || :
	@echo "\n$(ccgreen)package behavior:$(ccreset)"
	@env | grep -E "DATA_SOURCE" || :

	@echo "\n$(ccgreen)GCP:$(ccreset)"
	@env | grep -E "GCR_IMAGE|GCP_PROJECT|GCR_REGION|GCR_MULTI_REGION|GCR_MEMORY" || :


list:
	@echo "\nHelp for the \`bookclub\` package \`Makefile\`"

	@echo "\n$(ccgreen)$(fbold)PACKAGE$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)environment rules:$(ccreset)"
	@echo "\n        $(fbold)show_env$(ccreset)"
	@echo "            Show the environment variables used by the package by category."

	@echo "\n$(ccgreen)$(fbold)TESTS$(ccreset)"

	@echo "\n    $(ccgreen)$(fbold)student rules:$(ccreset)"
	@echo "\n        $(fbold)reinstall_package$(ccreset)"
	@echo "            Install the version of the package corresponding to the challenge."
	@echo "\n        $(fbold)test_cloud_training$(ccreset)"
	@echo "            Run the tests."
