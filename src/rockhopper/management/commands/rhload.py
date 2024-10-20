# rockhopper/management/commands/rhload.py
from django.conf import settings
from django.core.management.base import BaseCommand

from rockhopper.loaders import load_file, load_groups

class Command(BaseCommand):
    help = "Loads source files into the CMS"

    def handle(self, *args, **options):
        load_groups()

        # Load the source files into the CMS
        for filename in args:
            path = Path(filename).resolve()
            self.stdout.write("Loading " + str(path))
            load_file(path)
