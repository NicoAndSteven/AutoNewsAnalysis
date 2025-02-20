# AutoNewsAnalysis

部署项目https://github.com/LLM-Red-Team/deepseek-free-api.git作为响应文本分析的服务器

获取NEWSAPI的API_KEY https://newsapi.org

![](D:\AI_AUTO\AutoNewsAnalysis\note\newsapi.png)

## 原生部署

请先安装好Node.js环境并且配置好环境变量，确认node命令可用。

安装依赖

```shell
npm i
```

安装PM2进行进程守护

```shell
npm i -g pm2
```

编译构建，看到dist目录就是构建完成

```shell
npm run build
```



构建完成后，后续只需启动服务即可

启动服务

```shell
pm2 start dist/index.js --name "deepseek-free-api"
```

查看服务实时日志

```shell
pm2 logs deepseek-free-api
```

重启服务

```shell
pm2 reload deepseek-free-api
```

停止服务

```shell
pm2 stop deepseek-free-api
```

