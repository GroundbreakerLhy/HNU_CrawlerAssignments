from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    DateField,
    DateTimeField,
)
import datetime
from prettytable import PrettyTable
import sys

db = SqliteDatabase("patients.db")
db.connect()
if not db.is_connection_usable():
    raise Exception("Failed to connect database.")


class Patient(Model):
    admission_time = DateTimeField(null=True)
    name = CharField(null=True)
    birthday = DateField(null=True)
    gender = CharField(null=True)
    diagnosis = CharField(null=True)
    record = CharField(null=True)

    class Meta:
        database = db


if not Patient.table_exists():
    Patient.create_table()

prompt = {
    "main": {
        "welcome": "### 患者记录系统 ###",
        "help prompt": "按'h'查看帮助",
        "input prompt": "> ",
        "invalid input": "输入不正确",
    },
    "query": {
        "query limit": "查询最近的条数：",
        "invalid top_n": "条数输入不正确",
    },
    "ask": {
        "please select": "请选择，按Ctrl + C跳过：",
        "please input": "请输入,按Ctrl + C跳过：",
        "please input date": "请按yyyy-mm-dd格式输入日期，按Ctrl + C跳过",
        "please input datetime": "请按yyyy-mm-dd hh:mm格式输入日期，按Ctrl + C跳过",
        "show default": "默认：",
        "invalid input": "输入不正确",
        "skip": "已跳过",
    },
    "admit": {
        "start": "录入患者信息：",
        "info": {
            "admission_time": "收治时间：",
            "name": "姓名：",
            "birthday": "出生日期：",
            "gender": "性别：",
            "diagnosis": "诊断：",
            "record": "详细记录：",
        },
    },
    "modify": {
        "start": "修改记录",
        "choose id": "请选择要修改记录的id：",
        "choose field": "请选择要修改的列：",
        "invalid input": "输入不正确",
        "not exists": "所选记录不存在",
        "wrong field": "所选列不存在",
        "modified": "已修改",
    },
    "delete": {
        "start": "删除记录",
        "choose id": "请选择要删除记录的id：",
        "not exists": "所选记录不存在",
        "comfirm": "确定要删除吗？",
        "deleted": "已删除",
        "intact": "未修改",
    },
}


def ask_choice(options, default=None):
    if default is not None:
        assert default in options
    try:
        while True:
            print(prompt["ask"]["please select"], list(options), sep="")
            if default is not None:
                print(prompt["ask"]["show default"], end="")
                print(default)
            choice = input()
            if default is not None and choice == "":
                choice = default
            if choice in options:
                return choice
            else:
                print(prompt["ask"]["invalid input"])
    except KeyboardInterrupt:
        print(prompt["ask"]["skip"])
        return None


def ask_int(default=None, check_valid=lambda x: True):
    try:
        while True:
            print(prompt["ask"]["please input"])
            if default is not None:
                print(prompt["ask"]["show default"], default)
            input_str = input()
            if default is not None and input_str == "":
                return default
            try:
                ret_int = int(input_str)
                if check_valid(ret_int):
                    return ret_int
                else:
                    raise ValueError
            except ValueError:
                print(prompt["ask"]["invalid input"])
    except KeyboardInterrupt:
        print(prompt["ask"]["skip"])
        return None


def ask_str(default=None, check_valid=lambda x: True):
    try:
        while True:
            print(prompt["ask"]["please input"])
            if default is not None:
                print(prompt["ask"]["show default"], default)
            input_str = input()
            if default is not None and input_str == "":
                return default
            if check_valid(input_str):
                return input_str
            else:
                print(prompt["ask"]["invalid input"])
    except KeyboardInterrupt:
        print(prompt["ask"]["skip"])
        return None


def ask_date(default=None, check_valid=lambda x: True):
    try:
        while True:
            print(prompt["ask"]["please input date"])
            if default is not None:
                print(prompt["ask"]["show default"], default)
            input_date = input()
            if default is not None and input_date == "":
                return default
            try:
                date = datetime.datetime.strptime(input_date, "%Y-%m-%d").date()
            except ValueError:
                print(prompt["ask"]["invalid input"])
                continue
            if check_valid(input_date):
                return date
            else:
                print(prompt["ask"]["invalid input"])
    except KeyboardInterrupt:
        print(prompt["ask"]["skip"])
        return None


def ask_datetime(default=None, check_valid=lambda x: True):
    try:
        while True:
            print(prompt["ask"]["please input datetime"])
            if default is not None:
                print(prompt["ask"]["show default"], default)
            input_date = input()
            if default is not None and input_date == "":
                return default
            try:
                date = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M")
            except ValueError:
                print(prompt["ask"]["invalid input"])
                continue
            if check_valid(input_date):
                return date
            else:
                print(prompt["ask"]["invalid input"])
    except KeyboardInterrupt:
        print(prompt["ask"]["skip"])
        return None


def print_patients(patients):
    pt = PrettyTable()
    pt.field_names = Patient._meta.fields.keys()
    for field in pt.field_names:
        pt.max_width[field] = 20
    for p in patients:
        pt.add_row([getattr(p, key) for key in pt.field_names])
    print(pt)


def query():
    print(prompt["query"]["query limit"])
    if top_n := ask_int(check_valid=lambda x: x > 0):
        q = Patient.select().order_by(Patient.admission_time.desc()).limit(top_n)
        print_patients(q)


def admit():
    print(prompt["admit"]["start"])
    p = prompt["admit"]["info"]
    info = {}
    print(p["admission_time"])
    info["admission_time"] = ask_datetime(default=datetime.datetime.today())
    print(p["name"])
    info["name"] = ask_str()
    print(p["birthday"])
    info["birthday"] = ask_date()
    print(p["gender"])
    info["gender"] = ask_choice(["m", "f"])
    print(p["diagnosis"])
    info["diagnosis"] = ask_str()
    print(p["record"])
    info["record"] = ask_str()

    patient_to_admit = Patient.create(**info)
    patient_to_admit.save()
    print_patients([patient_to_admit])


def modify():
    print(prompt["modify"]["start"])
    try:
        patient_id = int(input(prompt["modify"]["choose id"]))
        field = input(prompt["modify"]["choose field"])
    except ValueError:
        print(prompt["modify"]["invalid input"])

    patient_to_modify = Patient.get_or_none(Patient.id == patient_id)
    if patient_to_modify is None:
        print(prompt["modify"]["not exists"])
        return
    print_patients([patient_to_modify])

    match (field):
        case "admission_time":
            setattr(patient_to_modify, "admission_time", ask_datetime())
        case "name":
            setattr(patient_to_modify, "name", ask_str())
        case "birthday":
            setattr(patient_to_modify, "birthday", ask_date())
        case "gender":
            setattr(patient_to_modify, "gender", ask_choice(["m", "f"]))
        case "diagnosis":
            setattr(patient_to_modify, "diagnosis", ask_str())
        case "record":
            setattr(patient_to_modify, "record", ask_str())
        case _:
            print(prompt["modify"]["wrong field"])
            return
    patient_to_modify.save()
    print(prompt["modify"]["modified"])
    print_patients([patient_to_modify])


def delete():
    print(prompt["delete"]["start"])
    try:
        patient_id = int(input(prompt["delete"]["choose id"]))

    except ValueError:
        print(prompt["delete"]["invalid input"])

    patient_to_delete = Patient.get_or_none(Patient.id == patient_id)
    if patient_to_delete is None:
        print(prompt["delete"]["not exists"])
        return

    print(prompt["delete"]["comfirm"])
    print_patients([patient_to_delete])

    if ask_choice(["y", "n"], default="n") == "y":
        patient_to_delete.delete_instance()
        print(prompt["delete"]["deleted"])
    else:
        print(prompt["delete"]["intact"])


def exit_system():
    db.close()
    sys.exit()


def main():
    action = {}

    def help():
        for key in action:
            print(key, ":", action[key]["help"])

    print(prompt["main"]["welcome"])
    print(prompt["main"]["help prompt"])

    action = {
        "q": {
            "func": query,
            "name": "查询",
            "help": "查询最近收治的记录",
        },
        "a": {
            "func": admit,
            "name": "录入",
            "help": "录入患者信息",
        },
        "m": {
            "func": modify,
            "name": "修改",
            "help": "修改记录",
        },
        "d": {
            "func": delete,
            "name": "删除",
            "help": "删除记录",
        },
        "exit": {
            "func": exit_system,
            "name": "退出",
            "help": "退出系统",
        },
        "h": {
            "func": help,
            "name": "帮助",
            "help": "查看帮助",
        },
    }

    while True:
        act = input(prompt["main"]["input prompt"])
        if act in action:
            action[act]["func"]()
        else:
            print(prompt["main"]["invalid input"])
        print()


if __name__ == "__main__":
    main()
