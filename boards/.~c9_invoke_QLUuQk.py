# from django.test import TestCase
from test_plus.test import TestCase
from django.conf import settings
from django.urls import reverse
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
        
    def test_02_boardform(self):
        data = {
            'title': '제목',
            'content': '내용'
        }
        self.assertEqual(BoardForm(data).is_valid(), True)
    
    def test_03_boardform_without_title(self):
        data = {
            'content': '내용'
        }
        self.assertEqual(BoardForm(data).is_valid(), False)
    
    def test_04_boardform_without_content(self):
        data = {
            'title': '제목'
        }
        self.assertEqual(BoardForm(data).is_valid(), False)

# 3. View test
class BoardViewTest(TestCase):
    def setUp(self):
        # given
        self.user = self.make_user(username='test', password='1qs2wd3ef!@#')

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
            
    def test_05_detail_contains(self):
        # given
        board = Board.objects.create(title='title', content='content', user=self.user)
        # then
        self.assertResponseContains(board.title, html=False)
        self.assertResponseContains(board.content, html=False)
        
    # def test_06_detail_template(self):
    #     board = Board.objects.create(title='test title', content='test content', user=self.user)
    #     response = self.get_check_200('boards:detail', board_pk=board.pk)
    #     self.assertTemplateUsed(response, 'boards/detail.html')
    
    # def test_06_detail_template(self):
    #     # Given
    #     board = Board.objects.create(title='test title', content='test content', user=self.user)
    #     response = self.get_check_200('boards:detail', board_pk=board.pk)
    #     self.assertTemplateUsed(response, 'boards/detail.html')
    
    
    def test_07_get_index(self):
        self.get_check_200('boards:index')
        
    def test_08_index_template(self):
        response = self.get_check_200('boards:index')
        self.assertTemplateUsed(response, 'boards/index.html')
        
    def test_09_index_queryset(self):
        board = Board.objects.create(title='title', content='content', user=self.user)
        board = Board.objects.create(title='title', content='content', user=self.user)
        boards = Board.objects.order_by('-pk')
        
        response = self.get_check_200('boards:index')
        
        self.assertQuerysetEqual(response.context['boards'], map(repr, boards))
        
    # def test_10_delete(self):
    #     board = Board.objects.create(title='title', content='content', user=self.user)
    #     with self.login(username='test', password='1qs2wd3ef!@#'):
    #         self.get_check_200('boards:delete', board_pk=board.pk)
    
    def test_11_delete_post(self):
        board = Board.objects.create(title='title', content='content', user=self.user)
        with self.login(username='test', password='1qs2wd3ef!@#'):
            self.post('boards:delete', board_pk=board.pk)
            self.assertEqual(Board.objects.count(), 0)
    
    def test_12_delete_redirect(self):
        board = Board.objects.create(title='title', content='content', user=self.user)
            self.
            response = self.post('boards:delete', board_pk=board.pk)
            self.assertRedirects(response, reverse('boards:index'))
    
    def test_13_get_update(self):
        board = Board.objects.create(title='title', content='content', user=self.user)
        with self.login(username='test', password='1qs2wd3ef!@#'):
            response = self.get_check_200('boards:update', board.pk)
            self.assertEqual(response.context['form'].instance.pk, board.pk)
            
    def test_14_get_update_login_required(self):
        self.assertLoginRequired('boards:update', board_pk=1)
            