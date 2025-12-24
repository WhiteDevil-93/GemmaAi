import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# --- MOCK DEPENDENCIES BEFORE IMPORTING APP ---
sys.modules["llama_cpp"] = MagicMock()
sys.modules["llama_index"] = MagicMock()
sys.modules["llama_index.core"] = MagicMock()
sys.modules["llama_index.llms"] = MagicMock()
sys.modules["llama_index.llms.llama_cpp"] = MagicMock()
sys.modules["llama_index.embeddings"] = MagicMock()
sys.modules["llama_index.embeddings.huggingface"] = MagicMock()
sys.modules["llama_index.vector_stores"] = MagicMock()
sys.modules["llama_index.vector_stores.chroma"] = MagicMock()
sys.modules["chromadb"] = MagicMock()

# Ensure app can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestCurator(unittest.TestCase):
    def setUp(self):
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            "MODEL_PATH_CURATOR": "/fake/path/to/model.gguf",
            "CONTEXT_WINDOW": "2048",
            "THREADS": "4",
            "GPU_LAYERS_CURATOR": "0"
        })
        self.env_patcher.start()

        self.mock_llama_module = sys.modules["llama_cpp"]
        self.mock_llama_class = self.mock_llama_module.Llama
        self.mock_llama_instance = self.mock_llama_class.return_value

    def tearDown(self):
        self.env_patcher.stop()

    def test_curator_initialization(self):
        from app.core.curator import Curator
        curator = Curator()
        self.assertIsNotNone(curator)
        # Verify Llama was instantiated with correct path
        self.mock_llama_class.assert_called()
        args, kwargs = self.mock_llama_class.call_args
        self.assertEqual(kwargs['model_path'], "/fake/path/to/model.gguf")

    def test_curator_generation(self):
        from app.core.curator import Curator
        curator = Curator()

        # Mock response structure for llama-cpp-python
        self.mock_llama_instance.return_value = {
            "choices": [{"text": " This is a test response."}]
        }

        response = curator.generate_response("Hello")
        self.assertEqual(response, "This is a test response.")

class TestDevourer(unittest.TestCase):
    def setUp(self):
        self.env_patcher = patch.dict(os.environ, {
            "MODEL_PATH_DEVOURER": "/fake/path/to/devourer.gguf",
            "THREADS": "4"
        })
        self.env_patcher.start()

        # Get references to the mocked modules in sys.modules
        self.mock_llamappp = sys.modules["llama_index.llms.llama_cpp"].LlamaCPP
        self.mock_chroma_client = sys.modules["chromadb"].PersistentClient
        self.mock_directory_reader = sys.modules["llama_index.core"].SimpleDirectoryReader

        # Configure ChromaDB mock to return an integer for count()
        self.mock_chroma_collection = self.mock_chroma_client.return_value.get_or_create_collection.return_value
        self.mock_chroma_collection.count.return_value = 0

    def tearDown(self):
        self.env_patcher.stop()

    def test_devourer_initialization(self):
        from app.tools.devourer import Devourer
        devourer = Devourer()
        self.assertIsNotNone(devourer)
        self.mock_llamappp.assert_called()

    def test_devourer_ingest_no_docs(self):
        from app.tools.devourer import Devourer

        # Mock SimpleDirectoryReader to return empty list
        mock_reader_instance = self.mock_directory_reader.return_value
        mock_reader_instance.load_data.return_value = []

        devourer = Devourer()
        result = devourer.ingest_data()
        self.assertIn("No documents found", result)

if __name__ == '__main__':
    unittest.main()
