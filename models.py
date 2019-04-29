from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from data import config
import datetime

Base = declarative_base()


DRAFT = -2
PENDING_REVIEW = 0
PUBLISH = 1
UNPUBLISH = -1
DELETED = -3
TEMP = -4
PUBLISH_STATUS = (
    (TEMP, '临时'),
    (DRAFT, '草稿'),
    (PENDING_REVIEW, '待审核'),
    (PUBLISH, '上架'),
    (UNPUBLISH, '下架'),
    (DELETED, '删除'),
)


class Work(Base):
    __tablename__ = 'web_work'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    ont_id = Column(String(200), nullable=True)
    tx_hash = Column(String(200), nullable=True)
    ont_status = Column(Integer, nullable=True)


class ONTWorkRecord(Base):
    __tablename__ = 'web_ontworkrecord'

    id = Column(Integer, primary_key=True)
    work_id = Column(Integer, ForeignKey('web_work.id'))
    ont_id = Column(String(200), default='')
    tx_hash = Column(String(200), default='')
    ont_status = Column(Integer, default=0)
    create_uid = Column(Integer, default=2)
    update_uid = Column(Integer, default=2)
    create_date = Column(DateTime, default=datetime.datetime.now())
    update_date = Column(DateTime, default=datetime.datetime.now())


def with_engine(func):
    def wrapper(*args, **kwargs):
        engine = create_engine(config.MYSQL_CONN_STR)
        Base.metadata.create_all(engine)
        return func(engine, *args, **kwargs)
    return wrapper


@with_engine
def get_work(engine, id):
    Session = sessionmaker(bind=engine)
    session = Session()
    work = session.query(Work).filter_by(id=id).one()
    return work


@with_engine
def set_work_ont_id(engine, work_id, ont_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    work = session.query(Work).get(work_id)
    work.ont_id = ont_id

    ont_work_record = ONTWorkRecord(work_id=work_id, ont_id=ont_id, ont_status=0)
    session.add(ont_work_record)

    session.commit()


@with_engine
def set_work_ont_id_and_tx_hash(engine, work_id, ont_id, tx_hash):
    Session = sessionmaker(bind=engine)
    session = Session()
    work = session.query(Work).get(work_id)
    work.ont_id = ont_id
    work.tx_hash = tx_hash

    ont_work_record = ONTWorkRecord(work_id=work_id, ont_id=ont_id, tx_hash=tx_hash, ont_status=0)
    session.add(ont_work_record)

    session.commit()


@with_engine
def set_work_tx_hash(engine, work_id, ont_id, tx_hash):
    Session = sessionmaker(bind=engine)
    session = Session()
    work = session.query(Work).get(work_id)
    work.tx_hash = tx_hash

    ont_work_record = ONTWorkRecord(work_id=work_id, ont_id=ont_id, tx_hash=tx_hash, ont_status=0)
    session.add(ont_work_record)

    session.commit()


@with_engine
def set_work_tx_hash_and_ont_status(engine, work_id, ont_id, tx_hash, ont_status):
    Session = sessionmaker(bind=engine)
    session = Session()
    work = session.query(Work).get(work_id)
    work.tx_hash = tx_hash
    work.ont_status = ont_status

    ont_work_record = ONTWorkRecord(work_id=work_id, ont_id=ont_id, tx_hash=tx_hash, ont_status=ont_status)
    session.add(ont_work_record)

    session.commit()
