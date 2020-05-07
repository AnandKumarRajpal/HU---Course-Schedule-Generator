from tkinter import *

colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink', "yellow", "orange", "red", "green", "blue", 'pink']
def raise_frame(frame):
    frame.tkraise()

root = Tk()
root.configure(bg='white')

schedules = {}
buttons = {}
print(listofschedules)
for m in range(len(listofschedules)):
    schedules[m] = Frame(root)
    schedules[m].grid(row=0, column=0, sticky='news')

    courses = listofschedules[m]

    label = Label(schedules[m], text='Schedule '+str(m+1), font='Times', bg='white')
    label.pack(side='top', fill=X)
    canvas = Canvas(schedules[m], width=700, height=650, bg='white')
    canvas.pack()

    mon = canvas.create_rectangle(100, 0, 200, 30)
    tues = canvas.create_rectangle(200, 0, 300, 30)
    wed = canvas.create_rectangle(300, 0, 400, 30)
    thurs = canvas.create_rectangle(400, 0, 500, 30)
    fri = canvas.create_rectangle(500, 0, 600, 30)
    sat = canvas.create_rectangle(600, 0, 700, 30)

    canvas.create_text((150, 15), text='Monday')
    canvas.create_text((250, 15), text='Tuesday')
    canvas.create_text((350, 15), text='Wednesday')
    canvas.create_text((450, 15), text='Thursday')
    canvas.create_text((550, 15), text='Friday')
    canvas.create_text((650, 15), text='Saturday')

    time_boxes = {}
    initial_box_y1 = 30
    initial_box_y2 = 60

    for i in range(1, 22):
        time_boxes['t' + str(i)] = canvas.create_rectangle(0, initial_box_y1, 100, initial_box_y2)
        initial_box_y1 = initial_box_y2
        initial_box_y2 = initial_box_y1 + 30

    canvas.create_text((50, 45), text='8:30')
    canvas.create_text((50, 75), text='9:00')
    canvas.create_text((50, 105), text='9:30')
    canvas.create_text((50, 135), text='10:00')
    canvas.create_text((50, 165), text='10:30')
    canvas.create_text((50, 195), text='11:00')
    canvas.create_text((50, 225), text='11:30')
    canvas.create_text((50, 255), text='12:00')
    canvas.create_text((50, 285), text='12:30')
    canvas.create_text((50, 315), text='1:00')
    canvas.create_text((50, 345), text='1:30')
    canvas.create_text((50, 375), text='2:00')
    canvas.create_text((50, 405), text='2:30')
    canvas.create_text((50, 435), text='3:00')
    canvas.create_text((50, 465), text='3:30')
    canvas.create_text((50, 495), text='4:00')
    canvas.create_text((50, 525), text='4:30')
    canvas.create_text((50, 555), text='5:00')
    canvas.create_text((50, 585), text='5:30')
    canvas.create_text((50, 615), text='6:00')
    canvas.create_text((50, 645), text='6:30')

    hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    timetable = {}

    c = 0
    for j in courses:
        if j[5] == 0:
            stime = j[6][:-1].split(':')
            etime = j[7][:-1].split(':')
            timetable[j[3] + ' M ' + j[6]] = canvas.create_rectangle(100, (
                        (hours.index(int(stime[0])) * 60) + int(stime[1])), 200, ((hours.index(
                int(etime[0])) * 60) + int(etime[1]) + 30), fill=colors[c]), canvas.create_text(
                (150, ((hours.index(int(stime[0])) * 60) + int(stime[1]) + 40)), text=j[3] + ' ' + j[6] + '-' + j[7],
                width=70)
        if 1 == j[5]:
            stime = j[6][:-1].split(':')
            etime = j[7][:-1].split(':')
            timetable[j[3] + ' T ' + j[6]] = canvas.create_rectangle(200,
                                                                     ((hours.index(int(stime[0])) * 60) + int(
                                                                         stime[1])),
                                                                     300,
                                                                     ((hours.index(int(etime[0])) * 60) + int(
                                                                         etime[1]) + 30),
                                                                     fill=colors[c]), canvas.create_text(
                (250, ((hours.index(int(stime[0])) * 60) + int(stime[1]) + 40)), text=j[3] + ' ' + j[6] + '-' + j[7],
                width=70)
        if 2 == j[5]:
            stime = j[6][:-1].split(':')
            etime = j[7][:-1].split(':')
            timetable[j[3] + ' W ' + str(stime[0])] = canvas.create_rectangle(300,
                                                                              ((hours.index(int(stime[0])) * 60) + int(
                                                                                  stime[1])),
                                                                              400,
                                                                              ((hours.index(int(etime[0])) * 60) + int(
                                                                                  etime[1]) + 30),
                                                                              fill=colors[c]), canvas.create_text(
                (350, ((hours.index(int(stime[0])) * 60) + int(stime[1]) + 40)), text=j[3] + ' ' + j[6] + '-' + j[7],
                width=70)
        if 3 == j[5]:
            stime = j[6][:-1].split(':')
            etime = j[7][:-1].split(':')
            timetable[j[3] + ' T ' + str(stime[0])] = canvas.create_rectangle(400,
                                                                              ((hours.index(int(stime[0])) * 60) + int(
                                                                                  stime[1])),
                                                                              500,
                                                                              ((hours.index(int(etime[0])) * 60) + int(
                                                                                  etime[1]) + 30),
                                                                              fill=colors[c]), canvas.create_text(
                (450, ((hours.index(int(stime[0])) * 60) + int(stime[1]) + 40)), text=j[3] + ' ' + j[6] + '-' + j[7],
                width=70)
        if 4 == j[5]:
            stime = j[6][:-1].split(':')
            etime = j[7][:-1].split(':')
            timetable[j[3] + ' F ' + str(stime[0])] = canvas.create_rectangle(500,
                                                                              ((hours.index(int(stime[0])) * 60) + int(
                                                                                  stime[1])),
                                                                              600,
                                                                              ((hours.index(int(etime[0])) * 60) + int(
                                                                                  etime[1]) + 30),
                                                                              fill=colors[c]), canvas.create_text(
                (550, ((hours.index(int(stime[0])) * 60) + int(stime[1]) + 40)), text=j[3] + ' ' + j[6] + '-' + j[7],
                width=70)
        if 5 == j[5]:
            stime = j[6][:-1].split(':')
            etime = j[7][:-1].split(':')
            timetable[j[3] + ' S ' + str(stime[0])] = canvas.create_rectangle(600,
                                                                              ((hours.index(int(stime[0])) * 60) + int(
                                                                                  stime[1])),
                                                                              700,
                                                                              ((hours.index(int(etime[0])) * 60) + int(
                                                                                  etime[1]) + 30),
                                                                              fill=colors[c]), canvas.create_text(
                (650, ((hours.index(int(stime[0])) * 60) + int(stime[1]) + 40)), text=j[3] + ' ' + j[6] + '-' + j[7],
                width=70)
        c += 1





print(schedules)
# print(len(schedules))
# for v in range(len(schedules)+1):
#     print(v)
#     buttons[v] = Button(schedules[v], text='Next'+str(v), command=lambda: raise_frame(schedules[v]))
#     buttons[v].pack()

# for s in schedules:
#     buttons[s] = Button(s, text='Next',command=lambda: )
#
# buttons[2] = Button(schedules[2], text='Next', command= lambda: raise_frame(schedules[3]))
# buttons[2].pack()
# buttons[1] = Button(schedules[1], text='Next', command= lambda: raise_frame(schedules[2]))
# buttons[1].pack()
# buttons[0] = Button(schedules[0], text='Next', command= lambda: raise_frame(schedules[1]))
# buttons[0].pack()

try:
    buttons[0] = Button(schedules[0], text='Next', command=lambda: raise_frame(schedules[1]))
    buttons[0].pack(side='top')
    buttons[1] = Button(schedules[1], text='Next', command=lambda: raise_frame(schedules[2]))
    buttons[1].pack()
    buttons[2] = Button(schedules[2], text='Next', command=lambda: raise_frame(schedules[3]))
    buttons[2].pack()
    buttons[3] = Button(schedules[3], text='Next', command=lambda: raise_frame(schedules[4]))
    buttons[3].pack()
    buttons[4] = Button(schedules[4], text='Next', command=lambda: raise_frame(schedules[5]))
    buttons[4].pack()
    buttons[5] = Button(schedules[5], text='Next', command=lambda: raise_frame(schedules[6]))
    buttons[5].pack()
    buttons[6] = Button(schedules[6], text='Next', command=lambda: raise_frame(schedules[7]))
    buttons[6].pack()
    buttons[7] = Button(schedules[7], text='Next', command=lambda: raise_frame(schedules[8]))
    buttons[7].pack()
    buttons[8] = Button(schedules[8], text='Next', command=lambda: raise_frame(schedules[8]))
    buttons[8].pack()
    buttons[9] = Button(schedules[8], text='Next', command=lambda: raise_frame(schedules[10]))
    buttons[9].pack()
except:
    pass
print('hi')
raise_frame(schedules[0])
root.mainloop()