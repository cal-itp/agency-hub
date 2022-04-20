from django.core.management.base import BaseCommand
from pathlib import Path
import yaml

from agency.models import Agency


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("yml_path", type=str)

    def handle(self, *args, **kwargs):
        f = Path(kwargs["yml_path"]).read_text()
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
        for slug, data in yaml_data.items():
            url_count = len(data["feeds"])
            agency, new = Agency.objects.get_or_create(
                itp_id=data["itp_id"],
                defaults=dict(name=data["agency_name"], slug=slug, url_count=url_count),
            )
            if new:
                print(f"New Agency: {agency}")
            else:
                agency.url_count = url_count
                agency.save()
