#!/usr/bin/env python3
"""test_client"""
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import Mock, patch, PropertyMock

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient"""
    @parameterized.expand([
        ("google", {'name': 'google'}),
        ("abc", {'name': 'abc'}),
    ])
    @patch('client.get_json')
    def test_org(self, org, expected, mocked_get_json):
        """Test GithubOrgClient.org"""
        mocked_get_json.return_value = Mock(return_value=expected)
        test_org = GithubOrgClient(org)
        self.assertEqual(test_org.org(), expected)
        mocked_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org))

    def test_public_repos_url(self):
        """Test for GithubOrgClient._public_repos_url"""
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mocked_org:
            mocked_org.return_value = {
                "repos_url": "https://api.github.com/repos_name"}
            obj = GithubOrgClient('abc')
            self.assertEqual(
                obj._public_repos_url,
                "https://api.github.com/repos_name")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """test for GithubOrgClient.public_repos"""
        test_payload = {"repos_url":
                        {"repos_url":
                         "https://api.github.com/orgs/google/repos"
                         },
                        "repos": [{"id": 7697149,
                                   "node_id": "MDEwOlJlcG9zaXRvcnk3Njk3MTQ5",
                                   "name": "episodes.dart",
                                   "full_name": "google/episodes.dart",
                                   "private": False, },
                                  {"id": 7776515,
                                   "node_id": "MDEwOlJlcG9zaXRvcnk3Nzc2NTE1",
                                   "name": "cpp-netlib",
                                   "full_name": "google/cpp-netlib",
                                   "private": False, }]}
        mock_get_json.return_value = test_payload["repos"]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mocked_repos_url:
            mocked_repos_url.return_value = test_payload["repos_url"]
            obj = GithubOrgClient('abc')
            self.assertEqual(
                obj.public_repos(), [
                    "episodes.dart", "cpp-netlib"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test for GithubOrgClient.has_license"""
        self.assertEqual(
            GithubOrgClient.has_license(
                repo, license_key), expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubClient(unittest.TestCase):
    """Test integration for GitHubOrgClient.repos"""
    @classmethod
    def setUpClass(cls):
        """Setup class for integration tests"""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return None

        cls.get_patcher = patch('requests.get', side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self):
        """test GithubOrgClient.public_repos"""
        self.assertEqual(
            GithubOrgClient('google').public_repos(),
            self.expected_repos)

    def test_public_repos_with_license(self):
        """test GithubOrgClient.public_repos
            with the argument license="apache-2.0"
        """
        self.assertEqual(
            GithubOrgClient('google').public_repos(
                license='apache-2.0'),
            self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """Teardown class for integration tests"""
        cls.get_patcher.stop()
