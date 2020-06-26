from peewee import *
from datetime import datetime
import random

db = SqliteDatabase('test.db')


class BaseModel(Model):
    class Meta:
        database = db


class Theme(BaseModel):
    name = CharField(unique=True)


class TestExample(BaseModel):
    theme = ForeignKeyField(Theme, backref='examples')
    photo = CharField()
    answer = CharField()


def init_db():
    db.connect()
    db.create_tables([
        Theme,
        TestExample
    ], safe=True)


class Example:
    theme: str
    photo: str
    answer: str
    id: int

    def __init__(self, theme, photo, answer):
        self.theme = theme
        self.photo = photo
        self.answer = answer
        self.id = id


def new_example_added_to_bd(example: Example):
    TestExample.create(theme=example.theme, photo=example.photo, answer=example.answer)


class Multi_dz_theme:
    tema: str
    active: str
    count: int

    def __init__(self, tema, active, count):
        self.tema = tema
        self.active = active
        self.count = count

#--For Student_bot

class Parallel(BaseModel):
    name = CharField(unique=True)

class Klass(BaseModel):
    name = CharField(unique=True)
    paral = ForeignKeyField(Parallel, backref='classes')

class UserTab(BaseModel):
    teleg_id = CharField(unique=True)
    name = CharField()
    klass = ForeignKeyField(Klass, backref='users')
    cur_selftest_1t = IntegerField()
    reg_date = DateTimeField()
    reg_status = CharField()
    status = CharField()
    cur_multitest = IntegerField()


class DzTable(BaseModel):
    id = AutoField()
    klass = ForeignKeyField(Klass, backref='dz_po_klassu')
    theme = ForeignKeyField(Theme, backref='dz_po_teme')
    count = IntegerField()
    name = CharField()
    date_create = DateTimeField()


class MultiDzTable(BaseModel):
    id = AutoField()
    klass = ForeignKeyField(Klass, backref='multidz_po_klassu')
    name = CharField()
    zadanie = CharField()
    date_create = DateTimeField()


class SelfTest_1t(BaseModel):
    id = AutoField()
    user = ForeignKeyField(UserTab, backref='tests')
    theme = ForeignKeyField(Theme, backref='tests')
    ex_data = CharField()
    ex_count = IntegerField()
    done_ex_count = IntegerField()
    right_count = IntegerField()
    date_start = DateTimeField()
    date_finish = DateTimeField()
    dz_id = ForeignKeyField(DzTable, backref='tests')


class MultiTest(BaseModel):
    id = AutoField()
    multidz_id = ForeignKeyField(MultiDzTable, backref='tests')
    user = ForeignKeyField(UserTab, backref='multitests')
    ex_data = CharField()
    ex_count = IntegerField()
    done_ex_count = IntegerField()
    right_count = IntegerField()
    date_start = DateTimeField()
    date_finish = DateTimeField()


class SelfTest_1t_ex(BaseModel):
    test_id = ForeignKeyField(SelfTest_1t, backref='tests_ex', null=True)
    test_ex_id = ForeignKeyField(TestExample, backref='selftets_1t')
    user_answer = CharField()
    right = CharField()
    date = DateField()
    multitest_id = ForeignKeyField(MultiTest, backref='tests_ex', null=False)




# DzTable.create_table()

# UserTab.drop_table()
# UserTab.create_table()
# SelfTest_1t_ex.drop_table()
# SelfTest_1t_ex.create_table()
# SelfTest_1t.drop_table()
# SelfTest_1t.create_table()


#генерация id заданий по одной теме в запрашиваемом количестве
def gen_numex_1t(message):
    user_id=message.chat.id
    ex_data = TestExample.select().where(TestExample.theme == UserTab.get(teleg_id=user_id).status.split('_')[1])
    ex_n = []
    for ex in ex_data:
        ex_n.append(ex.id)
    exam = random.sample(ex_n, int(message.text))
    return exam


def gen_numex_dz_1t(dz):
    ex_data_dz = dz.theme.examples
    #ex_data = TestExample.select().where(TestExample.theme == UserTab.get(teleg_id=user_id).status.split('_')[1])
    ex_n_dz = []
    for ex_dz in ex_data_dz:
        ex_n_dz.append(ex_dz.id)
    exam_dz = random.sample(ex_n_dz, dz.count)
    return exam_dz


def gen_numex_multi_dz(zadanie):
    ex_data = []
    for part in zadanie.split(';'):
        ex_data_part = []
        part_ex = Theme.get(name=part.split('_')[0]).examples
        for ex in part_ex:
            ex_data_part.append(ex.id)
        ex_data += random.sample(ex_data_part, int(part.split('_')[1]))
        print(ex_data)
    return ex_data

def multidz_count_sum(zadanie):
    count_sum = 0
    print('считаем')
    for part in zadanie.split(';'):
        count_sum += int(part.split('_')[1])
    print(count_sum, 'заданий')
    return count_sum


# user_id = 646951760
# mas = UserTab.get(teleg_id=user_id).tests[-1].ex_data
# print(mas)
# new =[]
# for i in mas[1:-1].split(', '):
#     new.append(i)
#     print(i)
# print(new[0])

# SelfTest_1t.update({SelfTest_1t.ex_data: new}).where(SelfTest_1t.user==UserTab.get(teleg_id=user_id)).execute()
# print(UserTab.get(teleg_id=user_id).tests[-1].ex_data[0])

# Klass.drop_table()
# Klass.create_table()4
# UserTab.drop_table()
# UserTab.create_table()
#
# Klass.create(name='8В', paral=Parallel.get(name='8') )
# for i in range(7, 12):
#     Parallel.create(name=i)
# TestExample.drop_table()
# TestExample.create_table()
# SelfTest_1t.drop_table()
# SelfTest_1t.create_table()
# SelfTest_1t_ex.drop_table()
# SelfTest_1t_ex.create_table()
# DzTable.drop_table()
# DzTable.create_table()
# MultiDzTable.drop_table()
# MultiDzTable.create_table()
# MultiTest.drop_table()
# MultiTest.create_table()