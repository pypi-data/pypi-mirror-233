"""
一个基于matplotlib的按钮图形界面工具

v0.1 : 2022-10-18
v0.11: 2022-12-25 GUI部分独立出来
v0.2 : 2023R 发布到pypi
v0.24: 2023-09, add close action, fix some bugs
v0.25: 2023-10，button required in action parameters
v0.26: Fix some bugs

本模块用于在指定的ax上画按钮，并且在循环中等候按钮点击事件。
提供两个类：按钮 i_button 和 按钮控制器 i_btn_ctl
按钮一般不直接建立，通过控制器去建立按钮，并且管理。
按钮有以下属性：color背景颜色，text文本，cmd命令关键字，checked是否被选中，
  chk_color chk_text选中后的颜色和文字
按钮添加的时候需要指定中点x、y和宽度高度。
按钮有一个action属性，可以关联一个回调函数。当按钮被点击时会调用。
在控制器上也可以指定通用的点击回调函数。
优先级是：按钮自带的回调函数--创建控制器时的回调函数。
"""


from ._i_btn_ import i_button, i_btn_ctl
__version__ = "0.26"
__pubdate__ = "2023-10-04"
