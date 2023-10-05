import ast
import textwrap
import binascii

from xnode.pyboard import PyboardError

BUFFER_SIZE = 32

class DirectoryExistsError(Exception):
    pass

class Files(object):
    def __init__(self, pyboard):
        self._pyboard = pyboard

    def get(self, filename):
        command = """
            import sys
            import ubinascii
            with open('{0}', 'rb') as infile:
                while True:
                    result = infile.read({1})
                    if result == b'':
                        break
                    len = sys.stdout.write(ubinascii.hexlify(result))
        """.format(
            filename, BUFFER_SIZE
        )
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            if ex.args[2].decode("utf-8").find("OSError: [Errno 2] ENOENT") != -1:
                raise RuntimeError("No such file: {0}".format(filename))
            else:
                raise ex
        self._pyboard.exit_raw_repl()
        return binascii.unhexlify(out)

    def ls(self, directory="/", long_format=True, recursive=False):
        if not directory.startswith("/"):
            directory = "/" + directory

        command = """
                import os\r\n
        """

        if recursive:
            command += """
                def listdir(directory):
                    result = set()
                    
                    def _listdir(dir_or_file):
                        try:
                            children = os.listdir(dir_or_file)
                        except OSError:                        
                            os.stat(dir_or_file)
                            result.add(dir_or_file) 
                        else:
                            if children:
                                for child in children:
                                    if dir_or_file == '/':
                                        next = dir_or_file + child
                                    else:
                                        next = dir_or_file + '/' + child
                                    
                                    _listdir(next)
                            else:
                                result.add(dir_or_file)                     

                    _listdir(directory)
                    return sorted(result)\n"""
        else:
            command += """
                def listdir(directory):
                    if directory == '/':                
                        return sorted([directory + f for f in os.listdir(directory)])
                    else:
                        return sorted([directory + '/' + f for f in os.listdir(directory)])\n"""

        if long_format:
            command += """
                r = []
                for f in listdir('{0}'):
                    size = os.stat(f)[6]                    
                    r.append('{{0}} - {{1}} bytes'.format(f, size))
                print(r)
            """.format(
                directory
            )
        else:
            command += """
                print(listdir('{0}'))
            """.format(
                directory
            )
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            if ex.args[2].decode("utf-8").find("OSError: [Errno 2] ENOENT") != -1:
                raise RuntimeError("No such directory: {0}".format(directory))
            else:
                raise ex
        self._pyboard.exit_raw_repl()
        return ast.literal_eval(out.decode("utf-8"))

    def mkdir(self, directory, exists_okay=False):
        command = """
            import os
    
            os.mkdir('{0}')
        """.format(
            directory
        )
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            if ex.args[2].decode("utf-8").find("OSError: [Errno 17] EEXIST") != -1:
                if not exists_okay:
                    raise DirectoryExistsError(
                        "Directory already exists: {0}".format(directory)
                    )
            else:
                #raise ex
                pass

        self._pyboard.exit_raw_repl()

    def put(self, filename, data):
        self._pyboard.enter_raw_repl()
        try:
            self._pyboard.exec_("f = open('{0}', 'wb')".format(filename))
        except PyboardError as e:
            if "EEXIST" in str(e):
                self._pyboard.exit_raw_repl()
                self.rm(filename)
                self.put(filename, data)
            return
                                
        size = len(data)

        for i in range(0, size, BUFFER_SIZE):
            chunk_size = min(BUFFER_SIZE, size - i)
            chunk = repr(data[i : i + chunk_size])

            if not chunk.startswith("b"):
                chunk = "b" + chunk
            self._pyboard.exec_("f.write({0})".format(chunk))
        self._pyboard.exec_("f.close()")
        self._pyboard.exit_raw_repl()

    def rm(self, filename):
        command = """
            import os

            os.remove('{0}')
        """.format(
            filename
        )
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            message = ex.args[2].decode("utf-8")
            if message.find("OSError: [Errno 2] ENOENT") != -1:
                raise RuntimeError("No such file/directory: {0}".format(filename))
            if message.find("OSError: [Errno 13] EACCES") != -1:
                raise RuntimeError("Directory is not empty: {0}".format(filename))
            else:
                raise ex
        self._pyboard.exit_raw_repl()

    def rmdir(self, directory, missing_okay=False):
        command = """
            import os

            def rmdir(directory):
                os.chdir(directory)
                for f in os.listdir():
                    try:
                        os.remove(f)
                    except OSError:
                        pass
                for f in os.listdir():
                    rmdir(f)
                os.chdir('..')
                os.rmdir(directory)
                
            rmdir('{0}')
        """.format(
            directory
        )
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            message = ex.args[2].decode("utf-8")
            if message.find("OSError: [Errno 2] ENOENT") != -1:
                if not missing_okay:
                    raise RuntimeError("No such directory: {0}".format(directory))
            else:
                raise ex
        self._pyboard.exit_raw_repl()

    def format_a(self):
        command = """
            import os

            os.fsformat('/flash')
        """
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            raise ex
        self._pyboard.exit_raw_repl()

    def format_b(self):
        command = """
            import os

            os.format()
        """
        self._pyboard.enter_raw_repl()
        try:
            out = self._pyboard.exec_(textwrap.dedent(command))
        except PyboardError as ex:
            raise ex
        self._pyboard.exit_raw_repl()


    def run(self, filename, stream_output=True, input_on=False):
        self._pyboard.enter_raw_repl()

        if not stream_output and not input_on: 
            with open(filename, "rb") as infile:
                self._pyboard.exec_raw_no_follow(infile.read())
        elif stream_output and not input_on: 
            self._pyboard.execfile(filename, True, False)
        elif not stream_output and input_on: 
            self._pyboard.execfile(filename, False, True)
        else: 
            self._pyboard.execfile(filename, True, True)

        self._pyboard.exit_raw_repl()

