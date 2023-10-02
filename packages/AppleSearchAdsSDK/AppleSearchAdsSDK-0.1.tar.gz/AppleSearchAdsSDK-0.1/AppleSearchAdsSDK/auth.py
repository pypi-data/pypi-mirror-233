# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : authentication
# Time       ：2023/7/20 16:14
# Author     ：leo.wang
# version    ：python 3.9
# Description：实现 Apple Search Ads API OAuth 功能
"""
import datetime
import subprocess
import urllib
from typing import Optional

import jwt
import requests

from AppleSearchAdsSDK.libs.utils import get_logger
from AppleSearchAdsSDK.settings import AUTH_ENDPOINT, TOKEN_ENDPOINT

log = get_logger(level=10)


class Auth:
    def __init__(self, client_id, team_id, key_id, client_secret=None, redirect_uri=None):
        self.client_id = client_id
        self.team_id = team_id
        self.key_id = key_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_endpoint = AUTH_ENDPOINT
        self.token_endpoint = TOKEN_ENDPOINT
        self.access_token = None
        self.refresh_token = None

    def create_private_key(self, out: str):
        """
        创建私钥,私钥文件存储在out指定的位置
        :param out: 用于生成和存储密钥对的文件名。如：private-key.pem
        """
        openssl_cmd = ["openssl", "ecparam", "-genkey", "-name", "prime256v1", "-noout", "-out", out]
        try:
            subprocess.run(openssl_cmd, check=True)
            log.debug(f"私钥 {out} 生成成功！")
        except subprocess.CalledProcessError as e:
            log.error(f"私钥 {out} 生成失败: {e}")

    def create_public_key(self, private_key: str, out: str):
        """
        从私钥中提取公钥
        :param private_key: 私钥文件名
        :param out: 在其中生成和存储公钥的文件。如：ec256-public-key
        """
        openssl_cmd = ["openssl", "ec", "-in", private_key, "-pubout", "-out", out]
        try:
            subprocess.run(openssl_cmd, check=True)
            log.debug(f"私钥 {out} 生成成功！")
        except subprocess.CalledProcessError as e:
            log.error(f"私钥 {out} 生成失败: {e}")

    def create_client_secret(self, private_key_path: str, out: str) -> str:
        """
        创建client_secret
        :param private_key_path: 私钥文件目录
        :param out: 最终client_secret文件目录
        :return: client_secret 字符串
        """
        audience = 'https://appleid.apple.com'
        alg = 'ES256'

        # Define issue timestamp.
        issued_at_timestamp = int(datetime.datetime.utcnow().timestamp())
        # Define expiration timestamp. May not exceed 180 days from issue timestamp.
        expiration_timestamp = issued_at_timestamp + 86400 * 180

        # Define JWT headers.
        headers = dict()
        headers['alg'] = alg
        headers['kid'] = self.key_id

        # Define JWT payload.
        payload = dict()
        payload['sub'] = self.client_id
        payload['aud'] = audience
        payload['iat'] = issued_at_timestamp
        payload['exp'] = expiration_timestamp
        payload['iss'] = self.team_id

        with open(private_key_path, "rb") as rf, open(out, "wb") as wf:
            client_secret = jwt.encode(
                payload=payload,
                headers=headers,
                algorithm=alg,
                key=rf.read().decode("utf-8")
            )
            wf.write(client_secret.encode("utf-8"))

        return client_secret

    def get_authorization_url(self, state: str) -> str:
        """
        sign with apple 前置接口
        返回authorization_url 和缓存用户信息（用于授权后关联系统账户）
        """
        log.debug("state:%s", state)
        auth_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'searchads',
            'state': state,
        }
        params = urllib.parse.urlencode(auth_params)
        authorization_url = f"{self.auth_endpoint}?{params}"
        log.debug("authorization_url:%s", authorization_url)
        return authorization_url

    def get_access_token(self, client_secret: str, grant_type: Optional[str] = "client_credentials", scope: Optional[str] = "searchadsorg") -> dict:
        """请求苹果oauth2接口获取 access_token"""
        data = {
            "client_id": self.client_id,
            "client_secret": client_secret,
            "grant_type": grant_type,
            "scope": scope
        }
        headers = {
            "Host": "appleid.apple.com",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        resp = requests.post(self.token_endpoint, data=data, headers=headers, timeout=60)
        status_code = resp.status_code
        if status_code != 200:
            log.warning(f"获取token:{status_code} 异常:{resp.text} .")
            raise IOError(f"获取Access Token 异常:{self.client_id} {status_code} {resp.text}")
        return resp.json()


if __name__ == '__main__':
    #     private_key = "/tmp/private-key.pem"
    #     out = "/tmp/ec256-public-key"
    #     client_id = 'your_client_id'
    #     client_secret = 'your_client_secret'
    #     redirect_uri = 'your_redirect_uri'
    #     auth_endpoint = 'authorization_endpoint_url'
    #     token_endpoint = 'token_endpoint_url'
    #
    auth = Auth()
    auth.get_access_token()
#     auth.create_public_key(private_key, out)
