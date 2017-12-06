#!/usr/bin/python
#coding:utf-8

# 脚本使用方法
# 1.手动加载命令(在LLDB模式下运行以下命令，~/block.py为当前文件路径)
#   command script import ~/block.py          
# 2.自动加载命令
# 
import lldb
import commands
import optparse
import shlex
import re
import string

showDebug = 1

# 获取ASLR偏移地址
def get_ASLR():
	# 获取'image list -o' 命令的返回结果
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('image list -o',returnObject)
	output = returnObject.GetOutput();
	# 正则匹配出第一个0x开头的16进制地址
	match = re.match(r'.+(0x[0-9a-fA-F]+)', output)
	if match:
		return match.group(1)
	else:
		return None

# 根据block首地址打印后续地址
def get_Address(command):
	# 获取'image list -o' 命令的返回结果
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('memory read --size 8 --format x %s' % command,returnObject)
	output = returnObject.GetOutput();
	
	if showDebug:
		print '初始地址 ' + command + '输出结果\n' + output
	
	arr = output.split()

	if arr:
		return arr
	else:
		return None

def get_block_funcDesChar(address):
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('p (char *) %s' % address,returnObject)
	output = returnObject.GetOutput();
	#output 实际输出结果为 (char *) $5 = 0x06c07873 "v8@?0@"SAKError"4"
	arr = output.split()
	length = len(arr)
	#获取最后一个元素 "v8@?0@"SAKError"4"
	result = arr[length - 1]
	#删除第一个及最后一个双引号
	newResult = result[1:-1]
	#剩余的每个双引号前面加上斜杠转义字符
	newResult = newResult.replace('"','\\"')
	#首尾恢复双引号
	newResult = '"' + newResult + '"'
	if showDebug:
		print 'oldName ' + result + ' newName ' + newResult

	if newResult:
		return newResult
	else:
		return None

# 获取函数参数类型
def get_block_funcParamers(funcCharName):
	interpreter = lldb.debugger.GetCommandInterpreter()
	returnObject = lldb.SBCommandReturnObject()
	interpreter.HandleCommand('po [NSMethodSignature signatureWithObjCTypes:%s]' % funcCharName,returnObject)
	output = returnObject.GetOutput();

	if output:
		return output
	else:
		return None

def block64(debugger,command,result,internal_dict):
	#用户是否输入了地址参数
	if not command:
		print >>result,'Please input the address!'
		return
		print >>result,'Please i1111!'
		return
    # 根据block首地址打印后续地址
	ASLR = get_ASLR()

	blockAddressList = get_Address(command)
	# block 函数实现地址 16个字节之后
	blockFuncAddress = blockAddressList[4]
	print 'S:' + blockFuncAddress
	# block ida中的函数实现地址
	idaFuncAddress = hex(eval(blockFuncAddress) - eval(ASLR))
	# block函数描述结构体地址连续地址
	blocDesAddressList = get_Address(blockAddressList[5])
	# char 类型参数
	blockParamsCharName = get_block_funcDesChar(blocDesAddressList[4])
	# block 函数参数
	blockParams = get_block_funcParamers(blockParamsCharName)
	print '\nFuncAddress: ' + blockFuncAddress + '\nASLR: ' + ASLR + '\nIDA_FuncAddress:' + idaFuncAddress + '\nParames: ' + blockParams

	if blockParams:
		print 'Success!'
	else:
		print 'Failure!'

def __lldb_init_module(debugger,internal_dict):
	# 'command script add block64' : 给lldb增加一个'block64'命令
	# '-f block64.block64' : 该命令调用了block64文件的block64函数	 
	debugger.HandleCommand('command script add block64 -f block64.block64')
	print 'The "block64" python command has been installed and is ready for use.'