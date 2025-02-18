

class Task(Base)
    __tablename__ = 'tasks'

    id:
    batch_id:
    data:
    assessments:


class Assessment(Base):
    __tablename__ = 'assessments'

    id:
    task_id:
    assessor_id:
    result:
    created_at: