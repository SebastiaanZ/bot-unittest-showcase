from __future__ import annotations

import asyncio
import datetime
import unittest
from unittest.mock import MagicMock, patch

from dateutil.relativedelta import relativedelta
from discord.ext.commands import BadArgument

from bot.converters import Duration, TagContentConverter, TagNameConverter, ValidPythonIdentifier


class ConverterTests(unittest.TestCase):
    """Tests our custom argument converters."""

    @classmethod
    def setUpClass(cls: ConverterTests):
        cls.context = MagicMock
        cls.context.author = 'bob'

        cls.fixed_utc_now = datetime.datetime.fromisoformat('2019-01-01T00:00:00')

    def test_tag_content_converter_for_valid(self):
        """Tests if TagContentConverter returns the correct value for valid tag content."""
        test_values = (
            ('hello', 'hello'),
            ('  h ello  ', 'h ello'),
        )

        for content, expected_conversion in test_values:
            with self.subTest(content=content, expected_conversion=expected_conversion):
                conversion = asyncio.run(TagContentConverter.convert(self.context, content))
                self.assertEqual(conversion, expected_conversion)

    def test_tag_content_converter_for_invalid(self):
        """Tests if TagContentConverter raises the proper exception for invalid tag content,"""
        test_values = (
            ('', "Tag contents should not be empty, or filled with whitespace."),
            ('   ', "Tag contents should not be empty, or filled with whitespace."),
        )

        for value, exception_message in test_values:
            with self.subTest(tag_content=value, exception_message=exception_message):
                with self.assertRaises(BadArgument, msg=exception_message):
                    asyncio.run(TagContentConverter.convert(self.context, value))

    def test_tag_name_converter_for_valid(self):
        """Tests if TagNameConverter returns the correct values for valid tag names."""
        test_values = (
            ('tracebacks', 'tracebacks'),
            ('Tracebacks', 'tracebacks'),
            ('  Tracebacks  ', 'tracebacks'),
        )

        for name, expected_conversion in test_values:
            with self.subTest(name=name, expected_conversion=expected_conversion):
                conversion = asyncio.run(TagNameConverter.convert(self.context, name))
                self.assertEqual(conversion, expected_conversion)

    def test_tag_name_converter_for_invalid(self):
        """Tests if TagNameConverter raises the correct exception for invalid tag names."""
        test_values = (
            ('👋', "Don't be ridiculous, you can't use that character!"),
            ('', "Tag names should not be empty, or filled with whitespace."),
            ('  ', "Tag names should not be empty, or filled with whitespace."),
            ('42', "Tag names can't be numbers."),
            ('x' * 128, "Are you insane? That's way too long!"),
        )

        for invalid_name, exception_message in test_values:
            with self.subTest(invalid_name=invalid_name, exception_message=exception_message):
                with self.assertRaises(BadArgument, msg=exception_message):
                    asyncio.run(TagNameConverter.convert(self.context, invalid_name))

    def test_valid_python_identifier_for_valid(self):
        """Tests if ValidPythonIdentifier returns valid identifiers unchanged."""
        test_values = ('foo', 'lemon')

        for name in test_values:
            with self.subTest(identifier=name):
                conversion = asyncio.run(ValidPythonIdentifier.convert(self.context, name))
                self.assertEqual(name, conversion)

    def test_valid_python_identifier_for_invalid(self):
        """Tests if ValidPythonIdentifier raises the proper exception for invalid identifiers."""
        test_values = ('nested.stuff', '#####')

        for name in test_values:
            with self.subTest(identifier=name):
                exception_message = f'`{name}` is not a valid Python identifier'
                with self.assertRaises(BadArgument, msg=exception_message):
                    asyncio.run(ValidPythonIdentifier.convert(self.context, name))

    def test_duration_converter_for_valid(self):
        """Tests if Duration returns the correct `datetime` for valid duration strings."""
        test_values = (
            # Simple duration strings
            ('1Y', {"years": 1}),
            ('1y', {"years": 1}),
            ('1year', {"years": 1}),
            ('1years', {"years": 1}),
            ('1m', {"months": 1}),
            ('1month', {"months": 1}),
            ('1months', {"months": 1}),
            ('1w', {"weeks": 1}),
            ('1W', {"weeks": 1}),
            ('1week', {"weeks": 1}),
            ('1weeks', {"weeks": 1}),
            ('1d', {"days": 1}),
            ('1D', {"days": 1}),
            ('1day', {"days": 1}),
            ('1days', {"days": 1}),
            ('1h', {"hours": 1}),
            ('1H', {"hours": 1}),
            ('1hour', {"hours": 1}),
            ('1hours', {"hours": 1}),
            ('1M', {"minutes": 1}),
            ('1minute', {"minutes": 1}),
            ('1minutes', {"minutes": 1}),
            ('1s', {"seconds": 1}),
            ('1S', {"seconds": 1}),
            ('1second', {"seconds": 1}),
            ('1seconds', {"seconds": 1}),

            # Complex duration strings
            (
                '1y1m1w1d1H1M1S',
                {
                    "years": 1,
                    "months": 1,
                    "weeks": 1,
                    "days": 1,
                    "hours": 1,
                    "minutes": 1,
                    "seconds": 1
                }
            ),
            ('5y100S', {"years": 5, "seconds": 100}),
            ('2w28H', {"weeks": 2, "hours": 28}),

            # Duration strings with spaces
            ('1 year 2 months', {"years": 1, "months": 2}),
            ('1d 2H', {"days": 1, "hours": 2}),
            ('1 week2 days', {"weeks": 1, "days": 2}),
        )

        converter = Duration()

        for duration, duration_dict in test_values:
            expected_datetime = self.fixed_utc_now + relativedelta(**duration_dict)

            with patch('bot.converters.datetime') as mock_datetime:
                mock_datetime.utcnow.return_value = self.fixed_utc_now

                with self.subTest(duration=duration, duration_dict=duration_dict):
                    converted_datetime = asyncio.run(converter.convert(self.context, duration))
                    self.assertEqual(converted_datetime, expected_datetime)

    def test_duration_converter_for_invalid(self):
        """Tests if Duration raises the right exception for invalid duration strings."""
        test_values = (
            # Units in wrong order
            ('1d1w'),
            ('1s1y'),

            # Duplicated units
            ('1 year 2 years'),
            ('1 M 10 minutes'),

            # Unknown substrings
            ('1MVes'),
            ('1y3breads'),

            # Missing amount
            ('ym'),

            # Incorrect whitespace
            (" 1y"),
            ("1S "),
            ("1y  1m"),

            # Garbage
            ('Guido van Rossum'),
            ('lemon lemon lemon lemon lemon lemon lemon'),
        )

        converter = Duration()

        for invalid_duration in test_values:
            with self.subTest(invalid_duration=invalid_duration):
                exception_message = f'`{invalid_duration}` is not a valid duration string.'
                with self.assertRaises(BadArgument, msg=exception_message):
                    asyncio.run(converter.convert(self.context, invalid_duration))
