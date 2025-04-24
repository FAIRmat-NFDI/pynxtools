# Run `pynxtools` Tests in Parallel
Pytest test framework also allows tests to run in parallel with some other third party pytest plugin, e.g. `pytest-xdist`. In our pytest for pynxtools we are using `[pytest-xdist](https://pytest-xdist.readthedocs.io/en/stable/)` to execute the test in prallel. In case of sheared resources among multiple test, the tests are being grouped by fixtures by `pytest.mark.xdist_group` to prevent any classic race coditions.



