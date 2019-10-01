# A `unittest` variant of our test suite

A couple of weeks ago, we started extending our test suite for our main Discord bot, [@Python](https://github.com/python-discord/bot). I want to propose for us to switch to the `unittest` framework instead of the `pytest` framework we're currently using. I think that making this decision is especially important given the ambition we have with regards to requiring test coverage on `bot` as well as `site`.


## Consistency

The main reason why I think we should switch is consistency. Both our `bot` and `site` repositories are central to our community and they are highly related as well. Therefore, I think it makes sense for us to use the same testing framework for both of them. Since the built-in testing utilities of Django are based on `unittest`, the most logical test for that framework would be `unittest`, not `pytest`.

I think that there are three major arguments in favor of that consistency:

- Consistency in appearance and structure means our tests suites will be easer to read once someone gets used to that appearance.

- Contributors will not have to learn two frameworks in order to contribute to these two central repositories.

- The output of both test suites (`site` and `bot`) will be equal, making it easier to interpret the results you get back once you get used to that output.

There are other arguments as well, such reducing the number of dependencies, increasing the number of reviewers who feel confident enough with the framework to make reviews, and being able to have a similar/identical set-up for the linting & testing phase in the pipeline of both repositories.

## Examples of output

TODO
