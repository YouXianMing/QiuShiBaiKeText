import os
import time


class FileObject:
    """
    文件对象
    """

    def __init__(self, filePath):
        """
        创建FileObject对象
        :param filePath: 文件路径
        """

        self.__tree_file_objects = None
        self.__scan_depth = None

        self.__exists = False
        self.__file_path = None
        self.__is_file = None
        self.__is_dir = None
        self._is_link = None
        self.__size = None
        self.__last_modification_time = None
        self.__last_access_time = None
        self.__metadata_change_time = None
        self.__file_name = None
        self.__dir_name = None

        if os.path.exists(filePath):

            self.__scan_depth = 0
            self.__exists = True
            self.__file_path = filePath
            self.__is_file = os.path.isfile(filePath)
            self.__is_dir = os.path.isdir(filePath)
            self._is_link = os.path.islink(filePath)
            self.__size = os.path.getsize(filePath)
            self.__last_modification_time = os.path.getmtime(filePath)
            self.__last_access_time = os.path.getatime(filePath)
            self.__metadata_change_time = os.path.getctime(filePath)
            self.__file_name = os.path.basename(filePath)
            self.__dir_name = os.path.dirname(filePath)

            if self.__is_dir:
                self.__tree_file_objects = []

    @property
    def scan_depth(self):
        """
        扫描深度的设置
        :return: 设置的扫描深度
        """
        return self.__scan_depth

    @scan_depth.setter
    def scan_depth(self, depth):
        self.__scan_depth = depth

    @property
    def tree_file_objects(self):
        """
        树形对象结构列表
        :return: 数组
        """
        return self.__tree_file_objects

    @tree_file_objects.setter
    def tree_file_objects(self, fileList):

        self.__tree_file_objects = fileList

    @property
    def exists(self):
        """
        文件是否存在
        :return: 存在返回True,不存在返回False
        """
        return self.__exists

    @property
    def file_path(self):
        """
        文件路径(初始化成功之后可取)
        :return: 初始化成功则有路径,没有初始化成功则没有路径
        """
        return self.__file_path

    @property
    def is_file(self):
        """
        是否是文件(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,是文件返回True,不是文件返回False
        """
        return self.__is_file

    @property
    def is_dir(self):
        """
        是否是文件夹(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,是文件夹返回True,不是文件返回False
        """
        return self.__is_dir

    @property
    def is_link(self):
        """
        是否是link(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,是link返回True,不是文件返回False
        """
        return self._is_link

    @property
    def size(self):
        """
        文件大小(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,返回文件大小
        """
        return self.__size

    @property
    def last_modification_time(self):
        """
        最后修改时间(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,返回最后修改时间
        """
        return self.__last_modification_time

    @property
    def last_access_time(self):
        """
        最后操作时间(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,返回最后操作时间
        """
        return self.__last_access_time

    @property
    def metadata_change_time(self):
        """
        最后元数据修改时间(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,返回最后元数据修改时间
        """
        return self.__metadata_change_time

    @property
    def file_name(self):
        """
        文件名(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,返回文件名
        """
        return self.__file_name

    @property
    def dir_name(self):
        """
        文件夹名(初始化成功之后可取)
        :return: 未初始化成功返回None,初始化成功时,返回文件夹名
        """
        return self.__dir_name

    def show_info(self):

        if self.exists:
            string = "[%s]\n" % self.file_name
            string += "------------------------------------------\n"
            string += "filePath             : %s\n" % self.file_path
            string += "size                 : %.2f kb\n" % (self.size / 1024.0)
            string += "isDir                : %s\n" % self.is_dir
            string += "isFile               : %s\n" % self.is_file
            string += "isLink               : %s\n" % self.is_link
            string += "lastAccessTime       : %s\n" % time.strftime('%Y-%m-%d %H:%M:%S %A',
                                                                    time.localtime(self.last_access_time))
            string += "lastModificationTime : %s\n" % time.strftime('%Y-%m-%d %H:%M:%S %A',
                                                                    time.localtime(self.last_modification_time))
            string += "metadataChangeTime   : %s\n" % time.strftime('%Y-%m-%d %H:%M:%S %A',
                                                                    time.localtime(self.metadata_change_time))
            string += "------------------------------------------\n"
            print(string)


class FileObjectManager:
    """
    用来扫描FileObject的类
    """

    def __init__(self, rootFile):

        self.rootFile = None

        if isinstance(rootFile, FileObject):
            self.rootFile = rootFile

    def all_file_objects(self):
        """
        获取扫描出来的文件
        :return: 扫描文件的数组
        """

        filesList = []

        if self.rootFile:
            FileObjectManager.__get_all_files(self.rootFile, filesList)

        return filesList

    def scan_with_depth(self, depth=999999):
        """
        开始扫描
        :param depth: 扫描深度
        :return: FileObjectManager对象本身
        """

        if self.rootFile:

            # 扫描之前清空rootFile中的数组的数据
            self.rootFile.tree_file_objects = []
            self.__scan_with_depth(self.rootFile, depth)

        return self

    @staticmethod
    def __get_all_files(rootFile, filesList):
        """
        静态方法:获取所有文件
        :param rootFile: FileObject对象,作为rootFile传入
        :param filesList: 集合
        :return: 无
        """

        # 判断rootFile是否是File类型
        if not isinstance(rootFile, FileObject):
            assert False, 'rootFile不是FileObject类型.'

        if type(filesList) != list:
            assert False, 'filesList不是List类型'

        # 遍历获取所有的文件
        for tmpFile in rootFile.tree_file_objects:

            filesList.append(tmpFile)
            if tmpFile.is_dir:
                FileObjectManager.__get_all_files(tmpFile, filesList)

    @staticmethod
    def __scan_with_depth(rootFile, depth):
        """
        静态方法:递归使用的扫描方法
        :param rootFile: 最为rootFile的FileObject对象
        :param depth: 扫描深度
        :return: 无
        """

        # 如果扫描等级超过了depth,则不扫描了
        if rootFile.scan_depth >= depth:
            return

        # 如果rootFile是文件夹
        if rootFile.is_dir:

            # 获取当前文件夹下的所有子文件
            filePathList = os.listdir(rootFile.file_path)

            # 遍历文件并创建文件夹
            for fileName in filePathList:

                # 创建FileObject对象
                file = FileObject(os.path.join(rootFile.file_path, fileName))

                # 设置扫描深度
                file.scan_depth = rootFile.scan_depth + 1

                # 将此文件添加到rootFile的treeFileObjects中
                rootFile.tree_file_objects.append(file)

                # 如果这个文件也是文件夹,则递归调用
                if file.is_dir:
                    FileObjectManager.__scan_with_depth(file, depth)


class Dir:

    def __init__(self, dir_path=None):

        self.__dir_path = dir_path
        self.__result_path = os.getcwd()

    @property
    def path(self):
        """
        文件路径
        :return: :class:`str <str>` object
        :rtype: str
        """
        return self.__result_path

    def file_name(self, file_name):

        dir_path = None

        if not self.__dir_path:
            dir_path = os.getcwd()
        else:
            dir_path = self.__dir_path

        self.__result_path = os.path.join(dir_path, file_name)

        return self


