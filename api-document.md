## api文档
### 用户

#### 手机验证码
地址:	/api/captcha/
方法:	POST
参数: 	mobile:Number

#### 注册
地址:	/api/register/
方法:	POST
参数:	username | password | name | captcha

#### 登录
地址:	/api/login/
方法:	POST
参数:	username | password 

#### 获取自己信息 
地址:	/api/user_self/
方法:	GET
授权:	yes

#### 获取他人信息
地址:	/api/user/:id
方法:	GET

#### 关于指定用户
地址:	/api/user_follow/:id
方法:	GET
授权:	yes

#### 我关注了谁
地址:	/api/user_followed/
方法:	GET
授权:	yes

#### 谁关注了该用户
地址:	/api/user_followers
方法:	GET

#### 修改密码
地址:	/api/user_change_password/
方法:	POST
参数:	password | old_password 
授权:	yes

####  编辑资料
地址:	/api/user_edit_profile/
方法:	POST
参数:	email | name | location | about_me | avatar | company | blog 
授权:	yes