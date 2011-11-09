from django.core.management.base import NoArgsCommand, CommandError

from openauth.openid.models import Nonce


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--all', default=False, help='Delete all Nonces including non-expired'),
    )
    help = 'Cleans expired Nonces'
    
    def handle_noargs(self, **options):
        if options.get('all', False):
            nonces = Nonce.objects.all()
        else:
            nonces = Nonce.objects.expired()
        nonces.delete()
        
        for nonce in nonces:
            self.stdout.write('%s\n' % nonce)
