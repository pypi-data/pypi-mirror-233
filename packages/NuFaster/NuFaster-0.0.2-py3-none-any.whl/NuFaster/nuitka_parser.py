from optparse import Option

from nuitka.OptionParsing import parser as _parser

print(_parser)


class Parser:
    
    @property
    def options(self):
        res_list = {}
        for option in _parser.option_list:
            option: Option
            long_opts = option._long_opts
            short_opts = option._short_opts
            for field in [*long_opts, *short_opts]:
                field = str(field).strip('-').replace('-', '_')
                if field in res_list:
                    print(field, 'is has')
                res_list[field] = option
        for group in _parser.option_groups:
            
            for option in group.option_list:
                option: Option
                long_opts = option._long_opts
                short_opts = option._short_opts
                for field in [*long_opts, *short_opts]:
                    field = str(field).strip('-').replace('-', '_')
                    if field in res_list:
                        print(field, 'is has')
                    res_list[field] = option
        return res_list
    
    def parser_kwargs(self, kwargs):
        usages = ['nuitka']
        options = self.options
        for key, val in kwargs.items():
            if val is None:
                continue
            key = str(key).strip('-').replace('-', '_')
            if key in options:
                option: Option = options.get(key)
                option_key = option._long_opts[0]
                if isinstance(val, bool):
                    if val:
                        usages.append(option_key)
                elif isinstance(val, str):
                    usages.append(f'{option_key}={val}')
                elif isinstance(val, (list, set, tuple)):
                    if not isinstance(option.default, list):
                        print('np_error: 关键字类型不为list')
                    val_str = ','.join([str(item) for item in val])
                    usages.append(f'{option_key}={val_str}')
        return usages


np_parser = Parser()

if __name__ == '__main__':
    """
    Main run
    """
    print(np_parser.options)
