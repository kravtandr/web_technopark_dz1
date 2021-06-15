from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice, shuffle, seed
from faker import Faker
from faker.providers.lorem import Provider



fake = Faker()


class Command(BaseCommand):

    avatar_list = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '5.jpg', '6.jpg', '7.jpg','8.jpg', '9.jpg', '10.jpg']

    def add_arguments(self, parser):
        parser.add_argument('--db_size', default='small', type=str, help='The size of database data to create.')

    def fill_profiles(self, cnt):
        usernames = set()
        profiles = []
        for i in range(cnt):
            username = fake.simple_profile().get('username')
            while username in usernames:
                username = fake.simple_profile().get('username')
            user = User.objects.create(
                username=username,
                password=fake.password(length=10, special_chars=True)
            )
            profiles.append(Profile(
                user_id=user.id,
                avatar=choice(self.avatar_list)
            ))
            usernames.add(username)

        Profile.objects.bulk_create(profiles)

    def fill_questions(self, cnt):
        questions = []
        for i in range(cnt):
            questions.append(Question(author_id=choice(list(Profile.objects.values_list('id', flat=True))),
                text=' '.join(fake.sentences(10)),
                title=fake.sentence(5)[:-1]+"?",
                date=fake.date_between(start_date='-5y', end_date='today'),
            ))

        Question.objects.bulk_create(questions)
        tags_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        for q in Question.objects.all():
            tag1 = Tag.objects.get(id=choice(tags_ids))
            tag2 = Tag.objects.get(id=choice(tags_ids))
            if tag1 != tag2:
                q.tags.add(tag1, tag2)
            else:
                q.tags.add(tag1)

    def fill_tags(self, cnt):
        tags = set()
        tags_list = []
        for i in range(cnt):
            tag = fake.word()
            while tag in tags:
                tag += '_' + fake.word()
            tags_list.append(Tag(
                name=tag,
            ))
            tags.add(tag)
        Tag.objects.bulk_create(tags_list)


    def fill_answers(self, cnt):
        answers = []
        for i in range(cnt):
            question_id = choice(list(Question.objects.values_list('id', flat=True)))
            answers.append(Answer(
                text=' '.join(fake.sentences(fake.random_int(min=5, max=10))),
                author_id=choice(list(Profile.objects.values_list('id', flat=True))),
                question_id=question_id,
                date=Question.objects.get(id=question_id).date
            ))
        Answer.objects.bulk_create(answers)
    
    def fill_question_likes(self, cnt):
        LIKE_CHOICES = ['1', '-1']
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        question_likes = []
        for i in range(cnt):
            question_id = choice(questions_ids)
            like = choice(LIKE_CHOICES)
            question_likes.append(QuestionLike(
                like=like,
                author_id=choice(author_ids),
                question_id=question_id
            ))
            Question.objects.filter(id=question_id).update(rating=F('rating') + like)

        QuestionLike.objects.bulk_create(question_likes)

    def fill_answer_likes(self, cnt):
        LIKE_CHOICES = ['1', '-1']
        answers_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        answers_likes = []
        for i in range(cnt):
            answers_likes.append(AnswerLike(
                like=choice(LIKE_CHOICES),
                author_id=choice(author_ids),
                answer_id=choice(answers_ids)
            ))
        AnswerLike.objects.bulk_create(answers_likes)

    # def fill_likes(self, cnt):
    #     vote_type = ['1', '-1']
    #     questions_ids = list(
    #         Question.objects.values_list(
    #             'id', flat=True
    #         )
    #     )
    #     answers_ids = list(
    #         Answer.objects.values_list(
    #             'id', flat=True
    #         )
    #     )
    #     author_ids = list(
    #         Profile.objects.values_list(
    #             'id', flat=True
    #         )
    #     )
    #     likes = []
    #     for i in range(cnt):
    #         like = choice(vote_type)
    #         if(fake.random_int(min=0, max=1)):
    #             curr_id = choice(questions_ids)
    #             Question.objects.get(id=curr_id).update(rating=F('rating') + like)
    #         else:
    #             curr_id = choice(answers_ids)
                
    #         likes.append(Like(
    #             like=like,
    #             author_id=choice(author_ids),
    #             question_id=curr_id
    #         ))

    #     Like.objects.bulk_create(likes)


    def handle(self, *args, **options):
        if options['db_size'] == 'large':
            sizes = [10001, 11000, 100001, 1000001, 900000, 900000]
        elif options['db_size'] == 'medium':
            sizes = [500, 1000, 1200, 2500, 1800, 1800]
        else:
            sizes = [10, 20, 20, 40, 30, 30]

        self.fill_profiles(sizes[0])
        self.stdout.write("Профили заполнены")
        self.fill_tags(sizes[1])
        self.stdout.write("Тэги заполнены")
        self.fill_questions(sizes[2])
        self.stdout.write("Вопросы заполнены")
        self.fill_answers(sizes[3])
        self.stdout.write("Ответы заполнены")
        self.fill_question_likes(sizes[4])
        self.stdout.write("Лайки вопросов заполнены")
        self.fill_answer_likes(sizes[5])
        self.stdout.write("Лайки ответов заполнены")
        self.stdout.write("Успешно", ending='')
