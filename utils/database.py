from sqlalchemy.orm.exc import NoResultFound
import uuid
import os
import json


class Database:

    @staticmethod
    def open_json_file(filepath):
        try:
            if os.path.isfile(filepath):
                with open(filepath) as file:
                    return json.load(file)
            else:
                return None
        except FileNotFoundError as e:
            print(f"Error: Ensure file is existed.")
            return e

    @staticmethod
    def get_uuid4_str() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def get_or_create(session, model, **kwargs):
        def get_instance(session, model, **kwargs):
            try:
                result = session.query(model).filter_by(**kwargs).first()
                return result
            except NoResultFound:
                return None

        def create_instance(session, model, **kwargs):
            try:
                instance = model(**kwargs)
                print(f"Created instance: {instance}")
                # session.add(instance)
                # session.flush()

            except Exception as msg:
                mtext = f"model:{model}, args:{kwargs} => msg:{msg}"
                session.rollback()
                raise (msg)
            return instance

        def update_instance(session, model, **kwargs):
            try:
                xd

        instance = get_instance(session, model, **kwargs)
        print(f"instance: {instance}")
        print(f"is instance None?: {instance is None}")
        if instance is None:
            print(f"Create [{model}]")
            instance = create_instance(session, model, **kwargs)

        return instance
