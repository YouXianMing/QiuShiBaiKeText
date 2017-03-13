import re


class RegExpAbsModel:
    """
    用正则表达式来将字符串转换成对象,便于操作
    """

    def __init__(self, match_string):
        self.match_string = match_string

    def convert(self):
        """
        由子类重载,用来处理match_string,正则表达式将其转换成各种属性
        :return:
        """
        return self


class RegExpString:

    def __init__(self, match_string):

        self.__match_string = match_string

        # [字符串] 先调用了search_with_pattern之后再获取这个值,匹配成功返回字符串,匹配失败,返回None
        self.__search_result = None

        # [字符串] 先调用了replace_with_pattern之后再获取这个值,匹配成功返回字符串,匹配失败,返回None
        self.__replace_result = None

        # [字符串数组] 先调用find_all最后再获这个值,匹配成功返回字符串数组,匹配失败,返回None
        self.__item_list = None

    # Property
    # ---------------------------------------

    @property
    def search_result(self):
        return self.__search_result

    @property
    def replace_result(self):
        return self.__replace_result

    @property
    def item_list(self):
        return self.__item_list

    # Public method
    # ---------------------------------------

    def replace_with_pattern(self, pattern, replace_string, flags=0):
        """
        用正则表达式替换
        :param pattern: 正则表达式
        :param replace_string: 替换的字符串
        :param flags: 匹配方式
        :return: RegExpString对象
        """

        # 开始替换
        result = re.sub(repl=replace_string, pattern=pattern, flags=flags, string=self.__match_string)

        # 获取替换结果
        self.__replace_result = None
        if len(result):
            self.__replace_result = result

        return self

    def search_with_pattern(self, pattern, flags=0):
        """
        用正则表达式匹配一次
        :param pattern: 正则表达式
        :param flags: 匹配方式
        :return: RegExpString对象
        """

        # 开始匹配
        result = re.search(pattern, self.__match_string, flags)

        # 获取匹配结果
        self.__search_result = None
        if result:
            self.__search_result = result.group(0)

        return self

    def find_all(self, pattern, flags=0):
        """
        用正则表达式匹配所有的结果
        :param pattern: 正则表达式
        :param flags: 匹配方式
        :return: RegExpString对象
        """

        # 获取匹配的数组
        self.__item_list = None
        item_list = re.findall(pattern, self.__match_string, flags)
        if len(item_list):
            self.__item_list = item_list

        return self

    @staticmethod
    def check_pattern_valid(pattern):
        """
        验证正则表达式是否合法
        :param pattern: 正则表达式
        :return: 合法返回True,不合法返回False
        """

        is_valid = None

        try:
            re.compile(pattern)
            is_valid = True
        except re.error:
            is_valid = False

        return is_valid

    def get_item_list_with_pattern(self, pattern):
        """
        以 re.I | re.M | re.S 获取匹配数据的数组
        :param pattern: 正则表达式
        :return: 匹配上则返回数组,没有匹配上,则返回None
        """

        return self.find_all(pattern, re.I | re.M | re.S).item_list
