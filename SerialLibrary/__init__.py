"""
Package: robotframework-SerialLibrary
Module:  SerialLibrary
Purpose: Provides a Robot Framework keyword wrapper for the freeware AutoIt tool
         (http://www.autoitscript.com/autoit3/index.shtml) via AutoIt's AutoItX.dll COM object.

         Copyright (c) 2008-2010 Texas Instruments, Inc.

         Licensed under the Apache License, Version 2.0 (the "License");
         you may not use this file except in compliance with the License.
         You may obtain a copy of the License at

             http://www.apache.org/licenses/LICENSE-2.0

         Unless required by applicable law or agreed to in writing, software
         distributed under the License is distributed on an "AS IS" BASIS,
         WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
         See the License for the specific language governing permissions and
         limitations under the License.
"""

from SerialOperation import SerialOperate


__version__ = '0.1'

class SerialLibrary(SerialOperate):
    """
    this keyword supply a method to operate the window you specified by windows handle.
    you can move the windows or set it on front in order to operate it.
    
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
