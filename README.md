# ApiTestByCurl
通过curl的方式对web api接口进行自动化测试

# Usage
 ## 准备
 1. 接口测试用例依赖tencent的TAPD敏捷研发平台，使用了它的测试用例管理功能，对接口测试用例进行维护
 2. 且TAPD项目需开通开放API。
 3. 本工程在python3上进行开发和调试。
 
 ## 使用步骤
 1. 在tapd上进行用例编写，把浏览器上的请求以“copy as curl(bash)”的方式粘贴到tapd中，且包在‘【】’中。
 2. python main.py
 
# 说明
1. 如果没有TAPD维护接口自动化测试用例，可使用其他方式，如：excel、数据库方式存储和编写接口测试用例。
2. 基于上面1点，需自行开发用例读取功能，具体在AbcUtils->TestCaseParser.py中，override对应方法。
