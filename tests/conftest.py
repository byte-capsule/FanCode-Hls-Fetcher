import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch


@pytest.fixture
def temp_dir():
    """Provides a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def temp_file(temp_dir):
    """Provides a temporary file path."""
    file_path = temp_dir / "test_file.txt"
    yield file_path
    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def mock_requests():
    """Provides a mock requests module."""
    with patch("requests.get") as mock_get, \
         patch("requests.post") as mock_post, \
         patch("requests.put") as mock_put, \
         patch("requests.delete") as mock_delete:
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_response.text = "mock response"
        
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        mock_put.return_value = mock_response
        mock_delete.return_value = mock_response
        
        yield {
            "get": mock_get,
            "post": mock_post,
            "put": mock_put,
            "delete": mock_delete,
            "response": mock_response
        }


@pytest.fixture
def mock_os_environ():
    """Provides a mock os.environ for testing environment variables."""
    with patch.dict("os.environ", {"password": "test_password", "TEST_VAR": "test_value"}):
        yield


@pytest.fixture
def sample_zip_file(temp_dir):
    """Creates a sample zip file for testing."""
    import zipfile
    
    zip_path = temp_dir / "test.zip"
    test_content = "This is test content"
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr("test.txt", test_content)
    
    return zip_path


@pytest.fixture
def mock_cache():
    """Provides a mock cache object."""
    cache_mock = Mock()
    cache_mock.get.return_value = None
    cache_mock.set.return_value = True
    cache_mock.delete.return_value = True
    cache_mock.clear.return_value = True
    return cache_mock


@pytest.fixture
def sample_html():
    """Provides sample HTML content for BeautifulSoup testing."""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <div class="content">
                <h1>Test Header</h1>
                <p>Test paragraph</p>
                <a href="https://example.com">Test Link</a>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def mock_file_operations():
    """Provides mocks for file operations."""
    with patch("builtins.open", create=True) as mock_open, \
         patch("os.path.exists") as mock_exists, \
         patch("os.remove") as mock_remove, \
         patch("os.system") as mock_system:
        
        mock_exists.return_value = True
        mock_remove.return_value = None
        mock_system.return_value = 0
        
        yield {
            "open": mock_open,
            "exists": mock_exists,
            "remove": mock_remove,
            "system": mock_system
        }


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Automatically cleanup any test files created during tests."""
    yield
    
    # Clean up any test files that might have been created
    test_files = ["test_output.txt", "temp_test_file.txt"]
    for file_path in test_files:
        if Path(file_path).exists():
            Path(file_path).unlink()