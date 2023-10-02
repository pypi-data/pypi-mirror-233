## 简介

AppleSearchAdsSDK是一个用于与Apple Search Ads Campaign Management API进行交互的软件开发工具包（SDK）。它提供了一组功能丰富的工具和方法，用于简化与Apple Search Ads广告系列进行交互的过程。
以下是 Apple Search Ads SDK 的主要功能和用途：
* 广告活动管理: 开发者可以使用 SDK 创建、修改和管理其 Apple Search Ads 广告活动。这包括创建新广告系列、设定广告组和关键字的出价等。
* 拉取广告报告数据: SDK 可以帮助开发者生成广告活动报告，以便进行数据分析和决策制定。这些报告可以用于了解广告活动的整体表现和趋势，以及评估广告投资的回报。

## 特性
- Oauth2 授权Token管理
- 封装API功能，简化API交互
- 持续更新，及时根据Apple Search Ads Campaign Management API 新特性

## API文档

[Apple Search Ads Campaign Management API文档地址](https://developer.apple.com/documentation/apple_search_ads)

## 准备

- [Python](https://www.python.org/) 和 [git](https://git-scm.com/) -项目开发环境


## 使用

- 获取项目代码

```bash
git clone git@github.com:wangjiabiao/AppleSearchAdsSDK.git
```

- 安装

```bash
pip install AppleSearchAdsSDK
```

- 如何使用此SDK 管理你的AppleSearchAds
* 1、在Apple Search Ads 广告系列管理 API V4版本中，使用OAuth 2进行身份验证。 在正式开始前请先阅读：[Implementing OAuth for the Apple Search Ads API](https://developer.apple.com/documentation/apple_search_ads/implementing_oauth_for_the_apple_search_ads_api) .在本项目中auth.py模块帮助实现了以下功能：
    - 生成私钥
    - 提取公钥
    - 创建客户端密码
    

## 更新日志

[CHANGELOG](./CHANGELOG.md)

## 维护者
[@wangjiabiao](https://github.com/wangjiabiao)

