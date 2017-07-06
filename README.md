# python
简单封装python常用方法：

1.excelToJson 把excel格式化为json对象。
commUtils.excelToJson('eg.xls')
2. formatJson json格式化。
commUtils.formatJson('{'a':'0','b':'2'}')
3. formatSql sql替换。
commUtils.formatSql('建表语句')
4. formatUrl 获取url参数。返回json
commUtils.formatUrl('url?a=b&b=c')
5. getDate 获取当前日期。
commUtils.getDate()
6. jsonToExcel json转excel
commUtils.jsonToExcel({})
7. random 随机数
commUtils.random()
8. uuid 获取uuid
commUtils.uuid()
9. replaceName 下划线名称字段取出转大写 ui_id -> uiId	
commUtils.replaceName('ui_id')
10.parsing_sql sql 字段信息打印	
