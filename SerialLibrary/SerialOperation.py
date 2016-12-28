#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Purpose:     SerialLibrary for robot framework frame.
#
# Author:      majun11
# Created:     2016-12-03
# Version:     0.1
# Copyright:   (c) junma188902@gamil.com 2016
#---------------------------------------------------------

import serial
from time import *
import logging
import traceback
from serial.serialwin32 import Serial
from serial.config import Configuration, IntegerEntry, LogLevelEntry, NewlineEntry,StringEntry, TimeEntry
from serial.serialutil import *
import SerialLibrary
try:
    from robot.api import logger
except ImportError:
    logger = None

from robot.utils import ConnectionCache

import thread

__version__ = "1.0.0"

class IndoorException(Exception):
    
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
        
 
class serialinfo(object):
    def __init__(self):
        self.port = None
        self.baudrate = None
        self.timeout = 0.01
    def setvalue(self,port,baudrate):
        self.port = port
        self.baudrate = baudrate


class SerialOperate(object):
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    DEFAULT_TIMEOUT = 0.1
    DEFAULT_NEWLINE = 'LF'
    DEFAULT_PROMPT = '>'
    DEFAULT_LOGLEVEL = 'INFO'
    DEFAULT_TERM_TYPE = 'vt100'
    DEFAULT_TERM_WIDTH = 80
    DEFAULT_TERM_HEIGHT = 24
    DEFAULT_PATH_SEPARATOR = '/'
    DEFAULT_ENCODING = 'UTF-8'
    
    def __init__(self, developer_email="majun11@hikvision.com.cn",
                 timeout=DEFAULT_TIMEOUT,
                 newline=DEFAULT_NEWLINE,
                 prompt=DEFAULT_PROMPT,
                 loglevel=DEFAULT_LOGLEVEL,
                 term_type=DEFAULT_TERM_TYPE,
                 width=DEFAULT_TERM_WIDTH,
                 height=DEFAULT_TERM_HEIGHT,
                 path_separator=DEFAULT_PATH_SEPARATOR,
                encoding=DEFAULT_ENCODING):       
        self.developer_email=developer_email
        self._connections = ConnectionCache()
        self._config = _DefaultConfiguration(
        timeout or self.DEFAULT_TIMEOUT,
        newline or self.DEFAULT_NEWLINE,
        prompt or self.DEFAULT_PROMPT,
        loglevel or self.DEFAULT_LOGLEVEL,
        term_type or self.DEFAULT_TERM_TYPE,
        width or self.DEFAULT_TERM_WIDTH,
        height or self.DEFAULT_TERM_HEIGHT,
        path_separator or self.DEFAULT_PATH_SEPARATOR,
        encoding or self.DEFAULT_ENCODING
        )
        print "init ok\n"
        
    @property
    def current(self):
        return self._connections.current
    
    
    def open_serial_connection(self, port='com1',baudrate = 115200, alias=None, timeout=None,
                        newline=None, prompt=None, term_type=None, width=None,
                        height=None, path_separator=None, encoding=None):
        """Opens a new serial connection to the given `host` and `port`.

        The new connection is made active. Possible existing connections
        are left open in the background.

        This keyword returns the index of the new connection which can be used
        later to switch back to it. Indices start from `1` and are reset
        when `Close All Connections` is used.

        Optional `alias` can be given for the connection and can be used for
        switching between connections, similarly as the index.
        See `Switch Connection` for more details.

        Connection parameters, like [#Default timeout|`timeout`] and
        [#Default newline|`newline`] are documented in `configuration`.
        If they are not defined as arguments, [#Configuration|the library
        defaults] are used for the connection.

        All the arguments, except `host`, `alias` and `port`
        can be later updated with `Set Client Configuration`.

        Starting from SerialLibrary 1.1, a shell is automatically opened
        by this keyword.

        Port `22` is assumed by default:
        | ${index}= | Open Connection | my.server.com |

        Non-standard port may be given as an argument:
        | ${index}= | Open Connection | 192.168.1.1 | port=23 |

        Aliases are handy, if you need to switch back to the connection later:
        | Open Connection   | my.server.com | alias=myserver |
        | # Do something with my.server.com |
        | Open Connection   | 192.168.1.1   |
        | Switch Connection | myserver      |                | # Back to my.server.com |

        Settings can be overridden per connection, otherwise the ones set on
        `library importing` or with `Set Default Configuration` are used:
        | Open Connection | 192.168.1.1   | timeout=1 hour    | newline=CRLF          |
        | # Do something with the connection                  |
        | Open Connection | my.server.com | # Default timeout | # Default line breaks |

        [#Default terminal settings|The terminal settings] are also configurable
        per connection:
        | Open Connection | 192.168.1.1  | term_type=ansi | width=40 |

        Arguments [#Default path separator|`path_separator`] and
        [#Default encoding|`encoding`]
        were added in SSHLibrary 2.0.
        """
        timeout = timeout or self._config.timeout
        newline = newline or self._config.newline
        prompt = prompt or self._config.prompt
        term_type = term_type or self._config.term_type
        width = width or self._config.width
        height = height or self._config.height
        path_separator = path_separator or self._config.path_separator
        encoding = encoding or self._config.encoding
 #       client = SSHClient(host, alias, port, timeout, newline, prompt,
 #                          term_type, width, height, path_separator, encoding)
        client = Serial(port,baudrate, timeout = 0.1)
        connection_index = self._connections.register(client, alias)
        client.config.update(index=connection_index)
        return connection_index
    def switch_serial_connection(self, index_or_alias):
        """Switches the active connection by index or alias.

        `index_or_alias` is either connection index (an integer) or alias
        (a string). Index is got as the return value of `Open Connection`.
        Alternatively, both index and alias can queried as attributes
        of the object returned by `Get Connection`.

        This keyword returns the index of the previous active connection,
        which can be used to switch back to that connection later.

        Example:
        | ${myserver}=      | Open Connection | my.server.com |
        | Login             | johndoe         | secretpasswd  |
        | Open Connection   | build.local.net | alias=Build   |
        | Login             | jenkins         | jenkins       |
        | Switch Connection | ${myserver}     |               | # Switch using index          |
        | ${username}=      | Execute Command | whoami        | # Executed on my.server.com   |
        | Should Be Equal   | ${username}     | johndoe       |
        | Switch Connection | Build           |               | # Switch using alias          |
        | ${username}=      | Execute Command | whoami        | # Executed on build.local.net |
        | Should Be Equal   | ${username}     | jenkins       |
        """
        old_index = self._connections.current_index
        if index_or_alias is None:
            self.close_connection()
        else:
            self._connections.switch(index_or_alias)
        return old_index
#     def open_serial(self,*args, **kwargs):
#         try:
#             self.console = Serial(*args, **kwargs)
#         except Exception as e: 
#             raise IndoorException("open serial failed")
#         if self.console.isOpen():
#             logging.info(u'[ open serial successfully\n')
#         else:
#             logging.info(u'[open serial failed\n')
#         return self.console
    def close_serial_connection(self):
        """Closes the current connection.

        No other connection is made active by this keyword. Manually use
        `Switch Connection` to switch to another connection.

        Example:
        | Open Connection  | my.server.com  |
        | Login            | johndoe        | secretpasswd |
        | Get File         | results.txt    | /tmp         |
        | Close Connection |
        | # Do something with /tmp/results.txt             |
        """
        self.current.close()
        self._connections.current = self._connections._no_current
    def close_all_serial_connections(self):
        """Closes all open connections.

        This keyword is ought to be used either in test or suite teardown to
        make sure all the connections are closed before the test execution
        finishes.

        After this keyword, the connection indices returned by `Open Connection`
        are reset and start from `1`.

        Example:
        | Open Connection | my.server.com         |
        | Open Connection | build.local.net       |
        | # Do something with the connections     |
        | [Teardown]      | Close all connections |
        """
        self._connections.close_all()    
    
    def _info(self, msg):
        self._log(msg, 'INFO')

    def _log(self, msg, level=None):
        level = self._active_loglevel(level)
        msg = msg.strip()
        if not msg:
            return
        if logger:
            logger.write(msg, level)
        else:
            print '*%s* %s' % (level, msg)
    def _active_loglevel(self, level):
        if level is None:
            return self._config.loglevel
        if isinstance(level, basestring) and \
                level.upper() in ['TRACE', 'DEBUG', 'INFO', 'WARN', 'HTML']:
            return level.upper()
        raise AssertionError("Invalid log level '%s'." % level)
    
    def _legacy_output_options(self, stdout, stderr, rc):
        if not isinstance(stdout, basestring):
            return stdout, stderr, rc
        stdout = stdout.lower()
        if stdout == 'stderr':
            return False, True, rc
        if stdout == 'both':
            return True, True, rc
        return stdout, stderr, rc
    def execute_serial_command(self, command, return_stdout=True, return_stderr=False,
                        return_rc=False):
        """Executes `command` on the remote machine and returns its outputs.

        This keyword executes the `command` and returns after the execution
        has been finished. Use `Start Command` if the command should be
        started on the background.

        By default, only the standard output is returned:
        | ${stdout}=     | Execute Command | echo 'Hello John!' |
        | Should Contain | ${stdout}       | Hello John!        |

        Arguments `return_stdout`, `return_stderr` and `return_rc` are used
        to specify, what is returned by this keyword.
        If several arguments evaluate to true, multiple values are returned.
        Non-empty strings, except `false` and `False`, evaluate to true.

        If errors are needed as well, set the respective argument value to true:
        | ${stdout}       | ${stderr}= | Execute Command | echo 'Hello John!' | return_stderr=True |
        | Should Be Empty | ${stderr}  |

        Often checking the return code is enough:
        | ${rc}=                      | Execute Command | echo 'Hello John!' | return_stdout=False | return_rc=True |
        | Should Be Equal As Integers | ${rc}           | 0                  | # succeeded         |

        The `command` is always executed in a new shell. Thus possible changes
        to the environment (e.g. changing working directory) are not visible
        to the later keywords:
        | ${pwd}=         | Execute Command | pwd           |
        | Should Be Equal | ${pwd}          | /home/johndoe |
        | Execute Command | cd /tmp         |
        | ${pwd}=         | Execute Command | pwd           |
        | Should Be Equal | ${pwd}          | /home/johndoe |

        `Write` and `Read` can be used for
        [#Interactive shells|running multiple commands in the same shell].

        This keyword logs the executed command and its exit status with
        log level `INFO`.
        """
        self._info("Executing command '%s'." % command)
        opts = self._legacy_output_options(return_stdout, return_stderr,
                                           return_rc)
        self.current.write_cmd(command)
        return self.current.read(1024)
    
    def read_command_output(self, return_stdout=True, return_stderr=False,
                            return_rc=False):
        """Returns outputs of the most recent started command.

        At least one command must have been started using `Start Command`
        before this keyword can be used.

        By default, only the standard output of the started command is returned:
        | Start Command  | echo 'Hello John!'  |
        | ${stdout}=     | Read Command Output |
        | Should Contain | ${stdout}           | Hello John! |

        Arguments `return_stdout`, `return_stderr` and `return_rc` are used
        to specify, what is returned by this keyword.
        If several arguments evaluate to true, multiple values are returned.
        Non-empty strings, except `false` and `False`, evaluate to true.

        If errors are needed as well, set the argument value to true:
        | Start Command   | echo 'Hello John!' |
        | ${stdout}       | ${stderr}=         | Read Command Output | return_stderr=True |
        | Should Be Empty | ${stderr}          |

        Often checking the return code is enough:
        | Start Command               | echo 'Hello John!'  |
        | ${rc}=                      | Read Command Output | return_stdout=False | return_rc=True |
        | Should Be Equal As Integers | ${rc}               | 0                   | # succeeded    |

        Using `Start Command` and `Read Command Output` follows
        'last in, first out' (LIFO) policy, meaning that `Read Command Output`
        operates on the most recent started command, after which that command
        is discarded and its output cannot be read again.

        If several commands have been started, the output of the last started
        command is returned. After that, a subsequent call will return the
        output of the new last (originally the second last) command:
        | Start Command  | echo 'HELLO'        |
        | Start Command  | echo 'SECOND'       |
        | ${stdout}=     | Read Command Output |
        | Should Contain | ${stdout}           | 'SECOND' |
        | ${stdout}=     | Read Command Output |
        | Should Contain | ${stdout}           | 'HELLO'  |

        This keyword logs the read command with log level `INFO`.
        """
        self._info("Reading output of command '%s'." % self._last_command)
        opts = self._legacy_output_options(return_stdout, return_stderr,
                                           return_rc)
        stdout, stderr, rc = self.current.read(1024)
  
        return self._return_command_output(stdout, stderr, rc, *opts)

    
    def _return_command_output(self, stdout, stderr, rc, return_stdout,
                               return_stderr, return_rc):
        self._info("Command exited with return code %d." % rc)
        ret = []
        if self._output_wanted(return_stdout):
            ret.append(stdout.rstrip('\n'))
        if self._output_wanted(return_stderr):
            ret.append(stderr.rstrip('\n'))
        if self._output_wanted(return_rc):
            ret.append(rc)
        if len(ret) == 1:
            return ret[0]
        return ret
    
    def _output_wanted(self, value):
        return value and str(value).lower() != 'false'    

    def read(self, loglevel=None, delay=None):
        """Consumes and returns everything available on the server output.

        If `delay` is given, this keyword waits that amount of time and reads
        output again. This wait-read cycle is repeated as long as further reads
        return more output or the [#Default timeout|timeout] expires.
        `delay` must be given in Robot Framework's time format (e.g. `5`,
        `4.5s`, `3 minutes`, `2 min 3 sec`) that is explained in detail in
        the User Guide.

        This keyword is most useful for reading everything from
        the server output, thus clearing it.

        The read output is logged. `loglevel` can be used to override
        the [#Default loglevel|default log level].

        Example:
        | Open Serial Connection | com1 |
        | Login           | johndoe       | secretpasswd                 |
        | Write           | sudo su -     |                              |
        | ${output}=      | Read          | delay=0.5s                   |
        | Should Contain  | ${output}     | [sudo] password for johndoe: |
        | Write           | secretpasswd  |                              |
        | ${output}=      | Read          | loglevel=WARN | # Shown in the console due to loglevel |
        | Should Contain  | ${output}     | root@                        |

        See `interactive shells` for more information about writing and reading
        in general.

        Argument `delay` was added in SSHLibrary 2.0.
        """
        return self._read_and_log(loglevel, self.current.read, timeout = delay)    
    def read_until_prompt(self, loglevel=None):
        """Consumes and returns the server output until the prompt is found.

        Text up and until prompt is returned. [#Default prompt|The prompt must
        be set] before this keyword is used.

        If [#Default timeout|the timeout] expires before the match is found,
        this keyword fails.

        This keyword is useful for reading output of a single command when
        output of previous command has been read and that command does not
        produce prompt characters in its output.

        The read output is logged. `loglevel` can be used to override
        the [#Default loglevel|default log level].

        Example:
        | Open Connection          | my.server.com     | prompt=$         |
        | Login                    | johndoe           | ${PASSWORD}      |
        | Write                    | sudo su -         |                  |
        | Write                    | ${PASSWORD}       |                  |
        | Set Client Configuration | prompt=#          | # For root, the prompt is # |
        | ${output}=               | Read Until Prompt |                  |
        | Should End With          | ${output}         | root@myserver:~# |

        See also `Read Until` and `Read Until Regexp` keywords. For more
        details about reading and writing in general, see `interactive shells`
        section.
        """
        return self._read_and_log(loglevel, self.current.read_until_prompt)   
    
    def _read_and_log(self, loglevel, reader, *args):
        try:
            output = reader(*args)
        except Exception, e:
            raise SerialException(e)
        self._log(output, loglevel)
        return output         
    def exec_cmd(self,cmd):
        cmd = str(cmd)
        cmd += "\n"
        self.console.flushInput() 
        try:
            self.console.write(cmd) 
            traceback.print_exc()
        except Exception, e:
            logging.error(u"Write error")
        self.console.flushOutput()
        sleep(0.4)
#         return self.console.read(200)

    def close_serial(self):
        self.console.close()
        
    def output_read(self):
        info = ''
        x = self.console.read(1024)   # x is str type
        info = info + x
        return info
    
    def readoutputforever(self):
        while(1):
            info = self.output_read()
            if (info != ''):
                self.outputinfo += info
                
    def ReadOutTask(self):
        thread.start_new_thread(self.readoutputforever,())
    
    def sendcmdtask(self):
        while(1):
            if(self.cmd == None):
                self.exec_cmd(self.cmd)
                self.cmd = None                
    
    def sendcmd(self,string):
        self.cmd = string
              
    def readcmdoutput(self):
        output = self.outputinfo
        self.outputinfo = ''
        return output



class _DefaultConfiguration(Configuration):

    def __init__(self, timeout, newline, prompt, loglevel, term_type, width,
                 height, path_separator, encoding):
        super(_DefaultConfiguration, self).__init__(
            timeout=TimeEntry(timeout),
            newline=NewlineEntry(newline),
            prompt=StringEntry(prompt),
            loglevel=LogLevelEntry(loglevel),
            term_type=StringEntry(term_type),
            width=IntegerEntry(width),
            height=IntegerEntry(height),
            path_separator=StringEntry(path_separator),
            encoding=StringEntry(encoding)
        )


if __name__ == '__main__':
    s = SerialOperate()
    print "+++"
    s.open_serial_connection('com1',115200, alias = "COM1", timeout = 0.1)
    print "==="
    print s.execute_serial_command("openvpn")
    s.close_serial_connection()
