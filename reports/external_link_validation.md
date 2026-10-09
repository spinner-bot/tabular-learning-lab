# 外部来源链接可达性验证

验证日期：2026-10-09

运行命令：

```text
python code/check_external_links.py
```

结果文件：`reports/external_link_validation.json`

结果：20 个唯一外部来源 URL 均返回 HTTP 200。OpenReview 链接最终重定向到 challenge 页面，但 HTTP 可达；这只证明链接可访问，不证明页面内容已经逐条核读，也不证明来源支持课件中的全部主张。

该检查使用 HEAD 请求，遇到 403/405 时使用有限 GET 回退，并保存最终 URL、HTTP 状态和日期。网络状态会变化，后续引用核验仍需以来源内容、版本和适用边界为准。
