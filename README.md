# LLDB_EX
LLDB Python 扩展命令

脚本使用方法
1.手动加载命令(在LLDB模式下运行以下命令，~/block.py为被执行脚本文件路径)
	command script import ~/block.py          
2.自动加载命令
  检查~/.lldbinit 文件是否存在不存在则建一个 touch ~/.lldbinit
  打开终端命令 输入 vi ~/.lldbinit
  输入 command script import xxx      (xxx为待执行脚本的路径)
  重启Xcode,重启Xcode,重启Xcode重要的事情说3遍
  进入LLDB环境就可以使用扩展的命令了

1.block.py
  获取32位设备 block 函数实现地址,自动计算ida对应函数实现地址,自动获取block函数参数

2.sbr
  根据ida输入的地址添加获取主程序ALSR偏移地址自动下断点  