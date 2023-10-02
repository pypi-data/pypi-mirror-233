import dateparser
import datetime
import pandas as pd
import requests
import re
import smtplib
from dateutil.relativedelta import relativedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.policy import SMTPUTF8


# DAY_OF_MAILING_BIRTHDAYS = 3
# DAY_OF_MAILING_VACATIONS = 18
# RECEIVER_EMAILS = pd.read_csv('https://docs.google.com/spreadsheets/d/1SeBKtrw37Xofrx8ThVYbm6tavxKMSlYUZiUwkjBs-FY/export?format=csv&gid=141358182')['Почта']
# TEAMS_COLORS = {
#     'A': '#E1E0B2',
#     'B': '#A4E1E5',
# }
#
# LINK_BIRTHDAYS = 'https://docs.google.com/spreadsheets/d/1SeBKtrw37Xofrx8ThVYbm6tavxKMSlYUZiUwkjBs-FY/export?format=csv&gid=0'
# LINK_VACATIONS = 'https://docs.google.com/spreadsheets/d/1SeBKtrw37Xofrx8ThVYbm6tavxKMSlYUZiUwkjBs-FY/export?format=csv&gid=163864896'
# LINK_RECEIVER_EMAILS = 'https://docs.google.com/spreadsheets/d/1SeBKtrw37Xofrx8ThVYbm6tavxKMSlYUZiUwkjBs-FY/export?format=csv&gid=141358182'

month_translations = {
    1: 'ЯНВАРЬ',
    2: 'ФЕВРАЛЬ',
    3: 'МАРТ',
    4: 'АПРЕЛЬ',
    5: 'МАЙ',
    6: 'ИЮНЬ',
    7: 'ИЮЛЬ',
    8: 'АВГУСТ',
    9: 'СЕНТЯБРЬ',
    10: 'ОКТЯБРЬ',
    11: 'НОЯБРЬ',
    12: 'ДЕКАБРЬ'
}


def send_msg_email(msg, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT):
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print('Email sent successfully.')
    except Exception as e:
        print('Error sending email:', str(e))


def send_msg_telegram(msg, bot_token, group_id):
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id=@{group_id}&text={msg}&parse_mode=MarkdownV2"
    tel_resp = requests.get(telegram_api_url)
    if tel_resp.status_code == 200:
        print("Notification has been sent on Telegram")
    else:
        print("Could not send Message")


def get_html_birthday_table(teams_members_with_birthday, teams_colors):
    html_table = "<table style='border-collapse: collapse; border: 1px solid black;'>"
    html_table += f"""
    <tr style='text-align: center;'>
        <td style='border: 1px solid black; width: 30px;'><strong>Команда</strong></td>
        <td style='border: 1px solid black; width: 220px;'><strong>Фамилия Имя</strong></td>
        <td style='border: 1px solid black; width: 100px;'><strong>День рождение</strong></td>
    </tr>"""
    for team_member_with_birthday in sorted(teams_members_with_birthday, key=lambda x: (x['Команда'], x['День рождения (дата)'].day)):
        team = team_member_with_birthday['Команда']
        html_table += f"""
        <tr style='text-align: center; background-color: {teams_colors.get(team)};'>
            <td style='border: 1px solid black; width: 30px;'>{team}</td>
            <td style='border: 1px solid black; width: 220px;'>{team_member_with_birthday['Фамилия Имя']}</td>
            <td style='border: 1px solid black; width: 100px;'>{team_member_with_birthday['День рождения']}</td>
        </tr>"""
    html_table += "</table>"
    return html_table


def get_tgmsg_birthday_table(teams_members_with_birthday, subject):
    tgmsg = f"*{subject}*\n"
    traversed_teams = []
    for team_member_with_birthday in sorted(teams_members_with_birthday, key=lambda x: (x['Команда'], x['День рождения (дата)'].day)):
        team = team_member_with_birthday['Команда']
        if team not in traversed_teams:
            tgmsg += f'\n__*Команда {team}*__\n'
        traversed_teams.append(team)
        tgmsg += f"\t• {team_member_with_birthday['Фамилия Имя']} {team_member_with_birthday['День рождения']}\n"
    return tgmsg


def get_html_vacations_table(teams_members_with_vacation, teams_colors):
    html_table = "<table style='border-collapse: collapse; border: 1px solid black;'>"
    html_table += f"""
    <tr style='text-align: center;'>
        <td style='border: 1px solid black; width: 30px;'><strong>Команда</strong></td>
        <td style='border: 1px solid black; width: 220px;'><strong>Фамилия Имя</strong></td>
        <td style='border: 1px solid black; width: 100px;'><strong>Дата начала отпуска</strong></td>
        <td style='border: 1px solid black; width: 100px;'><strong>Дата окончания отпуска</strong></td>
        <td style='border: 1px solid black; width: 30px;'><strong>Количество дней отпуска</strong></td>
    </tr>"""
    for team_member_with_birthday in sorted(teams_members_with_vacation, key=lambda x: (x['Команда'], x['Дата начала отпуска (дата)'].day)):
        team = team_member_with_birthday['Команда']
        html_table += f"""
        <tr style='text-align: center; background-color: {teams_colors.get(team)};'>
            <td style='border: 1px solid black; width: 30px;'>{team}</td>
            <td style='border: 1px solid black; width: 220px;'>{team_member_with_birthday['Фамилия Имя']}</td>
            <td style='border: 1px solid black; width: 100px;'>{team_member_with_birthday['Дата начала отпуска']}</td>
            <td style='border: 1px solid black; width: 100px;'>{team_member_with_birthday['Дата окончания отпуска']}</td>
            <td style='border: 1px solid black; width: 100px;'>{team_member_with_birthday['Количество дней отпуска']}</td>
        </tr>"""
    html_table += "</table>"
    return html_table


def get_tgmsg_vacations_table(teams_members_with_vacation, subject):
    tgmsg = f"*{subject}*\n"
    traversed_teams = []
    for team_member_with_birthday in sorted(teams_members_with_vacation, key=lambda x: (x['Команда'], x['Дата начала отпуска (дата)'].day)):
        team = team_member_with_birthday['Команда']
        if team not in traversed_teams:
            traversed_teams.append(team)
            tgmsg += f'\n__*Команда {team}*__\n'
        tgmsg += f"""\t• {team_member_with_birthday['Фамилия Имя']} """ \
                 f"""_{re.escape(team_member_with_birthday['Дата начала отпуска'])} \- {re.escape(team_member_with_birthday['Дата окончания отпуска'])}_\n"""
    return tgmsg


def parse_date_birthday(date_string):
    current_date = datetime.datetime.now().date()
    dt = dateparser.parse(date_string, languages=['ru'])
    if dt.month <= current_date.month and dt.day < current_date.day:
        dt = datetime.datetime(dt.year + 1, dt.month, dt.day)
    return dt


def parse_date_vacation(date_string):
    return dateparser.parse(date_string, languages=['ru'])


def send_notifications(SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, SMTP_SERVER, SMTP_PORT,
                       LINK_BIRTHDAYS, LINK_VACATIONS, LINK_RECEIVER_EMAILS,
                       DAY_OF_MAILING_BIRTHDAYS, DAY_OF_MAILING_VACATIONS, TEAMS_COLORS,
                       bot_token, dr_group_ids, vac_group_ids):
    RECEIVER_EMAILS = ['cahr2001@mail.ru'] # pd.read_csv(LINK_RECEIVER_EMAILS)['Почта']
    current_date = datetime.datetime(year=2023, month=8, day=28) #.now().date()
    teams_members_birthdays = pd.read_csv(LINK_BIRTHDAYS)
    teams_members_birthdays['День рождения (дата)'] = teams_members_birthdays['День рождения'].apply(parse_date_birthday)
    teams_members_with_birthday_today = []
    teams_members_with_birthday_in_next_month = []
    for _, team_member in teams_members_birthdays.iterrows():
        team_member_birthday = team_member['День рождения (дата)']
        if (team_member_birthday.day == current_date.day and team_member_birthday.month == current_date.month) or \
                (team_member_birthday.weekday() == 5 and team_member_birthday.day == (current_date + datetime.timedelta(days=1)).day and team_member_birthday.month == (current_date + datetime.timedelta(days=1)).month) or \
                (team_member_birthday.weekday() == 6 and team_member_birthday.day == (current_date + datetime.timedelta(days=2)).day and team_member_birthday.month == (current_date + datetime.timedelta(days=2)).month):

            teams_members_with_birthday_today.append(team_member)
        if team_member_birthday.month == (current_date + relativedelta(months=1)).month:
            teams_members_with_birthday_in_next_month.append(team_member)

    if current_date.day == DAY_OF_MAILING_BIRTHDAYS and len(teams_members_with_birthday_in_next_month) != 0:
        msg = MIMEMultipart("alternative", policy=SMTPUTF8)
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAILS
        subject = f'Дни рождения {month_translations.get((current_date + relativedelta(months=1)).month)}'
        msg['Subject'] = subject

        html = f"""
            <html>
            <h2>Дни рождения коллег в следующем месяце:</h2> 
            {get_html_birthday_table(teams_members_with_birthday_in_next_month, TEAMS_COLORS)}
            </html>
        """
        msg.attach(MIMEText(html, "html"))
        send_msg_email(msg, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT)
        for dr_group_id in dr_group_ids:
            send_msg_telegram(get_tgmsg_birthday_table(teams_members_with_birthday_in_next_month, subject), bot_token, dr_group_id)

    if len(teams_members_with_birthday_today) != 0:
        msg = MIMEMultipart("alternative", policy=SMTPUTF8)
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAILS
        subject = 'Дни рождения СЕГОДНЯ'
        msg['Subject'] = subject

        html = f"""
            <html>
            <h2>У {'ваших коллег дни рождения' if len(teams_members_with_birthday_today) > 1 else 'вашего коллеги день рождение'}! Не забудьте передать свои пожелания :)</h2> 
            <ul>{''.join([f'<li>{m["Фамилия Имя"]} ({m["День рождения"]})</li>' for m in sorted(teams_members_with_birthday_today, key=lambda x: (x["Команда"], x["День рождения"]))])}</ul>
            </html>
        """
        msg.attach(MIMEText(html, "html"))
        send_msg_email(msg, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT)
        for dr_group_id in dr_group_ids:
            send_msg_telegram(get_tgmsg_birthday_table(teams_members_with_birthday_today, subject), bot_token, dr_group_id)

    if current_date.day == DAY_OF_MAILING_VACATIONS:
        teams_members_vacations = pd.read_csv(LINK_VACATIONS)
        teams_members_vacations['Дата начала отпуска (дата)'] = teams_members_vacations['Дата начала отпуска'].apply(parse_date_vacation)
        teams_members_with_vacations =[]
        for _, team_member in teams_members_vacations.iterrows():
            if team_member['Дата начала отпуска (дата)'].month == (current_date + relativedelta(months=1)).month and \
                    team_member['Дата начала отпуска (дата)'].year == (current_date + relativedelta(months=1)).year:
                teams_members_with_vacations.append(team_member)

        if len(teams_members_with_vacations) != 0:
            msg = MIMEMultipart("alternative", policy=SMTPUTF8)
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAILS
            subject = f'Отпуска коллег {month_translations.get((current_date + relativedelta(months=1)).month)}'
            msg['Subject'] = subject

            html = f"""
                <html>
                <h2>В следующем месяце планируются отпуска ваших коллег:</h2> 
                {get_html_vacations_table(teams_members_with_vacations, TEAMS_COLORS)}
                <p>Пожалуйста, планируйте свой график с учетом этих дат.</p> 
                </html>
            """
            msg.attach(MIMEText(html, "html"))
            send_msg_email(msg, SMTP_USERNAME, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT)
            for vac_group_id in vac_group_ids:
                send_msg_telegram(get_tgmsg_vacations_table(teams_members_with_vacations, subject), bot_token, vac_group_id)
