from wcwidth import wcwidth

class Utils:

    images_catalog = {}
    id_counter = 0

    @classmethod
    def show_images_catalog(cls):
        print(cls.images_catalog)

    @classmethod
    def modify_images_catalog(cls, new_value):
        cls.images_catalog = new_value

    @classmethod
    def show_id_counter(cls):
        print(cls.id_counter)

    @classmethod
    def modify_id_counter(cls, new_value):
        cls.id_counter = new_value


    @staticmethod
    def flat_and_add_to_list(lst, item):
        def flatten(items):
            for i in items:
                if isinstance(i, list):
                    yield from flatten(i)
                else:
                    yield i

        if isinstance(item, list):
            lst[:0] = list(flatten(item))  # Insère les éléments aplatis au début
        else:
            lst.insert(0, item)  # Ajoute un seul élément en début de liste

    @staticmethod
    def add_to_dict(dict, item):
        return dict.extend(item)

    @staticmethod
    def len_text(text):
        size = 0
        for txt in text.split('\n'):
            size = max(sum(max(wcwidth(ch), 1) for ch in txt), size)
        return size

    @staticmethod
    def split_text(text, size_newline):
        raw_lines = text.replace('\\n', '\n').split('\n')

        processed_lines = []
        for line in raw_lines:
            if len(line) > size_newline:
                middle_text = len(line) / 2
                text_blocs = line.split(' ')
                text_multiline = ''
                split = False
                for text_bloc in text_blocs:
                    if len(text_multiline) > middle_text and not split:
                        text_multiline += '\n'
                        split = True
                    text_multiline += text_bloc + ' '
                processed_lines.append(text_multiline.strip())
            else:
                processed_lines.append(line)

        return '\n'.join(processed_lines)
