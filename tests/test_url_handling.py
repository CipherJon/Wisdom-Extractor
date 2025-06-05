import unittest
from app import is_valid_youtube_url, extract_video_id

class TestURLHandling(unittest.TestCase):
    def test_valid_youtube_urls(self):
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "https://youtube.com/v/dQw4w9WgXcQ",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=123s",
            "https://youtu.be/dQw4w9WgXcQ?t=123"
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_youtube_url(url))
                self.assertIsNotNone(extract_video_id(url))
                self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")

    def test_invalid_youtube_urls(self):
        invalid_urls = [
            "https://www.youtube.com",
            "https://youtube.com",
            "https://www.google.com",
            "not a url",
            "https://youtube.com/watch",
            "https://youtube.com/watch?v=",
            "https://youtube.com/watch?v=invalid"
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid_youtube_url(url))
                self.assertIsNone(extract_video_id(url))

if __name__ == '__main__':
    unittest.main() 