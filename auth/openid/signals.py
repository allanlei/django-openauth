def generate_secret():
    return ''
    
def association_associate(sender, association, **kwargs):
    if association.pk is None:
        if not association.secret_key:
            association.secret_key = generate_secret()
