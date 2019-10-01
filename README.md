# A `unittest` variant of our test suite

A couple of weeks ago, we started extending our test suite for our main Discord bot, [@Python](https://github.com/python-discord/bot). I want to propose for us to switch to the `unittest` framework instead of the `pytest` framework we're currently using. I think that making this decision is especially important given the ambition we have with regards to requiring test coverage on `bot` as well as `site`.


## Consistency

The main reason why I think we should switch is consistency. Both our `bot` and `site` repositories are central to our community and they are highly related as well. Therefore, I think it makes sense for us to use the same testing framework for both of them. Since the built-in testing utilities of Django are based on `unittest`, the most logical test for that framework would be `unittest`, not `pytest`.

I think that there are three major arguments in favor of that consistency:

- Consistency in appearance and structure means our tests suites will be easer to read once someone gets used to that appearance and structure.

- Contributors will not have to learn two frameworks in order to contribute to these two central repositories.

- The output of both test suites (`site` and `bot`) will be identical, making it easier to interpret the results you get back once you get used to that output.

There are other arguments as well, such reducing the number of dependencies, increasing the number of reviewers who feel confident enough with the framework to make reviews, and being able to have a similar/identical set-up for the linting & testing phase in the pipeline of both repositories.

## Examples of output

The base output of both frameworks with no failing cases is very similar:
![base_output_correct](https://user-images.githubusercontent.com/33516116/65990999-efb9db00-e48c-11e9-80aa-0d6ebe93798b.png)

When a test fails, there's a difference in output, though. However, both output the test values you put in (given that you use the `self.subTest` context manager with `unittest` like in the exposition file). For `unittest`, it's in the `FAIL` line, for `pytest`, you need to look at the code context to see the test values used. `pytest` gives slightly more context, but I think they both provide sufficient output to interpret the failing test:
![test_failure](https://user-images.githubusercontent.com/33516116/65990997-efb9db00-e48c-11e9-87ec-1e48bd1f2338.png)


