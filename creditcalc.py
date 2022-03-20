import math
import argparse


def get_params():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["annuity", "diff"])
    parser.add_argument("--payment", type=float)
    parser.add_argument("--principal", type=int)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)
    args = parser.parse_args()
    return args


def check_for_errors(args):
    errors = False
    if args.type is None or args.interest is None:
        errors = True
    if len([val for val in vars(args).values() if val is None]) != 1:
        errors = True
    for arg in vars(args).values():
        if arg is not None:
            if type(arg) == int or type(arg) == float:
                if arg < 0:
                    errors = True
    if args.type == "diff" and args.payment is not None:
        errors = True
    if errors:
        print("Incorrect parameters")
    return errors


def diff_monthly_payment(args):
    i = args.interest / (12 * 100)
    m = 1
    payments = []
    while m <= args.periods:
        mth_payment = args.principal / args.periods + i * (args.principal - (args.principal * (m - 1) / args.periods))
        payments.append(math.ceil(mth_payment))
        print(f'Month {m}: payment is {math.ceil(mth_payment)}')
        m += 1
    overpayment = sum(payments) - args.principal
    print(f'Overpayment = {math.ceil(overpayment)}')


def months_number(args):
    i = args.interest / (12 * 100)
    number = math.log(args.payment / (args.payment - i * args.principal), (1 + i))
    number = math.ceil(number)
    overpayment = args.payment * number - args.principal
    years = number // 12
    months = number % 12
    union = " and "
    y_sign = " years"
    m_sign = " months"
    if years == 1:
        y_sign = " year"
    elif years == 0:
        years = ""
        y_sign = ""
        union = ""
    if months == 1:
        m_sign = " month "
    elif months == 0:
        months = ""
        m_sign = ""
        union = ""
    print(f'It will take {years}{y_sign}{union}{months}{m_sign} to repay this loan!')
    print(f'Overpayment = {math.ceil(overpayment)}')


def ann_monthly_payments(args):
    i = args.interest / (12 * 100)
    payment = args.principal * ((i * (1 + i) ** args.periods) / ((1 + i) ** args.periods - 1))
    payment = math.ceil(payment)
    overpayment = args.periods * payment - args.principal
    print(f'Your annuity payment = {payment}!')
    print(f'Overpayment = {math.ceil(overpayment)}')


def principal(args):
    i = args.interest / (12 * 100)
    principal = args.payment / ((i * (1 + i) ** args.periods) / ((1 + i) ** args.periods - 1))
    overpayment = args.periods * args.payment - principal
    print(f"Your loan principal = {round(principal)}!")
    print(f'Overpayment = {math.ceil(overpayment)}')


def choose_calculation(args):
    if args.type == "diff":
        diff_monthly_payment(args)
    elif args.type == "annuity" and args.periods is None:
        months_number(args)
    elif args.type == "annuity" and args.payment is None:
        ann_monthly_payments(args)
    elif args.type == "annuity" and args.principal is None:
        principal(args)


if __name__ == '__main__':
    args = get_params()
    errors = check_for_errors(args)
    if not errors:
        choose_calculation(args)
