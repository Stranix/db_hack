from datacenter.models import Schoolkid


def find_schoolkid_by_name(full_name: str) -> Schoolkid:
    from django.core.exceptions import ObjectDoesNotExist
    from django.core.exceptions import MultipleObjectsReturned
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
        return schoolkid
    except ObjectDoesNotExist:
        print('Ученик не найден')
    except MultipleObjectsReturned:
        print('Найдено слишком много учеников. Попробуйте указать имя точнее')


def fix_marks(schoolkid: Schoolkid):
    from datacenter.models import Mark
    bad_marks = Mark.objects.filter(schoolkid=schoolkid.id, points__in=[2, 3])
    if not bad_marks:
        print(f'Не нашел плохих оценок у ученика {schoolkid.full_name}')
        return
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()
    print('Заменил все плохие оценки')


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
    from datacenter.models import Schoolkid
    from datacenter.models import Lesson
    from datacenter.models import Commendation
    from django.core.exceptions import ObjectDoesNotExist
    from django.core.exceptions import MultipleObjectsReturned
    try:
        commendations = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                         'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                         'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!']
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_full_name)
        schoolkid_lessons = Lesson.objects.filter(subject__title=lesson,
                                                  year_of_study=schoolkid.year_of_study,
                                                  group_letter=schoolkid.group_letter)
        random_lesson = random.choice(schoolkid_lessons)
        Commendation.objects.create(text=random.choice(commendations),
                                    created=random_lesson.date,
                                    schoolkid=schoolkid,
                                    subject=random_lesson.subject,
                                    teacher=random_lesson.teacher
                                    )
    except ObjectDoesNotExist:
        print('Ученик не найден')
    except MultipleObjectsReturned:
        print('Найдено слишком много учеников. Попробуйте указать имя точнее')