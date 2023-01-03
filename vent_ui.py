import curses
import time
from datetime import datetime
import subprocess
import os

# get_io is using random values, but a real I/O handler would be here
values = [30]*9
old_values = []

            
def on_off_str(i):
    if values[i] == 30:
        res = 'ВКЛЮЧЕНО '
    else:
        res = 'ОТКЛЮЧЕНО'
    return res
    
def auto_flip():
    pass

def key_arr_of_read_system():
    global values
	bashCommand = "usbrelay"
	process =  subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()
    
	output = output.split()
	#print('output',output)
	for i in range(1,7):
		if ('HW554_' + str(i) + '=1').encode('UTF-8') in output:
            values[i] = 30
			#print('True ', i)
		elif ('HW554_' + str(i) + '=0').encode('UTF-8') in output:
			values[i] = 0
			#print('False ', i)
		else:
			print('Error: команда Вопрос ',i)
            
            
def startvent (i):
    s = 'HW554_' + str(i) + '=1'
    subprocess.call(["usbrelay", s], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    #print(s)
   
   
def stopvent (i):
    s = 'HW554_' + str(i) + '=0'
    subprocess.call(["usbrelay", s], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    #print(s)

def blue_rad_status():
    #ventview()
    global win1, win2, win3, win4, win5, win6, win7
    win1.clear()
    win1.border(0)
    
    win2.clear()
    win2.border(0)
    
    win3.clear()
    win3.border(0)
    
    win4.clear()
    win4.border(0)
    
    win5.clear()
    win5.border(0)
    
    win6.clear()
    win6.border(0)
    
    win7.clear()
    win7.border(0)
    
    # create bars bases on the returned values
    win1.addstr(1, 1, bar * values[1], curses.color_pair(2))
    win1.refresh()
    
    win2.addstr(1, 1, bar * values[2] , curses.color_pair(2))
    win2.refresh()
    
    win3.addstr(1, 1, bar * values[3] , curses.color_pair(2))
    win3.refresh()
    
    win4.addstr(1, 1, bar * values[4], curses.color_pair(2))
    win4.refresh()
    
    win5.addstr(1, 1, bar * values[5] , curses.color_pair(2))
    win5.refresh()
    
    win6.addstr(1, 1, bar * values[6] , curses.color_pair(1))
    win6.refresh()    

    win7.addstr(1, 1, bar * values[7] , curses.color_pair(1))
    win7.refresh()
    
    # win8.addstr(1, 1, bar * values[7] , curses.color_pair(1))
    # win8.refresh() 
    global stdscr
    # add numeric values beside the bars
    stdscr.addstr( 4,80, on_off_str(1) + " для изменения состояния нажмите клавишу 1",curses.A_BOLD )
    stdscr.addstr( 8,80, on_off_str(2) + " для изменения состояния нажмите клавишу 2",curses.A_BOLD )
    stdscr.addstr(12,80, on_off_str(3) + " для изменения состояния нажмите клавишу 3",curses.A_BOLD )
    stdscr.addstr(16,80, on_off_str(4) + " для изменения состояния нажмите клавишу 4",curses.A_BOLD )
    stdscr.addstr(20,80, on_off_str(5) + " для изменения состояния нажмите клавишу 5",curses.A_BOLD )
    stdscr.addstr(24,80, on_off_str(6) + " для изменения состояния нажмите клавишу 6",curses.A_BOLD )
    stdscr.addstr(28,80, on_off_str(7) + " для изменения состояния нажмите клавишу 7",curses.A_BOLD )
    # stdscr.addstr(32,80, on_off_str(8) + "для изменения состояния нажмите клавишу F8 ",curses.A_BOLD )
    
    #stdscr.addstr(36,80, "Состояние программы ",curses.A_BOLD )
    
    
    stdscr.refresh()
    
    stdscr.nodelay(1)


stdscr = curses.initscr()
curses.noecho()

bar = '█' # an extended ASCII 'fill' character
height, width = stdscr.getmaxyx() # get the window size
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

# layout the header and footer
stdscr.addstr(1,1, " " * (width -2),curses.color_pair(1) )
stdscr.addstr(1,15, "ВЕНТИЛЯЦИЯ КДЦ НЕФТЯНИК",curses.color_pair(1) )
stdscr.hline(2,1,"_",width)
stdscr.addstr(height -1,1, " " * (width -2),curses.color_pair(1) )
stdscr.addstr(height -1,5, "Для выхода нажмите Ctrl+C",curses.color_pair(1) )
 
# add some labels
stdscr.addstr(4,1,  "(B1)Вытяжка:________________Зрительный зал")
stdscr.addstr(8,1,  "(B2)Вытыжка:__________________Зал торжеств")
stdscr.addstr(12,1, "(B3)Вытыжка:______________________Гостиная")
stdscr.addstr(16,1, "(B4)Вытыжка:__________________Правое крыло")
stdscr.addstr(20,1, "(B12)Холодная приточка:_Студия звукозаписи")
stdscr.addstr(24,1, "(П1)Тёплая приточка:___Правое крыло здания")
stdscr.addstr(28,1, "(К1)Тёплая приточка:________Зрительный зал")
#stdscr.addstr(32,1, "__________________________________________")
 
# Define windows to be used for bar charts
win1 = curses.newwin(3, 32, 3, 45) # curses.newwin(height, width, begin_y, begin_x)
win2 = curses.newwin(3, 32, 7, 45) # curses.newwin(height, width, begin_y, begin_x)
win3 = curses.newwin(3, 32, 11, 45) # curses.newwin(height, width, begin_y, begin_x)
win4 = curses.newwin(3, 32, 15, 45) # curses.newwin(height, width, begin_y, begin_x)
win5 = curses.newwin(3, 32, 19, 45) # curses.newwin(height, width, begin_y, begin_x)
win6 = curses.newwin(3, 32, 23, 45) # curses.newwin(height, width, begin_y, begin_x)
win7 = curses.newwin(3, 32, 27, 45) # curses.newwin(height, width, begin_y, begin_x)
#win8 = curses.newwin(3, 32, 31, 45) # curses.newwin(height, width, begin_y, begin_x)


key_arr_of_read_system()
blue_rad_status() 
# Use the 'q' key to quit

k = 0
t_i = 0
while True:
    time.sleep(0.1)
    t_i += 1
    if t_i == 50:
        t_i = 0
        key_arr_of_read_system()
        
    
    # 1 k=49 , 2 k=50 ,3 k=51 ,4 k=52 ,5 k=53 ,6 k=54 ,7 k=55 , 0 k=48 ,
    if k == 49:
        if values[1] == 0:
            startvent(1)
            key_arr_of_read_system()
        else:
            stopvent(1)
            key_arr_of_read_system()
    elif k == 50:
        if values[2] == 0:
            startvent(2)
            key_arr_of_read_system()    
        else:
            stopvent(2)
            key_arr_of_read_system()
    elif k == 51:
        if values[3] == 0:
            startvent(3)
            key_arr_of_read_system()
        else:
            stopvent(3)
            key_arr_of_read_system()            
    elif k == 52:
        if values[4] == 0:
            startvent(4)
            key_arr_of_read_system()
        else:
            stopvent(4)
            key_arr_of_read_system()
    elif k == 53:
        if values[5] == 0:
            startvent(5)
            key_arr_of_read_system()
        else:
            stopvent(5)
            key_arr_of_read_system()
    elif k == 54:
        if values[6] == 0:
            startvent(6)
            key_arr_of_read_system()
        else:
            stopvent(6)
            key_arr_of_read_system()
    elif k == 55:
        if values[7] == 0:
            startvent(7)
            key_arr_of_read_system()
        else:
            stopvent(7)
            key_arr_of_read_system()
    elif k == 48:
        auto_flip()
    else:
        pass
    
    # stdscr.clear()
    
    if values != old_values:
        key_arr_of_read_system()
        blue_rad_status()
    
    old_values = values.copy()
    

    k = stdscr.getch() # look for a keyboard input, but don't wait
 
curses.endwin() # restore the terminal settings back to the original


    