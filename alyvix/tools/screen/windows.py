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

import numpy
import win32gui
import win32ui
import win32api
import win32con
from PIL import Image
import cv2
import cv2.cv as cv
from .base import ScreenManagerBase


class ScreenManager(ScreenManagerBase):

    def __init__(self):
        super(ScreenManager, self).__init__()

    def grab_desktop(self, return_type=0):
        """
        grab desktop screenshot.

        :type return_type: int
        :param return_type: 0 for pil image, 1 for color matrix, 2 for gray matrix
        :rtype: numpy.ndarray or Image.Image
        :return: the screenshot image
        """

        ret_image = None

        #we use pywin32 api instead of PIL ImageGrab.
        #ImageGrab is slower than pywin32
        w = win32api.GetSystemMetrics(0)
        h = win32api.GetSystemMetrics(1)
        hwnd = win32gui.GetDesktopWindow()
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
        bmpinfo = dataBitMap.GetInfo()
        bmpstr = dataBitMap.GetBitmapBits(True)

        ret_image = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        if return_type == self.get_color_mat:
            return self._get_cv_color_mat(ret_image)
        if return_type == self.get_gray_mat:
            mat = self._get_cv_color_mat(ret_image)
            return self._get_cv_gray_mat(mat)
        else:
            return ret_image