# -*- coding: utf-8 -*-
# Alyvix allows you to automate and monitor all types of applications
# Copyright (C) 2015 Alan Pipitone
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Developer: Alan Pipitone (Violet Atom) - http://www.violetatom.com/
# Supporter: Wuerth Phoenix - http://www.wuerth-phoenix.com/
# Official website: http://www.alyvix.com/

from alyvixcommon import *
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


def overwrite_alyvix_screen(overwrite="true"):

    overwrite_value = overwrite

    if overwrite.lower() == "true":
        overwrite_value = True
    elif overwrite.lower()  == "false":
        overwrite_value = False
        
    info_manager = InfoManager()
    
    info_manager.set_info("OVERWRITE LOG IMAGES", overwrite_value)
    
def alyvix_config(full_filename):
    os.environ["alyvix_testcase_config"] = full_filename

def send_keys(keys, encrypted="false"):

    encrypted_value = encrypted
    
    if encrypted.lower() == "true":
        encrypted_value = True
    elif encrypted.lower()  == "false":
        encrypted_value = False
        
    km = KeyboardManager()
    km.send(keys, encrypted_value)
    
def click(x, y, button="left", n=1):
    x_value = int(x)
    y_value = int(y)
    n_value = int(n)
    
    mm = MouseManager()
    
    button_value = mm.left_button
    
    if button.lower() == "right":
        button_value = mm.right_button
    
    mm.click(x_value, y_value, button_value, n_value)
    
def double_click(x, y):
    x_value = int(x)
    y_value = int(y)
    
    mm = MouseManager()
    mm.click(x_value, y_value, mm.left_button, 2)
    
def mouse_move(x, y):
    x_value = int(x)
    y_value = int(y)
    
    mm = MouseManager()
    mm.move(x_value, y_value)
    
def mouse_scroll(steps=2, direction="up"):
    steps_value = int(steps)
    
    mm = MouseManager()
        
    if direction.lower() == "up":
        direction = mm.wheel_up
    elif direction.lower()== "down":
        direction = mm.wheel_down
    
    mm.scroll(steps_value, direction)
    
def mouse_drag(x1, y1, x2, y2):

    mm = MouseManager()
    
    mm.drag(x1, y1, x2, y2)

def create_process(*popenargs, **kwargs):
    
    pm = ProcManager()
    proc = pm.create_process(popenargs)
    return proc.pid
    
def kill_process(process_name):
    
    pm = ProcManager()
    pm.kill_process(process_name)
    
def show_window(window_title):

    wm = WinManager()
    wm.show_window(window_title)
    
def maximize_window(window_title, timeout="60", exception="True"):

    exception_value = exception

    try:    
        if exception.lower() == "true":
            exception_value = True
        elif exception.lower() == "false":
            exception_value = False
    except:
        pass

    timeout_value = int(timeout)
    
    wm = WinManager()
    window_time = wm.maximize_window(window_title, timeout_value)
    
    if exception_value is True and window_time == -1:
        raise Exception("Window " + window_title + " has timed out: " + str(timeout) + " s.")
    
    return window_time
    
def wait_window(window_title, timeout="60", exception="True"):

    exception_value = exception
    
    try:     
        if exception.lower() == "true":
            exception_value = True
        elif exception.lower() == "false":
            exception_value = False
    except:
        pass

    timeout_value = int(timeout)

    wm = WinManager()
    window_time = wm.wait_window(window_title, timeout_value)
        
    if exception_value is True and window_time == -1:
        raise Exception("Window " + window_title + " has timed out: " + str(timeout) + " s.")
        
    return window_time
    
def wait_window_close(window_title, timeout="60", exception="True"):

    exception_value = exception
    
    try:     
        if exception.lower() == "true":
            exception_value = True
        elif exception.lower() == "false":
            exception_value = False
    except:
        pass

    timeout_value = int(timeout)

    wm = WinManager()
    window_time = wm.wait_window_close(window_title, timeout_value)
    
    if exception_value is True and window_time == -1:
        raise Exception("Window " + window_title + " has timed out: " + str(timeout) + " s.")
        
    return window_time
    
def check_window(window_title):
    
    wm = WinManager()
    return wm.check_if_window_exists(window_title)
    
def close_window(window_title):
    wm = WinManager()
    wm.close_window(window_title)

def alyvix_screenshot(filename_arg):

    variables = BuiltIn().get_variables()
    outdir = variables['${OUTPUTDIR}']

    filename = filename_arg

    if "." not in filename:
        ext = ".png"
        filename = filename + ext

    sm = ScreenManager()
    img = sm.grab_desktop()
    img_name = outdir + os.sep + filename

    img.save(img_name)

    logger.info('<a href="' + filename + '"><img src="' + filename + '" width="800px"></a>', html=True)
    
def add_perfdata(name, value=None, warning_threshold=None, critical_threshold=None, state=0):
    pm = PerfManager()
    #name_lower = str(name).lower().replace(" ", "_")
    pm.add_perfdata(name, value, warning_threshold, critical_threshold, state)
    
def rename_perfdata(old_name, new_name):
    
    #old_name_lower = str(old_name).lower().replace(" ", "_")
    #new_name_lower = str(new_name).lower().replace(" ", "_")

    pm = PerfManager()
    pm.rename_perfdata(old_name, new_name)

def get_perfdata(name, delete_perfdata="False"):
    delete_perfdata_value = delete_perfdata
    #name_lower = str(name).lower().replace(" ", "_")

    try:
        if delete_perfdata.lower() == "true":
            delete_perfdata_value = True
        elif delete_perfdata.lower() == "false":
            delete_perfdata_value = False
    except:
        pass

    pm = PerfManager()
    return pm.get_perfdata(name, delete_perfdata=delete_perfdata_value)

def delete_perfdata(name):
    #name_lower = str(name).lower().replace(" ", "_")

    pm = PerfManager()
    pm.delete_perfdata(name)

def sum_perfdata(*names, **kwargs):

    kwarglist = []

    for key in kwargs:
        if key == "delete_perfdata":

            try:
                if kwargs[key].lower() == "true":
                    value = True
                elif kwargs[key].lower()  == "false":
                    value = False

                kwargs[key] = value
            except:
                pass

        """
        if key == "name":
            kwargs[key] = str(kwargs[key]).lower().replace(" ", "_")
        """

    """
    new_names = []

    for name in names:
        new_names.append(str(name).lower().replace(" ", "_"))
    """

    pm = PerfManager()
    return pm.sum_perfdata(*names, **kwargs)

def update_alyvixdb(dbname=None):
    db = DbManager()
    db.insert_perfdata(str(dbname))

def print_perfdata(message=None, print_output="True"):

    message_value = None
    print_output_value = True
    
    try:
        if message.lower() != "":
            message_value = message
    except:
        pass
    
    try:    
        if print_output.lower() == "true":
            print_output_value = True
        elif print_output.lower() == "false":
            print_output_value = False
    except:
        pass

    pm = PerfManager()
    return pm.get_output(message_value, print_output_value)