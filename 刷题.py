import json

import pandas
import random
import time
import os
import tkinter
import threading

# 读入文件 2023版中国近现代史纲要（删减版）.xlsx
df = pandas.read_excel('2023版中国近现代史纲要（删减版）.xlsx', sheet_name='Sheet1')

# 计算题库大小
question_number = len(df)

# 自动跳过按钮
auto_skip = True
# 自动跳过时间
auto_skip_time = 2

# df目录包括目录	题型	题干	正确答案	答案解析	难易度	知识点	选项数	A	B	C	D
# 绘制刷题窗口
window = tkinter.Tk()
window.title('近现代史刷题')
window.geometry('800x600')
window.resizable(width=False, height=False)
# 绘制题目，文本可变
question = tkinter.Message(window, text='题目', font=('Arial', 20), width=700)
question.place(x=0, y=0, width=700, height=200)
# 绘制选项
optionA = tkinter.Button(window, text='A', font=('Arial', 20))
optionA.place(x=0, y=200, width=800, height=50)
optionB = tkinter.Button(window, text='B', font=('Arial', 20))
optionB.place(x=0, y=250, width=800, height=50)
optionC = tkinter.Button(window, text='C', font=('Arial', 20))
optionC.place(x=0, y=300, width=800, height=50)
optionD = tkinter.Button(window, text='D', font=('Arial', 20))
optionD.place(x=0, y=350, width=800, height=50)
# 绘制答案
answer = tkinter.Label(window, text='答案', font=('Arial', 20))
answer.place(x=0, y=400, width=200, height=100)
# 绘制答案解析
analysis = tkinter.Message(window, text='答案解析', font=('Arial', 20), width=400)
analysis.place(x=200, y=400, width=600, height=100)
# 绘制按钮
button = tkinter.Button(window, text='开始', font=('Arial', 20), command=lambda: button_action())
button.place(x=600, y=500, width=200, height=100)
# 绘制目录
catalog = tkinter.Label(window, text='正确数：0/已完成：0/总题数：{}'.format(question_number), font=('Arial', 20))
catalog.place(x=0, y=500, width=600, height=100)
# 绘制难度
difficulty = tkinter.Label(window, text='难度', font=('Arial', 20))
difficulty.place(x=700, y=0, width=100, height=200)

# shuffle题库
df = df.sample(frac=1).reset_index(drop=True)
i = -1
t = -1
correct = 0
choice = []
# 记录错误题目题号与正确题目题号
if not os.path.exists('wrong.json'):
    wrong = []
else:
    with open('wrong.json', 'r') as f:
        wrong = json.load(f)
if not os.path.exists('right.json'):
    right = {}
else:
    with open('right.json', 'r') as f:
        right = json.load(f)
if not os.path.exists('skip.json'):
    skip = []
else:
    with open('skip.json', 'r') as f:
        skip = json.load(f)
# 按钮事件
def button_action():
    global i, correct, question_number, button, question, optionA, optionB, optionC, optionD, answer, analysis, catalog, difficulty, t, wrong, right, skip
    i += 1
    t += 1
    print(len(skip))
    while str(df['题号'][i]) in skip:
        i += 1
        t += 1
        correct += 1
        print("skip!")
    if t == question_number:
        i = 0
        t = 0
        correct = 0
        # 重新计算题库大小
        question_number = len(df)
    if df['题型'][i] == '单选题' or df['题型'][i] == '判断题':
        button.config(text='下一题')
    else:
        button.config(text='提交', command=lambda: muti_choice())
    # 显示题目
    question_text = str(df['题号'][i]) + "." + df['题型'][i] + ":" + df['题干'][i]
    question.config(text=question_text)
    # 显示答案
    answer.config(text='答案')
    # 显示答案解析
    analysis.config(text='答案解析')
    # 显示选项
    optionA_text = df['A'][i]
    optionA.config(text=optionA_text, command=lambda: option_button('A', df['题型'][i]), bg='SystemButtonFace')
    optionB_text = df['B'][i]
    optionB.config(text=optionB_text, command=lambda: option_button('B', df['题型'][i]), bg='SystemButtonFace')
    optionC_text = df['C'][i]
    if pandas.isna(optionC_text):
        optionC.config(text='', command=lambda: None, bg='SystemButtonFace')
    else:
        optionC.config(text=optionC_text, command=lambda: option_button('C', df['题型'][i]), bg='SystemButtonFace')
    optionD_text = df['D'][i]
    if pandas.isna(optionD_text):
        optionD.config(text='', command=lambda: None, bg='SystemButtonFace')
    else:
        optionD.config(text=optionD_text, command=lambda: option_button('D', df['题型'][i]), bg='SystemButtonFace')

    # 显示目录
    catalog_text = '正确数：{}/已完成：{}/总题数：{}'.format(correct, t, question_number)
    catalog.config(text=catalog_text)
    # 显示难度
    difficulty_text = df['难易度'][i]
    difficulty.config(text=difficulty_text)

    # 保存wrong和right到json
    with open('wrong.json', 'w') as f:
        json.dump(wrong, f)
    with open('right.json', 'w') as f:
        json.dump(right, f)
    with open('skip.json', 'w') as f:
        json.dump(skip, f)

def click_button():
    global i, auto_skip_time
    temp = i
    time.sleep(auto_skip_time)
    if temp == i:
        button_action()

def option_button(option, question_type):
    global i, correct, question_number, button, question, optionA, optionB, optionC, optionD, answer, analysis, catalog, difficulty, choice, t, wrong, right, skip, auto_skip
    if question_type == '单选题' or question_type == '判断题':
        if option == df['正确答案'][i].strip(' '):
            correct += 1
            if str(df['题号'][i]) in right:
                right[str(df['题号'][i])] += 1
            else:
                right[str(df['题号'][i])] = 1
            if not str(df['题号'][i]) in wrong or (right[str(df['题号'][i])] >= 3):
                skip.append(str(df['题号'][i]))
        else:
            wrong.append(str(df['题号'][i]))
            if str(df['题号'][i]) in right:
                right[str(df['题号'][i])] = 0
        # 显示目录
        catalog_text = '正确数：{}/已完成：{}/总题数：{}'.format(correct, t+1, question_number)
        catalog.config(text=catalog_text)
        # 显示答案解析
        analysis_text = df['答案解析'][i]
        if pandas.isna(analysis_text):
            analysis_text = '无答案解析'
        analysis.config(text=analysis_text)
        # 显示答案
        answer_text = df['正确答案'][i].strip(' ')
        answer.config(text=answer_text)
        # 显示选项
        # 选项变色
        if option == 'A' and option != df['正确答案'][i].strip(' '):
            optionA.config(bg='red', command=lambda :None)
        elif option == 'B' and option != df['正确答案'][i].strip(' '):
            optionB.config(bg='red', command=lambda :None)
        elif option == 'C' and option != df['正确答案'][i].strip(' '):
            optionC.config(bg='red', command=lambda :None)
        elif option == 'D' and option != df['正确答案'][i].strip(' '):
            optionD.config(bg='red', command=lambda :None)
        elif option == 'A' and option == df['正确答案'][i].strip(' '):
            optionA.config(bg='green', command=lambda :None)
        elif option == 'B' and option == df['正确答案'][i].strip(' '):
            optionB.config(bg='green', command=lambda :None)
        elif option == 'C' and option == df['正确答案'][i].strip(' '):
            optionC.config(bg='green', command=lambda :None)
        elif option == 'D' and option == df['正确答案'][i].strip(' '):
            optionD.config(bg='green', command=lambda :None)
        # 按钮变成下一题
        button.config(text='下一题', command=lambda: button_action())
        if option == df['正确答案'][i].strip(' '):
            # 删除该题
            df.drop(i, inplace=True)
            # 重排索引
            df.reset_index(drop=True, inplace=True)
            i -= 1
            if auto_skip:
                t1 = threading.Thread(target=click_button)
                t1.start()
    elif question_type == '多选题':
        if option in choice:
            choice.remove(option)
            if option == 'A':
                optionA.config(bg='SystemButtonFace')
            elif option == 'B':
                optionB.config(bg='SystemButtonFace')
            elif option == 'C':
                optionC.config(bg='SystemButtonFace')
            elif option == 'D':
                optionD.config(bg='SystemButtonFace')
        else:
            choice.append(option)
            if option == 'A':
                optionA.config(bg='yellow')
            elif option == 'B':
                optionB.config(bg='yellow')
            elif option == 'C':
                optionC.config(bg='yellow')
            elif option == 'D':
                optionD.config(bg='yellow')
        # 按钮变成提交
        button.config(text='提交', command=lambda: muti_choice())

def muti_choice():
    global i, correct, question_number, button, question, optionA, optionB, optionC, optionD, answer, analysis, catalog, difficulty, choice, t, skip
    flag = False
    right_answer = [x for x in df['正确答案'][i].strip(' ')]
    if set(choice) == set(right_answer):
        correct += 1
        flag = True
        if str(df['题号'][i]) in right:
            right[str(df['题号'][i])] += 1
        else:
            right[str(df['题号'][i])] = 1
        if not str(df['题号'][i]) in wrong or (right[str(df['题号'][i])] >= 3):
            skip.append(str(df['题号'][i]))
    else:
        wrong.append(str(df['题号'][i]))
        if str(df['题号'][i]) in right:
            right[str(df['题号'][i])] = 0
    # 显示目录
    catalog_text = '正确数：{}/已完成：{}/总题数：{}'.format(correct, t+1, question_number)
    catalog.config(text=catalog_text)
    # 显示答案解析
    analysis_text = df['答案解析'][i]
    if pandas.isna(analysis_text):
        analysis_text = '无答案解析'
    analysis.config(text=analysis_text)
    # 显示答案
    answer_text = df['正确答案'][i].strip(' ')
    answer.config(text=answer_text)
    # 显示选项
    # 选项变色
    if 'A' in choice and 'A' not in right_answer:
        optionA.config(bg='red', command=lambda :None)
    if 'B' in choice and 'B' not in right_answer:
        optionB.config(bg='red', command=lambda :None)
    if 'C' in choice and 'C' not in right_answer:
        optionC.config(bg='red', command=lambda :None)
    if 'D' in choice and 'D' not in right_answer:
        optionD.config(bg='red', command=lambda :None)
    if 'A' in choice and 'A' in right_answer:
        optionA.config(bg='green', command=lambda :None)
    if 'B' in choice and 'B' in right_answer:
        optionB.config(bg='green', command=lambda :None)
    if 'C' in choice and 'C' in right_answer:
        optionC.config(bg='green', command=lambda :None)
    if 'D' in choice and 'D' in right_answer:
        optionD.config(bg='green', command=lambda :None)
    if 'A' not in choice and 'A' in right_answer:
        optionA.config(bg='red', command=lambda :None)
    if 'B' not in choice and 'B' in right_answer:
        optionB.config(bg='red', command=lambda :None)
    if 'C' not in choice and 'C' in right_answer:
        optionC.config(bg='red', command=lambda :None)
    if 'D' not in choice and 'D' in right_answer:
        optionD.config(bg='red', command=lambda :None)
    # choice清空
    choice = []
    # 按钮变成下一题
    button.config(text='下一题', command=lambda: button_action())
    if flag:
        # 删除该题
        df.drop(i, inplace=True)
        # 重排索引
        df.reset_index(drop=True, inplace=True)
        i -= 1
        if auto_skip:
            t1 = threading.Thread(target=click_button)
            t1.start()



tkinter.mainloop()
