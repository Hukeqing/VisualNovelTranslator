# VisualNovelTranslator
_(version: 0.21)_

这是一个通过OCR和在线翻译的API实现的翻译工具
你需要在根目录下建立一个名为`setting.json`的文件，并在其中按照下面的格式输入你的信息

```json
{
  "OCR": {
    "apiKey": "key_1",
    "SecretKey": "key_2"
  },
  "translate": {
    "baidu": {
      "appid": "key_3",
      "secretKey": "key_4"
    }
  }
}
```

其中，四处key请使用对应的id和key代替
