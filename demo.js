/*
 author:cyhu(viskey.hu@gmail.com) 2014.7.8
 --modified 2014.7.24 cyhu
 --modified 2014.12.26 cyhu

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:

 1. Redistributions of source code must retain the above copyright notice,
 this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright
 notice, this list of conditions and the following disclaimer in
 the documentation and/or other materials provided with the distribution.

 3. The names of the authors may not be used to endorse or promote products
 derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED WARRANTIES,
 INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
 FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JCRAFT,
 INC. OR ANY CONTRIBUTORS TO THIS SOFTWARE BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
 OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
/***************************************************ELEMENT**************************************************************/
var HINT_IFLYTEK = '科大讯飞成立于1999年，是中国最大的智能化语音技术提供商，其语音核心技术代表世界最高水平。2008年科大讯飞在深圳证券交易所挂牌上市';

var HINT_API = 're do mi so';

var HINT_RENAISSANCE =
'IFLYTEK.AI enables developers to add a natural language interface to their app or device in minutes. It’s faster and more accurate than Siri, and requires no upfront investment, expertise, or training dataset.';
/***************************************************ELEMENT**************************************************************/
/***********************************************local Variables**********************************************************/

/**
  * 初始化Session会话
  * url                 连接的服务器地址（可选）
  * reconnection        客户端是否支持断开重连
  * reconnectionDelay   重连支持的延迟时间
  */
var session = new IFlyTtsSession({
									'url'                : 'http://webapi.openspeech.cn/',
									'reconnection'       : true,
									'reconnectionDelay'  : 30000
								});
/* 音频播放对象 */
window.iaudio = null;
/* 音频播放状态 0:未播放且等待音频数据状态，1:正播放且等待音频数据状态，2：未播放且不等待音频数据*/
var audio_state = 0;
/***********************************************local Variables**********************************************************/


Date.prototype.format = function(format) {
    var o = {
        "M+": this.getMonth() + 1,
        // month
        "d+": this.getDate(),
        // day
        "h+": this.getHours(),
        // hour
        "m+": this.getMinutes(),
        // minute
        "s+": this.getSeconds(),
        // second
        "q+": Math.floor((this.getMonth() + 3) / 3),
        // quarter
        "S": this.getMilliseconds(),
        // AM|PM
        "P": this.getHours() <= 12?"上午":"下午"
    };
    if (/(y+)/.test(format) || /(Y+)/.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    for (var k in o) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length));
        }
    }
    return format;
};

function current_timestamp() {
    return (new Date(Math.round(new Date().getTime()/1000) * 1000));
}

function play(content, vcn){
    reset();
	/**
	  * 参数说明:
	  * gat ( get audio type )  获取音频的类型，取值范围包括wav,mp3.
	  * caller.appid            应用的APPID，在语音云官网(open.voicecloud.cn)上申请.
	  * timestamp               当前时间戳，服务器使用该字符串进行数字签名
      * expires                 失效时间，服务器使用该字符串进行数字签名
      * signature 	            数字签名，MD5(appid + '&' + timestamp + '&' + expires + '&' + secret_key)
	  */
  var appid = "56f2b1c9";
  var timestamp = current_timestamp().format("Ph:m:s");
  var expires = 60000;
  var signature = faultylabs.MD5(appid + '&' + timestamp + '&' + expires + '&' + "8110b402d07b5bff");

	var param = {"params" : "aue = speex-wb;7, ent=intp65, spd = 50, vol = 50, tte=utf8, caller.appid=" + appid + ",timestamp = " + timestamp + ",expires=" + expires + ",vcn=" + vcn, "signature" : signature, "gat" : "mp3"};

	session.start(param, content, function (err, obj)
	{
		var audio_url = "http://webapi.openspeech.cn/" + obj.audio_url;

		/* 若返回音频链接，则直接使用audio标签进行播放 优点：兼容性高*/
		if( audio_url != null && audio_url != undefined )
		{
			window.iaudio.src = audio_url;
			window.iaudio.play();
		/* 若返回音频数据，则插入音频缓存队列，依次进行播放 优点：合成速度快*/
		}
	});
};

/**
  * 停止播放音频
  *
  */
function stop() {
    audio_state = 2;
    audio.pause();
}

function play_xiaoqi(){play(HINT_API, 'xiaoqi')};

/**
  * 重置音频缓存队列和播放对象
  * 若音频正在播放，则暂停当前播放对象，创建并使用新的播放对象.
  */
function reset()
{
	audio_array = [];
	audio_state = 0;
	if(window.iaudio != null)
	{
		window.iaudio.pause();
	}
	window.iaudio = new Audio();
	window.iaudio.src = '';
	window.iaudio.play();
};
