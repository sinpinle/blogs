# blogs
self blog
Mongodb 存储格式：

blog:
{
    "_id" : ObjectId("5a66e451c3033ccc0ff5cfe3"),
    "title" : "标题",
    "content" : "markdown 格式的文本",
    "is_reprint" : "", #是否转载
    "reprint_url" : "", #转载地址
    "tag" : "标签",
    "author" : "作者",
    "post_date" : "2018-01-23 15:25",
    "update_date":"2018-01-23 15:25",
    "top":0,
    "status" : 1
}

tag:
{
    "_id" : ObjectId("5a6b39262dc173a5140ac356"),
    "name" : "标签名称",
    "count" : 该标签下共有多少篇
}

user:
{
    "_id" : ObjectId("5a644636c3033ccc0ff59c4c"),
    "name" : "xxx",
    "password" : "xxxx",
    "email" : "xxx@xxx",
    "role" : "admin",
    "avatar" : "",
    "last_login" : "2018-02-26 05:34:44"
}

comment
