from dataclasses import dataclass

class Stage2:
    def __init__(self, sim, fs, tty):
        self.sim = sim
        self.tty = tty
        self.fs = fs
        self.vfs_code = fs.read_file("vfs.py").decode('utf-8')

        exec(self.vfs_code, globals())

        self.vfs = VFS()
        self.memfs = MemoryFS()

        self.vfs.add_mountpoint_obj(self.memfs.mountpoint)

        self.start()

    def start(self):
        self.tty.putsf("Stage 2!\n")