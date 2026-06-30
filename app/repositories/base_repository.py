from app.extensions import db

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        return db.session.get(self.model, id)

    def get_all(self):
        return self.model.query.all()

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
