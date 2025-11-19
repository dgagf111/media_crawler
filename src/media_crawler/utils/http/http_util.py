"""
HttpUtil 工具类

这个工具类封装了 HTTP 请求，支持 GET、POST、PUT、DELETE 请求，并且支持可选的重试机制和流式响应。
每次请求都需要明确指定请求头。

使用说明：

1. 初始化 HttpUtil 对象：
   http_util = HttpUtil(base_url="http://example.com", timeout=10, retries=3)

2. 发送 GET 请求：
   a. 基本 GET 请求：
      response = http_util.get("/path")

   b. 带查询参数的 GET 请求：
      response = http_util.get("/path", params={"key": "value"})

   c. 带自定义请求头的 GET 请求：
      response = http_util.get("/path", headers={"Custom-Header": "Value"})

   d. 流式 GET 请求：
      for chunk in http_util.get("/path", stream=True, chunk_size=1024):
          print(chunk)

3. 发送 POST 请求：
   a. 发送 JSON 数据的 POST 请求：
      response = http_util.post("/path", json={"key": "value"}, headers={"Content-Type": "application/json"})

   b. 发送表单数据的 POST 请求：
      response = http_util.post("/path", data={"key": "value"}, headers={"Content-Type": "application/x-www-form-urlencoded"})

   c. 发送多部分表单数据的 POST 请求（如上传文件）：
      with open('file.txt', 'rb') as f:
          files = {'file': ('file.txt', f, 'text/plain')}
          response = http_util.post("/upload", files=files)

4. 发送 PUT 请求：
   a. 发送 JSON 数据的 PUT 请求：
      response = http_util.put("/path", json={"key": "value"}, headers={"Content-Type": "application/json"})

   b. 发送表单数据的 PUT 请求：
      response = http_util.put("/path", data={"key": "value"}, headers={"Content-Type": "application/x-www-form-urlencoded"})

5. 发送 DELETE 请求：
   a. 基本 DELETE 请求：
      response = http_util.delete("/path")

   b. 带自定义请求头的 DELETE 请求：
      response = http_util.delete("/path", headers={"Custom-Header": "Value"})

6. 处理响应：
   a. JSON 响应：
      response = http_util.get("/path")
      print(response)  # 自动解析为 Python 字典

   b. 文本响应：
      response = http_util.get("/path")
      print(response)  # 如果不是 JSON，则返回文本内容

   c. 流式响应：
      for chunk in http_util.get("/path", stream=True, chunk_size=1024):
          print(chunk)  # 打印每个数据块

7. 错误处理：
   try:
       response = http_util.get("/path")
   except requests.RequestException as e:
       print(f"请求失败: {e}")

8. 设置超时：
   http_util = HttpUtil(timeout=5)  # 5秒超时
   response = http_util.get("/path")  # 这个请求会在5秒后超时

9. 使用重试机制：
   http_util = HttpUtil(retries=3, backoff_factor=0.3)  # 最多重试3次，每次重试间隔递增
   response = http_util.get("/path")  # 这个请求会在失败时自动重试

10. 运行测试：
    直接运行此文件即可执行测试：
    python utils/http/http_utils.py
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Any, Dict, Optional, Union, Iterator
import logging

logger = logging.getLogger(__name__)

class HttpUtil:
    def __init__(self, base_url: str = "", timeout: int = 10, retries: Optional[int] = None, backoff_factor: float = 0.3):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        if retries is not None:
            retry_strategy = Retry(
                total=retries,
                backoff_factor=backoff_factor,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def _request(self, method: str, url: str, **kwargs) -> Union[Dict[str, Any], str, Iterator[bytes]]:
        full_url = f"{self.base_url}{url}"
        stream = kwargs.pop('stream', False)
        chunk_size = kwargs.pop('chunk_size', None)  # 默认为 None，使用 requests 的默认行为

        try:
            response = self.session.request(method, full_url, timeout=self.timeout, stream=stream, **kwargs)
            response.raise_for_status()

            if stream:
                return response.iter_content(chunk_size=chunk_size)
            
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.RequestException as e:
            logger.error(f"HTTP请求失败: {e}")
            raise

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Union[Dict[str, Any], str, Iterator[bytes]]:
        return self._request("GET", url, params=params, headers=headers, **kwargs)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Union[Dict[str, Any], str, Iterator[bytes]]:
        return self._request("POST", url, data=data, json=json, headers=headers, **kwargs)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, **kwargs) -> Union[Dict[str, Any], str, Iterator[bytes]]:
        return self._request("PUT", url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Union[Dict[str, Any], str, Iterator[bytes]]:
        return self._request("DELETE", url, headers=headers, **kwargs)

if __name__ == "__main__":
    import unittest
    from unittest.mock import patch, Mock

    class TestHttpUtil(unittest.TestCase):
        def setUp(self):
            self.http_util = HttpUtil(base_url="http://example.com", retries=3)

        @patch("requests.Session.request")
        def test_get_request(self, mock_request):
            print("测试基本 GET 请求...")
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"key": "value"}
            mock_request.return_value = mock_response

            response = self.http_util.get("/test")
            self.assertEqual(response, {"key": "value"})
            mock_request.assert_called_once_with(
                "GET", 
                "http://example.com/test", 
                timeout=10, 
                headers=None,
                stream=False,
                params=None
            )
            print("基本 GET 请求测试通过")

        @patch("requests.Session.request")
        def test_get_request_with_params_and_headers(self, mock_request):
            print("测试带查询参数和自定义请求头的 GET 请求...")
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"key": "value"}
            mock_request.return_value = mock_response

            response = self.http_util.get("/test", params={"key": "value"}, headers={"Custom-Header": "Value"})
            self.assertEqual(response, {"key": "value"})
            mock_request.assert_called_once_with(
                "GET", 
                "http://example.com/test", 
                timeout=10, 
                headers={"Custom-Header": "Value"},
                stream=False,
                params={"key": "value"}
            )
            print("带查询参数和自定义请求头的 GET 请求测试通过")

        @patch("requests.Session.request")
        def test_post_request_with_json(self, mock_request):
            print("测试带 JSON 数据的 POST 请求...")
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"key": "value"}
            mock_request.return_value = mock_response

            response = self.http_util.post("/test", json={"data": "value"}, headers={"Content-Type": "application/json"})
            self.assertEqual(response, {"key": "value"})
            mock_request.assert_called_once_with(
                "POST", 
                "http://example.com/test", 
                timeout=10, 
                json={"data": "value"}, 
                data=None,
                headers={"Content-Type": "application/json"},
                stream=False
            )
            print("带 JSON 数据的 POST 请求测试通过")

        @patch("requests.Session.request")
        def test_put_request_with_form_data(self, mock_request):
            print("测试带表单数据的 PUT 请求...")
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"key": "value"}
            mock_request.return_value = mock_response

            response = self.http_util.put("/test", data={"key": "value"}, headers={"Content-Type": "application/x-www-form-urlencoded"})
            self.assertEqual(response, {"key": "value"})
            mock_request.assert_called_once_with(
                "PUT", 
                "http://example.com/test", 
                timeout=10, 
                data={"key": "value"}, 
                json=None,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                stream=False
            )
            print("带表单数据的 PUT 请求测试通过")

        @patch("requests.Session.request")
        def test_delete_request_with_headers(self, mock_request):
            print("测试带自定义请求头的 DELETE 请求...")
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"key": "value"}
            mock_request.return_value = mock_response

            response = self.http_util.delete("/test", headers={"Custom-Header": "Value"})
            self.assertEqual(response, {"key": "value"})
            mock_request.assert_called_once_with(
                "DELETE", 
                "http://example.com/test", 
                timeout=10, 
                headers={"Custom-Header": "Value"},
                stream=False
            )
            print("带自定义请求头的 DELETE 请求测试通过")

        @patch("requests.Session.request")
        def test_stream_response(self, mock_request):
            print("测试流式响应...")
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.iter_content.return_value = iter([b"chunk1", b"chunk2"])
            mock_request.return_value = mock_response

            response = self.http_util.get("/test", stream=True, headers={"Accept": "application/octet-stream"}, chunk_size=1)
            chunks = list(response)
            self.assertEqual(chunks, [b"chunk1", b"chunk2"])
            mock_request.assert_called_once_with(
                "GET", 
                "http://example.com/test", 
                timeout=10, 
                headers={"Accept": "application/octet-stream"},
                stream=True,
                params=None
            )
            print("流式响应测试通过")

        @patch("requests.Session.request")
        def test_stream_response_without_chunk_size(self, mock_request):
            print("测试不指定 chunk_size 的流式响应...")
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.iter_content.return_value = iter([b"chunk1", b"chunk2"])
            mock_request.return_value = mock_response

            response = self.http_util.get("/test", stream=True, headers={"Accept": "application/octet-stream"})
            chunks = list(response)
            self.assertEqual(chunks, [b"chunk1", b"chunk2"])
            mock_request.assert_called_once_with(
                "GET", 
                "http://example.com/test", 
                timeout=10, 
                headers={"Accept": "application/octet-stream"},
                stream=True,
                params=None
            )
            mock_response.iter_content.assert_called_once_with(chunk_size=None)
            print("不指定 chunk_size 的流式响应测试通过")

    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestHttpUtil))