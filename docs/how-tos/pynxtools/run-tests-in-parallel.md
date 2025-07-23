# Running `pynxtools` tests in parallel

The `pytest` framework allows tests to run in sequential and parallel using third-party plugins such as [`pytest-xdist`](https://pytest-xdist.readthedocs.io/en/stable/). In our `pytest` setup for `pynxtools`, we use `pytest-xdist` to execute tests in parallel. To handle shared resources among multiple tests, tests are grouped using the `@pytest.mark.xdist_group` fixture. This prevents classic race conditions by ensuring that tests sharing the same resources are executed sequentially.

## Running Tests Sequentially

In a local setup, tests can be run sequentially using the following command:

```console
pytest tests
```

This will execute all tests in a sequential manner. For more details, refer to the official documentation:

- [How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html)

## Running Tests in Parallel

The `pytest-xdist` plugin can be used to speed up test execution by distributing tests among available workers. To prevent race conditions, tests that share the same resources are grouped using the `@pytest.mark.xdist_group(name="group_name")` fixture. These grouped tests must be run with the `--dist loadgroup` flag. For example:

```console
pytest tests -n auto --dist loadgroup
```

Here:

- The `-n auto` flag tells `pytest` to automatically distribute tests among all available workers.
- The `--dist loadgroup` flag ensures that tests marked with the same @pytest.mark.xdist_group(name="...") are executed serially.

This setup allows for efficient parallel test execution while maintaining the integrity of tests that depend on shared resources.
