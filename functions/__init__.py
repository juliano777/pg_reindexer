# Built-in imports
from os import getcwd as os_getcwd
from os.path import abspath as os_path_abspath
from os.path import join as os_path_join
from sys import path as sys_path

sys_path.append(os_path_abspath(os_path_join(os_getcwd(), '..')))
