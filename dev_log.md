

【target】

软件工程：重新整理项目代码结构，不会随着项目增大而臃肿

后端部分：新增mysql支持，加速结构化数据查询速度，结合两种数据库在不同地方发挥各自优势。

前端部分：采用state受控组件优化此前基于refs的search功能。less重构。fix采用HOOK缓存解决重排问题（useMemo、useCalback）

项目新增：add详情页





【8-14 08点55分】 ：

fix： TypeError: Cannot read properties of undefined (reading ‘forEach‘)

description：Chrome无法正常启动项目

cause：由于浏览器内核的不同，在自动分割程序中，因为；的原因，产生一些分割和压缩的错误。并更新插件“React Develop Tools到4.25.0版本”

Done

-------



【8-21 12点14分】：

1，实践课题进展情况和任务完成情况。（计划完成的任务，已完成的任务）
2，存在的问题和拟解决的思路。
3，下一步计划。

熟悉代码，评估需求，

评估工作量是否在规定时间内可以完成优化和测试通过。



【详细设计-代码结构优化】：

此前的目录结构中，以back、pages、store、router为结构，随着项目越来越大，其中pages模块越来越大，给维护和优化工作带来困难。

将修改目录结构，拟定提取出公共模块common，pages中分不同部分进行拆分，解耦合。

pages下每个部分再进行组件化开发，新产生的公共组件再提取到各自的common中，按照公共组件所在层级划分复用范围。

back中加入新模块，使用mysql进行后端请求支持，多种支持共同运行。（可行性暂未评估，因为这里需要学习一些新东西）

![2-1](.\img\2-1.png)



进展：上周修复了Chrome内核无法启动项目的问题（一方面是多中浏览器的支持是基本的需求，算是重要bug了，另一方面是如果不修复则无法使用react_dev_tool查看重新渲染情况）。

另外是花了两天时间去熟悉上学期写得项目代码，发现一些耦合严重的地方，可以提取common模块定制一些项目中的通用组件。

评估：

- 优化项目代码结构，1-2天
- 优化search功能，1天
- detail page开发，2-4天
- 基于HOOK重构的渲染优化， 1-2天
- 使用less语言进行前处理重构，优化样式查找效率， 1-2天
- 后端新支持的接入，待学习了解和评估，接入方面也需要一些时间
- 单元测试与前后端联调，在每项功能开发完之后，以及整体完成之后

下周从优化代码结构开始，逐步完成各项需求，虽然有一个预期时间，但是后端支持方面了解甚少，所以前面的需求会尽量加速完成，给后面提供一些提前量。





-----------

【8-22 9点45分】

修改src/back文件结构，模块：新增mysql、封装neo4j

mysql运行于8001端口，neo4j仍然运行于8000端口



----------

【8-22 10点02分】

修改code runner插件设置，Run in Terminal 

fix：多后端程序运行的冲突问题。



---------------

【8-22 10点29分】

查找：多后端运行方法，vscode terminal 中 使用node运行

code runner只是修改了默认的执行方式，并未真正解决问题。

test：多端口同时监听测试成功，能够返回到数据



------------

【8-22 16点46分】

问题：无法连接MySQl数据库

错误报告：Error: ER_BAD_DB_ERROR: Unknown database 

1049：更新mysql版本，任务管理器清除mysqld.exe，然后在计算机管理面板，重启mysql服务，连接成功。



---------

【8-23 08点56分】

问题：搜索框在监听过程中，中文打字中间间隔为'，这与mysql模糊匹配中的一些内容相同，导致后端ERROR。

错误报告：[SELECT ERROR] - ER_PARSE_ERROR: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 's'd%' LIMIT 10' at line 1

fix：解析问题，在后端进行类型检查，一种是默认值检查；另一种方式是运用中间件进行转换编码。暂时选择第一种方式。



---------

