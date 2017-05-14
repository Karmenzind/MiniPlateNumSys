# coding: utf-8
import random
import string
import time
from dbOper import dbOper

QUERY_IF_EXISTS = '''select id from plate_nums where prefix='{prefix}' and plate_num='{content}';'''


def create_prefix():
    """
    前缀无I、O
    """
    avail_ltrs = string.uppercase.replace('I', '').replace('O', '')
    return random.choice(avail_ltrs)


def create_content():
    """
    号码由5位序号组成，首末为数字，中间三位有且只有一个字母，数字至少一个非零
    """
    res = []
    for i in xrange(5):
        res.append(random.choice(string.digits))
    letter_idx = random.randint(1, 3)
    res[letter_idx] = random.choice(string.uppercase)
    if res.count('0') == 4:
        not_zero_idxs = range(5)
        not_zero_idxs.pop(letter_idx)
        res[random.choice(not_zero_idxs)] = random.randint(1, 9).__str__()
    return ''.join(res)


def enlarge_table(num):
    """
    扩容
    :return: 
    """

    fail = 0
    for i in xrange(num):

        prefix = create_prefix()
        content = create_content()
        query_res = dbOper().query(QUERY_IF_EXISTS.format(prefix=prefix, content=content))
        if query_res:
            # print query_res, 'is already existed.'
            fail += 1
            continue
        else:
            _sql = '''insert into plate_nums values(NULL, '{}', '{}', 0, NULL);'''.format(prefix, content)
            dbOper().update(_sql)
            # print prefix, content, 'inserted.'
    # print fail


def select_over(user_account, prefix, plate_num, **kw):
    cust_id = dbOper().query('''SELECT cust_id FROM `customers_info` where user_account = '%s';''' % user_account)[0]['cust_id']
    update_customer = '''update customers_info set prefix='{prefix}', plate_num='{plate_num}', obt_plate_time='{obt_plate_time}' 
                    where cust_id = '{cust_id}';'''.format(prefix=prefix, plate_num=plate_num,
                                                           obt_plate_time=time.time(), cust_id=cust_id)
    update_plate = '''update plate_nums set cust_id='{cust_id}', occupied='1' where prefix='{prefix}' and plate_num='{plate_num}';''' \
        .format(prefix=prefix, plate_num=plate_num, cust_id=cust_id)
    dbOper().update(update_customer)
    dbOper().update(update_plate)


if __name__ == '__main__':
    pass
