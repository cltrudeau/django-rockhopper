# rockhopper/management/commands/rhload.py
from django.conf import settings
from django.core.management.base import BaseCommand

from rockhopper.loaders import load_file, load_groups

class Command(BaseCommand):
    help = "Loads changed files from the configured source dirs into the CMS"

    def handle(self, *args, **options):
        load_groups()

        # Load the source files into the CMS
        for path in settings.ROCKHOPPER['source']:
            self.stdout.write("Loading " + str(path))
            load_file(path)
