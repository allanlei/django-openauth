from django.core.management.base import NoArgsCommand, CommandError

from openauth.openid.models import Association

import time

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--all', default=False, help='Delete all Associations including non-expired'),
    )
    help = 'Cleans expired Associations'

    def handle_noargs(self, **options):
        if options.get('all', False):
            assocs = Association.objects.all()
        else:
            assocs = Association.objects.expired()
        assocs.delete()
        
        for assoc in assocs:
            self.stdout.write('%s\n' % assoc)
