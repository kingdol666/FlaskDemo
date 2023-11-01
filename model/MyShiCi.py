from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os

os.environ['MODELSCOPE_CACHE'] = 'D:/model'


class ShiCiGet:

    def __init__(self):
        self.text_generation_zh = pipeline(Tasks.text_generation, model='damo/nlp_gpt3_poetry-generation_chinese-large')

    def execute(self, text: str):
        result_zh = self.text_generation_zh(text)
        print(type(result_zh))
        return result_zh['text']


if __name__ == '__main__':
    shici = ShiCiGet()
    result = shici.execute("淅淅沥沥淅淅沥")
    print(result)
