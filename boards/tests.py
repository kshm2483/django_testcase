# from django.test import TestCase
from test_plus.test import TestCase
from django.conf import settings
from .models import Board
from .forms import BoardForm

# 1. settings test
class SettingsTest(TestCase):
    def test_01_settings(self):
        self.assertEqual(settings.USE_I18N, True)
        self.assertEqual(settings.USE_TZ, False)
        self.assertEqual(settings.LANGUAGE_CODE, 'ko-kr')
        self.assertEqual(settings.TIME_ZONE, 'Asia/Seoul')

# 2. Model test
class BoardModelTest(TestCase):
    def test_01_model(self):
        board = Board.objects.create(title='test', content='test', user_id=1)
        self.assertEqual(str(board), f'Board{board.pk}', msg='출력 값이 일치하지 않음')
    
# 3. View test
class BoardViewTest(TestCase):
    def setUp(self):
        # given
        user = self.make_user(username='test', password='1qs2wd3ef!@#')

    def test_01_create(self):
        with self.login(username='test', password='1qs2wd3ef!@#'):
            response = self.get_check_200('boards:create')
            self.assertIsInstance(response.context['form'], BoardForm)
            
    def test_02_get_create_login_required(self):
        self.assertLoginRequired('boards:create')
        
    def test_03_post_create(self):
        data = {
            'title': 'test title',
            'content': 'test content'
        }
        with self.login(username='test', password='1qs2wd3ef!@#'):
            self.post('boards:create', data=data)
    
    def test_04_board_create_without_content(self):
        data = {
            'title': 'test title',
        }
        with self.login(username='test', password='1qs2wd3ef!@#'):
            response = self.post('boards:create', data=data)
            self.assertContains(response, '필')