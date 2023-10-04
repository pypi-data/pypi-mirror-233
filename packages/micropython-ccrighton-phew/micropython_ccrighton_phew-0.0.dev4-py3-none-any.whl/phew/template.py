from.import logging
async def render_template(template,**kwargs):
	A='utf-8';import time;start_time=time.ticks_ms()
	with open(template,'rb')as f:
		data=f.read();token_caret=0
		while True:
			start=data.find(b'{{',token_caret);end=data.find(b'}}',start);match=start!=-1 and end!=-1
			if not match:yield data[token_caret:];break
			expression=data[start+2:end].strip();yield data[token_caret:start];params={};params.update(locals());params.update(kwargs)
			try:
				if expression.decode(A)in params:result=params[expression.decode(A)];result=result.replace('&','&amp;');result=result.replace('"','&quot;');result=result.replace("'",'&apos;');result=result.replace('>','&gt;');result=result.replace('<','&lt;')
				else:result=eval(expression,globals(),params)
				if type(result).__name__=='generator':
					for chunk in result:yield chunk
				elif result is not None:yield str(result)
			except:pass
			token_caret=end+2
	logging.debug('> parsed template:',template,'(took',time.ticks_ms()-start_time,'ms)')