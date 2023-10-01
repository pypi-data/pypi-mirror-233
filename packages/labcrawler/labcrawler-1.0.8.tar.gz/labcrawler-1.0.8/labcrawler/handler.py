import sys

from wizlib.command_handler import CommandHandler
from labcrawler.command import LabCrawlerCommand


class LabCrawlerHandler(CommandHandler):

    @classmethod
    def shell(cls):
        super().shell(LabCrawlerCommand)
