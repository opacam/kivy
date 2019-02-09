from kivy.tests.common import GraphicUnitTest

from kivy.uix.widget import Widget
from kivy.graphics import Fbo, Color, Rectangle


class FboTest(Widget):
    def __init__(self, **kwargs):
        super(FboTest, self).__init__(**kwargs)
        self.positions = (
            (260.0, 260.0),
            (192.0, 192.0),
            (96.0, 192.0),
            (192.0, 96.0),
            (96.0, 96.0),
            (32.0, 192.0),
            (192.0, 32.0),
            (32.0, 32.0)
        )

        self.fbo = Fbo(size=(256, 256))
        with self.fbo:
            Color(0.56789, 0, 0, 1)
            Rectangle(size=(256, 64))
            Color(0, 0.56789, 0, 1)
            Rectangle(size=(64, 256))
            Color(0.56789, 0, 0, .5)
            Rectangle(pos=(64, 64), size=(192, 64))
            Color(0, 0.56789, 0, .5)
            Rectangle(pos=(64, 64), size=(64, 192))
        self.fbo.draw()


class FBOPy2Py3TestCase(GraphicUnitTest):
    def test_fbo_get_pixel_color(self):
        print('************************')
        print('test_fbo_get_pixel_color')
        print('************************')
        fbow = FboTest()
        print('fbow is: {}'.format(fbow))
        render_error = 2
        values = (
            # out of bounds of FBO
            (tuple, int, (0, 0, 0, 0)),
            # in FBO, black
            (list, int, [0, 0, 0, 0]),
            # Color(0, 0.56789, 0, .5)
            (list, int, [0, 72, 0, 128]),
            # Color(0.56789, 0, 0, .5)
            (list, int, [72, 0, 0, 128]),
            # overlap above 2 w/ alpha
            (list, int, [36, 72, 0, 255]),
            # Color(0, 0.56789, 0, 1)
            (list, int, [0, 145, 0, 255]),
            # Color(0.56789, 0, 0, 1)
            (list, int, [145, 0, 0, 255]),
            # overlap above 2 w/o alpha
            (list, int, [0, 145, 0, 255]),
        )

        print('******************************************')
        print('Begin test for fbow.positions:\n* {} *'.format(fbow))
        print('******************************************')
        for i, pos in enumerate(fbow.positions):
            print('* testing: "{}" -> "{}"'.format(i, pos))
            c = fbow.fbo.get_pixel_color(pos[0], pos[1])
            print('\t- "c" is: "{}"'.format(c))
            print('\t\t* "c" should be: "{}"'.format(values[i][0]))
            # returned class
            self.assertTrue(isinstance(c, values[i][0]))
            # returned types in container
            for v in c:
                print('\t- "v" in c is: "{}"'.format(v))
                print('\t\t* "v" in c should be: "{}"'.format(values[i][0]))
                self.assertTrue(isinstance(v, values[i][1]))
            # returned values
            for j, val in enumerate(c):
                print('\t- "j", "val" is: "{}", "{}"'.format(j, val))
                print('\t\t* "v" in c should be: "{}"'.format(values[i][2][j]))
                self.assertAlmostEqual(
                    val, values[i][2][j],
                    delta=render_error
                )
        print('******************************************')


if __name__ == '__main__':
    import unittest
    unittest.main()
