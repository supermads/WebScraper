import ast
import re

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class WebScraperTest(StageTest):
    def generate(self):
        return [TestCase(stdin="https://www.imdb.com/title/tt10048342/", check_function=self.check_queens_gambit,
                         time_limit=50000),
                TestCase(stdin="https://www.imdb.com/title/tt0068646/", check_function=self.check_godfather,
                         time_limit=50000),
                TestCase(stdin="https://www.imdb.com/name/nm0001191/", check_function=self.check_incorrect_url,
                         time_limit=50000),
                TestCase(stdin="https://www.google.com/", check_function=self.check_incorrect_url, time_limit=50000)]

    def check_incorrect_url(self, reply, attach=None):
        if "Invalid movie page!" in reply:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("""If the link does not contain movie info or not an IMDB resource, 
            please respond with 'Invalid movie page!' message!""")

    def check_queens_gambit(self, reply, attach=None):
        possible_descriptions = ["prodigious introvert Beth Harmon discovers and masters the game of chess"]
        output = re.search('({.+})', reply)
        if output is None:
            return CheckResult.wrong("Output in the format of JSON was expected.\n"
                                     "However, it was not found.")
        reply_dict = ast.literal_eval(output.group(0))
        user_description = reply_dict["description"]
        correct_descriptions = sum([description.lower().strip() in user_description.lower().strip() for description in possible_descriptions]) > 0
        if reply_dict["title"] == "The Queen's Gambit" and correct_descriptions:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("Title or description in returned dict do not seem to be correct.")

    def check_godfather(self, reply, attach=None):
        possible_descriptions = ["An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son",
                                 "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."]
        reply_dict = ast.literal_eval(re.search('({.+})', reply).group(0))
        title = reply_dict.get("title")
        desc = reply_dict.get("description")
        if not title or not desc:
            return CheckResult.wrong("Seems like there is a title or a description missing in the output dictionary.")
        user_description = reply_dict["description"]
        correct_descriptions = sum([description.lower().strip() in user_description.lower().strip() for description in possible_descriptions]) > 0
        if reply_dict["title"] == "The Godfather" and correct_descriptions:
            return CheckResult.correct()
        else:
            return CheckResult.wrong("Title or description in returned dict do not seem to be correct.")


if __name__ == '__main__':
    WebScraperTest('webscraper.scraper').run_tests()
