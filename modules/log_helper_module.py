from db_models.modelsv2 import Log, Users
import modules.db_helper as db_helper


def add_log(message):
    try:
        db_helper.add_item(Log, {'message': message})
        pass
    except Exception as e:
        pass


def clean_log_by_condition():
    try:
        logs = session.query(Log).all()

        if (len(logs) > 2000):
            session.query(Log).delete()
            session.commit()
        pass
    except Exception as e:
        session.rollback()

def log_user_actions(route, user_id, action_type):
    try:
        clean_log_by_condition()
        user = db_helper.get_item(Users, user_id)
        user_name = user.first_name + ' ' + user.last_name
        client_name = user.client.name
        message =("Пользователь {0}, компания {1}, выполнил действие {2} на роуте {3}").format(user_name,client_name,action_type,route)
        db_helper.add_item(Log, {'message': message})
    except:
        pass