# 微信机器人

#### 项目介绍
微信机器人 是用Python包装Web微信协议实现的微信机器人框架

1 环境与依赖
此版本只能运行于Python 2环境 。

wxBot 用到了Python requests , pypng , Pillow 以及 pyqrcode 库。

使用之前需要所依赖的库:

pip install requests
pip install pyqrcode
pip install pypng
pip install Pillow
pip install mysql

4 接口
4.1 handle_msg_all
handle_msg_all 函数的参数 msg 是代表一条消息的字典。字段的内容为：

字段名	字段内容
msg_type_id	整数，消息类型，具体解释可以查看 消息类型表
msg_id	字符串，消息id
content	字典，消息内容，具体含有的字段请参考 消息类型表 ，一般含有 type(数据类型)与 data(数据内容)字段，type 与 data的对应关系可以参考 数据类型表
user	字典，消息来源，字典包含 name(发送者名称,如果是群则为群名称，如果为微信号，有备注则为备注名，否则为微信号或者群昵称)字段与 id(发送者id)字段，都是字符串
4.2 消息类型表
类型号	消息类型	content
0	初始化消息，内部数据	无意义，可以忽略
1	自己发送的消息	无意义，可以忽略
2	文件消息	字典，包含 type 与 data 字段
3	群消息	字典， 包含 user (字典，包含 id 与 name字段，都是字符串，表示发送此消息的群用户)与 type 、 data 字段，红包消息只有 type 字段， 文本消息还有detail、desc字段， 参考 群文本消息
4	联系人消息	字典，包含 type 与 data 字段
5	公众号消息	字典，包含 type 与 data 字段
6	特殊账号消息	字典，包含 type 与 data 字段
99	未知账号消息	无意义，可以忽略
4.3 数据类型表
type	数据类型	data
0	文本	字符串，表示文本消息的具体内容
1	地理位置	字符串，表示地理位置
3	图片	字符串，图片数据的url，HTTP POST请求此url可以得到jpg文件格式的数据
4	语音	字符串，语音数据的url，HTTP POST请求此url可以得到mp3文件格式的数据
5	名片	字典，包含 nickname (昵称)， alias (别名)，province (省份)，city (城市)， gender (性别)字段
6	动画	字符串， 动画url, HTTP POST请求此url可以得到gif文件格式的数据
7	分享	字典，包含 type (类型)，title (标题)，desc (描述)，url (链接)，from (源网站)字段
8	视频	不可用
9	视频电话	不可用
10	撤回消息	不可用
11	空内容	空字符串
12	红包	不可用
13	小视频	字符串，视频数据的url，HTTP POST请求此url可以得到mp4文件格式的数据
99	未知类型	不可用
4.4 群文本消息
由于群文本消息中可能含有@信息，因此群文本消息的 content 字典除了含有 type 与 data 字段外，还含有 detail 与 desc 字段。

各字段内容为：

字段	内容
type	数据类型， 为0(文本)
data	字符串，消息内容，含有@信息
desc	字符串，删除了所有@信息
detail	数组，元素类型为含有 type 与 value 字段的字典， type 为字符串 str (表示元素为普通字符串，此时value为消息内容) 或 at (表示元素为@信息， 此时value为所@的用户名)
4.5 WXBot对象属性
WXBot 对象在登录并初始化之后,含有以下的可用数据:

属性	描述
contact_list	当前用户的微信联系人列表
group_list	当前用户的微信群列表
public_list	当前用户关注的公众号列表
special_list	特殊账号列表
session	WXBot 与WEB微信服务器端交互所用的 Requests Session 对象
4.6 WXBot对象方法
WXBot 对象还含有一些可以利用的方法

方法	描述
get_icon(uid, gid)	获取联系人或者群聊成员头像并保存到本地文件 img_[uid].jpg , uid 为用户id, gid 为群id
get_head_img(id)	获取用户头像并保存到本地文件 img_[id].jpg ，id 为用户id(Web微信数据)
get_msg_img(msgid)	获取图像消息并保存到本地文件 img_[msgid].jpg , msgid 为消息id(Web微信数据)
get_voice(msgid)	获取语音消息并保存到本地文件 voice_[msgid].mp3 , msgid 为消息id(Web微信数据)
get_video(msgid)	获取视频消息并保存到本地文件 video_[msgid].mp4 , msgid 为消息id(Web微信数据)
get_contact_name(uid)	获取微信id对应的名称，返回一个可能包含 remark_name (备注名), nickname (昵称), display_name (群名称)的字典
send_msg_by_uid(word, dst)	向好友发送消息，word 为消息字符串，dst 为好友用户id(Web微信数据)
send_img_msg_by_uid(fpath, dst)	向好友发送图片消息，fpath 为本地图片文件路径，dst 为好友用户id(Web微信数据)
send_file_msg_by_uid(fpath, dst)	向好友发送文件消息，fpath 为本地文件路径，dst 为好友用户id(Web微信数据)
send_msg_by_uid(word, dst)	向好友发送消息，word 为消息字符串，dst 为好友用户id(Web微信数据)
send_msg(name, word, isfile)	向好友发送消息，name 为好友的备注名或者好友微信号， isfile为 False 时 word 为消息，isfile 为 True 时 word 为文件路径(此时向好友发送文件里的每一行)，此方法在有重名好友时会有问题，因此更推荐使用 send_msg_by_uid(word, dst)
is_contact(uid)	判断id为 uid 的账号是否是本帐号的好友，返回 True (是)或 False (不是)
is_public(uid)	判断id为 uid 的账号是否是本帐号所关注的公众号，返回 True (是)或 False (不是)

#### 参与贡献

1. Fork 本项目