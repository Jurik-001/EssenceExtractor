from unittest.mock import patch, MagicMock
from essence_extractor.src.blog_media_enhancer import BlogMediaEnhancer
import numpy as np
import os
import pytest
import faiss


@patch('src.blog_media_enhancer.VideoFileClip')
def test_extract_images(mock_video_clip):
    mock_video = MagicMock(duration=30)
    mock_video_clip.return_value = mock_video
    enhancer = BlogMediaEnhancer(output_path='test_output')

    extracted_images = enhancer._extract_images('dummy_video_path', interval=10)
    assert len(extracted_images) == 3


@patch('src.blog_media_enhancer.VideoFileClip')
def test_extract_images_with_negative_interval(mock_video_clip):
    mock_video = MagicMock(duration=30)
    mock_video_clip.return_value = mock_video
    enhancer = BlogMediaEnhancer(output_path='test_output')

    # Negative interval
    with pytest.raises(ValueError):
        enhancer._extract_images('dummy_video_path', interval=-10)


@patch('src.blog_media_enhancer.VideoFileClip')
def test_extract_images_with_short_video(mock_video_clip):
    mock_video = MagicMock(duration=5)  # 5 seconds video
    mock_video_clip.return_value = mock_video
    enhancer = BlogMediaEnhancer(output_path='test_output')

    # Short video
    extracted_images = enhancer._extract_images('dummy_video_path', interval=2)
    assert len(extracted_images) == 3, "Should handle short videos correctly"


@patch('src.blog_media_enhancer.pytesseract.image_to_string', return_value="Sample Text")
def test_extract_text_from_image(mock_image_to_string):
    enhancer = BlogMediaEnhancer(output_path='test_output')
    text = enhancer._extract_text_from_image(MagicMock())
    assert text == "Sample Text"


def test_create_index():
    enhancer = BlogMediaEnhancer(output_path='test_output')
    embeddings = np.random.rand(10, 768)
    index = enhancer._create_index(embeddings)
    assert index.ntotal == 10


def test_query_index():
    enhancer = BlogMediaEnhancer(output_path='test_output')
    dimension = 768
    num_images = 5
    embeddings = np.random.rand(num_images, dimension).astype('float32')
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    images_text_dict = {f'image_{i}': embeddings[i] for i in range(num_images)}

    query_embedding = embeddings[0].reshape(1, -1)

    retrieved_images = enhancer._query_index(index, query_embedding, images_text_dict, k=1)

    assert len(retrieved_images) == 1, "Should retrieve one image"
    assert retrieved_images[0] == 'image_0', "Should retrieve the correct image based on the query"


@patch('os.listdir', return_value=['image1.png', 'image2.png'])
@patch('os.remove')
def test_remove_unused_images(mock_remove, mock_listdir):
    enhancer = BlogMediaEnhancer(output_path='test_output')
    enhancer._remove_unused_images(['image1.png'])
    mock_remove.assert_called_once_with(os.path.join('test_output', 'images', 'image2.png'))


@patch('src.blog_media_enhancer.pytesseract.image_to_string', return_value="Image Text")
def test_extract_alt_text_with_image_tags(mock_image_to_string):
    markdown_content = """
    Here is an image: ![Alt text](image_url)
    """
    enhancer = BlogMediaEnhancer(output_path='test_output')
    result = enhancer._extract_alt_text_with_image_tags(markdown_content)
    assert "Alt text" in result
    assert result["Alt text"] == "![Alt text](image_url)"


def test_add_images_to_blog():
    enhancer = BlogMediaEnhancer(output_path='test_output')

    enhancer._extract_images = MagicMock(return_value={'image1.png': 'dummy_data'})

    enhancer._extract_alt_text_with_image_tags = MagicMock(return_value={'Alt text': '![Alt text](image_url)'})

    enhancer._embed_text = MagicMock(return_value=np.array([0.5]))

    mock_index = MagicMock()
    enhancer._create_index = MagicMock(return_value=mock_index)

    enhancer._query_index = MagicMock(return_value=['image1.png'])

    blog_content = "Here is an image: ![Alt text](image_url)"
    updated_content = enhancer.add_images_to_blog('dummy_video_path', blog_content)

    assert '![Alt text](images/image1.png)' in updated_content


@patch('src.blog_media_enhancer.YouTubeURL')
def test_add_url_timestamps_to_blog(mock_youtube_url):
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    blog_content = "Here is a timestamp: [01:03 - 07:58] in the video."

    enhancer = BlogMediaEnhancer(output_path='test_output')
    mock_youtube_url.return_value.url = youtube_url

    updated_content = enhancer.add_url_timestamps_to_blog(youtube_url, blog_content)

    assert "[01:03 - 07:58](https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=63s)" in updated_content
