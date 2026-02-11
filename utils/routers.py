class MiRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'appBase':
            return 'bd_peleteria'
        elif model._meta.app_label == 'appTSM':
            return 'bd_peleteria'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'appBase':
            return 'bd_peleteria'
        elif model._meta.app_label == 'appTSM':
            return 'bd_peleteria'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'appBase' or \
            obj2._meta.app_label == 'appBase':
            return True
        elif obj1._meta.app_label == 'appTSM' or \
            obj2._meta.app_label == 'appTSM':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'appBase':
            return db == 'bd_peleteria'
        elif app_label == 'appTSM':
            return db == 'bd_peleteria'
        return None
