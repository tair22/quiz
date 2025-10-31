# Задание 2 - Импортируй нужные классы
import telebot, os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Question:

    def __init__(self, text, answer_id, *options, image_path=None):
        self.__text = text
        self.__answer_id = answer_id
        self.options = options
        self.image_path = image_path
    # Задание 1 - Создай геттер для получения текста вопроса
    @property
    def text(self):
        return self.__text
    
    def gen_markup(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = len(self.options)
        for i, option in enumerate(self.options):
            if i == self.__answer_id:
                markup.add(InlineKeyboardButton(option, callback_data='correct'))
            else:
                markup.add(InlineKeyboardButton(option, callback_data='wrong'))
    # Задание 3 - Создай метод для генерации Inline клавиатуры
        return markup
    def has_image(self):
        return self.image_path and os.path.exists(self.image_path)

class MultipleChoiceQuestion(Question):
    def __init__(self, text, correct_answers, *options, image_path=None):
        super().__init__(text, 0, *options, image_path=image_path)
        self.correct_answers = correct_answers
        self.selected_answers = []
 
    def gen_markup(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        
        for i, option in enumerate(self.options):
            is_selected = i in self.selected_answers
            callback_data = f"mc_{i}"
            
            button_text = f"✅{option}" if is_selected else option
            markup.add(InlineKeyboardButton(button_text, callback_data=callback_data))
        
        submit_button = InlineKeyboardButton("✅Подтвердить ответ", callback_data="mc_submit")
        markup.add(submit_button)
        
        return markup

    def toggle_answer(self, answer_index):
        if answer_index in self.selected_answers:
            self.selected_answers.remove(answer_index)
        else:
            self.selected_answers.append(answer_index)
    
    def check_answers(self):
        return set(self.selected_answers) == set(self.correct_answers)

# Задание 4 - заполни список своими вопросами
quiz_questions = [
    Question("Что котики делают, когда никто их не видит?", 0, "Спят", "Пишут мемы",image_path="images/20088c0008e035d3af83bcd85d1e47ef.jpg"),
    Question("Как котики выражают свою любовь?", 0, "Громким мурлыканием", "Отправляют фото на Instagram", "Гавкают",image_path="images/0e8981de7a51998492f9133736bfec37.jpg"),
    Question("Какие книги котики любят читать?", 3, "Обретение вашего внутреннего урр-мирения", "Тайм-менеджмент или как выделить 18 часов в день для сна", "101 способ уснуть на 5 минут раньше, чем хозяин", "Пособие по управлению людьми",image_path="images/5f9bd16b0eeda5d210bb42705b63e0c0.jpg"),
    Question("Почему котики приносят 'подарки' хозяевам?", 2, "Хотят поделиться едой", "Демонстрируют охотничьи навыки", "Учат нас выживанию", "Просто так",image_path="images/09ed10b874eed8cbde218a7c50016bed.jpg"),
    MultipleChoiceQuestion("Что означает кошачий 'бодающийся' жест головой?",[0, 1, 2, 3], "Проявление любви и доверия", "Просьба покормить", "Желание поиграть", "Просьба убрать лоток",image_path="images/56c69758023ba5c76221f2f163028bed.jpg"),
    Question("Какой звук издают довольные котики?", 1, "Мяу", "Мурлыкание", "Шипение", "Топот",image_path="images/76ec0222f6fe17d784a7281869c7a139.jpg"),
    MultipleChoiceQuestion("Почему котики так много спят?", [0, 1, 2], "Им скучно", "Ленятся", "Экономят энергию для охоты", "Избегают хозяев",image_path="images/0146a13b734d5ef96b59ac96afd79adb.jpg"),
    MultipleChoiceQuestion("Что означает виляние хвостом у кота?", [1, 2, 3], "Радость как у собак", "Желание играть", "Просьба есть", "Раздражение или беспокойство",image_path="images/377d9aa83a86a32bb98c5c04324ccfda.jpg"),
    MultipleChoiceQuestion("Как котики показывают, что территория их?", [0, 1, 3], "Трутся о предметы", "Оставляют записки", "Ставят флажки", "Кричат 'мое!'",image_path="images/426c4ee434ad42135bc175383423fde6.jpg"),
    MultipleChoiceQuestion("Почему котики закапывают еду?", [1, 2], "Не понравилась еда", "Инстинкт прятать остатки", "Хотят сохранить на потом", "Играют с едой",image_path="images/cc18a1b03421840dcadff9c707e86ec1.jpg")
]
