var stlib = stlib || {
  functions: [],
  functionCount: 0,
  util: {
    prop: function(p, obj) {
      if (obj) {
        return obj[p];
      }
      return function(o) { return o[p]; };
    }
  },
  dynamicOn: true,
  setPublisher : function(pubKey){
    stlib.publisher = pubKey;
  },
  setProduct : function(prod){
    stlib.product = prod;
  },
  parseQuery: function( query ) {
    var Params = new Object ();
    if ( ! query ) return Params; // return empty object
    var Pairs = query.split(/[;&]/);
    for ( var i = 0; i < Pairs.length; i++ ) {
       var KeyVal = Pairs[i].split('=');
       if ( ! KeyVal || KeyVal.length != 2 ) continue;
       var key = unescape( KeyVal[0] );
       var val = unescape( KeyVal[1] );
       val = val.replace(/\+/g, ' ');
       Params[key] = val;
    }
    return Params;
  },
  getQueryParams : function(){
    var buttonScript = document.getElementById('st_insights_js');
    if(buttonScript && buttonScript.src){
      var queryString = buttonScript.src.replace(/^[^\?]+\??/,'');
      var params = stlib.parseQuery( queryString );
      stlib.setPublisher ( params.publisher);
      stlib.setProduct( params.product);
    }
  }
};

stlib.global = {
  hash: stlib.util.prop('hash', document.location).substr(1)
};

// Extract out parameters
stlib.getQueryParams();
stlib.debugOn = false;
stlib.debug = {
	count: 0,
	messages: [],
	debug: function(message, show) {
		if (show && (typeof console) != "undefined") {
			console.log(message);
		} 
		stlib.debug.messages.push(message);
	},
	show: function(errorOnly) {
		for (message in stlib.debug.messages) {
			if ((typeof console) != "undefined") {
				if (errorOnly) {
					/ERROR/.test(stlib.debug.messages[message]) ? console.log(stlib.debug.messages[message]) : null;
				} else {
					console.log(stlib.debug.messages[message]);
				}
			} 
		}
	},
	showError: function() { 
		stlib.debug.show(true); 
	}
};

var _$d = function(message) {	stlib.debug.debug(message, stlib.debugOn); }
var _$d0 = function() { _$d(" "); };
var _$d_ = function() { _$d("___________________________________________"); };
var _$d1 = function(m) { _$d(_$dt() + "| " + m); };
var _$d2 = function(m) { _$d(_$dt() + "|  * " + m); };
var _$de = function(m) { _$d(_$dt() + "ERROR: " + m); };

var _$dt = function() { 
	var today=new Date();
	var h=today.getHours();
	var m=today.getMinutes();
	var s=today.getSeconds();
	return h+":"+m+":"+s+" > ";
};
/***************START JSON ENCODE/DECODE***************/
stlib.json = {
	c : {"\b":"b","\t":"t","\n":"n","\f":"f","\r":"r",'"':'"',"\\":"\\","/":"/"},
	d : function(n){return n<10?"0".concat(n):n},
	e : function(c,f,e){e=eval;delete eval;if(typeof eval==="undefined")eval=e;f=eval(""+c);eval=e;return f},
	i : function(e,p,l){return 1*e.substr(p,l)},
	p : ["","000","00","0",""],
	rc : null,
	rd : /^[0-9]{4}\-[0-9]{2}\-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$/,
	rs : /(\x5c|\x2F|\x22|[\x0c-\x0d]|[\x08-\x0a])/g,
	rt : /^([0-9]+|[0-9]+[,\.][0-9]{1,3})$/,
	ru : /([\x00-\x07]|\x0b|[\x0e-\x1f])/g,
	s : function(i,d){return "\\".concat(stlib.json.c[d])},
	u : function(i,d){
		var	n=d.charCodeAt(0).toString(16);
		return "\\u".concat(stlib.json.p[n.length],n)
	},
	v : function(k,v){return stlib.json.types[typeof result](result)!==Function&&(v.hasOwnProperty?v.hasOwnProperty(k):v.constructor.prototype[k]!==v[k])},
	types : {
		"boolean":function(){return Boolean},
		"function":function(){return Function},
		"number":function(){return Number},
		"object":function(o){return o instanceof o.constructor?o.constructor:null},
		"string":function(){return String},
		"undefined":function(){return null}
	},
	$$ : function(m){
		function $(c,t) { 
			t=c[m];
			delete c[m];
			try {
				stlib.json.e(c)
			} catch(z){c[m]=t;return 1;}
		};
		return $(Array)&&$(Object);
	},
	encode : function(){
		var	self = arguments.length ? arguments[0] : this,
			result, tmp;
		if(self === null)
			result = "null";
		else if(self !== undefined && (tmp = stlib.json.types[typeof self](self))) {
			switch(tmp){
				case	Array:
					result = [];
					for(var	i = 0, j = 0, k = self.length; j < k; j++) {
						if(self[j] !== undefined && (tmp = stlib.json.encode(self[j])))
							result[i++] = tmp;
					};
					result = "[".concat(result.join(","), "]");
					break;
				case	Boolean:
					result = String(self);
					break;
				case	Date:
					result = '"'.concat(self.getFullYear(), '-', stlib.json.d(self.getMonth() + 1), '-', stlib.json.d(self.getDate()), 'T', stlib.json.d(self.getHours()), ':', stlib.json.d(self.getMinutes()), ':', stlib.json.d(self.getSeconds()), '"');
					break;
				case	Function:
					break;
				case	Number:
					result = isFinite(self) ? String(self) : "null";
					break;
				case	String:
					result = '"'.concat(self.replace(stlib.json.rs, stlib.json.s).replace(stlib.json.ru, stlib.json.u), '"');
					break;
				default:
					var	i = 0, key;
					result = [];
					for(key in self) {
						if(self[key] !== undefined && (tmp = stlib.json.encode(self[key])))
							result[i++] = '"'.concat(key.replace(stlib.json.rs, stlib.json.s).replace(stlib.json.ru, stlib.json.u), '":', tmp);
					};
					result = "{".concat(result.join(","), "}");
					break;
			}
		};
		return result;
	},
	decode : function(input){
		if(typeof(input)=='string')
		{
			var data=null;
			try{if ( /^[\],:{}\s]*$/.test(input.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g, "@")
			 .replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, "]")	
			 .replace(/(?:^|:|,)(?:\s*\[)+/g, "")) ) {
			 	data=window.JSON && window.JSON.parse ? window.JSON.parse(input) : (new Function("return " + input))();
			 	return data;
			 }else{
			 	return null;
			 }}catch(err){}	
		}
	}
};
try{stlib.json.rc=new RegExp('^("(\\\\.|[^"\\\\\\n\\r])*?"|[,:{}\\[\\]0-9.\\-+Eaeflnr-u \\n\\r\\t])+?$')}
catch(z){stlib.json.rc=/^(true|false|null|\[.*\]|\{.*\}|".*"|\d+|\d+\.\d+)$/}
/***************END JSON ENCODE/DECODE***************/
/********************START COOKIE LIBRARY***********************/
/*
 * This handles cookies
 */
var tpcCookiesEnableCheckingDone = false;
var tpcCookiesEnabledStatus = true;

stlib.cookie = {
	setCookie : function(name, value, days) {
		var safari =(navigator.userAgent.indexOf("Safari") !=-1 && navigator.userAgent.indexOf("Chrome") ==-1);
		var ie =(navigator.userAgent.indexOf("MSIE") !=-1);

		if (safari || ie) {
			  var expiration = (days) ? days*24*60*60 : 0;

			  var _div = document.createElement('div');
			  _div.setAttribute("id", name);
			  _div.setAttribute("type", "hidden");
			  document.body.appendChild(_div);

			  var
			  div = document.getElementById(name),
			  form = document.createElement('form');

			  try {
				  var iframe = document.createElement('<iframe name="'+name+'" ></iframe>');
					//try is ie
				} catch(err) {
					//catch is ff and safari
					iframe = document.createElement('iframe');
				}

			  iframe.name = name;
			  iframe.src = 'javascript:false';
			  iframe.style.display="none";
			  div.appendChild(iframe);

			  form.action = "https://sharethis.com/account/setCookie.php";
			  form.method = 'POST';

			  var hiddenField = document.createElement("input");
			  hiddenField.setAttribute("type", "hidden");
			  hiddenField.setAttribute("name", "name");
			  hiddenField.setAttribute("value", name);
			  form.appendChild(hiddenField);

			  var hiddenField2 = document.createElement("input");
			  hiddenField2.setAttribute("type", "hidden");
			  hiddenField2.setAttribute("name", "value");
			  hiddenField2.setAttribute("value", value);
			  form.appendChild(hiddenField2);

			  var hiddenField3 = document.createElement("input");
			  hiddenField3.setAttribute("type", "hidden");
			  hiddenField3.setAttribute("name", "time");
			  hiddenField3.setAttribute("value", expiration);
			  form.appendChild(hiddenField3);

			  form.target = name;
			  div.appendChild(form);

			  form.submit();
		}
		else {
			if (days) {
				var date = new Date();
				date.setTime(date.getTime()+(days*24*60*60*1000));
				var expires = "; expires="+date.toGMTString();
			} else {
				var expires = "";
			}
			var cookie_string = name + "=" + escape(value) + expires;
			cookie_string += "; domain=" + escape (".sharethis.com")+";path=/";
			document.cookie = cookie_string;
		}
	},
	setTempCookie : function(name, value, days) {
		if (days) {
				var date = new Date();
				date.setTime(date.getTime()+(days*24*60*60*1000));
				var expires = "; expires="+date.toGMTString();
		} else {
				var expires = "";
		}
		var cookie_string = name + "=" + escape(value) + expires;
		cookie_string += "; domain=" + escape (".sharethis.com")+";path=/";
		document.cookie = cookie_string;
	},
	getCookie : function(cookie_name) {
	  var results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');
	  if (results) {
		  return (unescape(results[2]));
	  } else {
		  return false;
	  }
	},
	deleteCookie : function(name) {

		// For all browsers
		var path="/";
		var domain=".sharethis.com";
		document.cookie = name.replace(/^\s+|\s+$/g,"") + "=" +( ( path ) ? ";path=" + path : "")
				  + ( ( domain ) ? ";domain=" + domain : "" ) +";expires=Thu, 01-Jan-1970 00:00:01 GMT";


		// For Safari and IE
		var safari =(navigator.userAgent.indexOf("Safari") !=-1 && navigator.userAgent.indexOf("Chrome") ==-1);
		var ie =(navigator.userAgent.indexOf("MSIE") !=-1);

		if (safari || ie) {
			var _div = document.createElement('div');
			_div.setAttribute("id", name);
			_div.setAttribute("type", "hidden");
			document.body.appendChild(_div);

			var
			div = document.getElementById(name),
			form = document.createElement('form');

			try {
			  var iframe = document.createElement('<iframe name="'+name+'" ></iframe>');
				//try is ie
			} catch(err) {
				//catch is ff and safari
				iframe = document.createElement('iframe');
			}

			iframe.name = name;
			iframe.src = 'javascript:false';
			iframe.style.display="none";
			div.appendChild(iframe);

			form.action = "https://sharethis.com/account/deleteCookie.php";
			form.method = 'POST';

			var hiddenField = document.createElement("input");
			hiddenField.setAttribute("type", "hidden");
			hiddenField.setAttribute("name", "name");
			hiddenField.setAttribute("value", name);
			form.appendChild(hiddenField);

			form.target = name;
			div.appendChild(form);

			form.submit();
		}
	},
	deleteAllSTCookie : function() {
		var a=document.cookie;
		a=a.split(';');
		for(var i=0;i<a.length;i++){
			var b=a[i];
			b=b.split('=');

      // do not delete the st_optout cookie
			if(!/st_optout/.test(b[0])){
				var name=b[0];
				var path="/";
				var domain=".edge.sharethis.com";
				document.cookie = name + "=;path=" + path + ";domain=" + domain +";expires=Thu, 01-Jan-1970 00:00:01 GMT";
			}
		}
	},
	setFpcCookie : function(name, value) {
//		var name="__unam";
		var current_date = new Date;
		var exp_y = current_date.getFullYear();
		var exp_m = current_date.getMonth() + 9;// set cookie for 9 months into future
		var exp_d = current_date.getDate();
		var cookie_string = name + "=" + escape(value);
		if (exp_y) {
			var expires = new Date (exp_y,exp_m,exp_d);
			cookie_string += "; expires=" + expires.toGMTString();
		}
		var domain=stlib.cookie.getDomain();
		cookie_string += "; domain=" + escape (domain)+";path=/";
		document.cookie = cookie_string;
	},
	getFpcCookie : function(cookie_name) {
		var results = document.cookie.match('(^|;) ?' + cookie_name + '=([^;]*)(;|$)');
		if (results)
			return (unescape(results[2]));
		else
			return false;
	},
	getDomain : function() {
		var str = document.domain.split(/\./);
		var domain="";
		if(str.length>1){
			domain="."+str[str.length-2]+"."+str[str.length-1];
		}
		return domain;
	},
	checkCookiesEnabled: function() {
		if(!tpcCookiesEnableCheckingDone) {
			stlib.cookie.setTempCookie("STPC", "yes", 1);
			if(stlib.cookie.getCookie("STPC") == "yes") {
				tpcCookiesEnabledStatus = true;
			}else {
				tpcCookiesEnabledStatus = false;
			}
			tpcCookiesEnableCheckingDone = true;
			return tpcCookiesEnabledStatus;
		}else{
			return tpcCookiesEnabledStatus;
		}
	},
	hasLocalStorage: function() {
		try {
			localStorage.setItem("stStorage", "yes");
			localStorage.removeItem("stStorage");
			return true;
		} catch(e) {
			return false;
		}
	}
};
/********************END COOKIE LIBRARY***********************/
stlib.validate = {
	regexes: {
		notEncoded:		/(%[^0-7])|(%[0-7][^0-9a-f])|["{}\[\]\<\>\\\^`\|]/gi,
		tooEncoded:		/%25([0-7][0-9a-f])/gi,
		publisher:		/^(([a-z]{2}(-|\.))|)[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i,
		url:			/^(http|https):\/\/([a-z0-9!'\(\)\*\.\-\+:]*(\.)[a-z0-9!'\(\)\*\.\-\+:]*)((\/[a-z0-9!'\(\)\*\.\-\+:]*)*)/i,
		fpc:			/^[0-9a-f]{7}-[0-9a-f]{11}-[0-9a-f]{7,8}-[0-9]*$/i,
		sessionID:		/^[0-9]*\.[0-9a-f]*$/i,
		title:			/.*/,
		description:	/.*/,
		buttonType:		/^(chicklet|vcount|hcount|large|custom|button|)$/, // TODO: verify, also, is blank ok.
		comment:		/.*/,
		destination:	/.*/, // TODO: check against all service (construct a regexp?)
		source:			/.*/, // TODO: Need to define this
		image:			/(^(http|https):\/\/([a-z0-9!'\(\)\*\.\-\+:]*(\.)[a-z0-9!'\(\)\*\.\-\+:]*)((\/[a-z0-9!'\(\)\*\.\-\+:]*)*))|^$/i,
		sourceURL:		/^(http|https):\/\/([a-z0-9!'\(\)\*\.\-\+:]*(\.)[a-z0-9!'\(\)\*\.\-\+:]*)((\/[a-z0-9!'\(\)\*\.\-\+:]*)*)/i,
		sharURL:		/(^(http|https):\/\/([a-z0-9!'\(\)\*\.\-\+:]*(\.)[a-z0-9!'\(\)\*\.\-\+:]*)((\/[a-z0-9!'\(\)\*\.\-\+:]*)*))|^$/i
	}
};

stlib.html = {
	encode : function(value) {
		if(stlib.html.startsWith(value, 'http')) {//URL check
			return String(value)
				.replace(/"/g, '&quot;')
				.replace(/'/g, '&#39;')
				.replace(/</g, '&lt;')
				.replace(/>/g, '&gt;');		
		} else {
			return String(value)
				.replace(/&/g, '&amp;')
				.replace(/"/g, '&quot;')
				.replace(/'/g, '&#39;')
				.replace(/</g, '&lt;')
				.replace(/>/g, '&gt;');
		}
	},
  
	startsWith : function(value, str) {
     return (value.match("^"+str)==str);
    }
};
/*
 * This holds critical data, requires the cookie object
 */
if (typeof(stlib.data) == "undefined") {
	stlib.data = {
		bInit: false,
		publisherKeySet: false,
		pageInfo: {
		},
		shareInfo: {
		},
		resetPageData: function() {
			//stlib.data.pageInfo.publisher 		= "00-00-00"; // The publisher key as given by the publisher
			//stlib.data.pageInfo.fpc 			= "ERROR"; // The cookie set on the publisher's domain to track the user on that domain
			stlib.data.pageInfo.sessionID 		= "ERROR"; // The session on any given pageview with our widget on it
			//stlib.data.pageInfo.sourceURL		= "ERROR"; // The source domain
			stlib.data.pageInfo.hostname		= "ERROR"; // The source domain
			stlib.data.pageInfo.location		= "ERROR"; // The source domain
			stlib.data.pageInfo.product             = "widget";
			stlib.data.pageInfo.stid            = "";
		},
		resetShareData: function() {
			stlib.data.shareInfo = {};
			stlib.data.shareInfo.url 			= "ERROR"; // The url the service is sharing before any modification
			stlib.data.shareInfo.sharURL		= ""; // The shar url the service is sharing before any modification
			stlib.data.shareInfo.buttonType		= "ERROR"; // The button type that were clicked (hcount or vcount)
			stlib.data.shareInfo.destination	= "ERROR"; // The channel that is being shared to (facebook, twitter)
			stlib.data.shareInfo.source 		= "ERROR"; // The widget or code location that is generating the request
			//stlib.data.shareInfo.title 			= ""; // The title of the article as best as can be determined
			//stlib.data.shareInfo.image 			= ""; // The title of the article as best as can be determined
			//stlib.data.shareInfo.description 	= "";	   // The description of the article as best as can be determined
			//stlib.data.shareInfo.comment	 	= "";	   // The description of the article as best as can be determined
		},
		resetData: function() {
			stlib.data.resetPageData();
			stlib.data.resetShareData();
		},
		validate: function () {
			var regexes = stlib.validate.regexes;

			function validateHelp(key, value) {
				if (value != encodeURIComponent(value)) {
					regexes.notEncoded.test(value) ? _$de(key + " not encoded") : null;
					regexes.tooEncoded.test(value) ? _$de(key + " has too much encoding") :null;
				}
				var valueOk = regexes[key] ? regexes[key].test(decodeURIComponent(value)) : true;
				if (!valueOk) {
					_$de(key + " failed validation");
				}
			}

			var p = stlib.data.pageInfo;
			var param;
			for (param in p) {
				validateHelp(param, p[param])
			}
			p = stlib.data.shareInfo;
			for (param in p) {
				validateHelp(param, p[param])
			}

		},
		init: function() {
			if (!stlib.data.bInit) {
				stlib.data.bInit = true;
				stlib.data.resetData();
				stlib.data.set("fcmp", typeof(window.__cmp) == 'function', "pageInfo");
                              stlib.data.set("fcmpv2", typeof(window.__tcfapi) == 'function', "pageInfo");

				if(stlib.publisher){
					stlib.data.setPublisher(stlib.publisher);
				}
				stlib.data.set("product",stlib.product,"pageInfo");
				var rawUrl = document.location.href, refDomain = '', refQuery = '', referArray = [], currentRefer = '', cleanUrl = '', hashString = "",
					baseURL = '', sessionID_time = '', sessionID_rand = '';

				//Fix for WID-343
				referArray = stlib.data.getRefDataFromUrl(rawUrl);//get referrer data coming from share.es
				if(referArray.length > 0) {
					refDomain = (typeof(referArray[0]) != "undefined") ? referArray[0] : "";
					refQuery = (typeof(referArray[1]) != "undefined") ? referArray[1] : "";
					cleanUrl = stlib.data.removeRefDataFromUrl(rawUrl);//Remove referrer data from the URL.

					//Displays the modified(without referrer data parameter) or original URL in the address bar
					stlib.data.showModifiedUrl(cleanUrl);
					stlib.data.set("url", cleanUrl, "shareInfo");
				} else { //For old non-secure shar urls
					currentRefer = document.referrer;
					referArray = currentRefer.replace("http://", "").replace("https://", "").split("/");
					refDomain = referArray.shift();
					refQuery = referArray.join("/");

					stlib.data.set("url", rawUrl,"shareInfo");
				}
				// TODO add option to not use hash tag

        stlib.data.set("title", document.title, "shareInfo");

				if (stlib.data.publisherKeySet != true) {
					stlib.data.set("publisher","ur.00000000-0000-0000-0000-000000000000","pageInfo");
				}

				// no longer using fpc
				// stlib.fpc.createFpc();
				// stlib.data.set("fpc",stlib.fpc.cookieValue,"pageInfo"); // Requires that the cookie has been created

				sessionID_time = (new Date()).getTime().toString();
				sessionID_rand = Number(Math.random().toPrecision(5).toString().substr(2)).toString();
				stlib.data.set("sessionID",sessionID_time + '.' + sessionID_rand,"pageInfo");

				//stlib.data.set("sourceURL", document.location.href,"pageInfo");
				stlib.data.set("hostname", document.location.hostname,"pageInfo");
				stlib.data.set("location", document.location.pathname,"pageInfo");

				stlib.data.set("refDomain", refDomain ,"pageInfo");
				stlib.data.set("refQuery", refQuery,"pageInfo");
			}
		},
		//Fix for WID-343
		showModifiedUrl: function(modUrl) {
			if (window.history && history.replaceState)
				history.replaceState(null, document.title, modUrl);
			else if ((/MSIE/).test(navigator.userAgent)) {
				var ampInHashIndex = 0, hashString = window.location.hash, patt1 = new RegExp("(\&st_refDomain=?)[^\&|]+"),
					patt2 = new RegExp("(\#st_refDomain=?)[^\&|]+"), hRef = document.location.href;
				if(patt1.test(hRef)) {
					ampInHashIndex = hashString.indexOf('&st_refDomain');
					window.location.hash = hashString.substr(0, ampInHashIndex);
				} else if(patt2.test(hRef))
					window.location.replace("#");
			} else {
				document.location.replace(modUrl);
			}
		},
		//Fix for WID-343
		getRefDataFromUrl: function(url) {
			var patt = new RegExp("st_refDomain="), tempDomain = '', tempQuery = '', result = [];

			if(patt.test(url)) {
				tempDomain = url.match(/(st_refDomain=?)[^\&|]+/g);
				result.push(tempDomain[0].split('=')[1]);

				tempQuery = url.match(/(st_refQuery=?)[^\&|]+/g);
				result.push(tempQuery[0].replace('st_refQuery=', ''));
			}

			return result;
		},
		//Fix for WID-343
		removeRefDataFromUrl: function(url) {
			var urlWoRefdomain = '',
				obj = '',
				patt1 = new RegExp("(\&st_refDomain=?)[^\&|]+"),
				patt2 = new RegExp("(\#st_refDomain=?)[^\&|]+");

			if(patt1.test(url)) {
				urlWoRefdomain = url.replace(/\&st_refDomain=(.*)/g,'');
			} else if(patt2.test(url)) {
				urlWoRefdomain = url.replace(/\#st_refDomain=(.*)/g,'');
			} else {
				urlWoRefdomain = url;
			}

			return urlWoRefdomain;
		},
		setPublisher: function(publisherKey) {
			// TODO: Add Validation
			stlib.data.set("publisher",publisherKey,"pageInfo");
			stlib.data.publisherKeySet = true;
		},
		setSource: function(src, options) {
			// TODO: Add Validation
			var source = "";
			// Inside widget logging
			if (options) {
				if (options.toolbar) {
					source = "toolbar"+src;
				} else if (options.page && options.page != "home" && options.page != "") {
					source = "chicklet"+src;
				} else {
					source = "button"+src;
				}
			}
			// Outside widget logging
			else {
				// can be share5x, share4x, chicklet, fastshare, mobile
				source = src;
			}
			stlib.data.set("source",source,"shareInfo");
		},
		set: function(key, value, table) {
			if (typeof(value) == "number" || typeof(value) == "boolean") {
				stlib.data[table][key] = value;
			} else if (typeof(value) == "undefined" || value == null) {
			} else {
//				_$d1("Stripping HTML: " + key + ": " + value.replace(/<[^<>]*>/gi, " "));
//				_$d1("decodeURI: " + key + ": " + decodeURI(value.replace(/<[^<>]*>/gi, " ")));
//				_$d1("Escape percent: " + key + ": " + decodeURI(value.replace(/<[^<>]*>/gi, " ")).replace(/%/gi, "%25"));
//				_$d1("Decoding: " + key + ": " + decodeURIComponent(decodeURI(value.replace(/<[^<>]*>/gi, " ")).replace(/%/gi, "%25")));
//				_$d1("Encoding: " + key + ": " + encodeURIComponent(decodeURIComponent(decodeURI(value.replace(/<[^<>]*>/gi, " ")).replace(/%/gi, "%25"))));
				stlib.data[table][key] = encodeURIComponent(decodeURIComponent(unescape(value.replace(/<[^<>]*>/gi, " ")).replace(/%/gi, "%25")));
				// These might have url encoded data
				if (key=="url" /*|| key=="sourceURL"*/ || key=="location" || key=="image") {
					try {
						stlib.data[table][key] = encodeURIComponent(decodeURIComponent(decodeURI(value.replace(/<[^<>]*>/gi, " ")).replace(/%/gi, "%25")));
					} catch (e) {
						stlib.data[table][key] = encodeURIComponent(decodeURIComponent(unescape(value.replace(/<[^<>]*>/gi, " ")).replace(/%/gi, "%25")));
					}
				}
			}
		},
		get: function(key, table) {
			try {
				if (stlib.data[table] && stlib.data[table][key])
					return decodeURIComponent(stlib.data[table][key]);
				else
					return false;
			}catch(e){
				return false
			}
		},
		unset: function(key, table) {
			if (stlib.data[table] && typeof(stlib.data[table][key])!="undefined")
				delete stlib.data[table][key];
		},
                bindEvent: function(element, eventName, eventHandler) {
                    if (element.addEventListener) {
                        element.addEventListener(eventName, eventHandler, false);
                    } else if (element.attachEvent) {
                        element.attachEvent('on' + eventName, eventHandler);
                    }
                },
                debug: function(endpoint, event) {
                  stlib.data.init();
                  var a = stlib.data.pageInfo;
                  var c = "";
                  var b;
                  for (b in a) {
                      c += b + "=" + a[b] + "&"
                  }
                  c = c.substring(0, c.length - 1);

                  var loggerUrl = "https://l.sharethis.com/";
                  loggerUrl += endpoint;
                  loggerUrl += "?event=" + event;
                  loggerUrl += "&" + c;

                  var e = new Image(1, 1);
                  e.src = loggerUrl;
                  e.onload = function() {
                      return
                  };
                },
                hostname: function(url) {
                  var a;
                  if (url == null) {
                    url = st.href;
                  }
                  a = document.createElement('a');
                  a.setAttribute('href', url);
                  return a.hostname;
                },
                protocol: function(url) {
                  var a;
                  if (url == null) {
                    url = st.href;
                  }
                  a = document.createElement('a');
                  a.setAttribute('href', url);
                  return a.protocol;
                },
                parseCookie: function (name, cookie) {
                  var values = cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
                  return values ? values.pop() : null;
                },
                writeCookie: function(name, value, max_age)  {
                  if (!max_age) {
                    max_age = 33696000
                  }
                  var host = (window && window.location && window.location.hostname) || '';
                  var parts = host.split('.');
                  var domain = "";
                  if (parts.length > 1) {
                    domain = "domain=." + parts.slice(-2).join('.');
                  }
                  var samesite_secure = "";
                  try {
                    document.cookie = "st_samesite=1;SameSite=None;Secure";
                    if (stlib.data.parseCookie("st_samesite", document.cookie)) {
                      samesite_secure = "SameSite=None;Secure"
                      document.cookie = "st_samesite=1;max-age=0;SameSite=None;Secure";
                    }
                  } catch (e) {}
                  document.cookie = name + "=" + value + ";" + domain + ";path=/;max-age=" + max_age + ";" + samesite_secure;
                },
                setConsent: function(consent) {
                    for(var consent_key in consent) {
                         stlib.data.set(consent_key,consent[consent_key],"pageInfo");
                    }
                },
                getEUConsent: function (c) {

                  function once(fn, context) { 
                    var result;
                    return function() { 
                      if(fn) {
                        result = fn.apply(context || this, arguments);
                        fn = null;
                      }
                      return result;
                    };
                  }
        
                  var done = once(c);

                  // set usprivacy first if we have it
                  var usprivacy = stlib.data.parseCookie("usprivacy", document.cookie);
                  if (usprivacy) {
                    stlib.data.setConsent({
                      usprivacy: usprivacy
                    });
                  }

                  // keep track of how long it takes to get consent
                  var start = Date.now();

                  var useCookie = once(function() {
        
                    // check for first party cookies
                    var euconsent_v2 = stlib.data.parseCookie("euconsent-v2", document.cookie);
                    if (euconsent_v2 !== null) {
                      stlib.data.setConsent({
                        gdpr_consent: euconsent_v2,
                        gdpr_domain: document.location.hostname,
                        gdpr_method: "cookie"
                      });
                    }
                    done();
                  });

                  if (typeof window.__tcfapi == "function") {

                    // fallback to cookie in case the tcf api is too slow or unavailable
                    var timeout = setTimeout(useCookie, 5000);
        
                    // first we try to get the data from the cmp
                    // wrap in a try catch since we don't control the tcfapi code on page
                    try {

                      const tcfapi_callback = (data) => {
                        if (data && data.tcString) {
                          var gdpr_domain = (data.isServiceSpecific)
                            ? document.location.hostname : ".consensu.org";
                          stlib.data.setConsent({
                            consent_duration: Date.now() - start,
                            gdpr_consent: data.tcString,
                            gdpr_domain: gdpr_domain,
                            gdpr_method: "api"
                          });
                          clearTimeout(timeout);
                          done();
                          __tcfapi('removeEventListener', 2, () => {}, data.listenerId);
                        } 
                      }
                      __tcfapi('addEventListener', 2, tcfapi_callback);
                      
                    } catch (e) {
        
                      // fallback to cookie if there is an error
                      useCookie();
                    }
                  } else {
        
                    // fallback to cookie if the tcfapi doesn't exist
                    useCookie();
                  }
                }
	};

	stlib.data.resetData();
}
stlib.hash = {
	doNotHash: false,
	hashAddressBar: false,
	doNotCopy: false,
	prefix:"sthash",
	shareHash: "",
	incomingHash: "",
	validChars: ["1","2","3","4","5","6","7","8","9","0",
				"A","B","C","D","E","F","G","H","I","J",
				"K","L","M","N","O","P","Q","R","S","T",
				"U","V","W","X","Y","Z","a","b","c","d",
				"e","f","g","h","i","j","k","l","m","n",
				"o","p","q","r","s","t","u","v","w","x",
				"y","z"],
	servicePreferences: {
		linkedin: "param",
		stumbleupon: "param",
		bebo: "param"
	},
	hashDestination: function(destination) {
		if (destination == "copy") {return "dpuf";}
		var condensedString = destination.substring(0,2) + destination.substring(destination.length-2, destination.length);
		var increment = function(string, pos) {
			if(string.charCodeAt(pos) == 122) {
				return "a";
			}
			return String.fromCharCode(string.charCodeAt(pos) + 1);
		}
		return increment(condensedString, 0) + increment(condensedString, 1) + increment(condensedString, 2) + increment(condensedString, 3);
	},
	getHash: function() {
		var sthashFound = false;
		var sthashValue = "";
		var urlWithoutHash = document.location.href;
		urlWithoutHash = urlWithoutHash.split("#").shift();
		var paramArray = urlWithoutHash.split("?");
		if (paramArray.length > 1) {
			paramArray = paramArray[1].split("&");
			for (arg in paramArray) {
				try {
					if (paramArray[arg].substring(0, 6) == "sthash") {
						sthashFound = true;
						sthashValue = paramArray[arg];
					}
				} catch (err) {

				}
			}
			if (sthashFound) {
				return sthashValue;
			} else {
				return document.location.hash.substring(1);
			}
		} else {
			return document.location.hash.substring(1);
		}
	},
	stripHash: function(url) {
		var urlWithoutHash = url;
		urlWithoutHash = urlWithoutHash.split("#");
		if (urlWithoutHash.length > 1)
			return urlWithoutHash[1];
		else
			return "";
	},
	clearHash: function() {
		if (stlib.hash.validateHash(document.location.hash)) {
			var baseHref = document.location.href.split("#").shift();

			if (window.history && history.replaceState)
//				history.replaceState(null, "ShareThis", "#");
				history.replaceState(null, document.title, baseHref);
			else if ((/MSIE/).test(navigator.userAgent))
				window.location.replace("#");
			else
				document.location.hash = "";
		}
	},
	init: function() {
		var finalHash = "";
		var max = stlib.hash.validChars.length;
		for (var i=0;i<8;i++) {
			finalHash += stlib.hash.validChars[Math.random()*max|0];
		}
		if (stlib.hash.getHash() == "") {
			stlib.hash.shareHash = stlib.hash.prefix + "." + finalHash;
		} else {
			var splitHash = stlib.hash.getHash().split(".");
			var key = splitHash.shift();
			if (key == stlib.hash.prefix || key == stlib.hash.prefix) {
				stlib.hash.incomingHash = stlib.hash.getHash();
				stlib.hash.shareHash = stlib.hash.prefix + "." + splitHash.shift() + "." + finalHash;
			} else {
				stlib.hash.shareHash = stlib.hash.prefix + "." + finalHash;
			}
		}
		if (!stlib.hash.doNotHash && stlib.hash.hashAddressBar) {
			if (document.location.hash == "" || stlib.hash.validateHash(document.location.hash)) {
				if (window.history && history.replaceState)
					history.replaceState(null, "ShareThis", "#"+stlib.hash.shareHash + ".dpbs");
				else if ((/MSIE/).test(navigator.userAgent))
					window.location.replace("#"+stlib.hash.shareHash + ".dpbs");
				else
					document.location.hash = stlib.hash.shareHash + ".dpbs";
			}
		} else {
			stlib.hash.clearHash();
		}
		if (!stlib.hash.doNotHash && !stlib.hash.doNotCopy) {
			stlib.hash.copyPasteInit();
		}
		stlib.hash.copyPasteLog();
	},
	checkURL: function() {
		var destination = stlib.data.get("destination", "shareInfo");
		var baseURL = stlib.hash.updateParams(destination);
		var shortenedDestination = "." + stlib.hash.hashDestination(destination);
		stlib.hash.updateDestination(shortenedDestination);
		if (!stlib.hash.doNotHash && typeof(stlib.data.pageInfo.shareHash) != "undefined") {
			var url = stlib.data.get("url", "shareInfo");
			var hash = stlib.hash.stripHash(url);
			if (stlib.hash.validateHash(hash) || hash == "") {
				if(typeof(stlib.hash.servicePreferences[destination]) != "undefined") {
					if(stlib.hash.servicePreferences[destination] == "param") {
						_$d1("Don't use hash, use params");
						_$d2(baseURL);
						if (baseURL.split("?").length > 1) {
							var parameterArray = baseURL.split("?")[1].split("&")
							var sthashExists = false;
							//for (arg in parameterArray) {
							for (var arg = 0; arg < parameterArray.length; arg++) {
								if (parameterArray[arg].split(".")[0] == "sthash") {
									sthashExists = true;
								}
							}
							if (sthashExists) {
								// Param was fixed by updateParams, dont need to add anything
								stlib.data.set("url",baseURL, "shareInfo");
							} else {
								// Param wasn't there, need to add it.
								stlib.data.set("url",baseURL + "&" + stlib.data.pageInfo.shareHash, "shareInfo");
							}
						} else {
							// There are no params, need to add the hash param
							stlib.data.set("url",baseURL + "?" + stlib.data.pageInfo.shareHash, "shareInfo");
						}
						if (destination == "linkedin") {	// shar url contains # which is an error in LinkedIn
							if (stlib.data.get("sharURL", "shareInfo") != "") {
								stlib.data.set("sharURL", stlib.data.get("url", "shareInfo"), "shareInfo");
							}
						}
					} else {
						_$d1("Using Hash");
						stlib.data.set("url",baseURL + "#" + stlib.data.pageInfo.shareHash, "shareInfo");
					}
				} else {
					_$d1("Not using custom destination hash type");
					stlib.data.set("url",baseURL + "#" + stlib.data.pageInfo.shareHash, "shareInfo");
				}
			}
		}
	},
	updateParams: function(destination) {
		var baseURL = stlib.data.get("url", "shareInfo").split("#").shift();
		var regex2a = /(\?)sthash\.[a-zA-z0-9]{8}\.[a-zA-z0-9]{8}/;
		var regex2b = /(&)sthash\.[a-zA-z0-9]{8}\.[a-zA-z0-9]{8}/;
		var regex1a = /(\?)sthash\.[a-zA-z0-9]{8}/;
		var regex1b = /(&)sthash\.[a-zA-z0-9]{8}/;
		if (regex2a.test(baseURL)) {
			baseURL = baseURL.replace(regex2a, "?" + stlib.data.pageInfo.shareHash);
		} else if (regex2b.test(baseURL)) {
			baseURL = baseURL.replace(regex2b, "&" + stlib.data.pageInfo.shareHash);
		} else if (regex1a.test(baseURL)) {
			baseURL = baseURL.replace(regex1a, "?" + stlib.data.pageInfo.shareHash);
		} else if (regex1b.test(baseURL)) {
			baseURL = baseURL.replace(regex1b, "&" + stlib.data.pageInfo.shareHash);
		}
		return baseURL;
	},
	updateDestination: function(destinationHash) {
		var regex2 = /sthash\.[a-zA-z0-9]{8}\.[a-zA-z0-9]{8}\.[a-z]{4}/;
		var regex1 = /sthash\.[a-zA-z0-9]{8}\.[a-z]{4}/;
		_$d_();
		_$d1("Updating Destination");
		if (regex2.test(stlib.data.pageInfo.shareHash)) {
			_$d2(stlib.data.pageInfo.shareHash.substring(0,24));
			stlib.data.pageInfo.shareHash = stlib.data.pageInfo.shareHash.substring(0,24) + destinationHash;
		} else if (regex1.test(stlib.data.pageInfo.shareHash)) {
			_$d2(stlib.data.pageInfo.shareHash.substring(0,15));
			stlib.data.pageInfo.shareHash = stlib.data.pageInfo.shareHash.substring(0,15) + destinationHash;
		} else {
			stlib.data.pageInfo.shareHash += destinationHash;
		}
	},
	validateHash: function(isValidHash) {
		var regex3 = /[\?#&]?sthash\.[a-zA-z0-9]{8}\.[a-zA-z0-9]{8}$/;
		var regex2 = /[\?#&]?sthash\.[a-zA-z0-9]{8}\.[a-zA-z0-9]{8}\.[a-z]{4}$/;
		var regex1 = /[\?#&]?sthash\.[a-zA-z0-9]{8}\.[a-z]{4}$/;
		var regex0 = /[\?#&]?sthash\.[a-zA-z0-9]{8}$/;
		return regex0.test(isValidHash) || regex1.test(isValidHash) || regex2.test(isValidHash) || regex3.test(isValidHash);
	},
	appendHash : function (url) {
		var hash = stlib.hash.stripHash(url);
		if (stlib.data.pageInfo.shareHash && (stlib.hash.validateHash(hash) || hash == "")) {
			url = url.replace("#"+hash,"") + "#" + stlib.data.pageInfo.shareHash;
		} else {
		}
		return url;
	},
	copyPasteInit: function() {
		var body = document.getElementsByTagName("body")[0];
		var replacement = document.createElement("div");
		replacement.id = "stcpDiv";
		replacement.style.position = "absolute";
		replacement.style.top = "-1999px";
		replacement.style.left = "-1988px";
		body.appendChild(replacement);
		replacement.innerHTML = "ShareThis Copy and Paste";
		var baseHref = document.location.href.split("#").shift();
		var hash = "#" + stlib.hash.shareHash;
		if (document.addEventListener) {
			body["addEventListener"]("copy",function(e){
				//TYNT CONFLICT FIX: do not copy if Tynt object exists
				if (typeof(Tynt)!="undefined"){
//					console.log("Tynt exists. Don't copy");
					return;
				}
//				console.log("Tynt doesn't exist. Proceed");

				//grab current range and append url to it
				var selection = document.getSelection();

				if (selection.isCollapsed) {
					return;
				}

				var markUp = selection.getRangeAt(0).cloneContents();
				replacement.innerHTML = "";
				replacement.appendChild(markUp);

				if (replacement.textContent.trim().length==0) {
				    return;
				}

				if((selection+"").trim().length==0) {
					//No text, don't need to do anything
				} else if (replacement.innerHTML == (selection+"") || replacement.textContent == (selection+"")) {
					//Fix for CNS FB:12969. Encode html data to avoid js script execution on content copy
					replacement.innerHTML = stlib.html.encode(stlib.hash.selectionModify(selection));
				} else {
					//Fix for CNS FB:12969. Encode html data to avoid js script execution on content copy
					replacement.innerHTML += stlib.html.encode(stlib.hash.selectionModify(selection, true));
				}
				var range = document.createRange();
				range.selectNodeContents(replacement);
				var oldRange = selection.getRangeAt(0);
			},false);
		} else if (document.attachEvent) {
			/*
			body.oncopy = function() {
				var oldRange = document.selection.createRange();
				replacement.innerHTML = oldRange.htmlText;
				try {
					var length = (oldRange.text).trim().length;
				} catch (e) {
					var length = (oldRange.text).replace(/^\s+|\s+$/g, '').length;
				}
				if(length==0) {
					//No text, don't need to do anything
				} else if (oldRange.htmlText == oldRange.text) {
					//Just text, treat normally
					replacement.innerHTML = stlib.hash.selectionModify(oldRange.text);
				} else {
					//Text and markup, special case
					replacement.innerHTML += stlib.hash.selectionModify(oldRange.text, true);
				}
				var range = document.body.createTextRange();
				range.moveToElementText(replacement);
				range.select();
				setTimeout(function() {oldRange.select();}, 1);
			};
			*/
		}
	},
	copyPasteLog: function() {
		var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
		var messageEvent1 = eventMethod == "attachEvent" ? "oncopy" : "copy";
		var body = document.getElementsByTagName("body")[0];
		if(body){
			body[eventMethod](messageEvent1,function(e){
				var pass = true;
				stlib.data.resetShareData();
				stlib.data.set("url", document.location.href, "shareInfo");
				stlib.data.setSource("copy");
				stlib.data.set("destination", "copy", "shareInfo");
		    	stlib.data.set("buttonType", "custom", "shareInfo");

				if (typeof(Tynt)!="undefined"){
					// Log Tynt
					stlib.data.set("result", "tynt", "shareInfo");
					pass = false;
				}
				if (typeof(addthis_config)!="undefined") {
					// Log AddThis
					stlib.data.set("result", "addThis", "shareInfo");
					if (typeof(addthis_config.data_track_textcopy)=="undefined"||addthis_config.data_track_textcopy) {
						stlib.data.set("enabled", "true", "shareInfo");
						pass = false;
					} else {
						stlib.data.set("enabled", "false", "shareInfo");
					}
				}
			},false);
		}
	},
	logCopy: function(url, selection) {
		stlib.data.resetShareData();
	    stlib.data.set("url", url, "shareInfo");
	    stlib.data.setSource("copy");
    	stlib.data.set("destination", "copy", "shareInfo");
    	stlib.data.set("buttonType", "custom", "shareInfo");
    	if (selection)
    		stlib.data.set("copy_text", selection, "shareInfo");
    	stlib.sharer.share();
	},
	selectionModify: function(selection, anchorOnly) {
		selection = "" + selection;
		_$d_();
		_$d1("Copy Paste");
		var regex = /^((http|https):\/\/([a-z0-9!'\(\)\*\.\-\+:]*(\.)[a-z0-9!'\(\)\*\.\-\+:]*)((\/[a-z0-9!'\(\)\*\.\-\+:]*)*))/i;
		var regex2 = /^([a-z0-9!'\(\)\*\.\-\+:]*(\.)[a-z0-9!'\(\)\*\.\-\+:]*)((\/[a-z0-9!'\(\)\*\.\-\+:]*)*)/i;
		var regexPhoneNumberUS = /^\+?1?[\.\-\\)_\s]?[\\(]?[0-9]{3}[\.\-\\)_\s]?[0-9]{3}[\.\-_\s]?[0-9]{4}$|^[0-9]{3}[\.\-_\s]?[0-9]{4}$/;
		var regexPhoneNumberIndia = /^[0-9]{3}[\.\-_\s]?[0-9]{8}$/;
		var regexPhoneNumberBrazil = /^[0-9]{2}[\.\-_\s]?[0-9]{4}[\.\-_\s]?[0-9]{4}$/;
		var regexEmail = /[\-_\.a-z0-9]+@[\-_\.a-z0-9]+\.[\-_\.a-z0-9]+/i;
		var regex3 = /[\s@]/;
		var baseHref = document.location.href.split("#").shift();
		var hash = "#" + stlib.hash.shareHash;
		var anchorStr = "";
		var urlStr = "";
		var returnStr = selection;
		if (typeof(anchorOnly) == "undefined" && ((regex.test(selection) || regex2.test(selection)) && !regex3.test(selection.trim()))) { // the selection is a url
			_$d2("is Url");
			if (selection.match(/#/) == null || stlib.hash.validateHash(selection)) {
				urlStr = selection.split("#")[0] + hash + ".dpuf";
			} else {
				urlStr = selection;
			}
		} else {
			_$d2("is Not Url");
			if (document.location.hash == "" || (/^#$/).test(document.location.hash) || stlib.hash.validateHash(document.location.hash)) {
				urlStr = baseHref + hash + ".dpuf";
			} else {
				urlStr = document.location.href;
			}
			returnStr = selection;
			if (selection.length > 50) {
				if (!regexPhoneNumberUS.test(selection) && !regexPhoneNumberIndia.test(selection) && !regexPhoneNumberBrazil.test(selection) && !regexEmail.test(selection)) {		// don't add if an email or phone number
					returnStr += anchorStr;
				}
			}
		}
		if (selection.length > 500) {
			selection = selection.substring(0, 497) + "...";
		}
		stlib.hash.logCopy(urlStr, selection);
		return returnStr;
	}
};

stlib.allServices = {
	adfty: {title: 'Adfty'},
	allvoices: {title:'Allvoices'},
	amazon_wishlist: {title:'Amazon Wishlist'},
	arto: {title:'Arto'}, 
	att: {title:'AT&T'},	
	baidu: {title: 'Baidu'},
	blinklist : {title : 'Blinklist'},
	blip: {title: 'Blip'},
	blogmarks : {title : 'Blogmarks'},
	blogger : {title : 'Blogger',type : 'post'},
	buddymarks: {title: 'BuddyMarks'},
	buffer: {title: 'Buffer'},
	care2 : {title : 'Care2'},
	chiq : {title:'chiq'},
	citeulike : {title : 'CiteULike'},
	chiq : {title : 'chiq'},
	corkboard: {title: 'Corkboard'},
	dealsplus : {title : 'Dealspl.us'},
	delicious : {title : 'Delicious'},
	digg : {title : 'Digg'},
	diigo : {title : 'Diigo'},
	dzone: {title: 'DZone'},
	edmodo : {title : 'Edmodo'},
	email : {title : 'Email'},
	embed_ly : {title : 'Embed.ly'},
	evernote: {title:'Evernote'},
	facebook : {title : 'Facebook'},
	fark : {title : 'Fark'},
	fashiolista: {title:'Fashiolista'},
	flipboard: {title:'Flipboard'},
	folkd:{title:'folkd.com'},
	foodlve: {title:'FoodLve'},
	fresqui : {title : 'Fresqui'},
	friendfeed : {title : 'FriendFeed'},
	funp : {title : 'Funp'},
	fwisp: {title:'fwisp'},
	google: {title: 'Google'},
	googleplus: {title: 'Google +'},
	google_bmarks : {title : 'Bookmarks'},
	google_reader: {title: 'Google Reader'},
	google_translate: {title: 'Google Translate'},
	hatena: {title:'Hatena'},
	instapaper : {title : 'Instapaper'},
	jumptags: {title:'Jumptags'},
	kaboodle:{title:'Kaboodle'},
	kik: {title:'Kik'},
	linkagogo:{title:'linkaGoGo'},
	linkedin : {title : 'LinkedIn'},
	livejournal : {title : 'LiveJournal',type : 'post'},
	mail_ru : {title : 'mail.ru'},
	meneame : {title : 'Meneame'},
	messenger : {title : 'Messenger'},
	mister_wong : {title : 'Mr Wong'},
	moshare : {title : 'moShare'},
	myspace : {title : 'MySpace'},
	n4g : {title : 'N4G'},
	netlog: {title: 'Netlog'},
	netvouz:{title:'Netvouz'},
	newsvine : {title : 'Newsvine'},
	nujij:{title:'NUjij'},
	odnoklassniki : {title : 'Odnoklassniki'},
	oknotizie : {title : 'Oknotizie'},
	pinterest:{title:'Pinterest'},
	pocket:{title:'Pocket'},
	print:{title:'Print'},
	raise_your_voice : {title : 'Raise Your Voice'},
	reddit : {title : 'Reddit'},
	segnalo : {title : 'Segnalo'},
	sharethis : {title : 'ShareThis'},
	sina: {title:'Sina'},
	sonico : {title : 'Sonico'},
	startaid:{title:'Startaid'},
	startlap:{title:'Startlap'},
	stumbleupon : {title : 'StumbleUpon'},
	stumpedia:{title:'Stumpedia'},
	typepad : {title : 'TypePad',type : 'post'},
	tumblr : {title : 'Tumblr'},
	twitter : {title : 'Twitter'},
	viadeo:{title:'Viadeo'},
	virb:{title:'Virb'},
	vkontakte : {title : 'Vkontakte'},
	voxopolis:{title: 'VOXopolis'},
	whatsapp : {title: 'WhatsApp'},
	weheartit : {title: 'We Heart It'},
	wordpress : {title : 'WordPress',type : 'post'},
	xerpi:{title:"Xerpi"},
	xing: {title:'Xing'},
	yammer : {title : 'Yammer'}
};
stlib.allOauthServices = {
	twitter: {title:'Twitter'},
	linkedIn : {title : 'LinkedIn'},
	facebook : {title : 'Facebook'}
};
stlib.allNativeServices = {
	fblike:{title:"Facebook Like"},
	fbrec:{title:"Facebook Recommend"},
	fbsend:{title:"Facebook Send"},
	fbsub:{title:"Facebook Subscribe"},
	foursquaresave:{title:"Foursquare Save"},
	foursquarefollow:{title:"Foursquare Follow"},
	instagram:{title:"Instagram Badge"},
	plusone: {title:'Google +1'},
	pinterestfollow : {title : 'Pinterest Follow'},
	twitterfollow : {title : 'Twitter Follow'},
	youtube : {title : 'Youtube Subscribe'}
};
stlib.allDeprecatedServices = {
	google_bmarks:{title:'Google Bookmarks'},
	yahoo_bmarks:{title:'Yahoo Bookmarks'}
};
stlib.allOtherServices = {
	copy:{title:'Copy Paste'},
	sharenow:{title:'ShareNow'},
	sharenow_auto:{title:'Frictionless Sharing'},
	fbunlike:{title:'Facebook Unlike'}
};
var _all_services = stlib.allServices;/********************START LOGGING***********************/
/*
 * This handles logging
 */
stlib.logger = {
  loggerUrl: "https://l.sharethis.com/",
  l2LoggerUrl: "https://l2.sharethis.com/",
  productArray: new Array(),
  version: '',
  lang: 'en',
  isFpEvent: false,

  constructParamString: function() {
    
    // Pull all the parameters from the page the widget was on
    var p = stlib.data.pageInfo;
    var paramString = "";
    var param;

    for (param in p) {
      
      // the following line creates "param=value&"
      if (p[param] == null || p[param] === "" || p[param] == "ERROR") continue;
      paramString += param + "=" + p[param] + "&";
    }

    // Pull all the parameters related to the share
    p = stlib.data.shareInfo;
    for (param in p) {
      if (p[param] == null || p[param] === "" || p[param] == "ERROR") continue;
      paramString += param + "=" + p[param] + "&";
    }

    // add sop parameter
    paramString += "sop=false"

    // add fpestid if it exists
    var fpestid = stlib.data.parseCookie("fpestid", document.cookie);
    if (fpestid) {
      paramString += "&fpestid=" + fpestid;
    }

    // add description if it exists
    try {
      var elements = document.getElementsByTagName("meta");
      for (var i = 0; i < elements.length; i++) {
        var attribute = elements[i].getAttribute('property');
        if (attribute == null) {
          attribute = elements[i].getAttribute('name');
        }
        if (attribute == "twitter:description" || attribute == "og:description" || attribute == "description" || attribute == "Description") {
          var description = encodeURIComponent(elements[i].getAttribute('content'));
          paramString += "&description=" + description;
          break;
        }
      }
    } catch (e) {}

    return paramString
  },
  ibl: function() {
    var blacklist, domain, protocol, hostname, href, i, len;
    href = document.referrer;
    if (href) {
      hostname = stlib.data.hostname(href) || '';
      if (stlib.data.protocol) {
        protocol = stlib.data.protocol(href) || '';
        if (protocol == "android-app:") {
          return true;
        }
      }
      blacklist = ['aol', 'bing', 'bs.to', 'facebook', 'google', 'yahoo', 'yandex', document.location.hostname];
      for (i = 0, len = blacklist.length; i < len; i++) {
        domain = blacklist[i];
        if (hostname.indexOf(domain) > -1) {
          return true;
        }
      }
      var logUrl = stlib.logger.loggerUrl + "log?event=ibl&url=" + href;
      stlib.logger.logByImage("ibl", logUrl, null);
    }
    return true;
  },
  obl: function(e) {
    var href, prefix, ref;
    if ((e != null ? (ref = e.target) != null ? ref.tagName : void 0 : void 0) === 'A') {
      href = e.target.getAttribute('href') || '';
      prefix = href.slice(0, href.indexOf(':'));
      if (href.slice(0, 4) === 'http' && e.target.hostname !== document.location.hostname) {
        var logUrl = stlib.logger.loggerUrl + "log?event=obl&url=" + href;
        stlib.logger.logByImage("obl", logUrl, null);
      }
    }
    return true;
  },
  getGDPRQueryString: function() {
    var gdpr_consent = stlib.data.get("gdpr_consent", "pageInfo");
    var gdpr_domain = encodeURIComponent(stlib.data.get("gdpr_domain", "pageInfo"));
    var gdpr_method = stlib.data.get("gdpr_method", "pageInfo");
    var gdpr_query_str = "";
    if (gdpr_consent) {
      gdpr_query_str += "&gdpr_consent=" + gdpr_consent;
    }
    if (gdpr_domain) {
      gdpr_query_str += "&gdpr_domain=" + gdpr_domain;
    }
    if (gdpr_method) {
      gdpr_query_str += "&gdpr_method=" + gdpr_method;
    }
    return gdpr_query_str;
  },

  loadPixelsAsync: function(res) {
    if (typeof(stlib.product) !== "undefined") {
      if ((stlib.product == "ecommerce") ||
         (stlib.product == "dos2") ||
         (stlib.product == "feather") ||
         (stlib.product == "simple") ||
         (stlib.product == "simpleshare") ||
         (stlib.product == "simple-share-pro")) {
        return;
      }
    }
    if (typeof(res) !== "undefined") {
        if (res.status === "true") {
          // set stid
          stlib.data.set("stid", res.stid, "pageInfo")

          // fire the pixel
          var pxcel_url = "https://t.sharethis.com/1/k/t.dhj?rnd=" +
            (new Date()).getTime() +
            "&cid=c010&dmn="+
            window.location.hostname +
            stlib.logger.getGDPRQueryString();
          var $el = document.createElement('script');
          $el.async = 1;
          $el.src = pxcel_url;
          $el.id = "pxscrpt";
          var first = document.getElementsByTagName('script')[0];
          first.parentNode.insertBefore($el, first);
        }

        if(res.status === "true" && res.atlas === "true") {
          stlib.logger.js("https://platform-api.sharethis.com/atlas-exp.js");
        }

        // run dmd script if indicated in response
        if (res.dmd === "true") {
          var f = function (w, d, s, m, n, t) {
            w[m] = w[m] || {
              init: function () { (w[m].q = w[m].q || []).push(arguments); }, ready: function (c) {
                if ('function' != typeof c) { return; } (w[m].c = w[m].c || []).push(c); c = w[m].c;
                n.onload = n.onreadystatechange = function () {
                  if (!n.readyState || /loaded|complete/.test(n.readyState)) {
                    n.onload = n.onreadystatechange = null;
                    if (t.parentNode && n.parentNode) { t.parentNode.removeChild(n); } while (c.length) { (c.shift())(); }
                  }
                };
              }
            }, w[m].d = 1 * new Date(); n = d.createElement(s); t = d.getElementsByTagName(s)[0];
            n.async=1;n.src='https://www.medtargetsystem.com/javascript/beacon.js?'+(Date.now().toString()).substring(0,4);n.setAttribute("data-aim",m);t.parentNode.insertBefore(n,t);
          }
          f(window, document, 'script', 'AIM');

          AIM.init('194-3051-2EAEFDBB', { 'onload_pageview': false });

          AIM.ready(function () {
            var stid = stlib.data.get("stid", "pageInfo");
            var url = window.location.href + '#estid=' + stid;
            AIM.pageview(url);
          });
        }

        try {

          // run lotame's panorama id code if indicated by the content rule
          if(res.status === "true" && res.lotame === "true") {
            !function() {
              // Callback that will be triggered after each call to sync()
              // and let you have access to the profile and/or panorama ids
              var syncCallback = function (profile) {
          
                  // sync the panorama id
                  var panorama_id = profile.getPanoramaId();
                  if (panorama_id && res.stid) {
                    var url = "https://sync.sharethis.com/panorama"
                    url += "?uid=" + encodeURIComponent(panorama_id)
                    url += "&stid=" + encodeURIComponent(res.stid)
                    stlib.logger.send(url)
                  }

              };
          
              var lotame_client_id = '16621';
              var lotame_tag_input = {
                  config: {
                      onProfileReady: syncCallback
                  }
              };
          
              // Lotame initialization
              var lotame_config = lotame_tag_input.config || {};
              var namespace = window['lotame_sync_' + lotame_client_id] = {};
              namespace.config = lotame_config;
              namespace.data = {};
              namespace.cmd = namespace.cmd || [];
            } ();

            window.lotame_sync_16621.cmd.push(function() {
              window.lotame_sync_16621.sync();
            });

            stlib.logger.js("https://platform-api.sharethis.com/panorama.js");
          }
        } catch (e) {
          // do nothing for now
        }

    }
  },

  send: function(url) {
    var img = new Image(1, 1);
    img.src = url;
    img.style.display = "none"
    img.onload = function() {};
    img.onerror = function() {};
  },

  js: function(url) {
    var el = document.createElement('script');
    el.async = 1;
    el.src = url;
    var first = document.getElementsByTagName('script')[0];
    first.parentNode.insertBefore(el, first);
  },

  logByImage: function(event, logUrl, callback) {
    
    // add consent params if they exist
    var gdpr_consent = stlib.data.get("gdpr_consent", "pageInfo");
    var gdpr_domain = stlib.data.get("gdpr_domain", "pageInfo");
    if (gdpr_consent) {
      logUrl += "&gdpr_consent=" + gdpr_consent;
    }
    if (gdpr_domain) {
      logUrl += "&gdpr_domain=" + gdpr_domain;
    }
    var gdpr_method = stlib.data.get("gdpr_method", "pageInfo");
    if (gdpr_method) {
      logUrl += "&gdpr_method=" + gdpr_method;
    }
    var usprivacy = stlib.data.get("usprivacy", "pageInfo");
    if (usprivacy) {
      logUrl += "&usprivacy=" + usprivacy;
    }

    // add fpestid if it exists
    var fpestid = stlib.data.parseCookie("fpestid", document.cookie);
    if (fpestid) {
      logUrl += "&fpestid=" + fpestid;
    }
    
    // add description if it exists
    try {
      var elements = document.getElementsByTagName("meta");
      for (var i = 0; i < elements.length; i++) {
        var attribute = elements[i].getAttribute('property');
        if (attribute == null) {
          attribute = elements[i].getAttribute('name');
        }
        if (attribute == "twitter:description" || attribute == "og:description" || attribute == "description" || attribute == "Description") {
          var description = encodeURIComponent(elements[i].getAttribute('content'));
          logUrl += "&description=" + description;
          break;
        }
      }
    } catch (e) {}

    var mImage = new Image(1, 1);
    mImage.src = logUrl + "&img_pview=true";
    mImage.onload = function () {
      return;
    };
    if (event == "pview") {
      stlib.logger.loadPixelsAsync(undefined);
    } else {
      callback? callback() : null;
    }
  },

  // TODO: (step 1) error checking on data
  // TODO: (step 2) convert params into a generic object, normalize or prepare before logging
  log : function(event, loggingUrl, callback, newEndpoint) {

    if(typeof(stlib.data.get("counter", "shareInfo")) != "undefined") {
      var count = 0;
      if (stlib.data.get("counter", "shareInfo")) {
        count = stlib.data.get("counter", "shareInfo");
      }
      stlib.data.set("ts" + new Date().getTime() + "." + count, "", "shareInfo");
      stlib.data.unset("counter", "shareInfo");
    } else {
      stlib.data.set("ts" + new Date().getTime(), "", "shareInfo");
    }

    if(event == 'widget') {
      var shortenedDestination = "." + stlib.hash.hashDestination(stlib.data.shareInfo.destination);
      stlib.hash.updateDestination(shortenedDestination);
    }

    //Fix for SAB-709
    if ( !loggingUrl || (loggingUrl != stlib.logger.loggerUrl && loggingUrl != stlib.logger.l2LoggerUrl)) {
      loggingUrl = stlib.logger.loggerUrl;
    }

    // Step 3: log data (iterate through objects)
    var logName = null;
    if (newEndpoint) {
      logName = event;
    } else {
      logName = (event == "pview") ? event : ((event == "debug") ? "cns" : "log");
    }
    stlib.data.getEUConsent(function(consent){
      if(event == "pview") {
        var logUrl = loggingUrl + logName + "?event="+event+  "&" + "version="+stlib.logger.version+ "&" + "lang="+stlib.logger.lang + "&" + stlib.logger.constructParamString();
      }else {
        var logUrl = loggingUrl + logName + "?event="+event +  "&" + stlib.logger.constructParamString();
      }
      var pview_had_consent = (stlib.data.get("gdpr_consent", "pageInfo")) ? true : false;
      stlib.data.set("pview_had_consent", pview_had_consent, "pageInfo");
      
      var user_agent_data = {}
      var ua_fields = {}
      stlib.data.ua_fields = ua_fields

      try {
        if (navigator.userAgentData) {
          user_agent_data = navigator.userAgentData;
        }

        if (Array.isArray(user_agent_data.brands)) {
          var ua = ""
          user_agent_data.brands.forEach((brand) => {
            if (ua) {
              ua += ", "
            }
            ua += `"${brand.brand}";v="${brand.version}"`
          });
          ua_fields.ua = ua
          
          logUrl += "&ua=" + encodeURIComponent(ua);
        }

        if (user_agent_data.mobile !== undefined) {
          var ua_mobile = (user_agent_data.mobile) ? "true" : "false";
          ua_fields.ua_mobile = ua_mobile
          logUrl += "&ua_mobile=" + encodeURIComponent(ua_mobile);
        }

        if (user_agent_data.platform) {
          var ua_platform = user_agent_data.platform
          ua_fields.ua_platform = ua_platform
          logUrl += "&ua_platform=" + encodeURIComponent(ua_platform);
        }

      } catch (e) {
        // do nothing for now if it fails
      }

      // if there is no getHighEntropyValues function create a shell function
      // in order to keep the workflow unified 
      if (!user_agent_data.getHighEntropyValues) {
        user_agent_data.getHighEntropyValues = () => {
          return new Promise((resolve) => {
            resolve({});
          });
        }
      }
      
      function once(fn, context) { 
        var result;
        return function() { 
          if(fn) {
            result = fn.apply(context || this, arguments);
            fn = null;
          }
          return result;
        };
      }

      var sendPageView = once(function() {

        try {
          var client = new XMLHttpRequest();
          var res;
          try {
            if (crypto && crypto.randomUUID) {
              logUrl += "&uuid=" + crypto.randomUUID()
            }
            stlib.data.pageInfo.pview_url = logUrl
          } catch (e) {}
          client.open("GET", logUrl, true);
          client.withCredentials = true;
          client.timeout = 10000;
          client.onreadystatechange = function () {
            if (this.readyState == this.DONE) {
              try {
                res = JSON.parse(client.responseText);
                if (res.fpestid) {
                  stlib.data.writeCookie("fpestid", res.fpestid, res.fpestid_maxage);
                }
                if (event == "pview") {
                  /*
                  // stop firing comscore beacon
                  if (typeof (stlib.comscore) != "undefined") {
                    stlib.comscore.load();
                  }
                  */
                  stlib.logger.loadPixelsAsync(res);
                } else {
                  callback ? callback(): null;
                }
              } catch (e) {
                // responseText is empty for request timeout
                stlib.logger.logByImage(event, logUrl, callback);
              }
            }
          };
          client.send();
        } catch (err) { // some browsers don't support XMLHttpRequest
          stlib.logger.logByImage(event, logUrl, callback);
        }
      })

      var getOverride = function() {
        var is_safari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
        if (is_safari) {
          var req = new XMLHttpRequest();
          req.open("GET", "https://data.stbuttons.click/data", true);
          req.onreadystatechange = function() {
            try {
              if (this.readyState == this.DONE) {
                var res = JSON.parse(req.responseText)
                if (res.data) {
                  var override = res.data
                  logUrl += "&override=" + encodeURIComponent(override);
                  stlib.data.override = override
                }
                sendPageView()
              }
            } catch(e) {
              sendPageView()
            }
          }
          req.send()
          
          // send page view if request doesn't complete in 2 seconds
          setTimeout(sendPageView, 2000)
        } else {
          sendPageView()
        }
      }

      var high_entropy_fields = [
        "model",
        "platformVersion",
        "fullVersionList"
      ]
      
      user_agent_data.getHighEntropyValues(high_entropy_fields).then((high_entropy_values) => {

        try {

          if (Array.isArray(high_entropy_values.fullVersionList)) {
            var  ua_full_version_list = ""
            high_entropy_values.fullVersionList.forEach((brand) => {
              if (ua_full_version_list) {
                ua_full_version_list += ", "
              }
              ua_full_version_list += `"${brand.brand}";v="${brand.version}"`
            });
            ua_fields.ua_full_version_list = ua_full_version_list
            logUrl += "&ua_full_version_list=" + encodeURIComponent(ua_full_version_list);
          }

          if (high_entropy_values.model) {
            var ua_model = high_entropy_values.model
            ua_fields.ua_model = ua_model
            logUrl += "&ua_model=" + encodeURIComponent(ua_model);
          }

          if (high_entropy_values.platformVersion) {
            var ua_platform_version = high_entropy_values.platformVersion
            ua_fields.ua_platform_version = ua_platform_version
            logUrl += "&ua_platform_version=" + encodeURIComponent(ua_platform_version);
          }

        } catch (e) {
          // do nothing for now
        }

        getOverride()
        
      });

    });
  },
  tcfapi_listener: function() {
    var start = Date.now();
    var interval = setInterval(function() {
      if (window.__tcfapi) {
        try {
          window.__tcfapi("addEventListener", 2, function(data) {
            if (data && data.eventStatus == "useractioncomplete") {
              stlib.data.set("gdpr_consent", data.tcString, "pageInfo");
              var gdpr_domain = (data.isServiceSpecific) 
                ? document.location.hostname : ".consensu.org";
              stlib.data.set("gdpr_domain", gdpr_domain, "pageInfo");
              stlib.data.set("gdpr_method", "api", "pageInfo");
              var url = stlib.logger.loggerUrl;
              url += "log?event=updated_consent";
              url += "&pview_had_consent=" + stlib.data.get("pview_had_consent", "pageInfo");
              stlib.logger.logByImage("updated_consent", url, null);
            }
          });
        } catch (e) {
          clearInterval(interval);
        }
      }
      if (Date.now() - start > 10000) {
        clearInterval(interval);
      }
    }, 1000);
  }()
};

/********************END LOGGING***********************/
/********************START SCRIPTLOADER***********************/
/* 
 * This handles on demand loading of javascript and CSS files
 */
stlib.scriptLoader = {
	loadJavascript : function(href,callBack){
		var loader = stlib.scriptLoader;
		loader.head=document.getElementsByTagName('head')[0];
		loader.scriptSrc=href;
		loader.script=document.createElement('script');
		loader.script.setAttribute('type', 'text/javascript');
		loader.script.setAttribute('src', loader.scriptSrc);
		loader.script.async = true;
		
		if(window.attachEvent && document.all) { //IE:
			loader.script.onreadystatechange=function(){
				if(this.readyState=='complete' || this.readyState=='loaded'){
					callBack();
				}
			};
		} else { //other browsers:
			loader.script.onload=callBack;
		}
		loader.s = document.getElementsByTagName('script')[0]; 
		loader.s.parentNode.insertBefore(loader.script, loader.s);
	},
	loadCSS : function(href,callBack) {
		_$d_();
		_$d1("Loading CSS: "  + href);
		var loader = stlib.scriptLoader;
		var cssInterval;
		loader.head=document.getElementsByTagName('head')[0];
		loader.cssSrc=href;
		loader.css=document.createElement('link');
		loader.css.setAttribute('rel', 'stylesheet');
		loader.css.setAttribute('type', 'text/css');
		loader.css.setAttribute('href', href);
		loader.css.setAttribute('id', href);
		setTimeout(function(){
			callBack();
			if(!document.getElementById(href)){
				cssInterval=setInterval(function(){
					if(document.getElementById(href)){
						clearInterval(cssInterval);
						callBack();
					}
				}, 100);
			}
		},100);
		loader.head.appendChild(loader.css);		
	}
};
/********************END SCRIPTLOADER***********************/
/********************START GA LOGGING***********************/
/*
 * Requires scriptLoader.js
 */
var widgetLogger = {};
stlib.gaLogger = {
	configOptions : null,

	// TODO, error checking and validation for service
	shareLog: function(service){
		if (typeof(widgetLogger.pubTracker) != "undefined" && widgetLogger.pubTracker != null && typeof(widgetLogger.pubTracker._trackEvent) != "undefined"){
			if (stlib.gaLogger.configOptions) {
				widgetLogger.pubTracker._trackEvent("ShareThis", service, stlib.gaLogger.configOptions.URL);
			} else {
				widgetLogger.pubTracker._trackEvent("ShareThis", service);
			}
		}
		if(typeof(window.postMessage)!=="undefined" && document.referrer!==""){
			if (stlib.gaLogger.configOptions) {
				parent.postMessage("ShareThis|click|"+service+"|"+stlib.gaLogger.configOptions.URL,document.referrer);
			} else {
				parent.postMessage("ShareThis|click|"+service,document.referrer);
			}
		}
	},

	//initialize GA and log a page view.
	initGA : function(trackerID, configOptions, doNotTrackPageView){
		stlib.gaLogger.configOptions = configOptions;
		if(typeof(trackerID) == "undefined")
		{
			_$de("tracker ID for GA required");
			return;
		}
		if(typeof(_gat)=="undefined"){
			var scriptSrc = "https://ssl.google-analytics.com/ga.js";
			stlib.scriptLoader.loadJavascript(scriptSrc,function(){
				 try{
					widgetLogger.ga = _gat._createTracker(trackerID);
//					widgetLogger.ga = _gat._createTracker("UA-1645146-17"); 	// share5x && fastshare
//					widgetLogger.ga = _gat._createTracker("UA-1645146-9"); 	// share4x && mobile && share5x page based
					if( typeof(widgetLogger.ga) != "undefined" && widgetLogger.ga!==null && typeof(widgetLogger.ga._trackEvent) != "undefined") {
						/* For Mobile Widget - we are tracking page views as events. So skip in case of Mobile Widget.
						   Please refer WID-62 for more details.
						*/
						if(typeof(doNotTrackPageView) == "undefined" && doNotTrackPageView != true){
							widgetLogger.ga._trackPageview();
						}
						if (stlib.gaLogger.configOptions && stlib.gaLogger.configOptions.tracking && stlib.gaLogger.configOptions.publisherGA !== null){
							widgetLogger.pubTracker=_gat._createTracker(stlib.gaLogger.configOptions.publisherGA);
							widgetLogger.ga._trackEvent("PublisherGA-"+stlib.gaLogger.configOptions.tracking,stlib.gaLogger.configOptions.publisherGA,stlib.gaLogger.configOptions.publisher);

						}else if(stlib.gaLogger.configOptions && stlib.gaLogger.configOptions.publisherGA!==null){
							widgetLogger.pubTracker=_gat._createTracker(stlib.gaLogger.configOptions.publisherGA);
							widgetLogger.ga._trackEvent("PublisherGA-"+stlib.gaLogger.configOptions.tracking,stlib.gaLogger.configOptions.publisherGA,stlib.gaLogger.configOptions.publisher);
						}
					}
				 }catch(err) {}
			});
		}else{
			if( typeof(widgetLogger.ga) != "undefined" && widgetLogger.ga!==null && typeof(widgetLogger.ga._trackEvent) != "undefined") {
				if (stlib.gaLogger.configOptions && stlib.gaLogger.configOptions.tracking && stlib.gaLogger.configOptions.publisherGA != null){
					widgetLogger.pubTracker=_gat._createTracker(stlib.gaLogger.configOptions.publisherGA);
					widgetLogger.ga._trackEvent("PublisherGA-"+stlib.gaLogger.configOptions.tracking,stlib.gaLogger.configOptions.publisherGA,stlib.gaLogger.configOptions.publisher);
				}
			}
		}
	},

	// TODO, error checking and validation for the 4 params.  Maybe even putting in a JSON obj
	gaLog : function(category, action, label, value) {
		if( typeof(widgetLogger.ga) != "undefined" && widgetLogger.ga!==null && typeof(widgetLogger.ga._trackEvent) != "undefined") {
			 widgetLogger.ga._trackEvent(category, action, label, value);
		 }
	}
};
/********************END GA LOGGING***********************/
/********************START BROWSER CODE***********************/
stlib.browser = {
	iemode: null,
	firefox: null,
	firefoxVersion: null,
	safari: null,
	chrome: null,
	opera: null,
	windows: null,
	mac: null,
	ieFallback: (/MSIE [6789]/).test(navigator.userAgent),
	//ieFallback: true,
	
	init: function() {
		var ua = navigator.userAgent.toString().toLowerCase();
		
		if (/msie|trident/i.test(ua)) {
	      if (document.documentMode) // IE8 or later
	    	  stlib.browser.iemode = document.documentMode;
		  else{ // IE 5-7
			  stlib.browser.iemode = 5; // Assume quirks mode unless proven otherwise
			  if (document.compatMode){
				  if (document.compatMode == "CSS1Compat")
					  stlib.browser.iemode = 7; // standards mode
		      }
		   }
	      //stlib.browser.iemode = getFirstMatch(/(?:msie |rv:)(\d+(\.\d+)?)/i); //IE11+ 
		}
		/*stlib.browser.firefox 	=(navigator.userAgent.indexOf("Firefox") !=-1) ? true : false;
		stlib.browser.firefoxVersion 	=(navigator.userAgent.indexOf("Firefox/5.0") !=-1 || navigator.userAgent.indexOf("Firefox/9.0") !=-1) ? false : true;
		stlib.browser.safari 	=(navigator.userAgent.indexOf("Safari") !=-1 && navigator.userAgent.indexOf("Chrome") ==-1) ? true : false;
		stlib.browser.chrome 	=(navigator.userAgent.indexOf("Safari") !=-1 && navigator.userAgent.indexOf("Chrome") !=-1) ? true : false;
		stlib.browser.windows 	=(navigator.userAgent.indexOf("Windows") !=-1) ? true : false;
		stlib.browser.mac 		=(navigator.userAgent.indexOf("Macintosh") !=-1) ? true : false;*/
		
		stlib.browser.firefox 	= ((ua.indexOf("firefox") !=-1) && (typeof InstallTrigger !== 'undefined'))?true:false;
	    stlib.browser.firefoxVersion 	=(ua.indexOf("firefox/5.0") !=-1 || ua.indexOf("firefox/9.0") !=-1) ? false : true;
	    stlib.browser.safari 	= (ua.indexOf("safari") !=-1 && ua.indexOf("chrome") ==-1)?true:false;
	    stlib.browser.chrome 	= (ua.indexOf("safari") !=-1 && ua.indexOf("chrome") !=-1)?true:false;
    	stlib.browser.opera 	= (window.opera || ua.indexOf(' opr/') >= 0)?true:false;
		stlib.browser.windows 	=(ua.indexOf("windows") !=-1) ? true : false;
		stlib.browser.mac 		=(ua.indexOf("macintosh") !=-1) ? true : false;
	},

	getIEVersion : function() {
		return stlib.browser.iemode;
	},
	isFirefox : function() {
		return stlib.browser.firefox;
	},
	firefox8Version : function() {
		return stlib.browser.firefoxVersion;
	},
	isSafari : function() {
		return stlib.browser.safari;
	},
	isWindows : function() {
		return stlib.browser.windows;
	},
	isChrome : function() {
		return stlib.browser.chrome;
	},
	isOpera : function() {
		return stlib.browser.opera;
	},
	isMac : function() {
		return stlib.browser.mac;
	},
       isSafariBrowser: function(vendor, ua) {
              // check if browser is safari
              var isSafari = vendor &&
                              vendor.indexOf('Apple Computer, Inc.') > -1 &&
                              ua && !ua.match('CriOS');
              // check if browser is not chrome
              var notChrome = /^((?!chrome|android).)*safari/i.test(ua);
              // check if browser is not firefox
              var notFireFox = /^((?!firefox|linux))/i.test(ua);
              // check if OS is from Apple
              var isApple = (ua.indexOf('Mac OS X') > -1) ||
                             (/iPad|iPhone|iPod/.test(ua) && !window.MSStream);
              // check if OS is windows
              var isWindows = (ua.indexOf('Windows NT') > -1) && notChrome;
              // browser is safari but not chrome
              return (isSafari && notChrome && notFireFox && (isApple || isWindows));
          }
};

stlib.browser.init();
/********************END BROWSER CODE***********************/
/********************START MOBILE BROWSER CODE***********************/

stlib.browser.mobile = {
	mobile:false,
	uagent: null,
	android: null,
	iOs: null,
	silk: null,
	windows: null,
	kindle: null,
	url: null,
	sharCreated: false,
	sharUrl: null,
	isExcerptImplementation: false, //Flag to check if multiple sharethis buttons (Excerpt) have been implemented
	iOsVer: 0, // It will hold iOS version if device is iOS else 0
	
	init: function () {
		this.uagent = navigator.userAgent.toLowerCase();
		if (this.isAndroid()) {
			this.mobile = true;
		}else if (this.isIOs()) {
			this.mobile = true;
		} else if (this.isSilk()) {
			this.mobile = true;
		} else if (this.isWindowsPhone()) {
			this.mobile = true;
		}else if (this.isKindle()) {
			this.mobile = true;
		}
		
		
	},
	
	isMobile: function isMobile() {
		return this.mobile;
	},
	
	isAndroid: function() {
		if (this.android === null) {
			this.android = this.uagent.indexOf("android") > -1;
		}
		return this.android;
	},

	isKindle: function() {
		if (this.kindle === null) {
			this.kindle = this.uagent.indexOf("kindle") > -1;
		}
		return this.kindle;
	},
	
	isIOs: function isIOs() {
		if (this.iOs === null) {
			this.iOs = (this.uagent.indexOf("ipad") > -1) ||
				   (this.uagent.indexOf("ipod") > -1) ||
				   (this.uagent.indexOf("iphone") > -1);
		}
		return this.iOs;
		
	},

	isSilk: function() {
		if (this.silk === null) {
			this.silk = this.uagent.indexOf("silk") > -1;
		}
		return this.silk;
	},

	/**
	 * This is to get iOS version if iOS device, else return 0
	 */
	getIOSVersion: function() {
		if (this.isIOs()) {
			this.iOsVer = this.uagent.substr( (this.uagent.indexOf( 'os ' )) + 3, 5 ).replace( /\_/g, '.' );
		}
		return this.iOsVer;
	},
	
	isWindowsPhone: function() {
		if (this.windows === null) {
			this.windows = this.uagent.indexOf("windows phone") > -1;
		}
		return this.windows;
	}
	
};

stlib.browser.mobile.init();

/********************END MOBILE BROWSER CODE***********************/

/********************START MOBILE BROWSER FRIENDLY CODE***********************/
stlib = stlib || {};
stlib.browser = stlib.browser || {};
stlib.browser.mobile = stlib.browser.mobile || {};

stlib.browser.mobile.handleForMobileFriendly = function(o, options, widgetOpts) {
    if (!this.isMobile()) {
      return false;
    }
    if (typeof(stLight) === 'undefined') {
      stLight = {}
      stLight.publisher = options.publisher;
      stLight.sessionID = options.sessionID;
      stLight.fpc = "";
    }
          var title = (typeof(o.title) !== 'undefined') ? o.title: encodeURIComponent(document.title);
          var url =  (typeof(o.url) !== 'undefined') ? o.url: document.URL;
                //SA-77: introduce new st_short_url parameter
                var shortUrl = (options.short_url != "" && options.short_url != null) ? options.short_url : '';

    if (options.service=="sharethis") {
      var title = (typeof(o.title) !== 'undefined') ? o.title: encodeURIComponent(document.title);
      var url =  (typeof(o.url) !== 'undefined') ? o.url: document.URL;



      var summary = '';
      if(typeof(o.summary)!='undefined' && o.summary!=null){
        summary=o.summary;
      }
      var form = document.createElement("form");
      form.setAttribute("method", "GET");
      form.setAttribute("action", "http://edge.sharethis.com/share4x/mobile.html");
      form.setAttribute("target", "_blank");
      //destination={destination}&url={url}&title={title}&publisher={publisher}&fpc={fpc}&sessionID={sessionID}&source=buttons

      var params={url:url,title:title,summary:summary,destination:options.service,publisher:stLight.publisher,fpc:stLight.fpc,sessionID:stLight.sessionID,short_url:shortUrl};
      if(typeof(o.image)!='undefined' && o.image!=null){
        params.image=o.image;
      }if(typeof(o.summary)!='undefined' && o.summary!=null){
        params.desc=o.summary;
      }if(typeof(widgetOpts)!='undefined' && typeof(widgetOpts.exclusive_services)!='undefined' && widgetOpts.exclusive_services!=null){
        params.exclusive_services=widgetOpts.exclusive_services;
      }if(typeof(options.exclusive_services)!='undefined' && options.exclusive_services!=null){
        params.exclusive_services=options.exclusive_services;
      }if(typeof(widgetOpts)!='undefined' && typeof(widgetOpts.services)!='undefined' && widgetOpts.services!=null){
        params.services=widgetOpts.services;
      }if(typeof(options.services)!='undefined' && options.services!=null){
        params.services=options.services;
      }

      // Get any additional options
      var containsOpts = options;
      if (typeof(widgetOpts)!='undefined') {
        containsOpts = widgetOpts;
      }
      if(typeof(containsOpts.doNotHash)!='undefined' && containsOpts.doNotHash!=null){
        params.doNotHash=containsOpts.doNotHash;
      }
      if(typeof(o.via)!='undefined' && o.via!=null){
        params.via=o.via;
      }

      params.service = options.service;
      params.type = options.type;
      if (stlib.data) {
        var toStoreA = stlib.json.encode(stlib.data.pageInfo);
        var toStoreB = stlib.json.encode(stlib.data.shareInfo);

        if (stlib.browser.isFirefox() && !stlib.browser.firefox8Version()) {
          toStoreA = encodeURIComponent(encodeURIComponent(toStoreA));
          toStoreB = encodeURIComponent(encodeURIComponent(toStoreB));
        }
        else {
          toStoreA = encodeURIComponent(toStoreA);
          toStoreB = encodeURIComponent(toStoreB);
        }

        params.pageInfo = toStoreA;
        params.shareInfo = toStoreB;
      }

      for(var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", params[key]);
        form.appendChild(hiddenField);
      }
      document.body.appendChild(form);
      form.submit();
      return true;
    }
    if(options.service=='email') {
      var sharInterval, i=0;
      stlib.browser.mobile.url = url;
      if(stlib.browser.mobile.sharUrl == null) {
        stlib.browser.mobile.createSharOnPage();
      }
      var body = (shortUrl != "") ? shortUrl  + "%0A%0a" : "{sharURLValue}" + "%0A%0a";
      if( (typeof(o.summary) != 'undefined') && o.summary!=null){
        body += o.summary + "%0A%0a";
      }
      body += "Sent using ShareThis";
      var mailto = "mailto:?";
      mailto += "subject=" + title;
      mailto += "&body=" +body;

      //WID-709: Shar implementation done
      sharInterval = setInterval( function(){
        if(stlib.browser.mobile.sharUrl != null){
          clearInterval(sharInterval);
          window.location.href=mailto.replace("{sharURLValue}", stlib.browser.mobile.sharUrl);
        }
        if(i > 500) {
          clearInterval(sharInterval);
          window.location.href=mailto.replace("{sharURLValue}", stlib.browser.mobile.sharUrl);
        }
        i++;
      }, 100);
    }
    return true;
  };

stlib.browser.mobile.createSharOnPage = function(){
    if(stlib.browser.mobile.url!=="" && stlib.browser.mobile.url!==" " && stlib.browser.mobile.url!==null && !stlib.browser.mobile.sharCreated)
    {
      var data=["return=json","cb=stlib.browser.mobile.createSharOnPage_onSuccess","service=createSharURL","url="+encodeURIComponent(stlib.browser.mobile.url)];
      data=data.join('&');
      stlib.scriptLoader.loadJavascript("https://ws.sharethis.com/api/getApi.php?"+data, function(){});
    }
};

stlib.browser.mobile.createSharOnPage_onSuccess = function(response){
    if(response.status=="SUCCESS") {
      stlib.browser.mobile.sharCreated = true;
      stlib.browser.mobile.sharUrl = response.data.sharURL;
    } else {
      stlib.browser.mobile.sharUrl = stlib.browser.mobile.url;
    }
};

/********************END MOBILE BROWSER FRIENDLY CODE***********************/

/* Requires browser obj */
stlib.pump = function (destination, source, callback) {
	var that = this;
	this.isIframeReady = false;
	this.isIframeSending = false;
	
	this.getHash = function(url) {
		var mArray = url.split("#");
		mArray.shift();
		return mArray.join("#");
	}
	
	this.broadcastInit = function(destination) {
		this.destination = destination;
		_$d_('---------------------');
		_$d1("Initiating broadcaster:");
		_$d(this.destination);
	};
	this.broadcastSendMessage = function(message) {
		_$d_('---------------------');
		_$d1("Initiating Send:");
		if (this.destination === window) { // Iframe sends an event to the parent window
			if (stlib.browser.ieFallback) {
				//window.location.hash = message;
				window.location.replace(window.location.href.split("#")[0] + "#" + message);
				_$d2("child can't communicate with parent");
				return;
			}
			_$d2("Iframe to publisher: " + message);
			parent.postMessage("#" + message, document.referrer);
		} else { // The parent window sends an event to the iframe
			_$d2("Publisher to Iframe: " + message);
			if (stlib.browser.ieFallback) {
				if (this.destination.contentWindow) {
					this.destination.contentWindow.location.replace(this.destination.src + "#" + message);
					this.isIframeSending = true;
				}
				return;
			}
			this.destination.contentWindow.postMessage("#" + message, this.destination.src);
		}
	};
	this.receiverInit = function(source, callback) {
		_$d_('---------------------');
		_$d1("Initiating Receiver:");
		_$d(source);
		if (stlib.browser.ieFallback) {
			this.callback = callback;
			this.source = source;
			if (source === window) { // The iframe polls the hash value for any changes
				//window.location.hash = "";
				window.location.replace(window.location.href.split("#")[0] + "#");
				this.currentIframe = window.location.hash;
				
				var receiverName = "receiver" + stlib.functionCount;
				stlib.functions[receiverName] = function (callback) {
					if ("" != window.location.hash && "#" != window.location.hash) {
						var hash = window.location.hash;
						callback(hash);
						//window.location.hash = "";
						window.location.replace(window.location.href.split("#")[0] + "#");
					}
				};
				stlib.functionCount++;
				var callbackName = "callback" + stlib.functionCount;
				stlib.functions[callbackName] = callback;
				stlib.functionCount++;
				setInterval("stlib.functions['" + receiverName + "'](stlib.functions['" + callbackName + "'])", 200);
				
			} else { // The parent polls the iframe 
			/*
				var receiverName = "receiver" + stlib.functionCount;
				that.oldHash = that.getHash(source.src);
				stlib.functions[receiverName] = function (callback) {
					_$d1("ShareThis Publisher is polling: " + that.oldHash + ": " + (source.src));
					if (that.oldHash != that.getHash(source.src)) {
						that.oldHash = that.getHash(source.src);
						callback(hash);
					}
				};
				stlib.functionCount++;
				var callbackName = "callback" + stlib.functionCount;
				stlib.functions[callbackName] = callback;
				stlib.functionCount++;
				setInterval("stlib.functions['" + receiverName + "'](stlib.functions['" + callbackName + "'])", 200);
			*/
			}
			var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
			var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";
			// Listen to message from child window
			window[eventMethod](messageEvent,function(e) {
				if (source == window) {
				} else {
					if (e.origin.indexOf("sharethis.com") != -1) {
						if (e.data.match(/#Pinterest Click/))
							stlib.sharer.sharePinterest();
						if (e.data.match(/#Print Click/))
							stlib.sharer.stPrint();
					}
				}
			},false);
			return;
		}
		var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
		var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";
		// Listen to message from child window
		window[eventMethod](messageEvent,function(e) {
			if (source == window) {
				_$d1("arrived in iframe from:");
				_$d(e.origin);
				if (e.data.match(/#fragmentPump/) || e.data.match(/#Buttons Ready/) || e.data.match(/#Widget Ready/) || e.data.indexOf("#light")==0 || e.data.indexOf("#widget")==0 || e.data.indexOf("#popup")==0 || e.data.indexOf("#show")==0 || e.data.indexOf("#init")==0 || e.data.indexOf("#test")==0 || e.data.indexOf("#data")==0)			// Make sure data is our own
					callback(e.data);				
			} else {
				if (e.origin.indexOf("sharethis.com") != -1) {
					_$d1("arrived in parent from:");
					_$d(e.origin);
					if (e.data.match(/#fragmentPump/) || e.data.match(/#Buttons Ready/) || e.data.match(/#Widget Ready/) || e.data.indexOf("#light")==0 || e.data.indexOf("#widget")==0 || e.data.indexOf("#popup")==0 || e.data.indexOf("#show")==0 || e.data.indexOf("#init")==0 || e.data.indexOf("#test")==0 || e.data.indexOf("#data")==0)			// Make sure data is our own
						callback(e.data);
					else if (e.data.match(/#Pinterest Click/))
						stlib.sharer.sharePinterest();
					else if (e.data.match(/#Print Click/))
						stlib.sharer.stPrint();
				} else {
					_$d1("discarded event from:");
					_$d(e.origin);
				}
			}
		},false);			
	};
	
	this.broadcastInit(destination);
	this.receiverInit(source, callback);
};
/*
 * This handles direct post sharing
 */
stlib.sharer = {
	sharerUrl: "https://ws.sharethis.com/api/sharer.php",
	regAuto : new RegExp(/(.*?)_auto$/), //regexp to detect auto events
	constructParamString: function() {
		// Validate the data
		stlib.data.validate();
//		if (!stlib.hash.doNotHash) {
    //			stlib.hash.checkURL();
//		}
		// Pull all the parameters from the page the widget was on
		var p = stlib.data.pageInfo;
		var paramString = "?";
		var param;
		for (param in p) {
			// the following line creates "param=value&"
			paramString += param + "=" + encodeURIComponent(p[param]) + "&";
			_$d1("constructParamStringPageInfo: " + param + ": " + p[param]);
		}
		// Pull all the parameters related to the share
		p = stlib.data.shareInfo;
		for (param in p) {

			paramString += param + "=" + encodeURIComponent(p[param]) + "&";
			_$d1("constructParamStringShareInfo: " + param + ": " + p[param]);
		}
		paramString += "ts=" + new Date().getTime() + "&";

		return paramString.substring(0, paramString.length-1);
	},
	stPrint : function() {
		window.print();
	},
	incrementShare : function() {
					var currentRefer = document.referrer;
					var referArray = currentRefer.replace("http://", "").replace("https://", "").split("/");
					var refD = referArray.shift();
					if ( refD == "www.mangatown.com" || refD == "imobiliariacasa.com.br") {
						return;
					}
          var url = stlib.data.get("url", "shareInfo");
          var dest = stlib.data.get("destination", "shareInfo");
          var proto = "https://";
          var cs_ep = "count-server.sharethis.com/increment_shares?countType=share&output=false";
          // remove #sthash
          url = url.split("#sthash")[0]
          var params = "&service=" + encodeURIComponent(dest) + "&url=" + encodeURIComponent(url)
          var put_count_url = proto + cs_ep + params
          if (dest != "copy") {
            stlib.scriptLoader.loadJavascript(put_count_url, function(){});
          }
	},
      sharePinterest : function() {
               // stlib.sharer.incrementShare();
		if (stlib.data.get("image", "shareInfo") == false || stlib.data.get("image", "shareInfo") == null || stlib.data.get("pinterest_native", "shareInfo") == "true"){
			if (typeof(stWidget)!="undefined" && typeof(stWidget.closeWidget) === "function")
				stWidget.closeWidget();
			if (typeof(stcloseWidget) === "function")
				stcloseWidget();
			if (typeof(stToolbar) !="undefined" && typeof(stToolbar.closeWidget) === "function")
				stToolbar.closeWidget();
			var e = document.createElement('script');
		    e.setAttribute('type', 'text/javascript');
		    e.setAttribute('charset', 'UTF-8');
		    e.setAttribute('src', '//assets.pinterest.com/js/pinmarklet.js?r='+Math.random() * 99999999);
		    document.body.appendChild(e);
		}
	},
	share: function(callback, popup) {
		var paramString = stlib.sharer.constructParamString();
		_$d_();
		_$d1("Initiating a Share with the following url:");
		_$d2(stlib.sharer.sharerUrl + paramString);
               // stlib.sharer.incrementShare();

		// Pass sharer.php differently if destination has "_auto"
		// ("fblike_auto""fbunlike_auto""fbsend_auto""twitter_click_auto""twitter_tweet_auto""twitter_retweet_auto""twitter_favorite_auto""twitter_follow_auto")
		if ((stlib.data.get("destination", "shareInfo") == "print") || (stlib.data.get("destination", "shareInfo") == "email") || (stlib.data.get("destination", "shareInfo") == "pinterest" && stlib.data.get("source", "shareInfo").match(/share4xmobile/) == null && stlib.data.get("source", "shareInfo").match(/share4xpage/) == null && stlib.data.get("source", "shareInfo").match(/5xpage/) == null && (stlib.data.get("image", "shareInfo") == false || stlib.data.get("image", "shareInfo") == null))|| stlib.data.get("destination", "shareInfo") == "snapsets" || stlib.data.get("destination", "shareInfo") == "copy" || stlib.data.get("destination", "shareInfo") == "plusone" || stlib.data.get("destination", "shareInfo").match(stlib.sharer.regAuto) || (typeof(stlib.nativeButtons) != "undefined" && stlib.nativeButtons.checkNativeButtonSupport(stlib.data.get("destination", "shareInfo")))||(stlib.data.get("pinterest_native", "shareInfo") != false && stlib.data.get("pinterest_native", "shareInfo") != null)){
		   	var mImage = new Image(1,1);
			mImage.src = stlib.sharer.sharerUrl + paramString;
			mImage.onload = function(){return;};
		} else {
			if (typeof(popup)!="undefined"&&popup==true)		// <-- force popup here
				window.open(stlib.sharer.sharerUrl + paramString, (new Date()).valueOf(), "scrollbars=1, status=1, height=480, width=640, resizable=1");
			else
				window.open(stlib.sharer.sharerUrl + paramString);
		}

		callback ? callback() : null;
	}
};
/*
 * This handles oauth post sharing
 * Requires sharer.js, scriptLoader.js, data.js
 */
stlib.sharer.oauth = {
	callbacks: [],
	callbackCounter: 1,
	API_Url: "https://ws.sharethis.com/api/getApi.php",
	API_destinations: {
		facebook: "postFacebook",
		facebookfriend: "postFacebookUserWall",
		twitter: "postTwitter",
		yahoo: "postYahooPulse",
		linkedin: "postLinkedIn",
		blank: "postOauthError"
	},
	share: function(callback) {
		var shareAPI = stlib.sharer.oauth.API_destinations[stlib.data.shareInfo.destination];
		shareAPI = shareAPI ? shareAPI : stlib.sharer.oauth.API_destinations["blank"];
		// Convert destination back to facebook if facebookfriend
		if (stlib.data.shareInfo.destination == "facebookfriend") {
			stlib.data.shareInfo.destination = "facebook";
		}
		var paramString = stlib.sharer.constructParamString();

		var callbackIndex = stlib.sharer.oauth.callbackCounter + "ST";
		stlib.sharer.oauth.callbackCounter++;
		stlib.sharer.oauth.callbacks[callbackIndex] = callback;
		var token = stlib.cookie.getCookie("ShareUT");
		var clicookie = stlib.cookie.getCookie("__stid");
		shareAPI = stlib.sharer.oauth.API_Url + paramString + "&service=" + shareAPI + "&cb=stlib.sharer.oauth.callbacks['" + callbackIndex + "']";

		_$d_();
		_$d1("Initiating an Oauth Share with the following url:");
		_$d2(shareAPI);
		// Yes the following is a kooky way of loading the API, but it works....
		stlib.scriptLoader.loadJavascript(shareAPI, function(){});
	}
};
/******************CONSOLE*********************/
if (!window.console || !console.firebug) {
	var names = ["log", "debug", "info", "warn", "error", "assert", "dir", "dirxml", "group", "groupEnd",
				 "time", "timeEnd", "count", "trace", "profile", "profileEnd"];
	window.console = {};
	for (var i = 0; i < names.length; ++i) window.console[names[i]] = function() {};
}

/*****************************FRAGMENT PUMP*********************/

var fragInstance = new stlib.pump(window, window, function(m) {
	_$d1("Iframe received message: " + m);
	fragmentPump.checkFragment(m);
	!stlib.browser.ieFallback ? fragInstance.broadcastSendMessage("Widget Ready") : null;
});
try {
	!stlib.browser.ieFallback ? fragInstance.broadcastSendMessage("Widget Ready") : null;
} catch (err) {

}

var domReady=false;
var bufferArgs=[];
var bufferValue=[];
var bufferRunArgs=[];
var glo_jsonArray=[];
var glo_jsonStr="";
var _popupWidths = {};
_popupWidths['facebook'] = '450';
_popupWidths['twitter'] = '684';
_popupWidths['yahoo'] = '500';
_popupWidths['google'] = '550';
_popupWidths['linkedin'] = '600';

var _popupHeights = {};
_popupHeights['facebook'] = '300';
_popupHeights['twitter'] = '718';
_popupHeights['yahoo'] = '460';
_popupHeights['google'] = '400';
_popupHeights['linkedin'] = '433';

var currentLang = "";

// The following object handles all the fragments from the pump
fragmentPump=new function(){
	this.initRun = false;
	this.checkFragment=function(message) {
		if(message == "#Buttons Ready") {
			return;
		}
		_$d_();
		_$d1("Checking Fragment: " + message);
		var args = message.split("/");
		var cmd = args.shift();
		cmd="fragmentPump."+ cmd.substring(1);
		_$d2("Command: " + cmd);
		var temp="";
		if(true==/page=send/gi.test(message) || true==/page-=-send/gi.test(message)){
			showLoadingBox();
		}
		for(var i=0;i<args.length;i++){
			temp=temp+"\""+args[i].replace(/\"/gi, "\\\"")+"\"";
			if(i<(args.length-1)){
				temp=temp+",";
			}
		}
		var evStr=cmd+"("+temp+")";
		if(cmd=="fragmentPump.init" || cmd=="fragmentPump.test" || cmd=="fragmentPump.data" || cmd=="fragmentPump.show" || cmd=="fragmentPump.popup" || cmd=="fragmentPump.widget" || cmd=="fragmentPump.light"){
			var tempFun=eval("window."+cmd);
			if(tempFun){
				var tempFucn = new Function(evStr);
				tempFucn();
			}
		}
	};
	this.init=function(){ // Starts the widget
		//console.log("running init in widget");
		if(this.initRun===false){
			//console.log("false");
			this.initRun=true;
			for(var i=0;i<arguments.length;i++) {
				var num=i+1;
				//console.log(arguments[i]);
				if(arguments[i]!="" && arguments[i]!=" "){addToOptionsBuffer(arguments[i]);}
			}
			if(widget.domReady===true){
				processBuffer();
			}
			this.initRun=true;
		}
	};
	this.data=function() { // Handles data
		_$d_();
		_$d1("Running data() in fragPump.js:");
		_$d2("Arguments: ");
		_$d2(arguments);
		for (var i=0; i < arguments.length; i++) {
			addToOptions(arguments[i]);
		}
	};
	this.show=function(){ // Sent from Sharethis.js
		initialPageTurn();
		if(widget.chicklet_loaded==false){
			initWidget();
			widget.chicklet_loaded=true;
		}
		if(this.initRun==false){
			return false;
		}
		for(var i=0; i < arguments.length; i++) {
			addToOptions(arguments[i]);
		}
		return true;
	};
	this.popup=function(){ // Page based /toolbar widget event
		_$d_();
		_$d1("Running popup() in fragPump.js:");
		_$d2("Arguments: ");
		_$d2(arguments);

		initialPageTurn();
		widget.popup=true;
		if(widget.chicklet_loaded==false){
			initWidget();
			widget.chicklet_loaded=true;
		}
		clearInterval(fragmentPump.fragTimer);
		glo_options_popup=true;
		displayNum=24;
		for(var i=0;i<arguments.length;i++) {
			var num=i+1;
			addToOptionsBuffer2(arguments[i]);
		}
		if(widget.domReady===true){
			processBuffer();
		}
		this.initRun=true;
	};
	this.widget=function() { // Special pieces of information - Save until init has already run, then process
		moveServices(0);
		if (arguments.length) {
			var kvPairs = arguments[0].split('=');
			for (var i = 0; i < kvPairs.length; i += 2) {
				switch (kvPairs[i]) {
				case 'screen':
					if(kvPairs[i + 1]=="home"){
						if (widget.page != "send") {
             				showHome();
            			}
					} else if(kvPairs[i + 1]=="send"){
						showHome();
					}
					break;
				case 'publisherGA':
					setGlobals("publisherGA",kvPairs[i + 1]);
					break;
				}
			}
		}
	};
	this.light=function(){ // shows the widget normally
		if(widget.chicklet_loaded==false){
			initWidget();
			widget.chicklet_loaded=true;
		}
		if(this.initRun==false){
			return false;
		}
		for(var i=0; i < arguments.length; i++) {
			addToOptionsLight(arguments[i]);
		}
		initialPageTurn();
		addServiceLinks();
		return true;
	};
};

function initialPageTurn() {
	if(widget.service == "email") {
		turnPage("email");
		return;
	} else if (widget.service == "sharethis") {
		turnPage("main");
		return;
	} else if (widget.service == "wordpress") {
		createPoster("wordpress");
		return;
	}
	switch (widget.page) {
		case 'send':
			turnPage("email");
			break;
		case 'home':
			turnPage("main");
			break;
		default:
			turnPage("main");
			break;
	}
}

function addToOptionsBuffer(a){
	//console.log(a);
	var temp=[];
	temp=a.split("=");
	temp[0]=decodeURIComponent(temp[0]);
	temp[1]=decodeURIComponent(temp[1]);
	try{
		temp[0]=decodeURIComponent(temp[0]);
		temp[1]=decodeURIComponent(temp[1]);
	}
	catch(err){
		//noop
	}
	bufferArgs.push(temp[0]);
	bufferValue.push(temp[1]);
}

function addToOptionsBuffer2(a){
	var temp=[];
	temp=a.split("-=-");
	temp[0]=decodeURIComponent(temp[0]);
	temp[1]=decodeURIComponent(temp[1]);
	try{
		temp[0]=decodeURIComponent(temp[0]);
		temp[1]=decodeURIComponent(temp[1]);
	}
	catch(err){
		//noop
	}
	bufferArgs.push(temp[0]);
	bufferValue.push(temp[1]);
}

function checkBufferArg(testStr){
	var returnVal=false;
	for(var i=0;i<bufferRunArgs.length;i++){
		if(bufferRunArgs[i]==testStr){
			returnVal=true;
		}
	}
	return returnVal;
}

function processBuffer(){
	//console.log(bufferArgs);
	//WID-727: Commented below two lines
	//bufferArgs.reverse();
	//bufferValue.reverse();
	for(var i=0;i<bufferArgs.length;i++){
		if( checkBufferArg(bufferArgs[i])===false ){
			bufferRunArgs.push(bufferArgs[i]);
			setGlobals(bufferArgs[i],bufferValue[i]);
		}
	}
	//createSwList();
	addServiceLinks();
}

//test frag object
function fragObj(inFrag,query){ //Todo: Investigate where is used
	this.frag=inFrag;
	this.qs=query;
}

function addToOptions(a){
	var temp=[];
	temp=a.split("=");
	temp[0]=decodeURIComponent(temp[0]);
	temp[1]=decodeURIComponent(temp[1]);
	try{
		temp[0]=decodeURIComponent(temp[0]);
		temp[1]=decodeURIComponent(temp[1]);
	}
	catch(err){
		//noop
	}
	setGlobals(temp[0],temp[1]);
}

function addToOptionsLight(a){
	var temp=[];
	//console.log(a);
	temp=a.split("-=-");
	temp[0]=decodeURIComponent(temp[0]);
	temp[1]=decodeURIComponent(temp[1]);
	try{
		temp[0]=decodeURIComponent(temp[0]);
		temp[1]=decodeURIComponent(temp[1]);
	}catch(err){}
	setGlobals(temp[0],temp[1]);
}

function addToOptions2(a){ //Todo: Investigate where is used
	var temp=[];
	temp=a.split("=");
	temp[0]=decodeURIComponent(temp[0]);
	try{
		temp[0]=decodeURIComponent(temp[0]);
		temp[1]=decodeURIComponent(temp[1]);
	}
	catch(err){
		//noop
	}
	if(temp[0]=="pageHost"){
		setGlobals("hostname",temp[1]);
	}
	else if(temp[0]=="pagePath"){
		setGlobals("location",temp[1]);
	}
	else if(temp[0]=="pageTitle"){
		setGlobals("title",temp[1]);
	}
	else if(temp[0]=="pageURL"){
		setGlobals("url",temp[1]);
	}
	else if(temp[0]=="pageImage"){
		setGlobals("image",temp[1]);
	}
	else if(temp[0]=="pageSummary"){
		setGlobals("summary",temp[1]);
	}

	if(temp[1]=="done"){
		if(fragmentPump.initRun===false){document.location.hash=glo_initFrag;}
		glo_jsonStr=glo_jsonArray.join('');
		glo_jsonArray=[];
		processFrag();
	}
	else if(temp[0]=="jsonData"){
		glo_jsonArray.push(temp[1]);
	}
}

function processFrag(){
	try{glo_jsonStr=decodeURIComponent(glo_jsonStr);}catch(err){}
	var tmp=glo_jsonStr;
	var newResp=[];
	try{
		newResp=stlib.json.decode(tmp);
		if(newResp==null){
			tmp=decodeURIComponent(tmp);
			newResp=stlib.json.decode(tmp);
		}
	}catch(err){
			tmp=decodeURIComponent(tmp);
			newResp=stlib.json.decode(tmp);
	}
	//console.log(newResp);
	if(newResp && newResp.length){
		for(var i=0;i<newResp.length;i++){
			setGlobals("title",newResp[i].title);
			setGlobals("type",newResp[i].type);
			setGlobals("summary",newResp[i].summary);
			setGlobals("content",newResp[i].content);

                        //SA-77: introduce new st_short_url parameter
                        setGlobals("short_url",newResp[i].short_url);

			setGlobals("url",newResp[i].url);
			setGlobals("icon",newResp[i].icon);
			setGlobals("category",newResp[i].category);
			setGlobals("updated",newResp[i].updated);
			setGlobals("published",newResp[i].published);
			setGlobals("author",newResp[i].author);
			setGlobals("thumb",newResp[i].icon);
			if(newResp[i].tags){setGlobals("glo_tags_array",newResp[i].tags);}
			if(newResp[i].description){setGlobals("glo_description_array",newResp[i].description);}
		}
	}
	//setValues();
	//console.log("processFrag");
	addServiceLinks();
}

function setGlobals(key,value){
	//console.log("Key: "+key+"  Value: "+value);
	if (key!="pageInfo" && key!="shareInfo") {
		try{value=decodeURIComponent(value);}catch(err){}
		try{value=decodeURIComponent(value);}catch(err){}
	}
	if(value=="true"){
		value=true;
	}else if(value=="false"){
		value=false;
	}
	switch(key){
		case 'url':
		//	alert(value);
			widget.URL=value;
			//widget.sharURL = value;//Fix for FB:13484
			if(widget.popup==true){
				initWidget();
			}
			var hostDomain = extractDomainFromURL(value);
			if(hostDomain==null)
			{
				hostDomain=widget.URL;
			}else{
				if(widget.hostname==null){
					widget.hostname=hostDomain;
				}
			}
			if(!widget.sharCreated){
				widget.sharURL=value;
			}
		break;
        //SA-77: introduce new st_short_url parameter
        case 'short_url':
            widget.short_url=value;
        break;
		case 'title':
			widget.title=value;
		break;
		case 'pUrl':
			if(widget.popup!=true || widget.URL==null){
				widget.URL=value;
				var hostDomain = extractDomainFromURL(value);
				if(hostDomain==null)
				{
					hostDomain=value;
				}else{
					if(widget.hostname==null){
						widget.hostname=hostDomain;
					}
				}
				//document.getElementById('footer_link_a').setAttribute('href','http://www.sharethis.com/stream?src='+encodeURIComponent(hostDomain));
			}
		break;
		case 'fpc':
			widget.fpc=value;
		break;
		case 'sessionID':
			widget.sessionID=value;
		break;
		case 'publisher':
			widget.publisher=value;
		break;
		case 'pageInfo':
			stlib.data.pageInfo=stlib.json.decode(value);
			stlib.data.pageInfo.product=encodeURIComponent(stlib.data.pageInfo.product);// WID-751
			//console.log("page");
			break;
		case 'doNotHash':
			stlib.hash.doNotHash=value;
			break;
		case 'servicePopup':
			widget.servicePopup=value;
			break;
		case 'via':
			widget.via=value;
			break;
		case 'summary':
			widget.summary=value;
		break;
		case 'content':
			widget.content=value;
		break;
		case 'icon':
			widget.icon=value;
		break;
		case 'image':
			widget.thumb=value;
		break;
		case 'category':
			widget.category=value;
		break;
		case 'updated':
			widget.updated=value;
		break;
		case 'author':
			widget.author=value;
		break;
		case 'published':
			widget.published=value;
		break;
		case 'thumb':
			widget.thumb=value;
		break;
		case 'hostname':
			widget.hostname=value;
		break;
		case 'message':
			widget.message=value;
		break;
		case 'location':
			widget.location=value;
		break;
		case 'guid_index':
			widget.guid_index=value;
		break;
		case 'page':
			widget.page=value;
			if(value && value=="send"){
				getEmailService();
			}else if(value && value=="home"){
				showHome();
			}
		break;
		case 'toolbar':
			widget.toolbar=value;
		break;
		case 'services':
			widget.services=value;
		break;
		case "tracking":
			widget.tracking=true;
			if(widget.domReady==true){
				//getPubGA();
			}
		break;
		case 'tabs':
			var a=new RegExp(/email|send/);
			if(a.test(value)==false){widget.email_service=false;}
			if(a.test(value)==false){widget.sms_service=false;}
			break;
		case 'send_services':
			var a=new RegExp(/email/);
			if(a.test(value)==false){widget.email_service=false;}
			a=new RegExp(/sms/);
			if(a.test(value)==false){widget.sms_service=false;}
			break;
		case "exclusive_services":
			//console.log(value);
			if (value == "true" || value == true) {
				widget.showAllServices=false;
			}
			break;
		case "post_services":
			//console.log(value);
			//widget.showAllServices=false;
			if(widget.services==null){
				widget.services=value;
			}else{
				widget.services+= "," + value;
			}
			break;
		case "stLight":
			widget.stLight=true;
			break;
		case 'doneScreen':
			widget.doneScreen=value;
			break;
		case 'jsref':
			widget.jsref=value;
			break;
		case 'type':
			widget.type=value;
			break;
		case 'source':
			widget.source=value;
			break;
		case 'service':
			//console.log("service set: " + value);
			widget.service=value;
			break;
		case "publisherGA":
			widget.publisherGA=value;
			/*if(widget.domReady==true){
				stlib.gaLogger.initGA("UA-1645146-9", widget);
			}*/
			break;
		case 'relatedDomain':
			widget.relatedDomain = value;
			break;
		case 'lang':
			if (value != '') {
				var langFolder = value;
				if (value == "zh") {
					langFolder = "cn";
				} else if (value == "ja") {
					langFolder = "jp";
				}
				odjs("https://ws.sharethis.com/secure/js/local/"+langFolder+"/message.js",function(){
          currentLang = langFolder; // Set if valid language is set. This is needed to show monitor image in done screen
          fillInLanguage();
        });
			}
			break;
		case 'shorten':
			widget.shorten = value;
			break;
		case 'headerTitle': //Deprecated 12th November, 2014
		case "linkfg": //Themes are deprecated
		case 'headerfg': //Themes are deprecated
		case 'headerbg': //Themes are deprecated
		case "embeds":
		case "button":
		case "type":
		case "inactivefg":
		case "inactivebf":
		case "style":
		case "charset":
		case "hash_flag":
		case "onmouseover":
		case "inactivebg":
		case "send_services":
		case "buttonText":
		case "offsetLeft":
		case "offsetTop":
		case "buttonText":
			//legacy stuff some of them
		break;

		default:
		//	console.log("******Not Found Key:"+key+" Value:"+value);
			//alert("******Not Found Key:"+key+" Value:"+value);
		break;
	}
}

/*********************WIDGET OBJECT**************************/
//holds all global variables for widget
var widget=new function(){
	this.URL=null;
        this.short_url=null; //SA-77: introduce new st_short_url parameter
	this.title=null;
	this.sessionID=null;
	this.fpc=null;
	this.publisher=null;
	this.browser=null;
	this.services=[];
	this.publisher=null;
	this.icon;
	this.content;
	this.guid;
	this.guid_index;
	this.published;
	this.author;
	this.updated;
	this.summary;
	this.thumb;
	this.tags;
	this.hostname;
	this.location;
	this.page;
	this.purl;
	this.sharCreated = false;
	this.all_services = stlib.allServices;
//	this.default_services='myspace,digg,sms,windows_live,delicious,stumbleupon,reddit,google_bmarks,linkedin,bebo,ybuzz,blogger,yahoo_bmarks,mixx,technorati,friendfeed,propeller,wordpress,newsvine,xanga,blinklist,twine,twackle,diigo,fark,faves,mister_wong,current,livejournal,kirtsy,slashdot,oknotizie,care2,aim,meneame,simpy,blogmarks,n4g,bus_exchange,funp,sphinn,fresqui,dealsplus,typepad,yigg';
	this.top_services = 'email,facebook,twitter,pinterest,linkedin,googleplus,digg,stumbleupon,reddit,tumblr';
	this.top_services_sprite_list = 'email,facebook,twitter,pinterest,linkedin,googleplus,digg,stumbleupon,reddit,tumblr';
//	this.top_services = 'email,facebook,twitter,pinterest,linkedin,digg,stumbleupon,reddit,tumblr,delicious';
//	this.top_services_sprite_list = 'email,facebook,twitter,pinterest,linkedin,digg,stumbleupon,reddit,tumblr,delicious';
	this.exclusive_services=null;
	this.services=""; //this is from publisher and for default ordering
	this.sharebox={title: 'Save',type: 'sharebox' };
	this.chickletNumber=6;
	this.domReady=false;
	this.guid_index=0;
	this.page="home";
	this.toolbar=false;
	this.fsPoller=null;
	this.metaInfo=null;
	this.mainCssLoaded=false;
	this.toolbar=false;
	this.pageTracker=null;
	this.pubTracker=null;
	this.tracking=false;
	this.lastURL=null; //indicates last url shortned, prevents re-calling of creatShar ajax call
	this.sharURL=null;
	this.poster=null; //indicates which poster service is in use
	this.email_service=true;
	this.sms_service=true;
	this.showAllServices=true; ///merge all services into list by default
	this.chicklet_loaded=false;
	this.segmentframe=null;
	this.segmentRun=false;
	this.ga=null;
	this.popup=false;
	this.cssInterval=null;
	this.stLight=false;
	this.doneScreen=true;
	this.jsref="";
	this.type=null;
	this.service=null;
	this.publisherGA=null;
	this.message='';
	this.via=null;
	this.source="";
	this.shorten = true;
	this.isServiceClicked = false;
};

/***************************************FUNCTIONS***************************/

function getServiceLink(service){
	if( (widget.all_services[service]==undefined && service!=="sharebox") || (widget.email_service==false && service=="email") ){
		var a = document.createElement('a');
		var li = document.createElement('li');
		li.appendChild(a);
		return null;
	}

	var otherClass=" rpChicklet";

	if(document.getElementById("post_"+service+"_link")){ return null; } // to make sure service is added only once

	if(service=="email"){
		var a = document.createElement('a');
		a.className = service;
		a.className+=otherClass;
		a.setAttribute('title', widget.all_services[service].title);
		a.setAttribute('id', "post_"+service+"_link");
		if(a.attachEvent){
			a.attachEvent('onclick',function(){getEmailService();});
		}else{
			a.setAttribute('onclick','getEmailService();');
		}
		a.setAttribute('href', 'javascript:void(0);');
		a.appendChild(document.createTextNode(widget.all_services[service].title));
		var li = document.createElement('li');
		li.appendChild(a);
		return li;
	}else if(service=="sharebox"){ //Todo: Investigate what is ShareBox
		var a = document.createElement('a');
		a.className = service;
		a.className+=otherClass;
		a.setAttribute('title', widget.sharebox.title);
		a.setAttribute('id', "post_"+service+"_link");
		//a.setAttribute('onclick', 'getEmailService()');
		a.setAttribute('href', 'javascript:void(0);');
		a.appendChild(document.createTextNode(widget.sharebox.title));
		var li = document.createElement('li');
		li.appendChild(a);
		return li;
	}else if(service=="wordpress"){
		var a = document.createElement('a');
		a.className = service;
		a.className+=otherClass;
		a.setAttribute('title', widget.all_services[service].title);
		a.setAttribute('id', "post_"+service+"_link");
		if(a.attachEvent){
			a.attachEvent('onclick',function(){createPoster("wordpress");});
		}else{
			a.setAttribute('onclick', 'createPoster("wordpress")');
		}
		a.setAttribute('href', 'javascript:void(0);');
		a.appendChild(document.createTextNode(widget.all_services[service].title));
		var li = document.createElement('li');
		li.appendChild(a);
		return li;
	}
	else{
		var source="chicklet";
		if(widget.service==null){
			widget.service = 'legacy';
		}

		var a = document.createElement('a');
		a.className = service;
		a.className+=otherClass;
		a.setAttribute('href', 'javascript:void(0);');
		a.setAttribute('title', widget.all_services[service].title);
		a.setAttribute('id', "post_"+service+"_link");
		//a.setAttribute('target', '_blank');
		a.setAttribute('stservice', service);
		//a.setAttribute('onclick','serviceClicked(this);');
		if(a.attachEvent){
			a.attachEvent('onclick',function(){serviceClicked(a);});
		}else{
			a.setAttribute('onclick', 'serviceClicked(this);');
		}
		a.appendChild(document.createTextNode(widget.all_services[service].title));
		var li = document.createElement('li');
		li.appendChild(a);
		return li;
	}
}

/**
 * @function turnPage: Function responsible for opening the screen
 * @param pageType: name of screen which is to open
 * */
function turnPage(pageType) { //Could be "email", "poster", "main", or "done", "loading"
	showLoadingBox();
	hideError();
	turnTitle(pageType, ""); //This is to update widget header line according to the screen
	//console.log("Page:" + pageType);
	document.getElementById("mainPage").style.display = "none";
	document.getElementById("emailPage").style.display = "none";
	hideEmailPage(); //To close email screen, by default
	document.getElementById("posterPage").style.display = "none";
	document.getElementById("donePage").style.display = "none";
	hideDoneScreen(); //To close done screen, by default
	document.getElementById(pageType+"Page").style.display = "block";
	if (pageType == "email") {
		createShar();
		showEmailPage();  //To open email screen
	}
	hideLoadingBox();
}

/**
 * @function turnTitle: Function responsible for updating header title
 * @param pageType: String to set widget header
 * @param customText: String to set as custom header of widget
 */
function turnTitle(pageType, customText) { //Could be "email", "poster", "main", or "done", "loading"
	var pgTitle = lang.strings['msg_share'];
	switch(pageType){
		case "main": //Home screen title
			pgTitle = lang.strings['msg_share'];
			break;
		case "email": //Email screen title
			pgTitle = lang.strings['msg_email'];
			break;
		case "done": //Done screen title
			pgTitle = lang.strings['msg_share_success'];
			break;
		case "other": //To set custom title
			pgTitle = customText;
			break;
	}
	document.getElementById('popular').innerHTML = pgTitle;
}

/**
 * Function is responsible for Email share on click of Email button from within the widget
 */
function getEmailService(type){
	stlib.gaLogger.gaLog("Chicklet","Email");
	widget.poster=null;
	updateServiceCount("email", 'Email');
	widget.isServiceClicked = true;
	turnPage("email"); // Update title of Email screen
}

function showLoadingBox(){
	document.getElementById('loadingPage').style.display="block";
}

function hideLoadingBox(){
	document.getElementById('loadingPage').style.display="none";
}

/**
 * @returns {addServiceLinks}
 * addServiceLinks function is responsible for adding service buttons in sheet
 * This function adds top service list as well as all services buttons
 */

function addServiceLinks(){
	var user_services=extractServicesFromCookie();

	var imageDiv;
	var newServiceLink; // A container for service links before they are added to the DOM
	var element=document.getElementById('top_chicklets'); // The div to add service links to top services section
	this.services={'abc':false};  // This keeps track of which services have already been added

	if (typeof(widget.all_services.email)!="undefined" && lang && lang.strings && lang.strings['msg_email_button'])
		stlib.allServices.email.title = lang.strings['msg_email_button'];

	/*
	 * This function creates DOM element for service button
	 */
	function addServiceLink(service) {
		//console.log(service);
		if(typeof(service)=="undefined" || service=="" || service == 'kik') { return; }

		// WhatsApp or Kik supports only iOS && Android
		if((service == 'whatsapp' || service == 'kik') && !(stlib.browser.mobile.isIOs() || stlib.browser.mobile.isAndroid())) {return;}// Feature WID-123 && WID-443

		var newServiceLink = getServiceLink(service);
		if(newServiceLink != null) {
			imageDiv = document.createElement('div');
			imageDiv.className += "largeChicklet lc_" + service;

			newServiceLink.getElementsByTagName('A')[0].appendChild(imageDiv);
			element.appendChild(newServiceLink);

			return true;
		}
		return false;
	}

	// First, remove all the elements inside the top_chicklets div
	while (element.childNodes.length >= 1 ){
        element.removeChild(element.firstChild );
    }

	var count=0; //Will have number of services added to the list of top services
	var publisherDefinedServices = widget.services.split(',');

	// Add all of the publisher defined services next
	for(var i=0;i<publisherDefinedServices.length;i++){
		if(typeof(this.services[publisherDefinedServices[i]])=="undefined"){
			if (addServiceLink(publisherDefinedServices[i])) {
				count++;
				this.services[publisherDefinedServices[i]]=true;
			}
		}
	}

	// If the publisher only wants certain sharing destinations, stop here.
	if (!widget.showAllServices) {
		return;
	}

	// Add all the user's recently shared to destinations first.
	if(user_services!==null){
		var user_services_array=user_services.split(',');
		for(var i=0;i<user_services_array.length;i++){
			if(count<10){
				if(typeof(this.services[user_services_array[i]])=="undefined"){
					if (addServiceLink(user_services_array[i])) {
						count++;
						this.services[user_services_array[i]]=true;
					}
				}
			}
		}
	}

	// Add the top services that people share to (up to 10).  If the publisher defined a lot there might already be more than that.
	var top_services_array = widget.top_services.split(",");
	for(var i=0;i<top_services_array.length;i++){
		if(count<10){
			if(typeof(this.services[top_services_array[i]])=="undefined"){
				if (addServiceLink(top_services_array[i])) {
					count++;
					this.services[publisherDefinedServices[i]]=true;
				}
			}
		}
	}

	// We don't want sharethis service to show up
	if (typeof(widget.all_services.sharethis)!="undefined")
		delete stlib.allServices.sharethis;

	// Penultimately, add an alphabetical list of all supported services.
	for(var i in widget.all_services){
		addServiceLink(i);
	}
}

function searchFocus(){
	var element=document.getElementById('chicklet_search_field');
	if(element.value==lang.strings['msg_search_services']){
		element.value="";
	}
	stlib.gaLogger.gaLog("Search","focus");
}
function searchBlur(){
	var element=document.getElementById('chicklet_search_field');
	if(element.value==""){
		element.value=lang.strings['msg_search_services'];
	}
}

function searchAndDisplay(searchTerm){
	if(searchTerm == "") {
		var chix = document.getElementById("top_chicklets");

		for(i=0;i<chix.childNodes.length;i++) {
			var currentLi = chix.childNodes[i];
			var currentA = currentLi.childNodes[0];

			currentA.innerHTML = currentA.innerHTML.replace("<span>", "");
			currentA.innerHTML = currentA.innerHTML.replace("</span>", "");
			currentA.className = currentA.className.replace(" searchedLi", "");
		}
		return;
	}

	try{var pReg = new RegExp("^" + searchTerm, "gi");}catch(err){return false;}
	try{var reg = new RegExp(searchTerm, "gi");}catch(err){return false;}
	//console.log("reg:"+reg);
	//preMatches
	var pMatches = [];
	var matches = [];
	//search for all matches in case you want to do something with them later (Legacy, left for future use)
	for(var i in widget.all_services){
		var text=widget.all_services[i].title;
	//console.log(text);
		if(reg.test(text)==true && i!="sharebox"){
			matches.push(i);
		}else{
			if(reg.test(text)==true){
				//console.log("not match:"+i);
			}
		}
		if(pReg.test(text)==true && i!="sharebox"){
			pMatches.push(i);
		}
	}
	var toIndexA = document.getElementById("post_"+pMatches[0]+"_link");
    toIndexA = toIndexA ? toIndexA : document.getElementById("post_"+matches[0]+"_link");

	if (toIndexA) {
		var row = 0;
		//for each li in top_chicklets:
		for(i=0;i<toIndexA.parentNode.parentNode.childNodes.length;i++) {
			var currentLi = toIndexA.parentNode.parentNode.childNodes[i];
			var currentA = currentLi.childNodes[0];
			var currentName = currentA.childNodes[0].data;
			if (currentLi == toIndexA.parentNode) {
				row = Math.floor(i/2);
				//HighlightRelevantText
				currentA.innerHTML = currentA.innerHTML.replace("<span>", "");
				currentA.innerHTML = currentA.innerHTML.replace("</span>", "");

				try{var mReg = new RegExp(searchTerm + "(?=.*<di)","i");}catch(err){return false;}

				currentA.innerHTML = currentA.innerHTML.replace(mReg, "<span>"+mReg.exec(currentA.innerHTML)+"</span>");

				currentA.className = currentA.className.replace(" searchedLi", "");
				currentA.className = currentA.className + " searchedLi";
			} else {
				currentA.innerHTML = currentA.innerHTML.replace("<span>", "");
				currentA.innerHTML = currentA.innerHTML.replace("</span>", "");
				currentA.className = currentA.className.replace(" searchedLi", "");
			}
		}
		moveServices(row, true);
	}
	widget.lastSearchTerm=searchTerm;
	return true;
}

function extractServicesFromCookie(){
	var usrSvc=stlib.json.decode(stlib.cookie.getCookie('ServiceHistory'));
	//alert(usrSvc);
	var array=[];
	var svc=null;
	for(o in usrSvc){
		array.push(usrSvc[o]);
	}
	array.sort(serviceSort);
	if(array.length>0){
		svc="";
	}
	for(var i=0;i<array.length;i++){
		//console.log(array[i].service+":"+array[i].count);
		if(i<array.length-1){
			svc+=array[i].service+",";
		}else{
			svc+=array[i].service;
		}
	}
	//console.log(svc);
	return svc;
}

function serviceClicked(elem){
	//console.log(elem.getAttribute('stservice'));

	var service=elem.getAttribute('stservice');
	var serviceTitle = elem.getAttribute('title');
	updateServiceCount(service, serviceTitle);

	stlib.data.resetShareData();
	stlib.data.set("url",widget.URL,"shareInfo");

    //SA-77: introduce new st_short_url parameter
    stlib.data.set("short_url",widget.short_url,"shareInfo");

	stlib.data.set("shorten", widget.shorten, "shareInfo");
	stlib.data.set("title",widget.title,"shareInfo");

	stlib.data.set("image",widget.thumb,"shareInfo");
	stlib.data.set("description",widget.summary,"shareInfo");

	stlib.data.set("buttonType","large","shareInfo");
	stlib.data.set("destination",service,"shareInfo");
	if (widget.popup==true && widget.source!="sharethis.js")
		stlib.data.setSource("share4xpage", widget);
	else
		stlib.data.setSource("share4x", widget);
	if(service=="twitter" && widget.via != null){
		stlib.data.set("via", widget.via, "shareInfo");
	}
	if(widget.message!=''){
		stlib.data.set("message",widget.message,"shareInfo");
	}

	stlib.sharer.share(null, widget.servicePopup);
	if (service=="pinterest" && (stlib.data.get("image", "shareInfo") == false || stlib.data.get("image", "shareInfo") == null) && stlib.data.get("source", "shareInfo").match(/share4xpage/) == null) {
		if (stlib.browser.ieFallback) {
			if(typeof(window.postMessage)!=="undefined" && document.referrer!==""){
				parent.postMessage("#Pinterest Click", document.referrer);
			}
		}
		else
			fragInstance.broadcastSendMessage("Pinterest Click");
	}
	stlib.gaLogger.gaLog("Share",service);

	if (service=="print") {
		if(typeof(window.postMessage)!=="undefined"){
			parent.postMessage("ShareThis|close|Print", document.referrer);
		}
		if (stlib.browser.ieFallback) {
			if(typeof(window.postMessage)!=="undefined" && document.referrer!==""){
				parent.postMessage("#Print Click", document.referrer);
			}
		}else{
			fragInstance.broadcastSendMessage("Print Click");
		}
	}else{
		showDoneScreen();
	}

	stlib.gaLogger.shareLog(service);
}

function updateServiceCount(service, serviceTitle){
	if(widget.all_services[service]==undefined || service=="sharebox"){
		return false;
	}
	var usrSvc=stlib.json.decode(stlib.cookie.getCookie('ServiceHistory'));
	if(usrSvc==false || usrSvc==null || usrSvc.length<1){
		usrSvc={};
		usrSvc[service]={};
		usrSvc[service].service=service;
		usrSvc[service].title = serviceTitle;
		usrSvc[service].count=1;
		stlib.cookie.setCookie('ServiceHistory',stlib.json.encode(usrSvc));
		//stlib.cookie.setCookie('ServiceHistory', "A");
		return true;
	}
	var obj={};
	var svc=null;
	var flag=false;
	var sortable=[];
	for(o in usrSvc){
		if(usrSvc[o].service==service){
			usrSvc[o].count++;
			usrSvc[o].title = serviceTitle;
			flag=true;
		}
		sortable.push(usrSvc[o]);
	}
	if(flag==false){
		usrSvc[service]={};
		usrSvc[service].service=service;
		usrSvc[service].title = serviceTitle;
		usrSvc[service].count=1;
	}
	else
	{
		sortable.sort(function(a,b){
			return b.count - a.count;
		});
		usrSvc={};
		for(var i=0;i<sortable.length;i++){
			usrSvc[sortable[i].service]= sortable[i];
		}
	}
	stlib.cookie.setCookie('ServiceHistory',stlib.json.encode(usrSvc));
	return true;
}


function serviceSort(a,b){
	if(a.count==b.count){
		return 0;
	}else if(a.count>b.count){
		return -1;
	}else{
		return 1;
	}
}

/**
 * @function getMainCss: Responsible for loading required CSS files
 * @returns {Boolean}
 */
function getMainCss(){
	if(widget.mainCssLoaded==false){
		// Main CSS file required for 4x widget's overall style
		odcss("https://ws.sharethis.com/secure/css/share.e4ab8fa373f4ff4f83a78dd89dfdbebc.css",function(){},true);
		// Flag to identify Main CSS is loaded
		widget.mainCssLoaded=true;
	}else{
		return false;
	}
}

function extractDomainFromURL(url, keepWWW) {
  try{var domain = url.replace(/(\w+):\/\/([^\/:]+)(:\d*)?([^# ]*)/, '$2');
	  if (!keepWWW && domain.toLowerCase().indexOf('www.') == 0) {
		  domain = domain.substring(4);
	  }
	  domain=domain.replace(/#.*?$/,''); //replace #onwards
	  return domain;
  }catch(err){
	  return null;
  }
}


function initWidget(){
	getMainCss();
	if(widget.URL==null){
		return true;
	}else{
		var data=['return=json',"url="+encodeURIComponent(widget.URL),"fpc="+widget.fpc,"cb=initWidgetOnSuccess","service=initWidget"];
		data=data.join('&');
		jsonp.makeRequest("https://ws.sharethis.com/api/getApi.php?"+data);
		return true;
	}
}

function initWidgetOnSuccess(response){
	if(response && response.data){
		widget.metaInfo=response.data;
	}

	if(response && response.data && response.data.ga && response.data.ga==true){
    stlib.gaLogger.initGA("UA-1645146-9", widget);
	}
}

/***************************JSONP********************/

var jsonp={};

jsonp.makeRequest=function(url){
	odjs(url,function(){});
};

/***************************ODJS********************/

function odjs(scriptSrc,callBack){
	stlib.scriptLoader.loadJavascript(scriptSrc,callBack);
}

function odcss(scriptSrc,callBack){
	stlib.scriptLoader.loadCSS(scriptSrc,callBack);
}

/***************************DOM READY CALLBACK********************/

function initialize(){
	showLoadingBox();
	//fragmentPump.checkFragment();
	var isBot=false;
	var nv=navigator.userAgent;
	var nvPat=/bot|gomez|keynote/gi;
	if(nv && nv!==null && nv.length>4){
		var tempMatch=nv.match(nvPat);
		if(tempMatch && tempMatch!==null && tempMatch.length>0){
			isBot=true;
		}
	}else{
		isBot=true;
	}

	if(fragmentPump.initRun==true){
		processBuffer();
	}

	//getMainCss();
	widget.domReady=true;
	/*
	if(widget.publisherGA!==null){
		stlib.gaLogger.initGA("UA-1645146-9", widget);
	}*/

	var searchField = document.getElementById('chicklet_search_field');
	searchField.onfocus=function(){searchFocus();};
	searchField.onblur=function(){searchBlur();};
	searchField.onkeyup=function(){
		searchAndDisplay(this.value);
	};

	// Apply localization
	fillInLanguage();
}

/**
 * This function is called to set text for localization
 * If "lang" parameter is set in configuration then it takes values from corresponding message.js file.
 * Else "lang" parameter is not set in configuration then it loads English Strings (default)
 */
function fillInLanguage(){
	turnTitle("main", ""); // Home screen, by default
	document.getElementById('chicklet_search_field').value=lang.strings['msg_search_services'];
	document.getElementById('chicklet_search_field').setAttribute("placeholder", lang.strings['msg_search_services']);
	document.getElementById('imgDoneScreenMonitor').setAttribute("alt",lang.strings['msg_share_anywhere']);
	//document.getElementById('imgDoneScreenMonitorText').setAttribute("alt",lang.strings['msg_share_anywhere']);
	document.getElementById('btnShareAgain').innerHTML=lang.strings['msg_share_again']+" &raquo;";
	document.getElementById('btnBookmark').innerHTML=lang.strings['msg_add_bookmark']+" &raquo;";
	document.getElementById('btnClose').innerHTML=lang.strings['msg_close'];
	document.getElementById('btnBack').innerHTML="&laquo; "+lang.strings['msg_back'];
	document.getElementById('powered_text').innerHTML=lang.strings['msg_powered']+"&nbsp;&nbsp;";
	document.getElementById('poster_message').innerHTML=lang.strings['msg_message'];
	document.getElementById('poster_message2').innerHTML=lang.strings['msg_blog_url'];
	document.getElementById('posterSubmit').innerHTML=lang.strings['msg_submit'];
	document.getElementById('posterCancel').innerHTML=lang.strings['msg_email_cancel'];
	document.getElementById('doNotTrack_text').innerHTML=lang.strings['msg_track'];
}

//Adds initialize to be called when dom ready
if (typeof(window.addEventListener) != 'undefined') {
    window.addEventListener("load",initialize, false);
} else if (typeof(document.addEventListener) != 'undefined') {
    document.addEventListener("load",initialize, false);
} else if (typeof window.attachEvent != 'undefined') {
    window.attachEvent("onload",initialize );
}

/**************DONE SCREEN ************************/
/*
 * To hide bookmarklet button and top-right link (Share again link) as these are out of donePage <div>
 */
function hideDoneScreen(){
	document.getElementById('btnBookmark').parentNode.parentNode.style.display = "none";
	document.getElementById('btnShareAgain').style.display='none';
}

/*
 * Callback of Share again link (top-right link) on done screen
 * It switches widget to Home home screen
 */
function doneShareAgainClick(){
	turnPage("main");
}

/**
 * To show done screen
 *  - Shows the share anywhere (monitor) image
 *  - Shows Bookmarklet button
 *  - Show/hide content of done screen according to the Browser
 */
function showDoneScreen(){
	turnPage("done");
	var img_url_initial="https://ws.sharethis.com/images/reskin2014/";

	var defaultClass='', defaultSrc='', imageVersion = '_noText';

	if(!currentLang){
		imageVersion = '';
	}

	if(stlib.browser.getIEVersion()){ //IE
		defaultClass = 'stBtnExplorer';
		defaultSrc = img_url_initial+'share_success.png';
	}else if(stlib.browser.isChrome()){ //Chrome
		defaultClass = 'stBtnChrome';
		defaultSrc = img_url_initial+'share_success.png';
	}else if(stlib.browser.isSafari()){ //Safari
		defaultClass = 'stBtnSafari';
		defaultSrc = img_url_initial+'share_success.png';
	}else if(stlib.browser.isOpera()){ // Opera
		defaultClass = 'stBtnOpera';
		defaultSrc = img_url_initial+'share_success.png';
	}else{ //Default case will show effects of FireFox browser
		defaultClass='stBtnFirefox';
		defaultSrc = img_url_initial+'share_success.png';
	}

	// Applies Monitor image according to Browser
	var imgDoneScreenMonitor = document.getElementById('imgDoneScreenMonitor');
	imgDoneScreenMonitor.src = defaultSrc;

	// Shows the bookmarklet button according to Browser
	var btnBookmark = document.getElementById('btnBookmark');
	btnBookmark.className = defaultClass;
	btnBookmark.parentNode.parentNode.style.display = "block";
	// Bind functionality for link click event
	btnBookmark.parentNode.onclick=function(){
	    		//addServiceLinks(); // Updates the services list
		moveServices(0); // Resets the service list preferences
		doneShareAgainClick(); // Turn widget screen to Home screen
		stlib.gaLogger.gaLog("DoneScreen","ShareAgain");
	};

	// Shows Share Again link on top-right corner of widget
	document.getElementById('btnShareAgain').style.display='block';

	// Bind functionality for Share Again link click event
	document.getElementById('btnShareAgain').onclick=function(){
		//addServiceLinks(); // Updates the services list
		moveServices(0); // Resets the service list preferences
		doneShareAgainClick(); // Turn widget screen to Home screen
		stlib.gaLogger.gaLog("DoneScreen","ShareAgain");
	};
}

function showHome(){
	turnPage("main");
}

/********************Posters**********/
var poster={};

//creates poster screen based on service
function createPoster(service){
	if(widget.title==null){	widget.title=widget.URL;}
//	console.log("createPoster");

	document.getElementById('poster_inputBox').value = "";
	document.getElementById('poster_inputBox').onfocus = function(){hideError();};

	var headerText = lang.strings['msg_post_to'];
	if(service=="twitter"){ // Todo: Investigate when this code is called
		updateServiceCount(service, 'Tweet');
		stlib.gaLogger.gaLog("Twitter","poster_clicked");
		widget.poster="twitter";
		document.getElementById('poster_textArea').style.display="block";
		document.getElementById('poster_textArea').value="";
		createShar();
		document.getElementById('comment_box').style.display="block";
		document.getElementById('poster_input_div').style.display="none";
		document.getElementById('poster_textArea').onkeypress=poster.updateCounter;
		document.getElementById('poster_message_counter').style.display="block";
		headerText += " Twitter";
		turnPage("poster");
	}else if(service=="wordpress"){ // Opens WordPress screen of widget
		updateServiceCount(service, 'Wordpress');
		widget.poster="wordpress";
		stlib.gaLogger.gaLog("Wordpress","poster_clicked");
		document.getElementById('poster_textArea').style.display="none";
		document.getElementById('comment_box').style.display="none";
		document.getElementById('poster_input_div').style.display="block";
		document.getElementById('poster_message_counter').style.display="none";
		document.getElementById('poster_message_counter').style.display="none";
		headerText = lang.strings['msg_post_wordpress'];
		turnPage("poster");
	}
	turnTitle("other", headerText); // Updates the widget header as per the service
}

//poster.hide=function(){}
poster.cancel=function(service){
	turnPage("main");
	widget.poster=null;
};

poster.getCount=function(){
	var element=document.getElementById('poster_textArea');
	var text=element.value;
	if(text.length>=117){
		return false;
	}else{
		return 117-text.length;
	}
};

poster.updateCounter=function(e){
	try{var KeyID = (window.event) ? event.keyCode : e.keyCode;}catch(err){KeyID=0;}
	var val=poster.getCount();
	var ctr=element=document.getElementById('counter');
	if(val===false){
		ctr.innerHTML=0;
		if(KeyID!==0){
			return true;
		}else{
			return false;
		}
	}else{
		if(val<11){
			ctr.style.color="red";
		}else{
			ctr.style.color="#666666";
		}
		ctr.innerHTML=val;
	}
};

poster.post=function(service){
	stlib.data.resetShareData();
	stlib.data.set("source", "share4xPoster","shareInfo");
	stlib.data.set("buttonType", "large","shareInfo");
	stlib.data.set("title", widget.title,"shareInfo");
	stlib.data.set("url", widget.URL, "shareInfo");

    //SA-77: introduce new st_short_url parameter
    stlib.data.set("short_url", widget.short_url, "shareInfo");

	stlib.data.set("sharURL", widget.sharURL, "shareInfo");
	stlib.data.set("status", document.getElementById('poster_textArea').value, "shareInfo");

	if(widget.poster=="wordpress"){
		//	console.log("post to wordpress");
		if(document.getElementById('poster_inputBox').value.length<1){
			showError(lang.strings['msg_valid_blog']);
			return false;
		}else{
			if(widget.service==null){
				widget.service = 'legacy';
			}
			var wpurl=document.getElementById('poster_inputBox').value;
			wpurl = wpurl.replace(/^https?:\/\//,'');
			stlib.data.set("destination", "wordpress", "shareInfo");
			stlib.data.set("wpurl", wpurl, "shareInfo");
			stlib.data.set("service", widget.service, "shareInfo");
			stlib.sharer.share(null, widget.servicePopup);
			widget.poster=null;
			showDoneScreen();
			return true;
		}
	}
	return true;
};

/***************SHAR URL******************/

function createShar(){
        var url=widget.URL;
	if(url==widget.lastURL && widget.shorten == false){
		var temp=( (widget.title!=null) ? widget.title+' - ' : "" )+widget.sharURL;
		document.getElementById('poster_textArea').value=temp;
		poster.updateCounter();
	//Fix for FB:12537
	}else if(((url!=="" && url!==" " && url!==null && widget.lastURL!=url) || widget.sharCreated == false) && widget.shorten == true){
    	widget.sharCreated = false;	//Fix for FB:12537
		widget.sharURL=url;//Fix for FB:12537
		document.getElementById('poster_textArea').value = lang.strings['msg_loading'];
                widget.lastURL=url;
		var data=["return=json","cb=createShar_onSuccess","service=createSharURL","url="+encodeURIComponent(url),"sessionID="+widget.sessionID,"fpc="+widget.fpc];
		data=data.join('&');
		jsonp.makeRequest("https://ws.sharethis.com/api/getApi.php?"+data);
	}
}

function createShar_onSuccess(response){
	if((typeof response) != "undefined" && response.status=="SUCCESS"){
		widget.sharURL=response.data.sharURL;
		widget.sharCreated = true;
	}
	//console.log(widget.title);
	var temp=( (widget.title!=null) ? widget.title+' - ' : "" )+widget.sharURL;
	document.getElementById('poster_textArea').value=temp;
	poster.updateCounter();
}

/***************I18N******************/
if(typeof(lang)=="undefined"){
	var lang={};

	lang.strings=new Object;
	lang.strings['msg_loading'] = 'Loading';
	lang.strings['msg_posting_t'] = 'Posting to Twitter';
	lang.strings['msg_text'] = 'Text to a Friend:';
	lang.strings['msg_sendign_inProgress'] = 'Sharing Message';
	lang.strings['msg_get_button'] = 'Get the add-on now!';
	lang.strings['msg_put_sharethis'] = 'Easily share your favorite finds online with a click of a button';
	lang.strings['msg_valid_blog'] = 'Sorry, there was something wrong with that URL, please try again.';
	lang.strings['msg_post_wordpress'] = 'Post to Wordpress';
	lang.strings['msg_email_to'] = 'To:';
	lang.strings['msg_email_from'] = 'From:';
	lang.strings['msg_email_send'] = 'Send';
	lang.strings['msg_email_cancel'] = 'Cancel';
	lang.strings['msg_email_preview'] = 'Preview';
	lang.strings['msg_email_close_preview'] = 'Close Preview';
	lang.strings['msg_email_char_limit'] = '2000 characters left';
	lang.strings['email_message'] = 'Message:';
	lang.strings['msg_email_privacy'] = 'Privacy Policy';
	lang.strings['msg_email_load_cont'] = 'Loading Contacts...';
	lang.strings['msg_import_serv'] = 'Import Contacts From';
	lang.strings['msg_email_captcha_info'] = 'Please type the words below:';
	lang.strings['msg_valid_email_add'] = 'Please enter a valid email address.';
	lang.strings['msg_valid_email_add_from'] = 'Please enter a valid email address in the "From" field.';
	lang.strings['msg_valid_recipients'] = 'Please enter a valid recipient';
	lang.strings['msg_captcha'] = 'Please enter the Captcha response.';
	lang.strings['msg_view_all']="View All";
	lang.strings['msg_hide_all']="Hide All";
	lang.strings['msg_share_success_fs']="Your message was successfully shared! Log-in with FastShare to share with just one click next time.";
	lang.strings['msg_fast_share']='Enable FastShare';
	lang.strings['msg_related_shares']="Popular Shares:";
	lang.strings['msg_post_to']="Post to";
	lang.strings['msg_message']="Message:";
	lang.strings['msg_submit']="Submit";
	lang.strings['msg_friends']="What are your friends sharing?";
	lang.strings['msg_my_acct']="My Account";
	lang.strings['msg_signin']="Sign In";
	lang.strings['msg_signout']="Sign Out";
	lang.strings['msg_notyou']="Not You?";
	lang.strings['msg_get_sharethis']="Get ShareThis";
	lang.strings['msg_free_plugin']="FREE Plug-In!";
	lang.strings['msg_recents']="Recents:";
	lang.strings['msg_greeting']="Hi";

	lang.strings['msg_share_anywhere']="Share from Anywhere";

	// Todo: Remove above strings which are overritten
	lang.strings['msg_close']="Close";
	lang.strings['msg_email'] = "Select your Email";
	lang.strings['msg_add_bookmark']="Share Again";
	lang.strings['msg_add_extension']="Share Again";
	lang.strings['msg_share_success']="Successfully Shared!";
	lang.strings['msg_share_again']="Share again";
	lang.strings['msg_track']="Opt out";
	lang.strings['msg_powered']="Powered by";
	lang.strings['msg_search_services'] = "Search for services";
	lang.strings["msg_email_cancel"]="Cancel";
	lang.strings["msg_post_wordpress"]="Post to Wordpress";
	lang.strings['msg_submit']="Submit";
	lang.strings["msg_valid_blog"]="Sorry, there was something wrong with that URL, please try again.";
	lang.strings["msg_email_send"]="Send";
	lang.strings['msg_share']="Share this with friends!";
	lang.strings['msg_back']="Back";
	lang.strings['msg_blog_url']="Blog URL";
	lang.strings['msg_popup_blocker']="Please disable your popup-blocker!";
}

/*
 * Reset top offset of services list
 */
function moveServices(row, search) {
	if (row == 0) {
		var element=document.getElementById('chicklet_search_field');
		if(element!=null && typeof(search)=="undefined" && !search){
			element.value=lang.strings['msg_search_services'];
		}
	}
	document.getElementById("all_chicklets").scrollTop = (row*46);
}

/**
 * @function showEmailPage: Responsible for opening the Email screen
 * @returns {Boolean}
 */
function showEmailPage() {
	if(!widget.isServiceClicked){ //Close link, if page's email button was clicked
		document.getElementById('btnBack').style.display = "none"; //Hide Back link
		document.getElementById('btnClose').style.display = "block"; // Show Close link
		document.getElementById('btnClose').onclick=function(){ //Register Close link click handler
			closeEmailWidget();
			stlib.gaLogger.gaLog("New Email share page - 4x","Close clicked");
		};
	}else{//Back link, if minor service email button was clicked
		document.getElementById('btnClose').style.display = "none"; // Hide Close link
		document.getElementById('btnBack').style.display = "block"; // Show Back link
		document.getElementById('btnBack').onclick=function(){ //Register Back link click handler
			moveServices(0); // Resets the service list preferences
			emailGoBackClick(); //Opens Home screen
			stlib.gaLogger.gaLog("New Email share page - 4x","Go Back clicked");
		};
	}

	document.getElementById('email_main').onclick=function(e){ //Register Email service click handler
		e = e || window.event;
		var svcEmailClicked = e.target || e.srcElement;
		return emailShareExternal(svcEmailClicked);
	};
	widget.isServiceClicked = false; // flag to identify which (within widget or pub page) email button clicked
	stlib.gaLogger.gaLog("New Email share page - 4x","Opened");
	return false;
}

/*
 * Sends message to buttons.js to close the widget
 */
function closeEmailWidget(){
	if(typeof(window.postMessage)!=="undefined"){
		parent.postMessage("ShareThis|close|Email", document.referrer);
	}
}

/*
 * To hide top-right links (Back and Close links) as these are out of emailPage <div>
 */
function hideEmailPage(){
	document.getElementById('btnBack').style.display = "none";
	document.getElementById('btnClose').style.display = "none";
}

function urlEncodeCharacter(c)
{
	return '%' + c.charCodeAt(0).toString(16);
}

function urlEncode( s )
{
	return escape(s);
}


/*
 * Function: getExternalEmailBody
 * Parameters:
 *  1. serviceType: Which email service button is clicked
 *  	- Possible values:
 *  		1.1 'gmail' - Gamil button is clicked
 *  		1.2 'yahoo' - Yahoo button is clicked
 *  		1.3 'outlook' - Outlook button is clicked
 *  		1.4 'mailto' - Native email button is clicked
 *  2. sharURLValue: Shortened URL
 *  	- Possible values:
 *  		2.1 '' - If URL is not shortened, due to some reason
 *  		2.2 Shortened URL
 *  3. trimData: Flag to trim data in case of very long data to share
 *  	- Possible values:
 *  		3.1 null - If data trimming is not required (Limited data being shared)
 *  		3.2 1 - If data is too long for GET request but can be managed if description is removed from it
 *  		3.3 2 - If data is too long for GET request and can not be managed by removing description only,
 *  			  then comment is also removed from sharing data
 *
 */


function getExternalEmailBody(serviceType, sharURLValue, trimData)
{
	// If trimData == 1: Remove Description from message

	var emailData={
			type:widget.type,
			recipients:"",
			url: widget.URL,
			title:(widget.title),
			thumbnail:widget.thumb,
			embed:widget.content,
			description:widget.summary,
			sharURL:(sharURLValue != '')?sharURLValue:widget.URL
		};

	var st_signature = 'This message was sent using ShareThis (https://www.sharethis.com)';
	var newLineSpacer = '\r\n\r\n';

	if(serviceType == "mailto"){
		newLineSpacer = urlEncode(newLineSpacer);
		if(emailData.description){
			emailData.description = emailData.description.replace(/%/g, urlEncodeCharacter );
		}
	}

	//var YahooEmailMessage = emailData.sharURL+'.'+newLineSpacer+st_signature;
	var emailMessage = emailData.sharURL;
	if(emailData.description && trimData != 1 && trimData != 2){
		emailMessage += newLineSpacer+emailData.description;
	}
	emailMessage += newLineSpacer+st_signature;

	var YahooEmailMessage = emailMessage; // assign the same Gmail emailMessage to Yahoo as well

	var emailTo = (emailData.recipients)?emailData.recipients:"";
	var emailSubject = (emailData.title)?emailData.title:"Message Subject";
	var emailBody = (emailMessage)?(emailMessage):"Message Body";
	YahooEmailMessage = (YahooEmailMessage)?(YahooEmailMessage):"Message Body";

	var emailServices = {};
	emailServices['gmail'] = {
		href: "https://mail.google.com/mail/?view=cm",
		su: encodeURIComponent(emailSubject),
		to: emailTo,
		body: encodeURIComponent(emailBody)
	};

	emailServices['yahoo'] = {
		href: "//compose.mail.yahoo.com/?",
		//href: "//mail.yahoo.com/neo/launch?action=compose",
		//href: "//us.mg1.mail.yahoo.com/dc/launch?sysreq=ignore&action=compose&login=1",
		Subject: encodeURIComponent(emailSubject.replace(/%/g, urlEncodeCharacter ).replace(/&/g, urlEncodeCharacter ).replace(/#/g, urlEncodeCharacter).replace(/'/g,urlEncodeCharacter).replace( /"/g, urlEncodeCharacter ).replace(/>/g, urlEncodeCharacter).replace(/</g,urlEncodeCharacter).replace(/\\n/g,"").replace(/\\r/g,"").replace(/\\/g,"")),
		To: emailTo,
		Body: urlEncode(YahooEmailMessage.replace( /#/g, urlEncodeCharacter ).replace(/\r\n/g,'<br>'))
	};

	emailServices['outlook'] = {
		href: "//mail.live.com/default.aspx?rru=compose",
		subject: encodeURIComponent(emailSubject),
		to: emailTo,
		body: encodeURIComponent(emailBody.replace(/\r\n/g,'<br>').replace(/\(/g, '[').replace(/\)/g, ']'))
	};

	emailServices['mailto'] = {
		href: "mailto:"+emailTo+"?",
		Subject: emailSubject.replace(/%/g, urlEncodeCharacter ).replace(/&/g, urlEncodeCharacter ).replace(/#/g, urlEncodeCharacter).replace(/'/g,urlEncodeCharacter).replace( /"/g, urlEncodeCharacter ).replace(/>/g, urlEncodeCharacter).replace(/</g,urlEncodeCharacter),
		Body: emailBody.replace(/&/g, urlEncodeCharacter ).replace(/#/g, urlEncodeCharacter).replace(/'/g,urlEncodeCharacter).replace( /"/g, urlEncodeCharacter ).replace(/>/g, urlEncodeCharacter).replace(/</g,urlEncodeCharacter)
	};

	var newHref = "";
	for(var arg in emailServices[serviceType]){
		if(arg == "href"){
			newHref += emailServices[serviceType][arg];
		}else{
			if(!(serviceType == "mailto" && arg == "Subject")){
				newHref += "&";
			}
			newHref += arg+"="+emailServices[serviceType][arg];
		}
	}

	return newHref;
}


function clearExEmailSharPoller(arrPollersToClear)
{
	for(var i=0; i< arrPollersToClear.length; i++){
		clearTimeout(arrPollersToClear[i]);
	}
}

function shareExternalEmail(winEmail, serviceType, sharURLValue)
{
	/***
	 * Maximum characters allowed in URL is 2048
	 * But it was not working on Google so implemented 1855 by following (http://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers)
	 * Also observed that if more than 1200 characters are sent for google compose window when NOT logged in to google (It breaks on successful sign-in redirect).
	 *
	 * 655 is the maximum number of characters can be used for redirects internally by email services (I observed till 479 characters in login success redirect window in Google)
	 */
	var maxCharactersAllowedInURL = 1200; //(1855-655)

	updateServiceCount("email", 'Email');

	var newHref = getExternalEmailBody(serviceType, sharURLValue, null); // Last parameter is null to trim nothing
	if(maxCharactersAllowedInURL < encodeURIComponent(newHref).length){
		newHref = getExternalEmailBody(serviceType, sharURLValue, 1); // Last parameter is 1 to remove description from data
	}

	// START: ShareThis logging
	// ShareUT will be available if user is logged in using sharethis.com website in same browser
	stlib.data.resetShareData();
    var ShareUT = '';
    ShareUT = stlib.cookie.getCookie('ShareUT');
    if ((ShareUT == false) || (ShareUT == "undefined") || (typeof(ShareUT) == "undefined")) {
        if( (stlib.cookie.checkCookiesEnabled() == false) && (stlib.cookie.hasLocalStorage() == true)){
        	ShareUT = localStorage['ShareUT'];
        }else{
        	ShareUT = '';
        }
    }

	if((widget.type==null) || (typeof(widget.type) == "undefined")){
		widget.type = "";
	}

    stlib.data.set("url",widget.URL,"shareInfo");

    //SA-77: introduce new st_short_url parameter
    stlib.data.set("short_url",widget.short_url,"shareInfo");

    stlib.data.set("title",widget.title,"shareInfo");
    stlib.data.set("destination",'email',"shareInfo");
    stlib.data.set("destinations",'email',"shareInfo");
    stlib.data.set("ip",'',"shareInfo");
    stlib.data.set("agent",navigator.userAgent,"shareInfo");
    stlib.data.set("clicookie",stlib.cookie.getCookie("__stid"),"shareInfo");
   	stlib.data.set("token",ShareUT,"shareInfo");
    stlib.data.set("buttonType",widget.type,"shareInfo");
    stlib.data.set("emailDestination", 'email', "shareInfo");
	stlib.data.set("sharURL", sharURLValue, "shareInfo");
	stlib.data.setSource("4x", widget); // It sets "source=chicklet4x" in logs

	stlib.sharer.share(null, null);
	// END: ShareThis logging

	stlib.gaLogger.shareLog("Email");
	stlib.gaLogger.gaLog("New Email share page - 4x","External_"+serviceType);

	winEmail.location = newHref;
	if(serviceType == "mailto"){
		setTimeout(function(){winEmail.close();},1000);
	}

	showDoneScreen(); // Show Done screen after email sharing
}

function emailShareExternal(target)
{
	var sharURLValue = '', serviceType = target.getAttribute('data-value'), winEmailTitle = "";

	switch(serviceType){
    	case 'gmail':
    		winEmailTitle = 'Connecting you to GMail';
    		break;
    	case 'yahoo':
    		winEmailTitle = 'Connecting you to Yahoo! Mail';
    		break;
    	case 'outlook':
    		winEmailTitle = 'Connecting you to Outlook';
    		break;
    	case 'mailto':
    		winEmailTitle = 'Connecting you to your native email client';
    		break;
    	default:
    		return false;
	}

	var removeExEmailSharPoller, exEmailSharPoller;
	var winEmail = window.open('');
	if(winEmail){
		var winEmailLightbox = '<!DOCTYPE><html><head><title>'+winEmailTitle+'</title></head><body>'+
								'<div id="lightbox" style="height:41px; width:410px; z-index:+1; position:fixed; border:4px solid #ccc; top:40%; left:33%; padding:8px; background-color:#eee; text-align:center; -moz-border-radius:9px; -webkit-border-radius:9px; border-radius:9px;">'+
							        '<div style="margin-right:10px">'+
								    	'<span id="lightboxText" style="color:#777; font-family:Tahoma; font-size:1.3em;">'+winEmailTitle+'</span>'+
								    	'<span style="display:block; font-size:0.7em;color:#999; padding-top:4px;">It will be just a second..</span>'+
								     '</div>'+
							    '</div>'+
								'<div id="overlay" style="width: 99%; height: 100%; opacity: 0.9;background-color:#000;position:fixed;"></div>'+
								'</body></html>';

		winEmail.document.write(winEmailLightbox);

		exEmailSharPoller = setInterval( function(){
			sharURLValue = widget.sharURL;
			if(sharURLValue != ''){
				clearExEmailSharPoller([exEmailSharPoller, removeExEmailSharPoller]);
				shareExternalEmail(winEmail, serviceType, sharURLValue);
			}
		}, 100);
		removeExEmailSharPoller=setTimeout(function(){
			clearExEmailSharPoller([exEmailSharPoller, removeExEmailSharPoller]);
			shareExternalEmail(winEmail, serviceType, '');
		},5000);

	}else{
		/*
		 * Show widget error message.
		 *
		 * if window open is called in context of direct user interaction, Popup-blocker should not block it.
		 * Added as a last resort in case of non-standard popup-blocker
		 *
		 */
		showError(lang.strings['msg_popup_blocker']);
	}
}

// Go back to Home screen from email screen
function emailGoBackClick(){
	turnPage('main');
}

/*
 * Show error message on top of widget
 */
function showError(errorMessage)
{
	var currentElement = document.getElementById('errorMsg');
	currentElement.innerHTML = errorMessage;
	currentElement.style.display = "block";
	document.getElementById('errorBottom').style.display = "block";
}

/*
 * Hides error message
 */
function hideError()
{
	var currentElement = document.getElementById('errorMsg');
	currentElement.innerHTML = "";
	currentElement.style.display = "none";
	document.getElementById('errorBottom').style.display = "none";
}

if (typeof(stlib.global.hash) == "string" && stlib.global.hash.substring(0,5) == "popup") {

	var cleanHash = "#" + stlib.global.hash;

	_$d_();
	_$d1("Popup initiated");
	_$d1(cleanHash);
	fragmentPump.checkFragment(cleanHash);
	_$d1("Done Checking Frag");

}
