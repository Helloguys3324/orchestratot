import re

class ProfanityFilter:
    def __init__(self, bad_words: list):
        self.bad_words = bad_words
        # Регулярка для поиска слов, которые могут содержать спецсимволы
        self.pattern = re.compile('|'.join([re.escape(word) for word in bad_words]), re.IGNORECASE)

    def contains_profanity(self, text: str) -> bool:
        # Убираем все пробелы и символы, оставляя только буквы
        # Это поможет ловить "м а т 1" и "м*а*т*1"
        clean_text = re.sub(r'[^a-zA-Zа-яА-ЯёЁ]', '', text)
        
        # Проверяем, содержится ли мат в очищенном тексте
        for word in self.bad_words:
            # Очищаем также само матное слово от лишних символов, если они там есть
            clean_word = re.sub(r'[^a-zA-Zа-яА-ЯёЁ]', '', word)
            if clean_word.lower() in clean_text.lower():
                return True
        return False