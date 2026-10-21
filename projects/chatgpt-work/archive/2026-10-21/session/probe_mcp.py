import subprocess,json
p=subprocess.Popen([r'C:\Program Files\VectorCraft\vectorcraft-cli.exe','mcp','--headless'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8')
for i,(method,params) in enumerate([('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'test','version':'0.4'}}),('tools/list',{})]):
 p.stdin.write(json.dumps({'jsonrpc':'2.0','id':i,'method':method,'params':params})+'\n');p.stdin.flush()
 result=json.loads(p.stdout.readline())
 if method=='tools/list':
  print(json.dumps(result,ensure_ascii=True)[:22000])
p.terminate()
