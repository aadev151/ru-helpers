# Copyright 2021 by Alexander Anisimov.
# All rights reserved.
# If you want to use this code or distribute it,
# please contact me via email:
# vomisina.xela@gmail.com or alex@hqbrowser.tk


import flask
import os

app = flask.Flask(__name__)


# index page
@app.route('/')
def main():
    deleted_tasks_file = open('deleted_tasks.txt', 'r')
    deleted_tasks = int(deleted_tasks_file.read())
    deleted_tasks_file.close()
    return flask.render_template('index.html', tasks=deleted_tasks)


# privacy policy
@app.route('/policy')
def policy():
    return flask.render_template('privacy.html')


# page for funds that creates a task
@app.route('/create-task')
def create_task():
    approved_funds = []
    funds = []
    funds_file = open('funds.txt')

    for line in funds_file:
        funds.append(line[:-1])

    funds_file.close()

    for fund in funds:
        fund_file = open('funds/' + fund + '/approved.txt')
        if fund_file.read() == "yes":
            approved_funds.append(fund)

        fund_file.close()

    questions = []

    for fund in approved_funds:
        question_file = open('funds/' + fund + '/question.txt', 'r')
        question = question_file.read()
        question_file.close()
        questions.append(question)


    return flask.render_template('create_task.html', approved_funds=approved_funds, questions=questions)


# page for developers
@app.route('/developers')
def developers():
    announcements = []

    announcements_names = open('announcements.txt', 'r')
    for line in announcements_names:
        text = line.split("|")
        announcements.append([text[0], text[1]])
    announcements_names.close()

    return flask.render_template('developers.html', announcements=announcements)


# page for funds
@app.route('/funds')
def funds():
    return flask.render_template('funds.html')


# page for donations
@app.route('/donate')
def donate():
    return flask.render_template('donate.html')


# info about an announcement
@app.route('/announcement/<announcement>')
def about_announcement(announcement):
    name_file = open('announcements/' + announcement + '/name.txt', 'r')
    announcement_name = name_file.read()
    name_file.close()
    info_file = open('announcements/' + announcement + '/info.txt', 'r')
    announcement_info = info_file.read().split('\n')
    info_file.close()

    return flask.render_template('about_task.html', name=announcement_name, info=announcement_info, href=announcement)


# perform an announcement
@app.route('/announcement/<announcement>/perform')
def perform_announcement(announcement):
    fund_file = open('announcements/' + announcement + '/fund.txt', 'r')
    fund = fund_file.read()
    fund_file.close()

    name_file = open('announcements/' + announcement + '/name.txt', 'r')
    name = name_file.read()
    name_file.close()
    info_file = open('announcements/' + announcement + '/info.txt', 'r')
    info = info_file.read().split('\n')
    info_file.close()

    email_file = open('funds/' + fund + '/email.txt', 'r')
    email = email_file.read()
    email_file.close()

    short_email = email[:3] + "..."

    return flask.render_template('perform_task.html', name=name, info=info, fund=fund,
                                 short_email=short_email, long_email=email, number=announcement)


# delete an announcement (if it is not necessary anymore)
@app.route('/announcement/<announcement>/delete')
def delete_announcement(announcement):
    fund_file = open('announcements/' + announcement + '/fund.txt', 'r')
    fund = fund_file.read()
    fund_file.close()

    name_file = open('announcements/' + announcement + '/name.txt', 'r')
    name = name_file.read()
    name_file.close()
    info_file = open('announcements/' + announcement + '/info.txt', 'r')
    info = info_file.read().split('\n')
    info_file.close()

    question_file = open('funds/' + fund + '/question.txt', 'r')
    question = question_file.read()
    question_file.close()

    return flask.render_template('delete_task.html', name=name, info=info, question=question, href=announcement)


@app.route('/announcement/<announcement>/delete/processing...', methods=["GET", "POST"])
def processing_delete_announcement(announcement):
    fund_file = open('announcements/' + announcement + '/fund.txt', 'r')
    fund = fund_file.read()
    fund_file.close()

    answer_file = open('funds/' + fund + '/answer.txt', 'r')
    needed_answer = answer_file.read()
    answer_file.close()

    answer = flask.request.form['answer']

    if answer.lower() != needed_answer.lower():
        name_file = open('announcements/' + announcement + '/name.txt', 'r')
        name = name_file.read()
        name_file.close()
        info_file = open('announcements/' + announcement + '/info.txt', 'r')
        info = info_file.read().split('\n')
        info_file.close()

        return flask.render_template('delete_task.html', name=name, info=info, href=announcement, error="Неправильный ответ! В доступе отказано. Попробуйте еще раз")

    announcements = []
    index = 0
    found = False
    announcements_names = open('announcements.txt', 'r')
    for line in announcements_names:
        text = line.split("|")
        announcements.append([text[0], text[1]])
        if not found:
            if text[1] == announcement:
                found = True
        else:
            index += 1
    announcements_names.close()

    del announcements[index]

    announcements_file = open('announcements.txt', 'w')
    for a in announcements:
        announcements_file.write(a[0] + '|' + a[1] + '\n')

    announcements_file.close()

    deleted_tasks_file = open('deleted_tasks.txt', 'r')
    deleted_tasks = int(deleted_tasks_file.read())
    deleted_tasks_file.close()

    deleted_tasks_file = open('deleted_tasks.txt', 'w')
    deleted_tasks_file.write(str(deleted_tasks + 1))
    deleted_tasks_file.close()

    return flask.render_template('funds.html')


@app.route('/processing...', methods=["GET", "POST"])
def processing_info():
    if flask.request.method == "GET":
        return flask.redirect('/')

    name = flask.request.form['name']
    info = flask.request.form['info']
    fund = flask.request.form['fund']
    answer = flask.request.form['answer']

    answer_file = open('funds/' + fund + '/answer.txt', 'r')
    needed_answer = answer_file.read()
    answer_file.close()



    if str(answer).lower() != needed_answer.lower():
        approved_funds = []
        funds = []
        funds_file = open('funds.txt')

        for line in funds_file:
            funds.append(line[:-1])

        funds_file.close()

        for fund in funds:
            fund_file = open('funds/' + fund + '/approved.txt')
            if fund_file.read() == "yes":
                approved_funds.append(fund)

            fund_file.close()

        questions = []

        for fund in approved_funds:
            question_file = open('funds/' + fund + '/question.txt', 'r')
            question = question_file.read()
            question_file.close()
            questions.append(question)

        return flask.render_template('create_task.html', approved_funds=approved_funds,
                                     questions=questions, error="Неправильный ответ! В доступе отказано. Попробуйте еще раз. Проверьте ответ на наличие пробела в конце, если он присутствует, удалите его",
                                     name=name, info=info)

    last_id_file = open('announcements/last_id.txt', 'r')
    last_id = str(int(last_id_file.read()) + 1)
    last_id_file.close()
    last_id_file = open('announcements/last_id.txt', 'w')
    last_id_file.write(last_id)
    last_id_file.close()

    os.mkdir('announcements/' + last_id)

    name_file = open('announcements/' + last_id + '/name.txt', 'w')
    name_file.write(name)
    name_file.close()
    info_file = open('announcements/' + last_id + '/info.txt', 'w')
    info_file.write(info)
    info_file.close()
    fund_file = open('announcements/' + last_id + '/fund.txt', 'w')
    fund_file.write(fund)
    fund_file.close()

    announcements_names = open('announcements.txt', 'a+')
    announcements_names.write(name + "|" + last_id + "\n")
    announcements_names.close()

    return flask.redirect('/funds')


@app.route('/processing-fund-partnership...', methods=["GET", "POST"])
def processing_fund_partnership():
    if flask.request.method == "GET":
        return flask.redirect('/')

    name = flask.request.form['name']
    email = flask.request.form['email']
    question = flask.request.form['question']
    answer = flask.request.form['answer']

    os.mkdir('funds/' + name)
    email_file = open('funds/' + name + '/email.txt', 'w')
    email_file.write(email)
    email_file.close()
    question_file = open('funds/' + name + '/question.txt', 'w')
    question_file.write(question)
    question_file.close()
    answer_file = open('funds/' + name + '/answer.txt', 'w')
    answer_file.write(answer)
    answer_file.close()
    approved_file = open('funds/' + name + '/approved.txt', 'w')
    approved_file.write("no")
    approved_file.close()

    funds = open('funds.txt', 'a+')
    funds.write(name + '\n')
    funds.close()

    return flask.redirect('/#partnership')


# error 404
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404


