from datacenter.models import Schoolkid

COMMENDATIONS = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                 'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                 'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!']


def find_schoolkid_by_name(full_name: str) -> Schoolkid:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print('Ученик не найден')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено слишком много учеников. Попробуйте указать имя точнее')


def fix_marks(schoolkid: Schoolkid):
    from datacenter.models import Mark
    bad_marks = Mark.objects.filter(schoolkid=schoolkid.id, points__in=[2, 3]).update(points=5)
    if not bad_marks:
        print(f'Не нашел плохих оценок у ученика {schoolkid.full_name}')
        return
    print(f'Заменил все плохие оценки. Количество: {bad_marks}')


def remove_chastisements(schoolkid: Schoolkid):
    from datacenter.models import Chastisement
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid.id)
    if not chastisements:
        print(f'Нет замечаний у ученика {schoolkid.full_name}')
        return
    count_deleted, lessons = chastisements.delete()
    print(f'Удаленных замечаний: {count_deleted}')


def create_commendation(schoolkid_full_name: str, lesson: str):
    import random
    from datacenter.models import Lesson
    from datacenter.models import Commendation

    schoolkid = find_schoolkid_by_name(schoolkid_full_name)
    if not schoolkid:
        return
    random_schoolkid_lessons = Lesson.objects.filter(subject__title=lesson,
                                                     year_of_study=schoolkid.year_of_study,
                                                     group_letter=schoolkid.group_letter
                                                     ).first()
    if not random_schoolkid_lessons:
        print('Нет подходящих уроков')
        return

    Commendation.objects.create(text=random.choice(COMMENDATIONS),
                                created=random_schoolkid_lessons.date,
                                schoolkid=schoolkid,
                                subject=random_schoolkid_lessons.subject,
                                teacher=random_schoolkid_lessons.teacher
                                )
