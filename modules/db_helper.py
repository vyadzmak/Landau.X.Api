from db.db import session
import modules.db_model_transformer_module as db_transformer


def get_item(model, id):
    try:
        entity = session.query(model).filter(model.id == id).first()
        return entity
    except Exception as e:
        session.rollback()
        raise e


def get_items(model):
    try:
        entities = session.query(model).all()
        return entities
    except Exception as e:
        session.rollback()
        raise e


def add_item(model, json_data):
    try:
        entity = model(json_data)
        session.add(entity)
        session.commit()
        return entity
    except Exception as e:
        session.rollback()
        raise e


def update_item(model, json_data, id):
    try:
        entity = session.query(model).filter(model.id == id).first()
        if entity is None:
            return None
        db_transformer.transform_update_params(entity, json_data)
        session.add(entity)
        session.commit()
        return entity
    except Exception as e:
        session.rollback()
        raise e


def delete_item(model, id):
    try:
        entity = session.query(model).filter(model.id == id).first()
        if entity is None:
            return None
        session.delete(entity)
        session.commit()
        return entity
    except Exception as e:
        session.rollback()
        raise e
