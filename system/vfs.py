from dataclasses import dataclass

@dataclass
class Mountpoint:
    name: str
    dirread: object
    dirwrite: object

class VFS:
    def __init__(self):
        self.elements: list[Mountpoint] = []

    def add_mountpoint(self, name, dirread, dirwrite):
        self.elements.append(
            Mountpoint(
                name,
                dirread,
                dirwrite
            )
        )


    def add_mountpoint_obj(self, obj):
        self.elements.append(obj)

    
    def remove_mountpoint(self, name):
        for n, i in enumerate(self.elements):
            if i == name:
                del self.elements[n]
                break


    def find_mountpoint(self, name):
        for n, i in enumerate(self.elements):
            if i.name.strip("/").split("/")[0] == name:
                return i
    
    
    def read_dir(self, path):
        a = self.find_mountpoint(path.strip("/").split("/")[0])

        if not a:
            return

        return a.dirread("/".join(path.strip("/").split("/")[1:]))
    
    
class MemoryFS:
    @dataclass
    class File:
        name: str
        length: int
        data: bytes

        dir_id: int
        dir_parent_id: int
    
    def __init__(self, point="/memory/"):
        self.elements: list[self.File] = []

        self.mountpoint = Mountpoint(point, self.read_dir, self.write_dir)

    def add_file(self, name, data, dir_id = 0, dir_pid = None):
        self.elements.append(
            self.File(
                name,
                len(data),
                data,
                dir_id,
                dir_pid
            )
        )

    def find_file(self, path) -> File:
        for i in self.elements:
            if i.name == path:
                return i

    def read_file(self, path):
        a = self.find_file(path)

        if not a:
            return

        return a.data

    def read_dir(self, path):
        return self.elements
    
    def write_dir(self, path):
        ...

if __name__ == "__main__":
    memfs = MemoryFS()

    vfs = VFS()
    vfs.add_mountpoint_obj(memfs.mountpoint)

    memfs.add_file("hello.txt", "hello")
    memfs.add_file("hyvaa.txt", "HYVAA HUOMENTA!!! (eng kbd)")

    print(vfs.read_dir("/memory/"))