/*! jQuery v3.1.0 | (c) jQuery Foundation | jquery.org/license */
!function(a,b){"use strict";"object"==typeof module&&"object"==typeof module.exports?module.exports=a.document?b(a,!0):function(a){if(!a.document)throw new Error("jQuery requires a window with a document");return b(a)}:b(a)}("undefined"!=typeof window?window:this,function(a,b){"use strict";var c=[],d=a.document,e=Object.getPrototypeOf,f=c.slice,g=c.concat,h=c.push,i=c.indexOf,j={},k=j.toString,l=j.hasOwnProperty,m=l.toString,n=m.call(Object),o={};function p(a,b){b=b||d;var c=b.createElement("script");c.text=a,b.head.appendChild(c).parentNode.removeChild(c)}var q="3.1.0",r=function(a,b){return new r.fn.init(a,b)},s=/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,t=/^-ms-/,u=/-([a-z])/g,v=function(a,b){return b.toUpperCase()};r.fn=r.prototype={jquery:q,constructor:r,length:0,toArray:function(){return f.call(this)},get:function(a){return null!=a?a<0?this[a+this.length]:this[a]:f.call(this)},pushStack:function(a){var b=r.merge(this.constructor(),a);return b.prevObject=this,b},each:function(a){return r.each(this,a)},map:function(a){return this.pushStack(r.map(this,function(b,c){return a.call(b,c,b)}))},slice:function(){return this.pushStack(f.apply(this,arguments))},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},eq:function(a){var b=this.length,c=+a+(a<0?b:0);return this.pushStack(c>=0&&c<b?[this[c]]:[])},end:function(){return this.prevObject||this.constructor()},push:h,sort:c.sort,splice:c.splice},r.extend=r.fn.extend=function(){var a,b,c,d,e,f,g=arguments[0]||{},h=1,i=arguments.length,j=!1;for("boolean"==typeof g&&(j=g,g=arguments[h]||{},h++),"object"==typeof g||r.isFunction(g)||(g={}),h===i&&(g=this,h--);h<i;h++)if(null!=(a=arguments[h]))for(b in a)c=g[b],d=a[b],g!==d&&(j&&d&&(r.isPlainObject(d)||(e=r.isArray(d)))?(e?(e=!1,f=c&&r.isArray(c)?c:[]):f=c&&r.isPlainObject(c)?c:{},g[b]=r.extend(j,f,d)):void 0!==d&&(g[b]=d));return g},r.extend({expando:"jQuery"+(q+Math.random()).replace(/\D/g,""),isReady:!0,error:function(a){throw new Error(a)},noop:function(){},isFunction:function(a){return"function"===r.type(a)},isArray:Array.isArray,isWindow:function(a){return null!=a&&a===a.window},isNumeric:function(a){var b=r.type(a);return("number"===b||"string"===b)&&!isNaN(a-parseFloat(a))},isPlainObject:function(a){var b,c;return!(!a||"[object Object]"!==k.call(a))&&(!(b=e(a))||(c=l.call(b,"constructor")&&b.constructor,"function"==typeof c&&m.call(c)===n))},isEmptyObject:function(a){var b;for(b in a)return!1;return!0},type:function(a){return null==a?a+"":"object"==typeof a||"function"==typeof a?j[k.call(a)]||"object":typeof a},globalEval:function(a){p(a)},camelCase:function(a){return a.replace(t,"ms-").replace(u,v)},nodeName:function(a,b){return a.nodeName&&a.nodeName.toLowerCase()===b.toLowerCase()},each:function(a,b){var c,d=0;if(w(a)){for(c=a.length;d<c;d++)if(b.call(a[d],d,a[d])===!1)break}else for(d in a)if(b.call(a[d],d,a[d])===!1)break;return a},trim:function(a){return null==a?"":(a+"").replace(s,"")},makeArray:function(a,b){var c=b||[];return null!=a&&(w(Object(a))?r.merge(c,"string"==typeof a?[a]:a):h.call(c,a)),c},inArray:function(a,b,c){return null==b?-1:i.call(b,a,c)},merge:function(a,b){for(var c=+b.length,d=0,e=a.length;d<c;d++)a[e++]=b[d];return a.length=e,a},grep:function(a,b,c){for(var d,e=[],f=0,g=a.length,h=!c;f<g;f++)d=!b(a[f],f),d!==h&&e.push(a[f]);return e},map:function(a,b,c){var d,e,f=0,h=[];if(w(a))for(d=a.length;f<d;f++)e=b(a[f],f,c),null!=e&&h.push(e);else for(f in a)e=b(a[f],f,c),null!=e&&h.push(e);return g.apply([],h)},guid:1,proxy:function(a,b){var c,d,e;if("string"==typeof b&&(c=a[b],b=a,a=c),r.isFunction(a))return d=f.call(arguments,2),e=function(){return a.apply(b||this,d.concat(f.call(arguments)))},e.guid=a.guid=a.guid||r.guid++,e},now:Date.now,support:o}),"function"==typeof Symbol&&(r.fn[Symbol.iterator]=c[Symbol.iterator]),r.each("Boolean Number String Function Array Date RegExp Object Error Symbol".split(" "),function(a,b){j["[object "+b+"]"]=b.toLowerCase()});function w(a){var b=!!a&&"length"in a&&a.length,c=r.type(a);return"function"!==c&&!r.isWindow(a)&&("array"===c||0===b||"number"==typeof b&&b>0&&b-1 in a)}var x=function(a){var b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u="sizzle"+1*new Date,v=a.document,w=0,x=0,y=ha(),z=ha(),A=ha(),B=function(a,b){return a===b&&(l=!0),0},C={}.hasOwnProperty,D=[],E=D.pop,F=D.push,G=D.push,H=D.slice,I=function(a,b){for(var c=0,d=a.length;c<d;c++)if(a[c]===b)return c;return-1},J="checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",K="[\\x20\\t\\r\\n\\f]",L="(?:\\\\.|[\\w-]|[^\0-\\xa0])+",M="\\["+K+"*("+L+")(?:"+K+"*([*^$|!~]?=)"+K+"*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|("+L+"))|)"+K+"*\\]",N=":("+L+")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|"+M+")*)|.*)\\)|)",O=new RegExp(K+"+","g"),P=new RegExp("^"+K+"+|((?:^|[^\\\\])(?:\\\\.)*)"+K+"+$","g"),Q=new RegExp("^"+K+"*,"+K+"*"),R=new RegExp("^"+K+"*([>+~]|"+K+")"+K+"*"),S=new RegExp("="+K+"*([^\\]'\"]*?)"+K+"*\\]","g"),T=new RegExp(N),U=new RegExp("^"+L+"$"),V={ID:new RegExp("^#("+L+")"),CLASS:new RegExp("^\\.("+L+")"),TAG:new RegExp("^("+L+"|[*])"),ATTR:new RegExp("^"+M),PSEUDO:new RegExp("^"+N),CHILD:new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\("+K+"*(even|odd|(([+-]|)(\\d*)n|)"+K+"*(?:([+-]|)"+K+"*(\\d+)|))"+K+"*\\)|)","i"),bool:new RegExp("^(?:"+J+")$","i"),needsContext:new RegExp("^"+K+"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\("+K+"*((?:-\\d)?\\d*)"+K+"*\\)|)(?=[^-]|$)","i")},W=/^(?:input|select|textarea|button)$/i,X=/^h\d$/i,Y=/^[^{]+\{\s*\[native \w/,Z=/^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,$=/[+~]/,_=new RegExp("\\\\([\\da-f]{1,6}"+K+"?|("+K+")|.)","ig"),aa=function(a,b,c){var d="0x"+b-65536;return d!==d||c?b:d<0?String.fromCharCode(d+65536):String.fromCharCode(d>>10|55296,1023&d|56320)},ba=/([\0-\x1f\x7f]|^-?\d)|^-$|[^\x80-\uFFFF\w-]/g,ca=function(a,b){return b?"\0"===a?"\ufffd":a.slice(0,-1)+"\\"+a.charCodeAt(a.length-1).toString(16)+" ":"\\"+a},da=function(){m()},ea=ta(function(a){return a.disabled===!0},{dir:"parentNode",next:"legend"});try{G.apply(D=H.call(v.childNodes),v.childNodes),D[v.childNodes.length].nodeType}catch(fa){G={apply:D.length?function(a,b){F.apply(a,H.call(b))}:function(a,b){var c=a.length,d=0;while(a[c++]=b[d++]);a.length=c-1}}}function ga(a,b,d,e){var f,h,j,k,l,o,r,s=b&&b.ownerDocument,w=b?b.nodeType:9;if(d=d||[],"string"!=typeof a||!a||1!==w&&9!==w&&11!==w)return d;if(!e&&((b?b.ownerDocument||b:v)!==n&&m(b),b=b||n,p)){if(11!==w&&(l=Z.exec(a)))if(f=l[1]){if(9===w){if(!(j=b.getElementById(f)))return d;if(j.id===f)return d.push(j),d}else if(s&&(j=s.getElementById(f))&&t(b,j)&&j.id===f)return d.push(j),d}else{if(l[2])return G.apply(d,b.getElementsByTagName(a)),d;if((f=l[3])&&c.getElementsByClassName&&b.getElementsByClassName)return G.apply(d,b.getElementsByClassName(f)),d}if(c.qsa&&!A[a+" "]&&(!q||!q.test(a))){if(1!==w)s=b,r=a;else if("object"!==b.nodeName.toLowerCase()){(k=b.getAttribute("id"))?k=k.replace(ba,ca):b.setAttribute("id",k=u),o=g(a),h=o.length;while(h--)o[h]="#"+k+" "+sa(o[h]);r=o.join(","),s=$.test(a)&&qa(b.parentNode)||b}if(r)try{return G.apply(d,s.querySelectorAll(r)),d}catch(x){}finally{k===u&&b.removeAttribute("id")}}}return i(a.replace(P,"$1"),b,d,e)}function ha(){var a=[];function b(c,e){return a.push(c+" ")>d.cacheLength&&delete b[a.shift()],b[c+" "]=e}return b}function ia(a){return a[u]=!0,a}function ja(a){var b=n.createElement("fieldset");try{return!!a(b)}catch(c){return!1}finally{b.parentNode&&b.parentNode.removeChild(b),b=null}}function ka(a,b){var c=a.split("|"),e=c.length;while(e--)d.attrHandle[c[e]]=b}function la(a,b){var c=b&&a,d=c&&1===a.nodeType&&1===b.nodeType&&a.sourceIndex-b.sourceIndex;if(d)return d;if(c)while(c=c.nextSibling)if(c===b)return-1;return a?1:-1}function ma(a){return function(b){var c=b.nodeName.toLowerCase();return"input"===c&&b.type===a}}function na(a){return function(b){var c=b.nodeName.toLowerCase();return("input"===c||"button"===c)&&b.type===a}}function oa(a){return function(b){return"label"in b&&b.disabled===a||"form"in b&&b.disabled===a||"form"in b&&b.disabled===!1&&(b.isDisabled===a||b.isDisabled!==!a&&("label"in b||!ea(b))!==a)}}function pa(a){return ia(function(b){return b=+b,ia(function(c,d){var e,f=a([],c.length,b),g=f.length;while(g--)c[e=f[g]]&&(c[e]=!(d[e]=c[e]))})})}function qa(a){return a&&"undefined"!=typeof a.getElementsByTagName&&a}c=ga.support={},f=ga.isXML=function(a){var b=a&&(a.ownerDocument||a).documentElement;return!!b&&"HTML"!==b.nodeName},m=ga.setDocument=function(a){var b,e,g=a?a.ownerDocument||a:v;return g!==n&&9===g.nodeType&&g.documentElement?(n=g,o=n.documentElement,p=!f(n),v!==n&&(e=n.defaultView)&&e.top!==e&&(e.addEventListener?e.addEventListener("unload",da,!1):e.attachEvent&&e.attachEvent("onunload",da)),c.attributes=ja(function(a){return a.className="i",!a.getAttribute("className")}),c.getElementsByTagName=ja(function(a){return a.appendChild(n.createComment("")),!a.getElementsByTagName("*").length}),c.getElementsByClassName=Y.test(n.getElementsByClassName),c.getById=ja(function(a){return o.appendChild(a).id=u,!n.getElementsByName||!n.getElementsByName(u).length}),c.getById?(d.find.ID=function(a,b){if("undefined"!=typeof b.getElementById&&p){var c=b.getElementById(a);return c?[c]:[]}},d.filter.ID=function(a){var b=a.replace(_,aa);return function(a){return a.getAttribute("id")===b}}):(delete d.find.ID,d.filter.ID=function(a){var b=a.replace(_,aa);return function(a){var c="undefined"!=typeof a.getAttributeNode&&a.getAttributeNode("id");return c&&c.value===b}}),d.find.TAG=c.getElementsByTagName?function(a,b){return"undefined"!=typeof b.getElementsByTagName?b.getElementsByTagName(a):c.qsa?b.querySelectorAll(a):void 0}:function(a,b){var c,d=[],e=0,f=b.getElementsByTagName(a);if("*"===a){while(c=f[e++])1===c.nodeType&&d.push(c);return d}return f},d.find.CLASS=c.getElementsByClassName&&function(a,b){if("undefined"!=typeof b.getElementsByClassName&&p)return b.getElementsByClassName(a)},r=[],q=[],(c.qsa=Y.test(n.querySelectorAll))&&(ja(function(a){o.appendChild(a).innerHTML="<a id='"+u+"'></a><select id='"+u+"-\r\\' msallowcapture=''><option selected=''></option></select>",a.querySelectorAll("[msallowcapture^='']").length&&q.push("[*^$]="+K+"*(?:''|\"\")"),a.querySelectorAll("[selected]").length||q.push("\\["+K+"*(?:value|"+J+")"),a.querySelectorAll("[id~="+u+"-]").length||q.push("~="),a.querySelectorAll(":checked").length||q.push(":checked"),a.querySelectorAll("a#"+u+"+*").length||q.push(".#.+[+~]")}),ja(function(a){a.innerHTML="<a href='' disabled='disabled'></a><select disabled='disabled'><option/></select>";var b=n.createElement("input");b.setAttribute("type","hidden"),a.appendChild(b).setAttribute("name","D"),a.querySelectorAll("[name=d]").length&&q.push("name"+K+"*[*^$|!~]?="),2!==a.querySelectorAll(":enabled").length&&q.push(":enabled",":disabled"),o.appendChild(a).disabled=!0,2!==a.querySelectorAll(":disabled").length&&q.push(":enabled",":disabled"),a.querySelectorAll("*,:x"),q.push(",.*:")})),(c.matchesSelector=Y.test(s=o.matches||o.webkitMatchesSelector||o.mozMatchesSelector||o.oMatchesSelector||o.msMatchesSelector))&&ja(function(a){c.disconnectedMatch=s.call(a,"*"),s.call(a,"[s!='']:x"),r.push("!=",N)}),q=q.length&&new RegExp(q.join("|")),r=r.length&&new RegExp(r.join("|")),b=Y.test(o.compareDocumentPosition),t=b||Y.test(o.contains)?function(a,b){var c=9===a.nodeType?a.documentElement:a,d=b&&b.parentNode;return a===d||!(!d||1!==d.nodeType||!(c.contains?c.contains(d):a.compareDocumentPosition&&16&a.compareDocumentPosition(d)))}:function(a,b){if(b)while(b=b.parentNode)if(b===a)return!0;return!1},B=b?function(a,b){if(a===b)return l=!0,0;var d=!a.compareDocumentPosition-!b.compareDocumentPosition;return d?d:(d=(a.ownerDocument||a)===(b.ownerDocument||b)?a.compareDocumentPosition(b):1,1&d||!c.sortDetached&&b.compareDocumentPosition(a)===d?a===n||a.ownerDocument===v&&t(v,a)?-1:b===n||b.ownerDocument===v&&t(v,b)?1:k?I(k,a)-I(k,b):0:4&d?-1:1)}:function(a,b){if(a===b)return l=!0,0;var c,d=0,e=a.parentNode,f=b.parentNode,g=[a],h=[b];if(!e||!f)return a===n?-1:b===n?1:e?-1:f?1:k?I(k,a)-I(k,b):0;if(e===f)return la(a,b);c=a;while(c=c.parentNode)g.unshift(c);c=b;while(c=c.parentNode)h.unshift(c);while(g[d]===h[d])d++;return d?la(g[d],h[d]):g[d]===v?-1:h[d]===v?1:0},n):n},ga.matches=function(a,b){return ga(a,null,null,b)},ga.matchesSelector=function(a,b){if((a.ownerDocument||a)!==n&&m(a),b=b.replace(S,"='$1']"),c.matchesSelector&&p&&!A[b+" "]&&(!r||!r.test(b))&&(!q||!q.test(b)))try{var d=s.call(a,b);if(d||c.disconnectedMatch||a.document&&11!==a.document.nodeType)return d}catch(e){}return ga(b,n,null,[a]).length>0},ga.contains=function(a,b){return(a.ownerDocument||a)!==n&&m(a),t(a,b)},ga.attr=function(a,b){(a.ownerDocument||a)!==n&&m(a);var e=d.attrHandle[b.toLowerCase()],f=e&&C.call(d.attrHandle,b.toLowerCase())?e(a,b,!p):void 0;return void 0!==f?f:c.attributes||!p?a.getAttribute(b):(f=a.getAttributeNode(b))&&f.specified?f.value:null},ga.escape=function(a){return(a+"").replace(ba,ca)},ga.error=function(a){throw new Error("Syntax error, unrecognized expression: "+a)},ga.uniqueSort=function(a){var b,d=[],e=0,f=0;if(l=!c.detectDuplicates,k=!c.sortStable&&a.slice(0),a.sort(B),l){while(b=a[f++])b===a[f]&&(e=d.push(f));while(e--)a.splice(d[e],1)}return k=null,a},e=ga.getText=function(a){var b,c="",d=0,f=a.nodeType;if(f){if(1===f||9===f||11===f){if("string"==typeof a.textContent)return a.textContent;for(a=a.firstChild;a;a=a.nextSibling)c+=e(a)}else if(3===f||4===f)return a.nodeValue}else while(b=a[d++])c+=e(b);return c},d=ga.selectors={cacheLength:50,createPseudo:ia,match:V,attrHandle:{},find:{},relative:{">":{dir:"parentNode",first:!0}," ":{dir:"parentNode"},"+":{dir:"previousSibling",first:!0},"~":{dir:"previousSibling"}},preFilter:{ATTR:function(a){return a[1]=a[1].replace(_,aa),a[3]=(a[3]||a[4]||a[5]||"").replace(_,aa),"~="===a[2]&&(a[3]=" "+a[3]+" "),a.slice(0,4)},CHILD:function(a){return a[1]=a[1].toLowerCase(),"nth"===a[1].slice(0,3)?(a[3]||ga.error(a[0]),a[4]=+(a[4]?a[5]+(a[6]||1):2*("even"===a[3]||"odd"===a[3])),a[5]=+(a[7]+a[8]||"odd"===a[3])):a[3]&&ga.error(a[0]),a},PSEUDO:function(a){var b,c=!a[6]&&a[2];return V.CHILD.test(a[0])?null:(a[3]?a[2]=a[4]||a[5]||"":c&&T.test(c)&&(b=g(c,!0))&&(b=c.indexOf(")",c.length-b)-c.length)&&(a[0]=a[0].slice(0,b),a[2]=c.slice(0,b)),a.slice(0,3))}},filter:{TAG:function(a){var b=a.replace(_,aa).toLowerCase();return"*"===a?function(){return!0}:function(a){return a.nodeName&&a.nodeName.toLowerCase()===b}},CLASS:function(a){var b=y[a+" "];return b||(b=new RegExp("(^|"+K+")"+a+"("+K+"|$)"))&&y(a,function(a){return b.test("string"==typeof a.className&&a.className||"undefined"!=typeof a.getAttribute&&a.getAttribute("class")||"")})},ATTR:function(a,b,c){return function(d){var e=ga.attr(d,a);return null==e?"!="===b:!b||(e+="","="===b?e===c:"!="===b?e!==c:"^="===b?c&&0===e.indexOf(c):"*="===b?c&&e.indexOf(c)>-1:"$="===b?c&&e.slice(-c.length)===c:"~="===b?(" "+e.replace(O," ")+" ").indexOf(c)>-1:"|="===b&&(e===c||e.slice(0,c.length+1)===c+"-"))}},CHILD:function(a,b,c,d,e){var f="nth"!==a.slice(0,3),g="last"!==a.slice(-4),h="of-type"===b;return 1===d&&0===e?function(a){return!!a.parentNode}:function(b,c,i){var j,k,l,m,n,o,p=f!==g?"nextSibling":"previousSibling",q=b.parentNode,r=h&&b.nodeName.toLowerCase(),s=!i&&!h,t=!1;if(q){if(f){while(p){m=b;while(m=m[p])if(h?m.nodeName.toLowerCase()===r:1===m.nodeType)return!1;o=p="only"===a&&!o&&"nextSibling"}return!0}if(o=[g?q.firstChild:q.lastChild],g&&s){m=q,l=m[u]||(m[u]={}),k=l[m.uniqueID]||(l[m.uniqueID]={}),j=k[a]||[],n=j[0]===w&&j[1],t=n&&j[2],m=n&&q.childNodes[n];while(m=++n&&m&&m[p]||(t=n=0)||o.pop())if(1===m.nodeType&&++t&&m===b){k[a]=[w,n,t];break}}else if(s&&(m=b,l=m[u]||(m[u]={}),k=l[m.uniqueID]||(l[m.uniqueID]={}),j=k[a]||[],n=j[0]===w&&j[1],t=n),t===!1)while(m=++n&&m&&m[p]||(t=n=0)||o.pop())if((h?m.nodeName.toLowerCase()===r:1===m.nodeType)&&++t&&(s&&(l=m[u]||(m[u]={}),k=l[m.uniqueID]||(l[m.uniqueID]={}),k[a]=[w,t]),m===b))break;return t-=e,t===d||t%d===0&&t/d>=0}}},PSEUDO:function(a,b){var c,e=d.pseudos[a]||d.setFilters[a.toLowerCase()]||ga.error("unsupported pseudo: "+a);return e[u]?e(b):e.length>1?(c=[a,a,"",b],d.setFilters.hasOwnProperty(a.toLowerCase())?ia(function(a,c){var d,f=e(a,b),g=f.length;while(g--)d=I(a,f[g]),a[d]=!(c[d]=f[g])}):function(a){return e(a,0,c)}):e}},pseudos:{not:ia(function(a){var b=[],c=[],d=h(a.replace(P,"$1"));return d[u]?ia(function(a,b,c,e){var f,g=d(a,null,e,[]),h=a.length;while(h--)(f=g[h])&&(a[h]=!(b[h]=f))}):function(a,e,f){return b[0]=a,d(b,null,f,c),b[0]=null,!c.pop()}}),has:ia(function(a){return function(b){return ga(a,b).length>0}}),contains:ia(function(a){return a=a.replace(_,aa),function(b){return(b.textContent||b.innerText||e(b)).indexOf(a)>-1}}),lang:ia(function(a){return U.test(a||"")||ga.error("unsupported lang: "+a),a=a.replace(_,aa).toLowerCase(),function(b){var c;do if(c=p?b.lang:b.getAttribute("xml:lang")||b.getAttribute("lang"))return c=c.toLowerCase(),c===a||0===c.indexOf(a+"-");while((b=b.parentNode)&&1===b.nodeType);return!1}}),target:function(b){var c=a.location&&a.location.hash;return c&&c.slice(1)===b.id},root:function(a){return a===o},focus:function(a){return a===n.activeElement&&(!n.hasFocus||n.hasFocus())&&!!(a.type||a.href||~a.tabIndex)},enabled:oa(!1),disabled:oa(!0),checked:function(a){var b=a.nodeName.toLowerCase();return"input"===b&&!!a.checked||"option"===b&&!!a.selected},selected:function(a){return a.parentNode&&a.parentNode.selectedIndex,a.selected===!0},empty:function(a){for(a=a.firstChild;a;a=a.nextSibling)if(a.nodeType<6)return!1;return!0},parent:function(a){return!d.pseudos.empty(a)},header:function(a){return X.test(a.nodeName)},input:function(a){return W.test(a.nodeName)},button:function(a){var b=a.nodeName.toLowerCase();return"input"===b&&"button"===a.type||"button"===b},text:function(a){var b;return"input"===a.nodeName.toLowerCase()&&"text"===a.type&&(null==(b=a.getAttribute("type"))||"text"===b.toLowerCase())},first:pa(function(){return[0]}),last:pa(function(a,b){return[b-1]}),eq:pa(function(a,b,c){return[c<0?c+b:c]}),even:pa(function(a,b){for(var c=0;c<b;c+=2)a.push(c);return a}),odd:pa(function(a,b){for(var c=1;c<b;c+=2)a.push(c);return a}),lt:pa(function(a,b,c){for(var d=c<0?c+b:c;--d>=0;)a.push(d);return a}),gt:pa(function(a,b,c){for(var d=c<0?c+b:c;++d<b;)a.push(d);return a})}},d.pseudos.nth=d.pseudos.eq;for(b in{radio:!0,checkbox:!0,file:!0,password:!0,image:!0})d.pseudos[b]=ma(b);for(b in{submit:!0,reset:!0})d.pseudos[b]=na(b);function ra(){}ra.prototype=d.filters=d.pseudos,d.setFilters=new ra,g=ga.tokenize=function(a,b){var c,e,f,g,h,i,j,k=z[a+" "];if(k)return b?0:k.slice(0);h=a,i=[],j=d.preFilter;while(h){c&&!(e=Q.exec(h))||(e&&(h=h.slice(e[0].length)||h),i.push(f=[])),c=!1,(e=R.exec(h))&&(c=e.shift(),f.push({value:c,type:e[0].replace(P," ")}),h=h.slice(c.length));for(g in d.filter)!(e=V[g].exec(h))||j[g]&&!(e=j[g](e))||(c=e.shift(),f.push({value:c,type:g,matches:e}),h=h.slice(c.length));if(!c)break}return b?h.length:h?ga.error(a):z(a,i).slice(0)};function sa(a){for(var b=0,c=a.length,d="";b<c;b++)d+=a[b].value;return d}function ta(a,b,c){var d=b.dir,e=b.next,f=e||d,g=c&&"parentNode"===f,h=x++;return b.first?function(b,c,e){while(b=b[d])if(1===b.nodeType||g)return a(b,c,e)}:function(b,c,i){var j,k,l,m=[w,h];if(i){while(b=b[d])if((1===b.nodeType||g)&&a(b,c,i))return!0}else while(b=b[d])if(1===b.nodeType||g)if(l=b[u]||(b[u]={}),k=l[b.uniqueID]||(l[b.uniqueID]={}),e&&e===b.nodeName.toLowerCase())b=b[d]||b;else{if((j=k[f])&&j[0]===w&&j[1]===h)return m[2]=j[2];if(k[f]=m,m[2]=a(b,c,i))return!0}}}function ua(a){return a.length>1?function(b,c,d){var e=a.length;while(e--)if(!a[e](b,c,d))return!1;return!0}:a[0]}function va(a,b,c){for(var d=0,e=b.length;d<e;d++)ga(a,b[d],c);return c}function wa(a,b,c,d,e){for(var f,g=[],h=0,i=a.length,j=null!=b;h<i;h++)(f=a[h])&&(c&&!c(f,d,e)||(g.push(f),j&&b.push(h)));return g}function xa(a,b,c,d,e,f){return d&&!d[u]&&(d=xa(d)),e&&!e[u]&&(e=xa(e,f)),ia(function(f,g,h,i){var j,k,l,m=[],n=[],o=g.length,p=f||va(b||"*",h.nodeType?[h]:h,[]),q=!a||!f&&b?p:wa(p,m,a,h,i),r=c?e||(f?a:o||d)?[]:g:q;if(c&&c(q,r,h,i),d){j=wa(r,n),d(j,[],h,i),k=j.length;while(k--)(l=j[k])&&(r[n[k]]=!(q[n[k]]=l))}if(f){if(e||a){if(e){j=[],k=r.length;while(k--)(l=r[k])&&j.push(q[k]=l);e(null,r=[],j,i)}k=r.length;while(k--)(l=r[k])&&(j=e?I(f,l):m[k])>-1&&(f[j]=!(g[j]=l))}}else r=wa(r===g?r.splice(o,r.length):r),e?e(null,g,r,i):G.apply(g,r)})}function ya(a){for(var b,c,e,f=a.length,g=d.relative[a[0].type],h=g||d.relative[" "],i=g?1:0,k=ta(function(a){return a===b},h,!0),l=ta(function(a){return I(b,a)>-1},h,!0),m=[function(a,c,d){var e=!g&&(d||c!==j)||((b=c).nodeType?k(a,c,d):l(a,c,d));return b=null,e}];i<f;i++)if(c=d.relative[a[i].type])m=[ta(ua(m),c)];else{if(c=d.filter[a[i].type].apply(null,a[i].matches),c[u]){for(e=++i;e<f;e++)if(d.relative[a[e].type])break;return xa(i>1&&ua(m),i>1&&sa(a.slice(0,i-1).concat({value:" "===a[i-2].type?"*":""})).replace(P,"$1"),c,i<e&&ya(a.slice(i,e)),e<f&&ya(a=a.slice(e)),e<f&&sa(a))}m.push(c)}return ua(m)}function za(a,b){var c=b.length>0,e=a.length>0,f=function(f,g,h,i,k){var l,o,q,r=0,s="0",t=f&&[],u=[],v=j,x=f||e&&d.find.TAG("*",k),y=w+=null==v?1:Math.random()||.1,z=x.length;for(k&&(j=g===n||g||k);s!==z&&null!=(l=x[s]);s++){if(e&&l){o=0,g||l.ownerDocument===n||(m(l),h=!p);while(q=a[o++])if(q(l,g||n,h)){i.push(l);break}k&&(w=y)}c&&((l=!q&&l)&&r--,f&&t.push(l))}if(r+=s,c&&s!==r){o=0;while(q=b[o++])q(t,u,g,h);if(f){if(r>0)while(s--)t[s]||u[s]||(u[s]=E.call(i));u=wa(u)}G.apply(i,u),k&&!f&&u.length>0&&r+b.length>1&&ga.uniqueSort(i)}return k&&(w=y,j=v),t};return c?ia(f):f}return h=ga.compile=function(a,b){var c,d=[],e=[],f=A[a+" "];if(!f){b||(b=g(a)),c=b.length;while(c--)f=ya(b[c]),f[u]?d.push(f):e.push(f);f=A(a,za(e,d)),f.selector=a}return f},i=ga.select=function(a,b,e,f){var i,j,k,l,m,n="function"==typeof a&&a,o=!f&&g(a=n.selector||a);if(e=e||[],1===o.length){if(j=o[0]=o[0].slice(0),j.length>2&&"ID"===(k=j[0]).type&&c.getById&&9===b.nodeType&&p&&d.relative[j[1].type]){if(b=(d.find.ID(k.matches[0].replace(_,aa),b)||[])[0],!b)return e;n&&(b=b.parentNode),a=a.slice(j.shift().value.length)}i=V.needsContext.test(a)?0:j.length;while(i--){if(k=j[i],d.relative[l=k.type])break;if((m=d.find[l])&&(f=m(k.matches[0].replace(_,aa),$.test(j[0].type)&&qa(b.parentNode)||b))){if(j.splice(i,1),a=f.length&&sa(j),!a)return G.apply(e,f),e;break}}}return(n||h(a,o))(f,b,!p,e,!b||$.test(a)&&qa(b.parentNode)||b),e},c.sortStable=u.split("").sort(B).join("")===u,c.detectDuplicates=!!l,m(),c.sortDetached=ja(function(a){return 1&a.compareDocumentPosition(n.createElement("fieldset"))}),ja(function(a){return a.innerHTML="<a href='#'></a>","#"===a.firstChild.getAttribute("href")})||ka("type|href|height|width",function(a,b,c){if(!c)return a.getAttribute(b,"type"===b.toLowerCase()?1:2)}),c.attributes&&ja(function(a){return a.innerHTML="<input/>",a.firstChild.setAttribute("value",""),""===a.firstChild.getAttribute("value")})||ka("value",function(a,b,c){if(!c&&"input"===a.nodeName.toLowerCase())return a.defaultValue}),ja(function(a){return null==a.getAttribute("disabled")})||ka(J,function(a,b,c){var d;if(!c)return a[b]===!0?b.toLowerCase():(d=a.getAttributeNode(b))&&d.specified?d.value:null}),ga}(a);r.find=x,r.expr=x.selectors,r.expr[":"]=r.expr.pseudos,r.uniqueSort=r.unique=x.uniqueSort,r.text=x.getText,r.isXMLDoc=x.isXML,r.contains=x.contains,r.escapeSelector=x.escape;var y=function(a,b,c){var d=[],e=void 0!==c;while((a=a[b])&&9!==a.nodeType)if(1===a.nodeType){if(e&&r(a).is(c))break;d.push(a)}return d},z=function(a,b){for(var c=[];a;a=a.nextSibling)1===a.nodeType&&a!==b&&c.push(a);return c},A=r.expr.match.needsContext,B=/^<([a-z][^\/\0>:\x20\t\r\n\f]*)[\x20\t\r\n\f]*\/?>(?:<\/\1>|)$/i,C=/^.[^:#\[\.,]*$/;function D(a,b,c){if(r.isFunction(b))return r.grep(a,function(a,d){return!!b.call(a,d,a)!==c});if(b.nodeType)return r.grep(a,function(a){return a===b!==c});if("string"==typeof b){if(C.test(b))return r.filter(b,a,c);b=r.filter(b,a)}return r.grep(a,function(a){return i.call(b,a)>-1!==c&&1===a.nodeType})}r.filter=function(a,b,c){var d=b[0];return c&&(a=":not("+a+")"),1===b.length&&1===d.nodeType?r.find.matchesSelector(d,a)?[d]:[]:r.find.matches(a,r.grep(b,function(a){return 1===a.nodeType}))},r.fn.extend({find:function(a){var b,c,d=this.length,e=this;if("string"!=typeof a)return this.pushStack(r(a).filter(function(){for(b=0;b<d;b++)if(r.contains(e[b],this))return!0}));for(c=this.pushStack([]),b=0;b<d;b++)r.find(a,e[b],c);return d>1?r.uniqueSort(c):c},filter:function(a){return this.pushStack(D(this,a||[],!1))},not:function(a){return this.pushStack(D(this,a||[],!0))},is:function(a){return!!D(this,"string"==typeof a&&A.test(a)?r(a):a||[],!1).length}});var E,F=/^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/,G=r.fn.init=function(a,b,c){var e,f;if(!a)return this;if(c=c||E,"string"==typeof a){if(e="<"===a[0]&&">"===a[a.length-1]&&a.length>=3?[null,a,null]:F.exec(a),!e||!e[1]&&b)return!b||b.jquery?(b||c).find(a):this.constructor(b).find(a);if(e[1]){if(b=b instanceof r?b[0]:b,r.merge(this,r.parseHTML(e[1],b&&b.nodeType?b.ownerDocument||b:d,!0)),B.test(e[1])&&r.isPlainObject(b))for(e in b)r.isFunction(this[e])?this[e](b[e]):this.attr(e,b[e]);return this}return f=d.getElementById(e[2]),f&&(this[0]=f,this.length=1),this}return a.nodeType?(this[0]=a,this.length=1,this):r.isFunction(a)?void 0!==c.ready?c.ready(a):a(r):r.makeArray(a,this)};G.prototype=r.fn,E=r(d);var H=/^(?:parents|prev(?:Until|All))/,I={children:!0,contents:!0,next:!0,prev:!0};r.fn.extend({has:function(a){var b=r(a,this),c=b.length;return this.filter(function(){for(var a=0;a<c;a++)if(r.contains(this,b[a]))return!0})},closest:function(a,b){var c,d=0,e=this.length,f=[],g="string"!=typeof a&&r(a);if(!A.test(a))for(;d<e;d++)for(c=this[d];c&&c!==b;c=c.parentNode)if(c.nodeType<11&&(g?g.index(c)>-1:1===c.nodeType&&r.find.matchesSelector(c,a))){f.push(c);break}return this.pushStack(f.length>1?r.uniqueSort(f):f)},index:function(a){return a?"string"==typeof a?i.call(r(a),this[0]):i.call(this,a.jquery?a[0]:a):this[0]&&this[0].parentNode?this.first().prevAll().length:-1},add:function(a,b){return this.pushStack(r.uniqueSort(r.merge(this.get(),r(a,b))))},addBack:function(a){return this.add(null==a?this.prevObject:this.prevObject.filter(a))}});function J(a,b){while((a=a[b])&&1!==a.nodeType);return a}r.each({parent:function(a){var b=a.parentNode;return b&&11!==b.nodeType?b:null},parents:function(a){return y(a,"parentNode")},parentsUntil:function(a,b,c){return y(a,"parentNode",c)},next:function(a){return J(a,"nextSibling")},prev:function(a){return J(a,"previousSibling")},nextAll:function(a){return y(a,"nextSibling")},prevAll:function(a){return y(a,"previousSibling")},nextUntil:function(a,b,c){return y(a,"nextSibling",c)},prevUntil:function(a,b,c){return y(a,"previousSibling",c)},siblings:function(a){return z((a.parentNode||{}).firstChild,a)},children:function(a){return z(a.firstChild)},contents:function(a){return a.contentDocument||r.merge([],a.childNodes)}},function(a,b){r.fn[a]=function(c,d){var e=r.map(this,b,c);return"Until"!==a.slice(-5)&&(d=c),d&&"string"==typeof d&&(e=r.filter(d,e)),this.length>1&&(I[a]||r.uniqueSort(e),H.test(a)&&e.reverse()),this.pushStack(e)}});var K=/\S+/g;function L(a){var b={};return r.each(a.match(K)||[],function(a,c){b[c]=!0}),b}r.Callbacks=function(a){a="string"==typeof a?L(a):r.extend({},a);var b,c,d,e,f=[],g=[],h=-1,i=function(){for(e=a.once,d=b=!0;g.length;h=-1){c=g.shift();while(++h<f.length)f[h].apply(c[0],c[1])===!1&&a.stopOnFalse&&(h=f.length,c=!1)}a.memory||(c=!1),b=!1,e&&(f=c?[]:"")},j={add:function(){return f&&(c&&!b&&(h=f.length-1,g.push(c)),function d(b){r.each(b,function(b,c){r.isFunction(c)?a.unique&&j.has(c)||f.push(c):c&&c.length&&"string"!==r.type(c)&&d(c)})}(arguments),c&&!b&&i()),this},remove:function(){return r.each(arguments,function(a,b){var c;while((c=r.inArray(b,f,c))>-1)f.splice(c,1),c<=h&&h--}),this},has:function(a){return a?r.inArray(a,f)>-1:f.length>0},empty:function(){return f&&(f=[]),this},disable:function(){return e=g=[],f=c="",this},disabled:function(){return!f},lock:function(){return e=g=[],c||b||(f=c=""),this},locked:function(){return!!e},fireWith:function(a,c){return e||(c=c||[],c=[a,c.slice?c.slice():c],g.push(c),b||i()),this},fire:function(){return j.fireWith(this,arguments),this},fired:function(){return!!d}};return j};function M(a){return a}function N(a){throw a}function O(a,b,c){var d;try{a&&r.isFunction(d=a.promise)?d.call(a).done(b).fail(c):a&&r.isFunction(d=a.then)?d.call(a,b,c):b.call(void 0,a)}catch(a){c.call(void 0,a)}}r.extend({Deferred:function(b){var c=[["notify","progress",r.Callbacks("memory"),r.Callbacks("memory"),2],["resolve","done",r.Callbacks("once memory"),r.Callbacks("once memory"),0,"resolved"],["reject","fail",r.Callbacks("once memory"),r.Callbacks("once memory"),1,"rejected"]],d="pending",e={state:function(){return d},always:function(){return f.done(arguments).fail(arguments),this},"catch":function(a){return e.then(null,a)},pipe:function(){var a=arguments;return r.Deferred(function(b){r.each(c,function(c,d){var e=r.isFunction(a[d[4]])&&a[d[4]];f[d[1]](function(){var a=e&&e.apply(this,arguments);a&&r.isFunction(a.promise)?a.promise().progress(b.notify).done(b.resolve).fail(b.reject):b[d[0]+"With"](this,e?[a]:arguments)})}),a=null}).promise()},then:function(b,d,e){var f=0;function g(b,c,d,e){return function(){var h=this,i=arguments,j=function(){var a,j;if(!(b<f)){if(a=d.apply(h,i),a===c.promise())throw new TypeError("Thenable self-resolution");j=a&&("object"==typeof a||"function"==typeof a)&&a.then,r.isFunction(j)?e?j.call(a,g(f,c,M,e),g(f,c,N,e)):(f++,j.call(a,g(f,c,M,e),g(f,c,N,e),g(f,c,M,c.notifyWith))):(d!==M&&(h=void 0,i=[a]),(e||c.resolveWith)(h,i))}},k=e?j:function(){try{j()}catch(a){r.Deferred.exceptionHook&&r.Deferred.exceptionHook(a,k.stackTrace),b+1>=f&&(d!==N&&(h=void 0,i=[a]),c.rejectWith(h,i))}};b?k():(r.Deferred.getStackHook&&(k.stackTrace=r.Deferred.getStackHook()),a.setTimeout(k))}}return r.Deferred(function(a){c[0][3].add(g(0,a,r.isFunction(e)?e:M,a.notifyWith)),c[1][3].add(g(0,a,r.isFunction(b)?b:M)),c[2][3].add(g(0,a,r.isFunction(d)?d:N))}).promise()},promise:function(a){return null!=a?r.extend(a,e):e}},f={};return r.each(c,function(a,b){var g=b[2],h=b[5];e[b[1]]=g.add,h&&g.add(function(){d=h},c[3-a][2].disable,c[0][2].lock),g.add(b[3].fire),f[b[0]]=function(){return f[b[0]+"With"](this===f?void 0:this,arguments),this},f[b[0]+"With"]=g.fireWith}),e.promise(f),b&&b.call(f,f),f},when:function(a){var b=arguments.length,c=b,d=Array(c),e=f.call(arguments),g=r.Deferred(),h=function(a){return function(c){d[a]=this,e[a]=arguments.length>1?f.call(arguments):c,--b||g.resolveWith(d,e)}};if(b<=1&&(O(a,g.done(h(c)).resolve,g.reject),"pending"===g.state()||r.isFunction(e[c]&&e[c].then)))return g.then();while(c--)O(e[c],h(c),g.reject);return g.promise()}});var P=/^(Eval|Internal|Range|Reference|Syntax|Type|URI)Error$/;r.Deferred.exceptionHook=function(b,c){a.console&&a.console.warn&&b&&P.test(b.name)&&a.console.warn("jQuery.Deferred exception: "+b.message,b.stack,c)},r.readyException=function(b){a.setTimeout(function(){throw b})};var Q=r.Deferred();r.fn.ready=function(a){return Q.then(a)["catch"](function(a){r.readyException(a)}),this},r.extend({isReady:!1,readyWait:1,holdReady:function(a){a?r.readyWait++:r.ready(!0)},ready:function(a){(a===!0?--r.readyWait:r.isReady)||(r.isReady=!0,a!==!0&&--r.readyWait>0||Q.resolveWith(d,[r]))}}),r.ready.then=Q.then;function R(){d.removeEventListener("DOMContentLoaded",R),a.removeEventListener("load",R),r.ready()}"complete"===d.readyState||"loading"!==d.readyState&&!d.documentElement.doScroll?a.setTimeout(r.ready):(d.addEventListener("DOMContentLoaded",R),a.addEventListener("load",R));var S=function(a,b,c,d,e,f,g){var h=0,i=a.length,j=null==c;if("object"===r.type(c)){e=!0;for(h in c)S(a,b,h,c[h],!0,f,g)}else if(void 0!==d&&(e=!0,
r.isFunction(d)||(g=!0),j&&(g?(b.call(a,d),b=null):(j=b,b=function(a,b,c){return j.call(r(a),c)})),b))for(;h<i;h++)b(a[h],c,g?d:d.call(a[h],h,b(a[h],c)));return e?a:j?b.call(a):i?b(a[0],c):f},T=function(a){return 1===a.nodeType||9===a.nodeType||!+a.nodeType};function U(){this.expando=r.expando+U.uid++}U.uid=1,U.prototype={cache:function(a){var b=a[this.expando];return b||(b={},T(a)&&(a.nodeType?a[this.expando]=b:Object.defineProperty(a,this.expando,{value:b,configurable:!0}))),b},set:function(a,b,c){var d,e=this.cache(a);if("string"==typeof b)e[r.camelCase(b)]=c;else for(d in b)e[r.camelCase(d)]=b[d];return e},get:function(a,b){return void 0===b?this.cache(a):a[this.expando]&&a[this.expando][r.camelCase(b)]},access:function(a,b,c){return void 0===b||b&&"string"==typeof b&&void 0===c?this.get(a,b):(this.set(a,b,c),void 0!==c?c:b)},remove:function(a,b){var c,d=a[this.expando];if(void 0!==d){if(void 0!==b){r.isArray(b)?b=b.map(r.camelCase):(b=r.camelCase(b),b=b in d?[b]:b.match(K)||[]),c=b.length;while(c--)delete d[b[c]]}(void 0===b||r.isEmptyObject(d))&&(a.nodeType?a[this.expando]=void 0:delete a[this.expando])}},hasData:function(a){var b=a[this.expando];return void 0!==b&&!r.isEmptyObject(b)}};var V=new U,W=new U,X=/^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,Y=/[A-Z]/g;function Z(a,b,c){var d;if(void 0===c&&1===a.nodeType)if(d="data-"+b.replace(Y,"-$&").toLowerCase(),c=a.getAttribute(d),"string"==typeof c){try{c="true"===c||"false"!==c&&("null"===c?null:+c+""===c?+c:X.test(c)?JSON.parse(c):c)}catch(e){}W.set(a,b,c)}else c=void 0;return c}r.extend({hasData:function(a){return W.hasData(a)||V.hasData(a)},data:function(a,b,c){return W.access(a,b,c)},removeData:function(a,b){W.remove(a,b)},_data:function(a,b,c){return V.access(a,b,c)},_removeData:function(a,b){V.remove(a,b)}}),r.fn.extend({data:function(a,b){var c,d,e,f=this[0],g=f&&f.attributes;if(void 0===a){if(this.length&&(e=W.get(f),1===f.nodeType&&!V.get(f,"hasDataAttrs"))){c=g.length;while(c--)g[c]&&(d=g[c].name,0===d.indexOf("data-")&&(d=r.camelCase(d.slice(5)),Z(f,d,e[d])));V.set(f,"hasDataAttrs",!0)}return e}return"object"==typeof a?this.each(function(){W.set(this,a)}):S(this,function(b){var c;if(f&&void 0===b){if(c=W.get(f,a),void 0!==c)return c;if(c=Z(f,a),void 0!==c)return c}else this.each(function(){W.set(this,a,b)})},null,b,arguments.length>1,null,!0)},removeData:function(a){return this.each(function(){W.remove(this,a)})}}),r.extend({queue:function(a,b,c){var d;if(a)return b=(b||"fx")+"queue",d=V.get(a,b),c&&(!d||r.isArray(c)?d=V.access(a,b,r.makeArray(c)):d.push(c)),d||[]},dequeue:function(a,b){b=b||"fx";var c=r.queue(a,b),d=c.length,e=c.shift(),f=r._queueHooks(a,b),g=function(){r.dequeue(a,b)};"inprogress"===e&&(e=c.shift(),d--),e&&("fx"===b&&c.unshift("inprogress"),delete f.stop,e.call(a,g,f)),!d&&f&&f.empty.fire()},_queueHooks:function(a,b){var c=b+"queueHooks";return V.get(a,c)||V.access(a,c,{empty:r.Callbacks("once memory").add(function(){V.remove(a,[b+"queue",c])})})}}),r.fn.extend({queue:function(a,b){var c=2;return"string"!=typeof a&&(b=a,a="fx",c--),arguments.length<c?r.queue(this[0],a):void 0===b?this:this.each(function(){var c=r.queue(this,a,b);r._queueHooks(this,a),"fx"===a&&"inprogress"!==c[0]&&r.dequeue(this,a)})},dequeue:function(a){return this.each(function(){r.dequeue(this,a)})},clearQueue:function(a){return this.queue(a||"fx",[])},promise:function(a,b){var c,d=1,e=r.Deferred(),f=this,g=this.length,h=function(){--d||e.resolveWith(f,[f])};"string"!=typeof a&&(b=a,a=void 0),a=a||"fx";while(g--)c=V.get(f[g],a+"queueHooks"),c&&c.empty&&(d++,c.empty.add(h));return h(),e.promise(b)}});var $=/[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,_=new RegExp("^(?:([+-])=|)("+$+")([a-z%]*)$","i"),aa=["Top","Right","Bottom","Left"],ba=function(a,b){return a=b||a,"none"===a.style.display||""===a.style.display&&r.contains(a.ownerDocument,a)&&"none"===r.css(a,"display")},ca=function(a,b,c,d){var e,f,g={};for(f in b)g[f]=a.style[f],a.style[f]=b[f];e=c.apply(a,d||[]);for(f in b)a.style[f]=g[f];return e};function da(a,b,c,d){var e,f=1,g=20,h=d?function(){return d.cur()}:function(){return r.css(a,b,"")},i=h(),j=c&&c[3]||(r.cssNumber[b]?"":"px"),k=(r.cssNumber[b]||"px"!==j&&+i)&&_.exec(r.css(a,b));if(k&&k[3]!==j){j=j||k[3],c=c||[],k=+i||1;do f=f||".5",k/=f,r.style(a,b,k+j);while(f!==(f=h()/i)&&1!==f&&--g)}return c&&(k=+k||+i||0,e=c[1]?k+(c[1]+1)*c[2]:+c[2],d&&(d.unit=j,d.start=k,d.end=e)),e}var ea={};function fa(a){var b,c=a.ownerDocument,d=a.nodeName,e=ea[d];return e?e:(b=c.body.appendChild(c.createElement(d)),e=r.css(b,"display"),b.parentNode.removeChild(b),"none"===e&&(e="block"),ea[d]=e,e)}function ga(a,b){for(var c,d,e=[],f=0,g=a.length;f<g;f++)d=a[f],d.style&&(c=d.style.display,b?("none"===c&&(e[f]=V.get(d,"display")||null,e[f]||(d.style.display="")),""===d.style.display&&ba(d)&&(e[f]=fa(d))):"none"!==c&&(e[f]="none",V.set(d,"display",c)));for(f=0;f<g;f++)null!=e[f]&&(a[f].style.display=e[f]);return a}r.fn.extend({show:function(){return ga(this,!0)},hide:function(){return ga(this)},toggle:function(a){return"boolean"==typeof a?a?this.show():this.hide():this.each(function(){ba(this)?r(this).show():r(this).hide()})}});var ha=/^(?:checkbox|radio)$/i,ia=/<([a-z][^\/\0>\x20\t\r\n\f]+)/i,ja=/^$|\/(?:java|ecma)script/i,ka={option:[1,"<select multiple='multiple'>","</select>"],thead:[1,"<table>","</table>"],col:[2,"<table><colgroup>","</colgroup></table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:[0,"",""]};ka.optgroup=ka.option,ka.tbody=ka.tfoot=ka.colgroup=ka.caption=ka.thead,ka.th=ka.td;function la(a,b){var c="undefined"!=typeof a.getElementsByTagName?a.getElementsByTagName(b||"*"):"undefined"!=typeof a.querySelectorAll?a.querySelectorAll(b||"*"):[];return void 0===b||b&&r.nodeName(a,b)?r.merge([a],c):c}function ma(a,b){for(var c=0,d=a.length;c<d;c++)V.set(a[c],"globalEval",!b||V.get(b[c],"globalEval"))}var na=/<|&#?\w+;/;function oa(a,b,c,d,e){for(var f,g,h,i,j,k,l=b.createDocumentFragment(),m=[],n=0,o=a.length;n<o;n++)if(f=a[n],f||0===f)if("object"===r.type(f))r.merge(m,f.nodeType?[f]:f);else if(na.test(f)){g=g||l.appendChild(b.createElement("div")),h=(ia.exec(f)||["",""])[1].toLowerCase(),i=ka[h]||ka._default,g.innerHTML=i[1]+r.htmlPrefilter(f)+i[2],k=i[0];while(k--)g=g.lastChild;r.merge(m,g.childNodes),g=l.firstChild,g.textContent=""}else m.push(b.createTextNode(f));l.textContent="",n=0;while(f=m[n++])if(d&&r.inArray(f,d)>-1)e&&e.push(f);else if(j=r.contains(f.ownerDocument,f),g=la(l.appendChild(f),"script"),j&&ma(g),c){k=0;while(f=g[k++])ja.test(f.type||"")&&c.push(f)}return l}!function(){var a=d.createDocumentFragment(),b=a.appendChild(d.createElement("div")),c=d.createElement("input");c.setAttribute("type","radio"),c.setAttribute("checked","checked"),c.setAttribute("name","t"),b.appendChild(c),o.checkClone=b.cloneNode(!0).cloneNode(!0).lastChild.checked,b.innerHTML="<textarea>x</textarea>",o.noCloneChecked=!!b.cloneNode(!0).lastChild.defaultValue}();var pa=d.documentElement,qa=/^key/,ra=/^(?:mouse|pointer|contextmenu|drag|drop)|click/,sa=/^([^.]*)(?:\.(.+)|)/;function ta(){return!0}function ua(){return!1}function va(){try{return d.activeElement}catch(a){}}function wa(a,b,c,d,e,f){var g,h;if("object"==typeof b){"string"!=typeof c&&(d=d||c,c=void 0);for(h in b)wa(a,h,c,d,b[h],f);return a}if(null==d&&null==e?(e=c,d=c=void 0):null==e&&("string"==typeof c?(e=d,d=void 0):(e=d,d=c,c=void 0)),e===!1)e=ua;else if(!e)return a;return 1===f&&(g=e,e=function(a){return r().off(a),g.apply(this,arguments)},e.guid=g.guid||(g.guid=r.guid++)),a.each(function(){r.event.add(this,b,e,d,c)})}r.event={global:{},add:function(a,b,c,d,e){var f,g,h,i,j,k,l,m,n,o,p,q=V.get(a);if(q){c.handler&&(f=c,c=f.handler,e=f.selector),e&&r.find.matchesSelector(pa,e),c.guid||(c.guid=r.guid++),(i=q.events)||(i=q.events={}),(g=q.handle)||(g=q.handle=function(b){return"undefined"!=typeof r&&r.event.triggered!==b.type?r.event.dispatch.apply(a,arguments):void 0}),b=(b||"").match(K)||[""],j=b.length;while(j--)h=sa.exec(b[j])||[],n=p=h[1],o=(h[2]||"").split(".").sort(),n&&(l=r.event.special[n]||{},n=(e?l.delegateType:l.bindType)||n,l=r.event.special[n]||{},k=r.extend({type:n,origType:p,data:d,handler:c,guid:c.guid,selector:e,needsContext:e&&r.expr.match.needsContext.test(e),namespace:o.join(".")},f),(m=i[n])||(m=i[n]=[],m.delegateCount=0,l.setup&&l.setup.call(a,d,o,g)!==!1||a.addEventListener&&a.addEventListener(n,g)),l.add&&(l.add.call(a,k),k.handler.guid||(k.handler.guid=c.guid)),e?m.splice(m.delegateCount++,0,k):m.push(k),r.event.global[n]=!0)}},remove:function(a,b,c,d,e){var f,g,h,i,j,k,l,m,n,o,p,q=V.hasData(a)&&V.get(a);if(q&&(i=q.events)){b=(b||"").match(K)||[""],j=b.length;while(j--)if(h=sa.exec(b[j])||[],n=p=h[1],o=(h[2]||"").split(".").sort(),n){l=r.event.special[n]||{},n=(d?l.delegateType:l.bindType)||n,m=i[n]||[],h=h[2]&&new RegExp("(^|\\.)"+o.join("\\.(?:.*\\.|)")+"(\\.|$)"),g=f=m.length;while(f--)k=m[f],!e&&p!==k.origType||c&&c.guid!==k.guid||h&&!h.test(k.namespace)||d&&d!==k.selector&&("**"!==d||!k.selector)||(m.splice(f,1),k.selector&&m.delegateCount--,l.remove&&l.remove.call(a,k));g&&!m.length&&(l.teardown&&l.teardown.call(a,o,q.handle)!==!1||r.removeEvent(a,n,q.handle),delete i[n])}else for(n in i)r.event.remove(a,n+b[j],c,d,!0);r.isEmptyObject(i)&&V.remove(a,"handle events")}},dispatch:function(a){var b=r.event.fix(a),c,d,e,f,g,h,i=new Array(arguments.length),j=(V.get(this,"events")||{})[b.type]||[],k=r.event.special[b.type]||{};for(i[0]=b,c=1;c<arguments.length;c++)i[c]=arguments[c];if(b.delegateTarget=this,!k.preDispatch||k.preDispatch.call(this,b)!==!1){h=r.event.handlers.call(this,b,j),c=0;while((f=h[c++])&&!b.isPropagationStopped()){b.currentTarget=f.elem,d=0;while((g=f.handlers[d++])&&!b.isImmediatePropagationStopped())b.rnamespace&&!b.rnamespace.test(g.namespace)||(b.handleObj=g,b.data=g.data,e=((r.event.special[g.origType]||{}).handle||g.handler).apply(f.elem,i),void 0!==e&&(b.result=e)===!1&&(b.preventDefault(),b.stopPropagation()))}return k.postDispatch&&k.postDispatch.call(this,b),b.result}},handlers:function(a,b){var c,d,e,f,g=[],h=b.delegateCount,i=a.target;if(h&&i.nodeType&&("click"!==a.type||isNaN(a.button)||a.button<1))for(;i!==this;i=i.parentNode||this)if(1===i.nodeType&&(i.disabled!==!0||"click"!==a.type)){for(d=[],c=0;c<h;c++)f=b[c],e=f.selector+" ",void 0===d[e]&&(d[e]=f.needsContext?r(e,this).index(i)>-1:r.find(e,this,null,[i]).length),d[e]&&d.push(f);d.length&&g.push({elem:i,handlers:d})}return h<b.length&&g.push({elem:this,handlers:b.slice(h)}),g},addProp:function(a,b){Object.defineProperty(r.Event.prototype,a,{enumerable:!0,configurable:!0,get:r.isFunction(b)?function(){if(this.originalEvent)return b(this.originalEvent)}:function(){if(this.originalEvent)return this.originalEvent[a]},set:function(b){Object.defineProperty(this,a,{enumerable:!0,configurable:!0,writable:!0,value:b})}})},fix:function(a){return a[r.expando]?a:new r.Event(a)},special:{load:{noBubble:!0},focus:{trigger:function(){if(this!==va()&&this.focus)return this.focus(),!1},delegateType:"focusin"},blur:{trigger:function(){if(this===va()&&this.blur)return this.blur(),!1},delegateType:"focusout"},click:{trigger:function(){if("checkbox"===this.type&&this.click&&r.nodeName(this,"input"))return this.click(),!1},_default:function(a){return r.nodeName(a.target,"a")}},beforeunload:{postDispatch:function(a){void 0!==a.result&&a.originalEvent&&(a.originalEvent.returnValue=a.result)}}}},r.removeEvent=function(a,b,c){a.removeEventListener&&a.removeEventListener(b,c)},r.Event=function(a,b){return this instanceof r.Event?(a&&a.type?(this.originalEvent=a,this.type=a.type,this.isDefaultPrevented=a.defaultPrevented||void 0===a.defaultPrevented&&a.returnValue===!1?ta:ua,this.target=a.target&&3===a.target.nodeType?a.target.parentNode:a.target,this.currentTarget=a.currentTarget,this.relatedTarget=a.relatedTarget):this.type=a,b&&r.extend(this,b),this.timeStamp=a&&a.timeStamp||r.now(),void(this[r.expando]=!0)):new r.Event(a,b)},r.Event.prototype={constructor:r.Event,isDefaultPrevented:ua,isPropagationStopped:ua,isImmediatePropagationStopped:ua,isSimulated:!1,preventDefault:function(){var a=this.originalEvent;this.isDefaultPrevented=ta,a&&!this.isSimulated&&a.preventDefault()},stopPropagation:function(){var a=this.originalEvent;this.isPropagationStopped=ta,a&&!this.isSimulated&&a.stopPropagation()},stopImmediatePropagation:function(){var a=this.originalEvent;this.isImmediatePropagationStopped=ta,a&&!this.isSimulated&&a.stopImmediatePropagation(),this.stopPropagation()}},r.each({altKey:!0,bubbles:!0,cancelable:!0,changedTouches:!0,ctrlKey:!0,detail:!0,eventPhase:!0,metaKey:!0,pageX:!0,pageY:!0,shiftKey:!0,view:!0,"char":!0,charCode:!0,key:!0,keyCode:!0,button:!0,buttons:!0,clientX:!0,clientY:!0,offsetX:!0,offsetY:!0,pointerId:!0,pointerType:!0,screenX:!0,screenY:!0,targetTouches:!0,toElement:!0,touches:!0,which:function(a){var b=a.button;return null==a.which&&qa.test(a.type)?null!=a.charCode?a.charCode:a.keyCode:!a.which&&void 0!==b&&ra.test(a.type)?1&b?1:2&b?3:4&b?2:0:a.which}},r.event.addProp),r.each({mouseenter:"mouseover",mouseleave:"mouseout",pointerenter:"pointerover",pointerleave:"pointerout"},function(a,b){r.event.special[a]={delegateType:b,bindType:b,handle:function(a){var c,d=this,e=a.relatedTarget,f=a.handleObj;return e&&(e===d||r.contains(d,e))||(a.type=f.origType,c=f.handler.apply(this,arguments),a.type=b),c}}}),r.fn.extend({on:function(a,b,c,d){return wa(this,a,b,c,d)},one:function(a,b,c,d){return wa(this,a,b,c,d,1)},off:function(a,b,c){var d,e;if(a&&a.preventDefault&&a.handleObj)return d=a.handleObj,r(a.delegateTarget).off(d.namespace?d.origType+"."+d.namespace:d.origType,d.selector,d.handler),this;if("object"==typeof a){for(e in a)this.off(e,b,a[e]);return this}return b!==!1&&"function"!=typeof b||(c=b,b=void 0),c===!1&&(c=ua),this.each(function(){r.event.remove(this,a,c,b)})}});var xa=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([a-z][^\/\0>\x20\t\r\n\f]*)[^>]*)\/>/gi,ya=/<script|<style|<link/i,za=/checked\s*(?:[^=]|=\s*.checked.)/i,Aa=/^true\/(.*)/,Ba=/^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;function Ca(a,b){return r.nodeName(a,"table")&&r.nodeName(11!==b.nodeType?b:b.firstChild,"tr")?a.getElementsByTagName("tbody")[0]||a:a}function Da(a){return a.type=(null!==a.getAttribute("type"))+"/"+a.type,a}function Ea(a){var b=Aa.exec(a.type);return b?a.type=b[1]:a.removeAttribute("type"),a}function Fa(a,b){var c,d,e,f,g,h,i,j;if(1===b.nodeType){if(V.hasData(a)&&(f=V.access(a),g=V.set(b,f),j=f.events)){delete g.handle,g.events={};for(e in j)for(c=0,d=j[e].length;c<d;c++)r.event.add(b,e,j[e][c])}W.hasData(a)&&(h=W.access(a),i=r.extend({},h),W.set(b,i))}}function Ga(a,b){var c=b.nodeName.toLowerCase();"input"===c&&ha.test(a.type)?b.checked=a.checked:"input"!==c&&"textarea"!==c||(b.defaultValue=a.defaultValue)}function Ha(a,b,c,d){b=g.apply([],b);var e,f,h,i,j,k,l=0,m=a.length,n=m-1,q=b[0],s=r.isFunction(q);if(s||m>1&&"string"==typeof q&&!o.checkClone&&za.test(q))return a.each(function(e){var f=a.eq(e);s&&(b[0]=q.call(this,e,f.html())),Ha(f,b,c,d)});if(m&&(e=oa(b,a[0].ownerDocument,!1,a,d),f=e.firstChild,1===e.childNodes.length&&(e=f),f||d)){for(h=r.map(la(e,"script"),Da),i=h.length;l<m;l++)j=e,l!==n&&(j=r.clone(j,!0,!0),i&&r.merge(h,la(j,"script"))),c.call(a[l],j,l);if(i)for(k=h[h.length-1].ownerDocument,r.map(h,Ea),l=0;l<i;l++)j=h[l],ja.test(j.type||"")&&!V.access(j,"globalEval")&&r.contains(k,j)&&(j.src?r._evalUrl&&r._evalUrl(j.src):p(j.textContent.replace(Ba,""),k))}return a}function Ia(a,b,c){for(var d,e=b?r.filter(b,a):a,f=0;null!=(d=e[f]);f++)c||1!==d.nodeType||r.cleanData(la(d)),d.parentNode&&(c&&r.contains(d.ownerDocument,d)&&ma(la(d,"script")),d.parentNode.removeChild(d));return a}r.extend({htmlPrefilter:function(a){return a.replace(xa,"<$1></$2>")},clone:function(a,b,c){var d,e,f,g,h=a.cloneNode(!0),i=r.contains(a.ownerDocument,a);if(!(o.noCloneChecked||1!==a.nodeType&&11!==a.nodeType||r.isXMLDoc(a)))for(g=la(h),f=la(a),d=0,e=f.length;d<e;d++)Ga(f[d],g[d]);if(b)if(c)for(f=f||la(a),g=g||la(h),d=0,e=f.length;d<e;d++)Fa(f[d],g[d]);else Fa(a,h);return g=la(h,"script"),g.length>0&&ma(g,!i&&la(a,"script")),h},cleanData:function(a){for(var b,c,d,e=r.event.special,f=0;void 0!==(c=a[f]);f++)if(T(c)){if(b=c[V.expando]){if(b.events)for(d in b.events)e[d]?r.event.remove(c,d):r.removeEvent(c,d,b.handle);c[V.expando]=void 0}c[W.expando]&&(c[W.expando]=void 0)}}}),r.fn.extend({detach:function(a){return Ia(this,a,!0)},remove:function(a){return Ia(this,a)},text:function(a){return S(this,function(a){return void 0===a?r.text(this):this.empty().each(function(){1!==this.nodeType&&11!==this.nodeType&&9!==this.nodeType||(this.textContent=a)})},null,a,arguments.length)},append:function(){return Ha(this,arguments,function(a){if(1===this.nodeType||11===this.nodeType||9===this.nodeType){var b=Ca(this,a);b.appendChild(a)}})},prepend:function(){return Ha(this,arguments,function(a){if(1===this.nodeType||11===this.nodeType||9===this.nodeType){var b=Ca(this,a);b.insertBefore(a,b.firstChild)}})},before:function(){return Ha(this,arguments,function(a){this.parentNode&&this.parentNode.insertBefore(a,this)})},after:function(){return Ha(this,arguments,function(a){this.parentNode&&this.parentNode.insertBefore(a,this.nextSibling)})},empty:function(){for(var a,b=0;null!=(a=this[b]);b++)1===a.nodeType&&(r.cleanData(la(a,!1)),a.textContent="");return this},clone:function(a,b){return a=null!=a&&a,b=null==b?a:b,this.map(function(){return r.clone(this,a,b)})},html:function(a){return S(this,function(a){var b=this[0]||{},c=0,d=this.length;if(void 0===a&&1===b.nodeType)return b.innerHTML;if("string"==typeof a&&!ya.test(a)&&!ka[(ia.exec(a)||["",""])[1].toLowerCase()]){a=r.htmlPrefilter(a);try{for(;c<d;c++)b=this[c]||{},1===b.nodeType&&(r.cleanData(la(b,!1)),b.innerHTML=a);b=0}catch(e){}}b&&this.empty().append(a)},null,a,arguments.length)},replaceWith:function(){var a=[];return Ha(this,arguments,function(b){var c=this.parentNode;r.inArray(this,a)<0&&(r.cleanData(la(this)),c&&c.replaceChild(b,this))},a)}}),r.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(a,b){r.fn[a]=function(a){for(var c,d=[],e=r(a),f=e.length-1,g=0;g<=f;g++)c=g===f?this:this.clone(!0),r(e[g])[b](c),h.apply(d,c.get());return this.pushStack(d)}});var Ja=/^margin/,Ka=new RegExp("^("+$+")(?!px)[a-z%]+$","i"),La=function(b){var c=b.ownerDocument.defaultView;return c&&c.opener||(c=a),c.getComputedStyle(b)};!function(){function b(){if(i){i.style.cssText="box-sizing:border-box;position:relative;display:block;margin:auto;border:1px;padding:1px;top:1%;width:50%",i.innerHTML="",pa.appendChild(h);var b=a.getComputedStyle(i);c="1%"!==b.top,g="2px"===b.marginLeft,e="4px"===b.width,i.style.marginRight="50%",f="4px"===b.marginRight,pa.removeChild(h),i=null}}var c,e,f,g,h=d.createElement("div"),i=d.createElement("div");i.style&&(i.style.backgroundClip="content-box",i.cloneNode(!0).style.backgroundClip="",o.clearCloneStyle="content-box"===i.style.backgroundClip,h.style.cssText="border:0;width:8px;height:0;top:0;left:-9999px;padding:0;margin-top:1px;position:absolute",h.appendChild(i),r.extend(o,{pixelPosition:function(){return b(),c},boxSizingReliable:function(){return b(),e},pixelMarginRight:function(){return b(),f},reliableMarginLeft:function(){return b(),g}}))}();function Ma(a,b,c){var d,e,f,g,h=a.style;return c=c||La(a),c&&(g=c.getPropertyValue(b)||c[b],""!==g||r.contains(a.ownerDocument,a)||(g=r.style(a,b)),!o.pixelMarginRight()&&Ka.test(g)&&Ja.test(b)&&(d=h.width,e=h.minWidth,f=h.maxWidth,h.minWidth=h.maxWidth=h.width=g,g=c.width,h.width=d,h.minWidth=e,h.maxWidth=f)),void 0!==g?g+"":g}function Na(a,b){return{get:function(){return a()?void delete this.get:(this.get=b).apply(this,arguments)}}}var Oa=/^(none|table(?!-c[ea]).+)/,Pa={position:"absolute",visibility:"hidden",display:"block"},Qa={letterSpacing:"0",fontWeight:"400"},Ra=["Webkit","Moz","ms"],Sa=d.createElement("div").style;function Ta(a){if(a in Sa)return a;var b=a[0].toUpperCase()+a.slice(1),c=Ra.length;while(c--)if(a=Ra[c]+b,a in Sa)return a}function Ua(a,b,c){var d=_.exec(b);return d?Math.max(0,d[2]-(c||0))+(d[3]||"px"):b}function Va(a,b,c,d,e){for(var f=c===(d?"border":"content")?4:"width"===b?1:0,g=0;f<4;f+=2)"margin"===c&&(g+=r.css(a,c+aa[f],!0,e)),d?("content"===c&&(g-=r.css(a,"padding"+aa[f],!0,e)),"margin"!==c&&(g-=r.css(a,"border"+aa[f]+"Width",!0,e))):(g+=r.css(a,"padding"+aa[f],!0,e),"padding"!==c&&(g+=r.css(a,"border"+aa[f]+"Width",!0,e)));return g}function Wa(a,b,c){var d,e=!0,f=La(a),g="border-box"===r.css(a,"boxSizing",!1,f);if(a.getClientRects().length&&(d=a.getBoundingClientRect()[b]),d<=0||null==d){if(d=Ma(a,b,f),(d<0||null==d)&&(d=a.style[b]),Ka.test(d))return d;e=g&&(o.boxSizingReliable()||d===a.style[b]),d=parseFloat(d)||0}return d+Va(a,b,c||(g?"border":"content"),e,f)+"px"}r.extend({cssHooks:{opacity:{get:function(a,b){if(b){var c=Ma(a,"opacity");return""===c?"1":c}}}},cssNumber:{animationIterationCount:!0,columnCount:!0,fillOpacity:!0,flexGrow:!0,flexShrink:!0,fontWeight:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,widows:!0,zIndex:!0,zoom:!0},cssProps:{"float":"cssFloat"},style:function(a,b,c,d){if(a&&3!==a.nodeType&&8!==a.nodeType&&a.style){var e,f,g,h=r.camelCase(b),i=a.style;return b=r.cssProps[h]||(r.cssProps[h]=Ta(h)||h),g=r.cssHooks[b]||r.cssHooks[h],void 0===c?g&&"get"in g&&void 0!==(e=g.get(a,!1,d))?e:i[b]:(f=typeof c,"string"===f&&(e=_.exec(c))&&e[1]&&(c=da(a,b,e),f="number"),null!=c&&c===c&&("number"===f&&(c+=e&&e[3]||(r.cssNumber[h]?"":"px")),o.clearCloneStyle||""!==c||0!==b.indexOf("background")||(i[b]="inherit"),g&&"set"in g&&void 0===(c=g.set(a,c,d))||(i[b]=c)),void 0)}},css:function(a,b,c,d){var e,f,g,h=r.camelCase(b);return b=r.cssProps[h]||(r.cssProps[h]=Ta(h)||h),g=r.cssHooks[b]||r.cssHooks[h],g&&"get"in g&&(e=g.get(a,!0,c)),void 0===e&&(e=Ma(a,b,d)),"normal"===e&&b in Qa&&(e=Qa[b]),""===c||c?(f=parseFloat(e),c===!0||isFinite(f)?f||0:e):e}}),r.each(["height","width"],function(a,b){r.cssHooks[b]={get:function(a,c,d){if(c)return!Oa.test(r.css(a,"display"))||a.getClientRects().length&&a.getBoundingClientRect().width?Wa(a,b,d):ca(a,Pa,function(){return Wa(a,b,d)})},set:function(a,c,d){var e,f=d&&La(a),g=d&&Va(a,b,d,"border-box"===r.css(a,"boxSizing",!1,f),f);return g&&(e=_.exec(c))&&"px"!==(e[3]||"px")&&(a.style[b]=c,c=r.css(a,b)),Ua(a,c,g)}}}),r.cssHooks.marginLeft=Na(o.reliableMarginLeft,function(a,b){if(b)return(parseFloat(Ma(a,"marginLeft"))||a.getBoundingClientRect().left-ca(a,{marginLeft:0},function(){return a.getBoundingClientRect().left}))+"px"}),r.each({margin:"",padding:"",border:"Width"},function(a,b){r.cssHooks[a+b]={expand:function(c){for(var d=0,e={},f="string"==typeof c?c.split(" "):[c];d<4;d++)e[a+aa[d]+b]=f[d]||f[d-2]||f[0];return e}},Ja.test(a)||(r.cssHooks[a+b].set=Ua)}),r.fn.extend({css:function(a,b){return S(this,function(a,b,c){var d,e,f={},g=0;if(r.isArray(b)){for(d=La(a),e=b.length;g<e;g++)f[b[g]]=r.css(a,b[g],!1,d);return f}return void 0!==c?r.style(a,b,c):r.css(a,b)},a,b,arguments.length>1)}});function Xa(a,b,c,d,e){return new Xa.prototype.init(a,b,c,d,e)}r.Tween=Xa,Xa.prototype={constructor:Xa,init:function(a,b,c,d,e,f){this.elem=a,this.prop=c,this.easing=e||r.easing._default,this.options=b,this.start=this.now=this.cur(),this.end=d,this.unit=f||(r.cssNumber[c]?"":"px")},cur:function(){var a=Xa.propHooks[this.prop];return a&&a.get?a.get(this):Xa.propHooks._default.get(this)},run:function(a){var b,c=Xa.propHooks[this.prop];return this.options.duration?this.pos=b=r.easing[this.easing](a,this.options.duration*a,0,1,this.options.duration):this.pos=b=a,this.now=(this.end-this.start)*b+this.start,this.options.step&&this.options.step.call(this.elem,this.now,this),c&&c.set?c.set(this):Xa.propHooks._default.set(this),this}},Xa.prototype.init.prototype=Xa.prototype,Xa.propHooks={_default:{get:function(a){var b;return 1!==a.elem.nodeType||null!=a.elem[a.prop]&&null==a.elem.style[a.prop]?a.elem[a.prop]:(b=r.css(a.elem,a.prop,""),b&&"auto"!==b?b:0)},set:function(a){r.fx.step[a.prop]?r.fx.step[a.prop](a):1!==a.elem.nodeType||null==a.elem.style[r.cssProps[a.prop]]&&!r.cssHooks[a.prop]?a.elem[a.prop]=a.now:r.style(a.elem,a.prop,a.now+a.unit)}}},Xa.propHooks.scrollTop=Xa.propHooks.scrollLeft={set:function(a){a.elem.nodeType&&a.elem.parentNode&&(a.elem[a.prop]=a.now)}},r.easing={linear:function(a){return a},swing:function(a){return.5-Math.cos(a*Math.PI)/2},_default:"swing"},r.fx=Xa.prototype.init,r.fx.step={};var Ya,Za,$a=/^(?:toggle|show|hide)$/,_a=/queueHooks$/;function ab(){Za&&(a.requestAnimationFrame(ab),r.fx.tick())}function bb(){return a.setTimeout(function(){Ya=void 0}),Ya=r.now()}function cb(a,b){var c,d=0,e={height:a};for(b=b?1:0;d<4;d+=2-b)c=aa[d],e["margin"+c]=e["padding"+c]=a;return b&&(e.opacity=e.width=a),e}function db(a,b,c){for(var d,e=(gb.tweeners[b]||[]).concat(gb.tweeners["*"]),f=0,g=e.length;f<g;f++)if(d=e[f].call(c,b,a))return d}function eb(a,b,c){var d,e,f,g,h,i,j,k,l="width"in b||"height"in b,m=this,n={},o=a.style,p=a.nodeType&&ba(a),q=V.get(a,"fxshow");c.queue||(g=r._queueHooks(a,"fx"),null==g.unqueued&&(g.unqueued=0,h=g.empty.fire,g.empty.fire=function(){g.unqueued||h()}),g.unqueued++,m.always(function(){m.always(function(){g.unqueued--,r.queue(a,"fx").length||g.empty.fire()})}));for(d in b)if(e=b[d],$a.test(e)){if(delete b[d],f=f||"toggle"===e,e===(p?"hide":"show")){if("show"!==e||!q||void 0===q[d])continue;p=!0}n[d]=q&&q[d]||r.style(a,d)}if(i=!r.isEmptyObject(b),i||!r.isEmptyObject(n)){l&&1===a.nodeType&&(c.overflow=[o.overflow,o.overflowX,o.overflowY],j=q&&q.display,null==j&&(j=V.get(a,"display")),k=r.css(a,"display"),"none"===k&&(j?k=j:(ga([a],!0),j=a.style.display||j,k=r.css(a,"display"),ga([a]))),("inline"===k||"inline-block"===k&&null!=j)&&"none"===r.css(a,"float")&&(i||(m.done(function(){o.display=j}),null==j&&(k=o.display,j="none"===k?"":k)),o.display="inline-block")),c.overflow&&(o.overflow="hidden",m.always(function(){o.overflow=c.overflow[0],o.overflowX=c.overflow[1],o.overflowY=c.overflow[2]})),i=!1;for(d in n)i||(q?"hidden"in q&&(p=q.hidden):q=V.access(a,"fxshow",{display:j}),f&&(q.hidden=!p),p&&ga([a],!0),m.done(function(){p||ga([a]),V.remove(a,"fxshow");for(d in n)r.style(a,d,n[d])})),i=db(p?q[d]:0,d,m),d in q||(q[d]=i.start,p&&(i.end=i.start,i.start=0))}}function fb(a,b){var c,d,e,f,g;for(c in a)if(d=r.camelCase(c),e=b[d],f=a[c],r.isArray(f)&&(e=f[1],f=a[c]=f[0]),c!==d&&(a[d]=f,delete a[c]),g=r.cssHooks[d],g&&"expand"in g){f=g.expand(f),delete a[d];for(c in f)c in a||(a[c]=f[c],b[c]=e)}else b[d]=e}function gb(a,b,c){var d,e,f=0,g=gb.prefilters.length,h=r.Deferred().always(function(){delete i.elem}),i=function(){if(e)return!1;for(var b=Ya||bb(),c=Math.max(0,j.startTime+j.duration-b),d=c/j.duration||0,f=1-d,g=0,i=j.tweens.length;g<i;g++)j.tweens[g].run(f);return h.notifyWith(a,[j,f,c]),f<1&&i?c:(h.resolveWith(a,[j]),!1)},j=h.promise({elem:a,props:r.extend({},b),opts:r.extend(!0,{specialEasing:{},easing:r.easing._default},c),originalProperties:b,originalOptions:c,startTime:Ya||bb(),duration:c.duration,tweens:[],createTween:function(b,c){var d=r.Tween(a,j.opts,b,c,j.opts.specialEasing[b]||j.opts.easing);return j.tweens.push(d),d},stop:function(b){var c=0,d=b?j.tweens.length:0;if(e)return this;for(e=!0;c<d;c++)j.tweens[c].run(1);return b?(h.notifyWith(a,[j,1,0]),h.resolveWith(a,[j,b])):h.rejectWith(a,[j,b]),this}}),k=j.props;for(fb(k,j.opts.specialEasing);f<g;f++)if(d=gb.prefilters[f].call(j,a,k,j.opts))return r.isFunction(d.stop)&&(r._queueHooks(j.elem,j.opts.queue).stop=r.proxy(d.stop,d)),d;return r.map(k,db,j),r.isFunction(j.opts.start)&&j.opts.start.call(a,j),r.fx.timer(r.extend(i,{elem:a,anim:j,queue:j.opts.queue})),j.progress(j.opts.progress).done(j.opts.done,j.opts.complete).fail(j.opts.fail).always(j.opts.always)}r.Animation=r.extend(gb,{tweeners:{"*":[function(a,b){var c=this.createTween(a,b);return da(c.elem,a,_.exec(b),c),c}]},tweener:function(a,b){r.isFunction(a)?(b=a,a=["*"]):a=a.match(K);for(var c,d=0,e=a.length;d<e;d++)c=a[d],gb.tweeners[c]=gb.tweeners[c]||[],gb.tweeners[c].unshift(b)},prefilters:[eb],prefilter:function(a,b){b?gb.prefilters.unshift(a):gb.prefilters.push(a)}}),r.speed=function(a,b,c){var e=a&&"object"==typeof a?r.extend({},a):{complete:c||!c&&b||r.isFunction(a)&&a,duration:a,easing:c&&b||b&&!r.isFunction(b)&&b};return r.fx.off||d.hidden?e.duration=0:e.duration="number"==typeof e.duration?e.duration:e.duration in r.fx.speeds?r.fx.speeds[e.duration]:r.fx.speeds._default,null!=e.queue&&e.queue!==!0||(e.queue="fx"),e.old=e.complete,e.complete=function(){r.isFunction(e.old)&&e.old.call(this),e.queue&&r.dequeue(this,e.queue)},e},r.fn.extend({fadeTo:function(a,b,c,d){return this.filter(ba).css("opacity",0).show().end().animate({opacity:b},a,c,d)},animate:function(a,b,c,d){var e=r.isEmptyObject(a),f=r.speed(b,c,d),g=function(){var b=gb(this,r.extend({},a),f);(e||V.get(this,"finish"))&&b.stop(!0)};return g.finish=g,e||f.queue===!1?this.each(g):this.queue(f.queue,g)},stop:function(a,b,c){var d=function(a){var b=a.stop;delete a.stop,b(c)};return"string"!=typeof a&&(c=b,b=a,a=void 0),b&&a!==!1&&this.queue(a||"fx",[]),this.each(function(){var b=!0,e=null!=a&&a+"queueHooks",f=r.timers,g=V.get(this);if(e)g[e]&&g[e].stop&&d(g[e]);else for(e in g)g[e]&&g[e].stop&&_a.test(e)&&d(g[e]);for(e=f.length;e--;)f[e].elem!==this||null!=a&&f[e].queue!==a||(f[e].anim.stop(c),b=!1,f.splice(e,1));!b&&c||r.dequeue(this,a)})},finish:function(a){return a!==!1&&(a=a||"fx"),this.each(function(){var b,c=V.get(this),d=c[a+"queue"],e=c[a+"queueHooks"],f=r.timers,g=d?d.length:0;for(c.finish=!0,r.queue(this,a,[]),e&&e.stop&&e.stop.call(this,!0),b=f.length;b--;)f[b].elem===this&&f[b].queue===a&&(f[b].anim.stop(!0),f.splice(b,1));for(b=0;b<g;b++)d[b]&&d[b].finish&&d[b].finish.call(this);delete c.finish})}}),r.each(["toggle","show","hide"],function(a,b){var c=r.fn[b];r.fn[b]=function(a,d,e){return null==a||"boolean"==typeof a?c.apply(this,arguments):this.animate(cb(b,!0),a,d,e)}}),r.each({slideDown:cb("show"),slideUp:cb("hide"),slideToggle:cb("toggle"),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"},fadeToggle:{opacity:"toggle"}},function(a,b){r.fn[a]=function(a,c,d){return this.animate(b,a,c,d)}}),r.timers=[],r.fx.tick=function(){var a,b=0,c=r.timers;for(Ya=r.now();b<c.length;b++)a=c[b],a()||c[b]!==a||c.splice(b--,1);c.length||r.fx.stop(),Ya=void 0},r.fx.timer=function(a){r.timers.push(a),a()?r.fx.start():r.timers.pop()},r.fx.interval=13,r.fx.start=function(){Za||(Za=a.requestAnimationFrame?a.requestAnimationFrame(ab):a.setInterval(r.fx.tick,r.fx.interval))},r.fx.stop=function(){a.cancelAnimationFrame?a.cancelAnimationFrame(Za):a.clearInterval(Za),Za=null},r.fx.speeds={slow:600,fast:200,_default:400},r.fn.delay=function(b,c){return b=r.fx?r.fx.speeds[b]||b:b,c=c||"fx",this.queue(c,function(c,d){var e=a.setTimeout(c,b);d.stop=function(){a.clearTimeout(e)}})},function(){var a=d.createElement("input"),b=d.createElement("select"),c=b.appendChild(d.createElement("option"));a.type="checkbox",o.checkOn=""!==a.value,o.optSelected=c.selected,a=d.createElement("input"),a.value="t",a.type="radio",o.radioValue="t"===a.value}();var hb,ib=r.expr.attrHandle;r.fn.extend({attr:function(a,b){return S(this,r.attr,a,b,arguments.length>1)},removeAttr:function(a){return this.each(function(){r.removeAttr(this,a)})}}),r.extend({attr:function(a,b,c){var d,e,f=a.nodeType;if(3!==f&&8!==f&&2!==f)return"undefined"==typeof a.getAttribute?r.prop(a,b,c):(1===f&&r.isXMLDoc(a)||(e=r.attrHooks[b.toLowerCase()]||(r.expr.match.bool.test(b)?hb:void 0)),void 0!==c?null===c?void r.removeAttr(a,b):e&&"set"in e&&void 0!==(d=e.set(a,c,b))?d:(a.setAttribute(b,c+""),c):e&&"get"in e&&null!==(d=e.get(a,b))?d:(d=r.find.attr(a,b),null==d?void 0:d))},attrHooks:{type:{set:function(a,b){if(!o.radioValue&&"radio"===b&&r.nodeName(a,"input")){var c=a.value;return a.setAttribute("type",b),c&&(a.value=c),b}}}},removeAttr:function(a,b){var c,d=0,e=b&&b.match(K);
if(e&&1===a.nodeType)while(c=e[d++])a.removeAttribute(c)}}),hb={set:function(a,b,c){return b===!1?r.removeAttr(a,c):a.setAttribute(c,c),c}},r.each(r.expr.match.bool.source.match(/\w+/g),function(a,b){var c=ib[b]||r.find.attr;ib[b]=function(a,b,d){var e,f,g=b.toLowerCase();return d||(f=ib[g],ib[g]=e,e=null!=c(a,b,d)?g:null,ib[g]=f),e}});var jb=/^(?:input|select|textarea|button)$/i,kb=/^(?:a|area)$/i;r.fn.extend({prop:function(a,b){return S(this,r.prop,a,b,arguments.length>1)},removeProp:function(a){return this.each(function(){delete this[r.propFix[a]||a]})}}),r.extend({prop:function(a,b,c){var d,e,f=a.nodeType;if(3!==f&&8!==f&&2!==f)return 1===f&&r.isXMLDoc(a)||(b=r.propFix[b]||b,e=r.propHooks[b]),void 0!==c?e&&"set"in e&&void 0!==(d=e.set(a,c,b))?d:a[b]=c:e&&"get"in e&&null!==(d=e.get(a,b))?d:a[b]},propHooks:{tabIndex:{get:function(a){var b=r.find.attr(a,"tabindex");return b?parseInt(b,10):jb.test(a.nodeName)||kb.test(a.nodeName)&&a.href?0:-1}}},propFix:{"for":"htmlFor","class":"className"}}),o.optSelected||(r.propHooks.selected={get:function(a){var b=a.parentNode;return b&&b.parentNode&&b.parentNode.selectedIndex,null},set:function(a){var b=a.parentNode;b&&(b.selectedIndex,b.parentNode&&b.parentNode.selectedIndex)}}),r.each(["tabIndex","readOnly","maxLength","cellSpacing","cellPadding","rowSpan","colSpan","useMap","frameBorder","contentEditable"],function(){r.propFix[this.toLowerCase()]=this});var lb=/[\t\r\n\f]/g;function mb(a){return a.getAttribute&&a.getAttribute("class")||""}r.fn.extend({addClass:function(a){var b,c,d,e,f,g,h,i=0;if(r.isFunction(a))return this.each(function(b){r(this).addClass(a.call(this,b,mb(this)))});if("string"==typeof a&&a){b=a.match(K)||[];while(c=this[i++])if(e=mb(c),d=1===c.nodeType&&(" "+e+" ").replace(lb," ")){g=0;while(f=b[g++])d.indexOf(" "+f+" ")<0&&(d+=f+" ");h=r.trim(d),e!==h&&c.setAttribute("class",h)}}return this},removeClass:function(a){var b,c,d,e,f,g,h,i=0;if(r.isFunction(a))return this.each(function(b){r(this).removeClass(a.call(this,b,mb(this)))});if(!arguments.length)return this.attr("class","");if("string"==typeof a&&a){b=a.match(K)||[];while(c=this[i++])if(e=mb(c),d=1===c.nodeType&&(" "+e+" ").replace(lb," ")){g=0;while(f=b[g++])while(d.indexOf(" "+f+" ")>-1)d=d.replace(" "+f+" "," ");h=r.trim(d),e!==h&&c.setAttribute("class",h)}}return this},toggleClass:function(a,b){var c=typeof a;return"boolean"==typeof b&&"string"===c?b?this.addClass(a):this.removeClass(a):r.isFunction(a)?this.each(function(c){r(this).toggleClass(a.call(this,c,mb(this),b),b)}):this.each(function(){var b,d,e,f;if("string"===c){d=0,e=r(this),f=a.match(K)||[];while(b=f[d++])e.hasClass(b)?e.removeClass(b):e.addClass(b)}else void 0!==a&&"boolean"!==c||(b=mb(this),b&&V.set(this,"__className__",b),this.setAttribute&&this.setAttribute("class",b||a===!1?"":V.get(this,"__className__")||""))})},hasClass:function(a){var b,c,d=0;b=" "+a+" ";while(c=this[d++])if(1===c.nodeType&&(" "+mb(c)+" ").replace(lb," ").indexOf(b)>-1)return!0;return!1}});var nb=/\r/g,ob=/[\x20\t\r\n\f]+/g;r.fn.extend({val:function(a){var b,c,d,e=this[0];{if(arguments.length)return d=r.isFunction(a),this.each(function(c){var e;1===this.nodeType&&(e=d?a.call(this,c,r(this).val()):a,null==e?e="":"number"==typeof e?e+="":r.isArray(e)&&(e=r.map(e,function(a){return null==a?"":a+""})),b=r.valHooks[this.type]||r.valHooks[this.nodeName.toLowerCase()],b&&"set"in b&&void 0!==b.set(this,e,"value")||(this.value=e))});if(e)return b=r.valHooks[e.type]||r.valHooks[e.nodeName.toLowerCase()],b&&"get"in b&&void 0!==(c=b.get(e,"value"))?c:(c=e.value,"string"==typeof c?c.replace(nb,""):null==c?"":c)}}}),r.extend({valHooks:{option:{get:function(a){var b=r.find.attr(a,"value");return null!=b?b:r.trim(r.text(a)).replace(ob," ")}},select:{get:function(a){for(var b,c,d=a.options,e=a.selectedIndex,f="select-one"===a.type,g=f?null:[],h=f?e+1:d.length,i=e<0?h:f?e:0;i<h;i++)if(c=d[i],(c.selected||i===e)&&!c.disabled&&(!c.parentNode.disabled||!r.nodeName(c.parentNode,"optgroup"))){if(b=r(c).val(),f)return b;g.push(b)}return g},set:function(a,b){var c,d,e=a.options,f=r.makeArray(b),g=e.length;while(g--)d=e[g],(d.selected=r.inArray(r.valHooks.option.get(d),f)>-1)&&(c=!0);return c||(a.selectedIndex=-1),f}}}}),r.each(["radio","checkbox"],function(){r.valHooks[this]={set:function(a,b){if(r.isArray(b))return a.checked=r.inArray(r(a).val(),b)>-1}},o.checkOn||(r.valHooks[this].get=function(a){return null===a.getAttribute("value")?"on":a.value})});var pb=/^(?:focusinfocus|focusoutblur)$/;r.extend(r.event,{trigger:function(b,c,e,f){var g,h,i,j,k,m,n,o=[e||d],p=l.call(b,"type")?b.type:b,q=l.call(b,"namespace")?b.namespace.split("."):[];if(h=i=e=e||d,3!==e.nodeType&&8!==e.nodeType&&!pb.test(p+r.event.triggered)&&(p.indexOf(".")>-1&&(q=p.split("."),p=q.shift(),q.sort()),k=p.indexOf(":")<0&&"on"+p,b=b[r.expando]?b:new r.Event(p,"object"==typeof b&&b),b.isTrigger=f?2:3,b.namespace=q.join("."),b.rnamespace=b.namespace?new RegExp("(^|\\.)"+q.join("\\.(?:.*\\.|)")+"(\\.|$)"):null,b.result=void 0,b.target||(b.target=e),c=null==c?[b]:r.makeArray(c,[b]),n=r.event.special[p]||{},f||!n.trigger||n.trigger.apply(e,c)!==!1)){if(!f&&!n.noBubble&&!r.isWindow(e)){for(j=n.delegateType||p,pb.test(j+p)||(h=h.parentNode);h;h=h.parentNode)o.push(h),i=h;i===(e.ownerDocument||d)&&o.push(i.defaultView||i.parentWindow||a)}g=0;while((h=o[g++])&&!b.isPropagationStopped())b.type=g>1?j:n.bindType||p,m=(V.get(h,"events")||{})[b.type]&&V.get(h,"handle"),m&&m.apply(h,c),m=k&&h[k],m&&m.apply&&T(h)&&(b.result=m.apply(h,c),b.result===!1&&b.preventDefault());return b.type=p,f||b.isDefaultPrevented()||n._default&&n._default.apply(o.pop(),c)!==!1||!T(e)||k&&r.isFunction(e[p])&&!r.isWindow(e)&&(i=e[k],i&&(e[k]=null),r.event.triggered=p,e[p](),r.event.triggered=void 0,i&&(e[k]=i)),b.result}},simulate:function(a,b,c){var d=r.extend(new r.Event,c,{type:a,isSimulated:!0});r.event.trigger(d,null,b)}}),r.fn.extend({trigger:function(a,b){return this.each(function(){r.event.trigger(a,b,this)})},triggerHandler:function(a,b){var c=this[0];if(c)return r.event.trigger(a,b,c,!0)}}),r.each("blur focus focusin focusout resize scroll click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup contextmenu".split(" "),function(a,b){r.fn[b]=function(a,c){return arguments.length>0?this.on(b,null,a,c):this.trigger(b)}}),r.fn.extend({hover:function(a,b){return this.mouseenter(a).mouseleave(b||a)}}),o.focusin="onfocusin"in a,o.focusin||r.each({focus:"focusin",blur:"focusout"},function(a,b){var c=function(a){r.event.simulate(b,a.target,r.event.fix(a))};r.event.special[b]={setup:function(){var d=this.ownerDocument||this,e=V.access(d,b);e||d.addEventListener(a,c,!0),V.access(d,b,(e||0)+1)},teardown:function(){var d=this.ownerDocument||this,e=V.access(d,b)-1;e?V.access(d,b,e):(d.removeEventListener(a,c,!0),V.remove(d,b))}}});var qb=a.location,rb=r.now(),sb=/\?/;r.parseXML=function(b){var c;if(!b||"string"!=typeof b)return null;try{c=(new a.DOMParser).parseFromString(b,"text/xml")}catch(d){c=void 0}return c&&!c.getElementsByTagName("parsererror").length||r.error("Invalid XML: "+b),c};var tb=/\[\]$/,ub=/\r?\n/g,vb=/^(?:submit|button|image|reset|file)$/i,wb=/^(?:input|select|textarea|keygen)/i;function xb(a,b,c,d){var e;if(r.isArray(b))r.each(b,function(b,e){c||tb.test(a)?d(a,e):xb(a+"["+("object"==typeof e&&null!=e?b:"")+"]",e,c,d)});else if(c||"object"!==r.type(b))d(a,b);else for(e in b)xb(a+"["+e+"]",b[e],c,d)}r.param=function(a,b){var c,d=[],e=function(a,b){var c=r.isFunction(b)?b():b;d[d.length]=encodeURIComponent(a)+"="+encodeURIComponent(null==c?"":c)};if(r.isArray(a)||a.jquery&&!r.isPlainObject(a))r.each(a,function(){e(this.name,this.value)});else for(c in a)xb(c,a[c],b,e);return d.join("&")},r.fn.extend({serialize:function(){return r.param(this.serializeArray())},serializeArray:function(){return this.map(function(){var a=r.prop(this,"elements");return a?r.makeArray(a):this}).filter(function(){var a=this.type;return this.name&&!r(this).is(":disabled")&&wb.test(this.nodeName)&&!vb.test(a)&&(this.checked||!ha.test(a))}).map(function(a,b){var c=r(this).val();return null==c?null:r.isArray(c)?r.map(c,function(a){return{name:b.name,value:a.replace(ub,"\r\n")}}):{name:b.name,value:c.replace(ub,"\r\n")}}).get()}});var yb=/%20/g,zb=/#.*$/,Ab=/([?&])_=[^&]*/,Bb=/^(.*?):[ \t]*([^\r\n]*)$/gm,Cb=/^(?:about|app|app-storage|.+-extension|file|res|widget):$/,Db=/^(?:GET|HEAD)$/,Eb=/^\/\//,Fb={},Gb={},Hb="*/".concat("*"),Ib=d.createElement("a");Ib.href=qb.href;function Jb(a){return function(b,c){"string"!=typeof b&&(c=b,b="*");var d,e=0,f=b.toLowerCase().match(K)||[];if(r.isFunction(c))while(d=f[e++])"+"===d[0]?(d=d.slice(1)||"*",(a[d]=a[d]||[]).unshift(c)):(a[d]=a[d]||[]).push(c)}}function Kb(a,b,c,d){var e={},f=a===Gb;function g(h){var i;return e[h]=!0,r.each(a[h]||[],function(a,h){var j=h(b,c,d);return"string"!=typeof j||f||e[j]?f?!(i=j):void 0:(b.dataTypes.unshift(j),g(j),!1)}),i}return g(b.dataTypes[0])||!e["*"]&&g("*")}function Lb(a,b){var c,d,e=r.ajaxSettings.flatOptions||{};for(c in b)void 0!==b[c]&&((e[c]?a:d||(d={}))[c]=b[c]);return d&&r.extend(!0,a,d),a}function Mb(a,b,c){var d,e,f,g,h=a.contents,i=a.dataTypes;while("*"===i[0])i.shift(),void 0===d&&(d=a.mimeType||b.getResponseHeader("Content-Type"));if(d)for(e in h)if(h[e]&&h[e].test(d)){i.unshift(e);break}if(i[0]in c)f=i[0];else{for(e in c){if(!i[0]||a.converters[e+" "+i[0]]){f=e;break}g||(g=e)}f=f||g}if(f)return f!==i[0]&&i.unshift(f),c[f]}function Nb(a,b,c,d){var e,f,g,h,i,j={},k=a.dataTypes.slice();if(k[1])for(g in a.converters)j[g.toLowerCase()]=a.converters[g];f=k.shift();while(f)if(a.responseFields[f]&&(c[a.responseFields[f]]=b),!i&&d&&a.dataFilter&&(b=a.dataFilter(b,a.dataType)),i=f,f=k.shift())if("*"===f)f=i;else if("*"!==i&&i!==f){if(g=j[i+" "+f]||j["* "+f],!g)for(e in j)if(h=e.split(" "),h[1]===f&&(g=j[i+" "+h[0]]||j["* "+h[0]])){g===!0?g=j[e]:j[e]!==!0&&(f=h[0],k.unshift(h[1]));break}if(g!==!0)if(g&&a["throws"])b=g(b);else try{b=g(b)}catch(l){return{state:"parsererror",error:g?l:"No conversion from "+i+" to "+f}}}return{state:"success",data:b}}r.extend({active:0,lastModified:{},etag:{},ajaxSettings:{url:qb.href,type:"GET",isLocal:Cb.test(qb.protocol),global:!0,processData:!0,async:!0,contentType:"application/x-www-form-urlencoded; charset=UTF-8",accepts:{"*":Hb,text:"text/plain",html:"text/html",xml:"application/xml, text/xml",json:"application/json, text/javascript"},contents:{xml:/\bxml\b/,html:/\bhtml/,json:/\bjson\b/},responseFields:{xml:"responseXML",text:"responseText",json:"responseJSON"},converters:{"* text":String,"text html":!0,"text json":JSON.parse,"text xml":r.parseXML},flatOptions:{url:!0,context:!0}},ajaxSetup:function(a,b){return b?Lb(Lb(a,r.ajaxSettings),b):Lb(r.ajaxSettings,a)},ajaxPrefilter:Jb(Fb),ajaxTransport:Jb(Gb),ajax:function(b,c){"object"==typeof b&&(c=b,b=void 0),c=c||{};var e,f,g,h,i,j,k,l,m,n,o=r.ajaxSetup({},c),p=o.context||o,q=o.context&&(p.nodeType||p.jquery)?r(p):r.event,s=r.Deferred(),t=r.Callbacks("once memory"),u=o.statusCode||{},v={},w={},x="canceled",y={readyState:0,getResponseHeader:function(a){var b;if(k){if(!h){h={};while(b=Bb.exec(g))h[b[1].toLowerCase()]=b[2]}b=h[a.toLowerCase()]}return null==b?null:b},getAllResponseHeaders:function(){return k?g:null},setRequestHeader:function(a,b){return null==k&&(a=w[a.toLowerCase()]=w[a.toLowerCase()]||a,v[a]=b),this},overrideMimeType:function(a){return null==k&&(o.mimeType=a),this},statusCode:function(a){var b;if(a)if(k)y.always(a[y.status]);else for(b in a)u[b]=[u[b],a[b]];return this},abort:function(a){var b=a||x;return e&&e.abort(b),A(0,b),this}};if(s.promise(y),o.url=((b||o.url||qb.href)+"").replace(Eb,qb.protocol+"//"),o.type=c.method||c.type||o.method||o.type,o.dataTypes=(o.dataType||"*").toLowerCase().match(K)||[""],null==o.crossDomain){j=d.createElement("a");try{j.href=o.url,j.href=j.href,o.crossDomain=Ib.protocol+"//"+Ib.host!=j.protocol+"//"+j.host}catch(z){o.crossDomain=!0}}if(o.data&&o.processData&&"string"!=typeof o.data&&(o.data=r.param(o.data,o.traditional)),Kb(Fb,o,c,y),k)return y;l=r.event&&o.global,l&&0===r.active++&&r.event.trigger("ajaxStart"),o.type=o.type.toUpperCase(),o.hasContent=!Db.test(o.type),f=o.url.replace(zb,""),o.hasContent?o.data&&o.processData&&0===(o.contentType||"").indexOf("application/x-www-form-urlencoded")&&(o.data=o.data.replace(yb,"+")):(n=o.url.slice(f.length),o.data&&(f+=(sb.test(f)?"&":"?")+o.data,delete o.data),o.cache===!1&&(f=f.replace(Ab,""),n=(sb.test(f)?"&":"?")+"_="+rb++ +n),o.url=f+n),o.ifModified&&(r.lastModified[f]&&y.setRequestHeader("If-Modified-Since",r.lastModified[f]),r.etag[f]&&y.setRequestHeader("If-None-Match",r.etag[f])),(o.data&&o.hasContent&&o.contentType!==!1||c.contentType)&&y.setRequestHeader("Content-Type",o.contentType),y.setRequestHeader("Accept",o.dataTypes[0]&&o.accepts[o.dataTypes[0]]?o.accepts[o.dataTypes[0]]+("*"!==o.dataTypes[0]?", "+Hb+"; q=0.01":""):o.accepts["*"]);for(m in o.headers)y.setRequestHeader(m,o.headers[m]);if(o.beforeSend&&(o.beforeSend.call(p,y,o)===!1||k))return y.abort();if(x="abort",t.add(o.complete),y.done(o.success),y.fail(o.error),e=Kb(Gb,o,c,y)){if(y.readyState=1,l&&q.trigger("ajaxSend",[y,o]),k)return y;o.async&&o.timeout>0&&(i=a.setTimeout(function(){y.abort("timeout")},o.timeout));try{k=!1,e.send(v,A)}catch(z){if(k)throw z;A(-1,z)}}else A(-1,"No Transport");function A(b,c,d,h){var j,m,n,v,w,x=c;k||(k=!0,i&&a.clearTimeout(i),e=void 0,g=h||"",y.readyState=b>0?4:0,j=b>=200&&b<300||304===b,d&&(v=Mb(o,y,d)),v=Nb(o,v,y,j),j?(o.ifModified&&(w=y.getResponseHeader("Last-Modified"),w&&(r.lastModified[f]=w),w=y.getResponseHeader("etag"),w&&(r.etag[f]=w)),204===b||"HEAD"===o.type?x="nocontent":304===b?x="notmodified":(x=v.state,m=v.data,n=v.error,j=!n)):(n=x,!b&&x||(x="error",b<0&&(b=0))),y.status=b,y.statusText=(c||x)+"",j?s.resolveWith(p,[m,x,y]):s.rejectWith(p,[y,x,n]),y.statusCode(u),u=void 0,l&&q.trigger(j?"ajaxSuccess":"ajaxError",[y,o,j?m:n]),t.fireWith(p,[y,x]),l&&(q.trigger("ajaxComplete",[y,o]),--r.active||r.event.trigger("ajaxStop")))}return y},getJSON:function(a,b,c){return r.get(a,b,c,"json")},getScript:function(a,b){return r.get(a,void 0,b,"script")}}),r.each(["get","post"],function(a,b){r[b]=function(a,c,d,e){return r.isFunction(c)&&(e=e||d,d=c,c=void 0),r.ajax(r.extend({url:a,type:b,dataType:e,data:c,success:d},r.isPlainObject(a)&&a))}}),r._evalUrl=function(a){return r.ajax({url:a,type:"GET",dataType:"script",cache:!0,async:!1,global:!1,"throws":!0})},r.fn.extend({wrapAll:function(a){var b;return this[0]&&(r.isFunction(a)&&(a=a.call(this[0])),b=r(a,this[0].ownerDocument).eq(0).clone(!0),this[0].parentNode&&b.insertBefore(this[0]),b.map(function(){var a=this;while(a.firstElementChild)a=a.firstElementChild;return a}).append(this)),this},wrapInner:function(a){return r.isFunction(a)?this.each(function(b){r(this).wrapInner(a.call(this,b))}):this.each(function(){var b=r(this),c=b.contents();c.length?c.wrapAll(a):b.append(a)})},wrap:function(a){var b=r.isFunction(a);return this.each(function(c){r(this).wrapAll(b?a.call(this,c):a)})},unwrap:function(a){return this.parent(a).not("body").each(function(){r(this).replaceWith(this.childNodes)}),this}}),r.expr.pseudos.hidden=function(a){return!r.expr.pseudos.visible(a)},r.expr.pseudos.visible=function(a){return!!(a.offsetWidth||a.offsetHeight||a.getClientRects().length)},r.ajaxSettings.xhr=function(){try{return new a.XMLHttpRequest}catch(b){}};var Ob={0:200,1223:204},Pb=r.ajaxSettings.xhr();o.cors=!!Pb&&"withCredentials"in Pb,o.ajax=Pb=!!Pb,r.ajaxTransport(function(b){var c,d;if(o.cors||Pb&&!b.crossDomain)return{send:function(e,f){var g,h=b.xhr();if(h.open(b.type,b.url,b.async,b.username,b.password),b.xhrFields)for(g in b.xhrFields)h[g]=b.xhrFields[g];b.mimeType&&h.overrideMimeType&&h.overrideMimeType(b.mimeType),b.crossDomain||e["X-Requested-With"]||(e["X-Requested-With"]="XMLHttpRequest");for(g in e)h.setRequestHeader(g,e[g]);c=function(a){return function(){c&&(c=d=h.onload=h.onerror=h.onabort=h.onreadystatechange=null,"abort"===a?h.abort():"error"===a?"number"!=typeof h.status?f(0,"error"):f(h.status,h.statusText):f(Ob[h.status]||h.status,h.statusText,"text"!==(h.responseType||"text")||"string"!=typeof h.responseText?{binary:h.response}:{text:h.responseText},h.getAllResponseHeaders()))}},h.onload=c(),d=h.onerror=c("error"),void 0!==h.onabort?h.onabort=d:h.onreadystatechange=function(){4===h.readyState&&a.setTimeout(function(){c&&d()})},c=c("abort");try{h.send(b.hasContent&&b.data||null)}catch(i){if(c)throw i}},abort:function(){c&&c()}}}),r.ajaxPrefilter(function(a){a.crossDomain&&(a.contents.script=!1)}),r.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/\b(?:java|ecma)script\b/},converters:{"text script":function(a){return r.globalEval(a),a}}}),r.ajaxPrefilter("script",function(a){void 0===a.cache&&(a.cache=!1),a.crossDomain&&(a.type="GET")}),r.ajaxTransport("script",function(a){if(a.crossDomain){var b,c;return{send:function(e,f){b=r("<script>").prop({charset:a.scriptCharset,src:a.url}).on("load error",c=function(a){b.remove(),c=null,a&&f("error"===a.type?404:200,a.type)}),d.head.appendChild(b[0])},abort:function(){c&&c()}}}});var Qb=[],Rb=/(=)\?(?=&|$)|\?\?/;r.ajaxSetup({jsonp:"callback",jsonpCallback:function(){var a=Qb.pop()||r.expando+"_"+rb++;return this[a]=!0,a}}),r.ajaxPrefilter("json jsonp",function(b,c,d){var e,f,g,h=b.jsonp!==!1&&(Rb.test(b.url)?"url":"string"==typeof b.data&&0===(b.contentType||"").indexOf("application/x-www-form-urlencoded")&&Rb.test(b.data)&&"data");if(h||"jsonp"===b.dataTypes[0])return e=b.jsonpCallback=r.isFunction(b.jsonpCallback)?b.jsonpCallback():b.jsonpCallback,h?b[h]=b[h].replace(Rb,"$1"+e):b.jsonp!==!1&&(b.url+=(sb.test(b.url)?"&":"?")+b.jsonp+"="+e),b.converters["script json"]=function(){return g||r.error(e+" was not called"),g[0]},b.dataTypes[0]="json",f=a[e],a[e]=function(){g=arguments},d.always(function(){void 0===f?r(a).removeProp(e):a[e]=f,b[e]&&(b.jsonpCallback=c.jsonpCallback,Qb.push(e)),g&&r.isFunction(f)&&f(g[0]),g=f=void 0}),"script"}),o.createHTMLDocument=function(){var a=d.implementation.createHTMLDocument("").body;return a.innerHTML="<form></form><form></form>",2===a.childNodes.length}(),r.parseHTML=function(a,b,c){if("string"!=typeof a)return[];"boolean"==typeof b&&(c=b,b=!1);var e,f,g;return b||(o.createHTMLDocument?(b=d.implementation.createHTMLDocument(""),e=b.createElement("base"),e.href=d.location.href,b.head.appendChild(e)):b=d),f=B.exec(a),g=!c&&[],f?[b.createElement(f[1])]:(f=oa([a],b,g),g&&g.length&&r(g).remove(),r.merge([],f.childNodes))},r.fn.load=function(a,b,c){var d,e,f,g=this,h=a.indexOf(" ");return h>-1&&(d=r.trim(a.slice(h)),a=a.slice(0,h)),r.isFunction(b)?(c=b,b=void 0):b&&"object"==typeof b&&(e="POST"),g.length>0&&r.ajax({url:a,type:e||"GET",dataType:"html",data:b}).done(function(a){f=arguments,g.html(d?r("<div>").append(r.parseHTML(a)).find(d):a)}).always(c&&function(a,b){g.each(function(){c.apply(this,f||[a.responseText,b,a])})}),this},r.each(["ajaxStart","ajaxStop","ajaxComplete","ajaxError","ajaxSuccess","ajaxSend"],function(a,b){r.fn[b]=function(a){return this.on(b,a)}}),r.expr.pseudos.animated=function(a){return r.grep(r.timers,function(b){return a===b.elem}).length};function Sb(a){return r.isWindow(a)?a:9===a.nodeType&&a.defaultView}r.offset={setOffset:function(a,b,c){var d,e,f,g,h,i,j,k=r.css(a,"position"),l=r(a),m={};"static"===k&&(a.style.position="relative"),h=l.offset(),f=r.css(a,"top"),i=r.css(a,"left"),j=("absolute"===k||"fixed"===k)&&(f+i).indexOf("auto")>-1,j?(d=l.position(),g=d.top,e=d.left):(g=parseFloat(f)||0,e=parseFloat(i)||0),r.isFunction(b)&&(b=b.call(a,c,r.extend({},h))),null!=b.top&&(m.top=b.top-h.top+g),null!=b.left&&(m.left=b.left-h.left+e),"using"in b?b.using.call(a,m):l.css(m)}},r.fn.extend({offset:function(a){if(arguments.length)return void 0===a?this:this.each(function(b){r.offset.setOffset(this,a,b)});var b,c,d,e,f=this[0];if(f)return f.getClientRects().length?(d=f.getBoundingClientRect(),d.width||d.height?(e=f.ownerDocument,c=Sb(e),b=e.documentElement,{top:d.top+c.pageYOffset-b.clientTop,left:d.left+c.pageXOffset-b.clientLeft}):d):{top:0,left:0}},position:function(){if(this[0]){var a,b,c=this[0],d={top:0,left:0};return"fixed"===r.css(c,"position")?b=c.getBoundingClientRect():(a=this.offsetParent(),b=this.offset(),r.nodeName(a[0],"html")||(d=a.offset()),d={top:d.top+r.css(a[0],"borderTopWidth",!0),left:d.left+r.css(a[0],"borderLeftWidth",!0)}),{top:b.top-d.top-r.css(c,"marginTop",!0),left:b.left-d.left-r.css(c,"marginLeft",!0)}}},offsetParent:function(){return this.map(function(){var a=this.offsetParent;while(a&&"static"===r.css(a,"position"))a=a.offsetParent;return a||pa})}}),r.each({scrollLeft:"pageXOffset",scrollTop:"pageYOffset"},function(a,b){var c="pageYOffset"===b;r.fn[a]=function(d){return S(this,function(a,d,e){var f=Sb(a);return void 0===e?f?f[b]:a[d]:void(f?f.scrollTo(c?f.pageXOffset:e,c?e:f.pageYOffset):a[d]=e)},a,d,arguments.length)}}),r.each(["top","left"],function(a,b){r.cssHooks[b]=Na(o.pixelPosition,function(a,c){if(c)return c=Ma(a,b),Ka.test(c)?r(a).position()[b]+"px":c})}),r.each({Height:"height",Width:"width"},function(a,b){r.each({padding:"inner"+a,content:b,"":"outer"+a},function(c,d){r.fn[d]=function(e,f){var g=arguments.length&&(c||"boolean"!=typeof e),h=c||(e===!0||f===!0?"margin":"border");return S(this,function(b,c,e){var f;return r.isWindow(b)?0===d.indexOf("outer")?b["inner"+a]:b.document.documentElement["client"+a]:9===b.nodeType?(f=b.documentElement,Math.max(b.body["scroll"+a],f["scroll"+a],b.body["offset"+a],f["offset"+a],f["client"+a])):void 0===e?r.css(b,c,h):r.style(b,c,e,h)},b,g?e:void 0,g)}})}),r.fn.extend({bind:function(a,b,c){return this.on(a,null,b,c)},unbind:function(a,b){return this.off(a,null,b)},delegate:function(a,b,c,d){return this.on(b,a,c,d)},undelegate:function(a,b,c){return 1===arguments.length?this.off(a,"**"):this.off(b,a||"**",c)}}),r.parseJSON=JSON.parse,"function"==typeof define&&define.amd&&define("jquery",[],function(){return r});var Tb=a.jQuery,Ub=a.$;return r.noConflict=function(b){return a.$===r&&(a.$=Ub),b&&a.jQuery===r&&(a.jQuery=Tb),r},b||(a.jQuery=a.$=r),r});


/*!
 * jQuery Migrate - v3.0.0 - 2016-06-09
 * Copyright jQuery Foundation and other contributors
 */
(function( jQuery, window ) {
"use strict";


jQuery.migrateVersion = "3.0.0";


( function() {

	// Support: IE9 only
	// IE9 only creates console object when dev tools are first opened
	// Also, avoid Function#bind here to simplify PhantomJS usage
	var log = window.console && window.console.log &&
			function() { window.console.log.apply( window.console, arguments ); },
		rbadVersions = /^[12]\./;

	if ( !log ) {
		return;
	}

	// Need jQuery 3.0.0+ and no older Migrate loaded
	if ( !jQuery || rbadVersions.test( jQuery.fn.jquery ) ) {
		log( "JQMIGRATE: jQuery 3.0.0+ REQUIRED" );
	}
	if ( jQuery.migrateWarnings ) {
		log( "JQMIGRATE: Migrate plugin loaded multiple times" );
	}

	// Show a message on the console so devs know we're active
	log( "JQMIGRATE: Migrate is installed" +
		( jQuery.migrateMute ? "" : " with logging active" ) +
		", version " + jQuery.migrateVersion );

} )();

var warnedAbout = {};

// List of warnings already given; public read only
jQuery.migrateWarnings = [];

// Set to false to disable traces that appear with warnings
if ( jQuery.migrateTrace === undefined ) {
	jQuery.migrateTrace = true;
}

// Forget any warnings we've already given; public
jQuery.migrateReset = function() {
	warnedAbout = {};
	jQuery.migrateWarnings.length = 0;
};

function migrateWarn( msg ) {
	var console = window.console;
	if ( !warnedAbout[ msg ] ) {
		warnedAbout[ msg ] = true;
		jQuery.migrateWarnings.push( msg );
		if ( console && console.warn && !jQuery.migrateMute ) {
			console.warn( "JQMIGRATE: " + msg );
			if ( jQuery.migrateTrace && console.trace ) {
				console.trace();
			}
		}
	}
}

function migrateWarnProp( obj, prop, value, msg ) {
	Object.defineProperty( obj, prop, {
		configurable: true,
		enumerable: true,
		get: function() {
			migrateWarn( msg );
			return value;
		}
	} );
}

if ( document.compatMode === "BackCompat" ) {

	// JQuery has never supported or tested Quirks Mode
	migrateWarn( "jQuery is not compatible with Quirks Mode" );
}


var oldInit = jQuery.fn.init,
	oldIsNumeric = jQuery.isNumeric,
	oldFind = jQuery.find,
	rattrHashTest = /\[(\s*[-\w]+\s*)([~|^$*]?=)\s*([-\w#]*?#[-\w#]*)\s*\]/,
	rattrHashGlob = /\[(\s*[-\w]+\s*)([~|^$*]?=)\s*([-\w#]*?#[-\w#]*)\s*\]/g;

jQuery.fn.init = function( arg1 ) {
	var args = Array.prototype.slice.call( arguments );

	if ( typeof arg1 === "string" && arg1 === "#" ) {

		// JQuery( "#" ) is a bogus ID selector, but it returned an empty set before jQuery 3.0
		migrateWarn( "jQuery( '#' ) is not a valid selector" );
		args[ 0 ] = [];
	}

	return oldInit.apply( this, args );
};
jQuery.fn.init.prototype = jQuery.fn;

jQuery.find = function( selector ) {
	var args = Array.prototype.slice.call( arguments );

	// Support: PhantomJS 1.x
	// String#match fails to match when used with a //g RegExp, only on some strings
	if ( typeof selector === "string" && rattrHashTest.test( selector ) ) {

		// The nonstandard and undocumented unquoted-hash was removed in jQuery 1.12.0
		// First see if qS thinks it's a valid selector, if so avoid a false positive
		try {
			document.querySelector( selector );
		} catch ( err1 ) {

			// Didn't *look* valid to qSA, warn and try quoting what we think is the value
			selector = selector.replace( rattrHashGlob, function( _, attr, op, value ) {
				return "[" + attr + op + "\"" + value + "\"]";
			} );

			// If the regexp *may* have created an invalid selector, don't update it
			// Note that there may be false alarms if selector uses jQuery extensions
			try {
				document.querySelector( selector );
				migrateWarn( "Attribute selector with '#' must be quoted: " + args[ 0 ] );
				args[ 0 ] = selector;
			} catch ( err2 ) {
				migrateWarn( "Attribute selector with '#' was not fixed: " + args[ 0 ] );
			}
		}
	}

	return oldFind.apply( this, args );
};

// Copy properties attached to original jQuery.find method (e.g. .attr, .isXML)
var findProp;
for ( findProp in oldFind ) {
	if ( Object.prototype.hasOwnProperty.call( oldFind, findProp ) ) {
		jQuery.find[ findProp ] = oldFind[ findProp ];
	}
}

// The number of elements contained in the matched element set
jQuery.fn.size = function() {
	migrateWarn( "jQuery.fn.size() is deprecated; use the .length property" );
	return this.length;
};

jQuery.parseJSON = function() {
	migrateWarn( "jQuery.parseJSON is deprecated; use JSON.parse" );
	return JSON.parse.apply( null, arguments );
};

jQuery.isNumeric = function( val ) {

	// The jQuery 2.2.3 implementation of isNumeric
	function isNumeric2( obj ) {
		var realStringObj = obj && obj.toString();
		return !jQuery.isArray( obj ) && ( realStringObj - parseFloat( realStringObj ) + 1 ) >= 0;
	}

	var newValue = oldIsNumeric( val ),
		oldValue = isNumeric2( val );

	if ( newValue !== oldValue ) {
		migrateWarn( "jQuery.isNumeric() should not be called on constructed objects" );
	}

	return oldValue;
};

migrateWarnProp( jQuery, "unique", jQuery.uniqueSort,
	"jQuery.unique is deprecated, use jQuery.uniqueSort" );

// Now jQuery.expr.pseudos is the standard incantation
migrateWarnProp( jQuery.expr, "filters", jQuery.expr.pseudos,
	"jQuery.expr.filters is now jQuery.expr.pseudos" );
migrateWarnProp( jQuery.expr, ":", jQuery.expr.pseudos,
	"jQuery.expr[\":\"] is now jQuery.expr.pseudos" );


var oldAjax = jQuery.ajax;

jQuery.ajax = function( ) {
	var jQXHR = oldAjax.apply( this, arguments );

	// Be sure we got a jQXHR (e.g., not sync)
	if ( jQXHR.promise ) {
		migrateWarnProp( jQXHR, "success", jQXHR.done,
			"jQXHR.success is deprecated and removed" );
		migrateWarnProp( jQXHR, "error", jQXHR.fail,
			"jQXHR.error is deprecated and removed" );
		migrateWarnProp( jQXHR, "complete", jQXHR.always,
			"jQXHR.complete is deprecated and removed" );
	}

	return jQXHR;
};


var oldRemoveAttr = jQuery.fn.removeAttr,
	oldToggleClass = jQuery.fn.toggleClass,
	rmatchNonSpace = /\S+/g;

jQuery.fn.removeAttr = function( name ) {
	var self = this;

	jQuery.each( name.match( rmatchNonSpace ), function( i, attr ) {
		if ( jQuery.expr.match.bool.test( attr ) ) {
			migrateWarn( "jQuery.fn.removeAttr no longer sets boolean properties: " + attr );
			self.prop( attr, false );
		}
	} );

	return oldRemoveAttr.apply( this, arguments );
};

jQuery.fn.toggleClass = function( state ) {

	// Only deprecating no-args or single boolean arg
	if ( state !== undefined && typeof state !== "boolean" ) {
		return oldToggleClass.apply( this, arguments );
	}

	migrateWarn( "jQuery.fn.toggleClass( boolean ) is deprecated" );

	// Toggle entire class name of each element
	return this.each( function() {
		var className = this.getAttribute && this.getAttribute( "class" ) || "";

		if ( className ) {
			jQuery.data( this, "__className__", className );
		}

		// If the element has a class name or if we're passed `false`,
		// then remove the whole classname (if there was one, the above saved it).
		// Otherwise bring back whatever was previously saved (if anything),
		// falling back to the empty string if nothing was stored.
		if ( this.setAttribute ) {
			this.setAttribute( "class",
				className || state === false ?
				"" :
				jQuery.data( this, "__className__" ) || ""
			);
		}
	} );
};


var internalSwapCall = false;

// If this version of jQuery has .swap(), don't false-alarm on internal uses
if ( jQuery.swap ) {
	jQuery.each( [ "height", "width", "reliableMarginRight" ], function( _, name ) {
		var oldHook = jQuery.cssHooks[ name ] && jQuery.cssHooks[ name ].get;

		if ( oldHook ) {
			jQuery.cssHooks[ name ].get = function() {
				var ret;

				internalSwapCall = true;
				ret = oldHook.apply( this, arguments );
				internalSwapCall = false;
				return ret;
			};
		}
	} );
}

jQuery.swap = function( elem, options, callback, args ) {
	var ret, name,
		old = {};

	if ( !internalSwapCall ) {
		migrateWarn( "jQuery.swap() is undocumented and deprecated" );
	}

	// Remember the old values, and insert the new ones
	for ( name in options ) {
		old[ name ] = elem.style[ name ];
		elem.style[ name ] = options[ name ];
	}

	ret = callback.apply( elem, args || [] );

	// Revert the old values
	for ( name in options ) {
		elem.style[ name ] = old[ name ];
	}

	return ret;
};

var oldData = jQuery.data;

jQuery.data = function( elem, name, value ) {
	var curData;

	// If the name is transformed, look for the un-transformed name in the data object
	if ( name && name !== jQuery.camelCase( name ) ) {
		curData = jQuery.hasData( elem ) && oldData.call( this, elem );
		if ( curData && name in curData ) {
			migrateWarn( "jQuery.data() always sets/gets camelCased names: " + name );
			if ( arguments.length > 2 ) {
				curData[ name ] = value;
			}
			return curData[ name ];
		}
	}

	return oldData.apply( this, arguments );
};

var oldTweenRun = jQuery.Tween.prototype.run;

jQuery.Tween.prototype.run = function( percent ) {
	if ( jQuery.easing[ this.easing ].length > 1 ) {
		migrateWarn(
			"easing function " +
			"\"jQuery.easing." + this.easing.toString() +
			"\" should use only first argument"
		);

		jQuery.easing[ this.easing ] = jQuery.easing[ this.easing ].bind(
			jQuery.easing,
			percent, this.options.duration * percent, 0, 1, this.options.duration
		);
	}

	oldTweenRun.apply( this, arguments );
};

var oldLoad = jQuery.fn.load,
	originalFix = jQuery.event.fix;

jQuery.event.props = [];
jQuery.event.fixHooks = {};

jQuery.event.fix = function( originalEvent ) {
	var event,
		type = originalEvent.type,
		fixHook = this.fixHooks[ type ],
		props = jQuery.event.props;

	if ( props.length ) {
		migrateWarn( "jQuery.event.props are deprecated and removed: " + props.join() );
		while ( props.length ) {
			jQuery.event.addProp( props.pop() );
		}
	}

	if ( fixHook && !fixHook._migrated_ ) {
		fixHook._migrated_ = true;
		migrateWarn( "jQuery.event.fixHooks are deprecated and removed: " + type );
		if ( ( props = fixHook.props ) && props.length ) {
			while ( props.length ) {
			   jQuery.event.addProp( props.pop() );
			}
		}
	}

	event = originalFix.call( this, originalEvent );

	return fixHook && fixHook.filter ? fixHook.filter( event, originalEvent ) : event;
};

jQuery.each( [ "load", "unload", "error" ], function( _, name ) {

	jQuery.fn[ name ] = function() {
		var args = Array.prototype.slice.call( arguments, 0 );

		// If this is an ajax load() the first arg should be the string URL;
		// technically this could also be the "Anything" arg of the event .load()
		// which just goes to show why this dumb signature has been deprecated!
		// jQuery custom builds that exclude the Ajax module justifiably die here.
		if ( name === "load" && typeof args[ 0 ] === "string" ) {
			return oldLoad.apply( this, args );
		}

		migrateWarn( "jQuery.fn." + name + "() is deprecated" );

		args.splice( 0, 0, name );
		if ( arguments.length ) {
			return this.on.apply( this, args );
		}

		// Use .triggerHandler here because:
		// - load and unload events don't need to bubble, only applied to window or image
		// - error event should not bubble to window, although it does pre-1.7
		// See http://bugs.jquery.com/ticket/11820
		this.triggerHandler.apply( this, args );
		return this;
	};

} );

// Trigger "ready" event only once, on document ready
jQuery( function() {
	jQuery( document ).triggerHandler( "ready" );
} );

jQuery.event.special.ready = {
	setup: function() {
		if ( this === document ) {
			migrateWarn( "'ready' event is deprecated" );
		}
	}
};

jQuery.fn.extend( {

	bind: function( types, data, fn ) {
		migrateWarn( "jQuery.fn.bind() is deprecated" );
		return this.on( types, null, data, fn );
	},
	unbind: function( types, fn ) {
		migrateWarn( "jQuery.fn.unbind() is deprecated" );
		return this.off( types, null, fn );
	},
	delegate: function( selector, types, data, fn ) {
		migrateWarn( "jQuery.fn.delegate() is deprecated" );
		return this.on( types, selector, data, fn );
	},
	undelegate: function( selector, types, fn ) {
		migrateWarn( "jQuery.fn.undelegate() is deprecated" );
		return arguments.length === 1 ?
			this.off( selector, "**" ) :
			this.off( types, selector || "**", fn );
	}
} );


var oldOffset = jQuery.fn.offset;

jQuery.fn.offset = function() {
	var docElem,
		elem = this[ 0 ],
		origin = { top: 0, left: 0 };

	if ( !elem || !elem.nodeType ) {
		migrateWarn( "jQuery.fn.offset() requires a valid DOM element" );
		return origin;
	}

	docElem = ( elem.ownerDocument || document ).documentElement;
	if ( !jQuery.contains( docElem, elem ) ) {
		migrateWarn( "jQuery.fn.offset() requires an element connected to a document" );
		return origin;
	}

	return oldOffset.apply( this, arguments );
};


var oldParam = jQuery.param;

jQuery.param = function( data, traditional ) {
	var ajaxTraditional = jQuery.ajaxSettings && jQuery.ajaxSettings.traditional;

	if ( traditional === undefined && ajaxTraditional ) {

		migrateWarn( "jQuery.param() no longer uses jQuery.ajaxSettings.traditional" );
		traditional = ajaxTraditional;
	}

	return oldParam.call( this, data, traditional );
};

var oldSelf = jQuery.fn.andSelf || jQuery.fn.addBack;

jQuery.fn.andSelf = function() {
	migrateWarn( "jQuery.fn.andSelf() replaced by jQuery.fn.addBack()" );
	return oldSelf.apply( this, arguments );
};


var oldDeferred = jQuery.Deferred,
	tuples = [

		// Action, add listener, callbacks, .then handlers, final state
		[ "resolve", "done", jQuery.Callbacks( "once memory" ),
			jQuery.Callbacks( "once memory" ), "resolved" ],
		[ "reject", "fail", jQuery.Callbacks( "once memory" ),
			jQuery.Callbacks( "once memory" ), "rejected" ],
		[ "notify", "progress", jQuery.Callbacks( "memory" ),
			jQuery.Callbacks( "memory" ) ]
	];

jQuery.Deferred = function( func ) {
	var deferred = oldDeferred(),
		promise = deferred.promise();

	deferred.pipe = promise.pipe = function( /* fnDone, fnFail, fnProgress */ ) {
		var fns = arguments;

		migrateWarn( "deferred.pipe() is deprecated" );

		return jQuery.Deferred( function( newDefer ) {
			jQuery.each( tuples, function( i, tuple ) {
				var fn = jQuery.isFunction( fns[ i ] ) && fns[ i ];

				// Deferred.done(function() { bind to newDefer or newDefer.resolve })
				// deferred.fail(function() { bind to newDefer or newDefer.reject })
				// deferred.progress(function() { bind to newDefer or newDefer.notify })
				deferred[ tuple[ 1 ] ]( function() {
					var returned = fn && fn.apply( this, arguments );
					if ( returned && jQuery.isFunction( returned.promise ) ) {
						returned.promise()
							.done( newDefer.resolve )
							.fail( newDefer.reject )
							.progress( newDefer.notify );
					} else {
						newDefer[ tuple[ 0 ] + "With" ](
							this === promise ? newDefer.promise() : this,
							fn ? [ returned ] : arguments
						);
					}
				} );
			} );
			fns = null;
		} ).promise();

	};

	if ( func ) {
		func.call( deferred, deferred );
	}

	return deferred;
};



})( jQuery, window );


/*!
Waypoints - 4.0.0
Copyright © 2011-2015 Caleb Troughton
Licensed under the MIT license.
https://github.com/imakewebthings/waypoints/blog/master/licenses.txt
*/
!function(){"use strict";function t(o){if(!o)throw new Error("No options passed to Waypoint constructor");if(!o.element)throw new Error("No element option passed to Waypoint constructor");if(!o.handler)throw new Error("No handler option passed to Waypoint constructor");this.key="waypoint-"+e,this.options=t.Adapter.extend({},t.defaults,o),this.element=this.options.element,this.adapter=new t.Adapter(this.element),this.callback=o.handler,this.axis=this.options.horizontal?"horizontal":"vertical",this.enabled=this.options.enabled,this.triggerPoint=null,this.group=t.Group.findOrCreate({name:this.options.group,axis:this.axis}),this.context=t.Context.findOrCreateByElement(this.options.context),t.offsetAliases[this.options.offset]&&(this.options.offset=t.offsetAliases[this.options.offset]),this.group.add(this),this.context.add(this),i[this.key]=this,e+=1}var e=0,i={};t.prototype.queueTrigger=function(t){this.group.queueTrigger(this,t)},t.prototype.trigger=function(t){this.enabled&&this.callback&&this.callback.apply(this,t)},t.prototype.destroy=function(){this.context.remove(this),this.group.remove(this),delete i[this.key]},t.prototype.disable=function(){return this.enabled=!1,this},t.prototype.enable=function(){return this.context.refresh(),this.enabled=!0,this},t.prototype.next=function(){return this.group.next(this)},t.prototype.previous=function(){return this.group.previous(this)},t.invokeAll=function(t){var e=[];for(var o in i)e.push(i[o]);for(var n=0,r=e.length;r>n;n++)e[n][t]()},t.destroyAll=function(){t.invokeAll("destroy")},t.disableAll=function(){t.invokeAll("disable")},t.enableAll=function(){t.invokeAll("enable")},t.refreshAll=function(){t.Context.refreshAll()},t.viewportHeight=function(){return window.innerHeight||document.documentElement.clientHeight},t.viewportWidth=function(){return document.documentElement.clientWidth},t.adapters=[],t.defaults={context:window,continuous:!0,enabled:!0,group:"default",horizontal:!1,offset:0},t.offsetAliases={"bottom-in-view":function(){return this.context.innerHeight()-this.adapter.outerHeight()},"right-in-view":function(){return this.context.innerWidth()-this.adapter.outerWidth()}},window.Waypoint=t}(),function(){"use strict";function t(t){window.setTimeout(t,1e3/60)}function e(t){this.element=t,this.Adapter=n.Adapter,this.adapter=new this.Adapter(t),this.key="waypoint-context-"+i,this.didScroll=!1,this.didResize=!1,this.oldScroll={x:this.adapter.scrollLeft(),y:this.adapter.scrollTop()},this.waypoints={vertical:{},horizontal:{}},t.waypointContextKey=this.key,o[t.waypointContextKey]=this,i+=1,this.createThrottledScrollHandler(),this.createThrottledResizeHandler()}var i=0,o={},n=window.Waypoint,r=window.onload;e.prototype.add=function(t){var e=t.options.horizontal?"horizontal":"vertical";this.waypoints[e][t.key]=t,this.refresh()},e.prototype.checkEmpty=function(){var t=this.Adapter.isEmptyObject(this.waypoints.horizontal),e=this.Adapter.isEmptyObject(this.waypoints.vertical);t&&e&&(this.adapter.off(".waypoints"),delete o[this.key])},e.prototype.createThrottledResizeHandler=function(){function t(){e.handleResize(),e.didResize=!1}var e=this;this.adapter.on("resize.waypoints",function(){e.didResize||(e.didResize=!0,n.requestAnimationFrame(t))})},e.prototype.createThrottledScrollHandler=function(){function t(){e.handleScroll(),e.didScroll=!1}var e=this;this.adapter.on("scroll.waypoints",function(){(!e.didScroll||n.isTouch)&&(e.didScroll=!0,n.requestAnimationFrame(t))})},e.prototype.handleResize=function(){n.Context.refreshAll()},e.prototype.handleScroll=function(){var t={},e={horizontal:{newScroll:this.adapter.scrollLeft(),oldScroll:this.oldScroll.x,forward:"right",backward:"left"},vertical:{newScroll:this.adapter.scrollTop(),oldScroll:this.oldScroll.y,forward:"down",backward:"up"}};for(var i in e){var o=e[i],n=o.newScroll>o.oldScroll,r=n?o.forward:o.backward;for(var s in this.waypoints[i]){var a=this.waypoints[i][s],l=o.oldScroll<a.triggerPoint,h=o.newScroll>=a.triggerPoint,p=l&&h,u=!l&&!h;(p||u)&&(a.queueTrigger(r),t[a.group.id]=a.group)}}for(var c in t)t[c].flushTriggers();this.oldScroll={x:e.horizontal.newScroll,y:e.vertical.newScroll}},e.prototype.innerHeight=function(){return this.element==this.element.window?n.viewportHeight():this.adapter.innerHeight()},e.prototype.remove=function(t){delete this.waypoints[t.axis][t.key],this.checkEmpty()},e.prototype.innerWidth=function(){return this.element==this.element.window?n.viewportWidth():this.adapter.innerWidth()},e.prototype.destroy=function(){var t=[];for(var e in this.waypoints)for(var i in this.waypoints[e])t.push(this.waypoints[e][i]);for(var o=0,n=t.length;n>o;o++)t[o].destroy()},e.prototype.refresh=function(){var t,e=this.element==this.element.window,i=e?void 0:this.adapter.offset(),o={};this.handleScroll(),t={horizontal:{contextOffset:e?0:i.left,contextScroll:e?0:this.oldScroll.x,contextDimension:this.innerWidth(),oldScroll:this.oldScroll.x,forward:"right",backward:"left",offsetProp:"left"},vertical:{contextOffset:e?0:i.top,contextScroll:e?0:this.oldScroll.y,contextDimension:this.innerHeight(),oldScroll:this.oldScroll.y,forward:"down",backward:"up",offsetProp:"top"}};for(var r in t){var s=t[r];for(var a in this.waypoints[r]){var l,h,p,u,c,d=this.waypoints[r][a],f=d.options.offset,w=d.triggerPoint,y=0,g=null==w;d.element!==d.element.window&&(y=d.adapter.offset()[s.offsetProp]),"function"==typeof f?f=f.apply(d):"string"==typeof f&&(f=parseFloat(f),d.options.offset.indexOf("%")>-1&&(f=Math.ceil(s.contextDimension*f/100))),l=s.contextScroll-s.contextOffset,d.triggerPoint=y+l-f,h=w<s.oldScroll,p=d.triggerPoint>=s.oldScroll,u=h&&p,c=!h&&!p,!g&&u?(d.queueTrigger(s.backward),o[d.group.id]=d.group):!g&&c?(d.queueTrigger(s.forward),o[d.group.id]=d.group):g&&s.oldScroll>=d.triggerPoint&&(d.queueTrigger(s.forward),o[d.group.id]=d.group)}}return n.requestAnimationFrame(function(){for(var t in o)o[t].flushTriggers()}),this},e.findOrCreateByElement=function(t){return e.findByElement(t)||new e(t)},e.refreshAll=function(){for(var t in o)o[t].refresh()},e.findByElement=function(t){return o[t.waypointContextKey]},window.onload=function(){r&&r(),e.refreshAll()},n.requestAnimationFrame=function(e){var i=window.requestAnimationFrame||window.mozRequestAnimationFrame||window.webkitRequestAnimationFrame||t;i.call(window,e)},n.Context=e}(),function(){"use strict";function t(t,e){return t.triggerPoint-e.triggerPoint}function e(t,e){return e.triggerPoint-t.triggerPoint}function i(t){this.name=t.name,this.axis=t.axis,this.id=this.name+"-"+this.axis,this.waypoints=[],this.clearTriggerQueues(),o[this.axis][this.name]=this}var o={vertical:{},horizontal:{}},n=window.Waypoint;i.prototype.add=function(t){this.waypoints.push(t)},i.prototype.clearTriggerQueues=function(){this.triggerQueues={up:[],down:[],left:[],right:[]}},i.prototype.flushTriggers=function(){for(var i in this.triggerQueues){var o=this.triggerQueues[i],n="up"===i||"left"===i;o.sort(n?e:t);for(var r=0,s=o.length;s>r;r+=1){var a=o[r];(a.options.continuous||r===o.length-1)&&a.trigger([i])}}this.clearTriggerQueues()},i.prototype.next=function(e){this.waypoints.sort(t);var i=n.Adapter.inArray(e,this.waypoints),o=i===this.waypoints.length-1;return o?null:this.waypoints[i+1]},i.prototype.previous=function(e){this.waypoints.sort(t);var i=n.Adapter.inArray(e,this.waypoints);return i?this.waypoints[i-1]:null},i.prototype.queueTrigger=function(t,e){this.triggerQueues[e].push(t)},i.prototype.remove=function(t){var e=n.Adapter.inArray(t,this.waypoints);e>-1&&this.waypoints.splice(e,1)},i.prototype.first=function(){return this.waypoints[0]},i.prototype.last=function(){return this.waypoints[this.waypoints.length-1]},i.findOrCreate=function(t){return o[t.axis][t.name]||new i(t)},n.Group=i}(),function(){"use strict";function t(t){this.$element=e(t)}var e=window.jQuery,i=window.Waypoint;e.each(["innerHeight","innerWidth","off","offset","on","outerHeight","outerWidth","scrollLeft","scrollTop"],function(e,i){t.prototype[i]=function(){var t=Array.prototype.slice.call(arguments);return this.$element[i].apply(this.$element,t)}}),e.each(["extend","inArray","isEmptyObject"],function(i,o){t[o]=e[o]}),i.adapters.push({name:"jquery",Adapter:t}),i.Adapter=t}(),function(){"use strict";function t(t){return function(){var i=[],o=arguments[0];return t.isFunction(arguments[0])&&(o=t.extend({},arguments[1]),o.handler=arguments[0]),this.each(function(){var n=t.extend({},o,{element:this});"string"==typeof n.context&&(n.context=t(this).closest(n.context)[0]),i.push(new e(n))}),i}}var e=window.Waypoint;window.jQuery&&(window.jQuery.fn.waypoint=t(window.jQuery)),window.Zepto&&(window.Zepto.fn.waypoint=t(window.Zepto))}();

/*!
Waypoints Inview Shortcut - 4.0.0
Copyright © 2011-2015 Caleb Troughton
Licensed under the MIT license.
https://github.com/imakewebthings/waypoints/blog/master/licenses.txt
*/
!function(){"use strict";function t(){}function e(t){this.options=i.Adapter.extend({},e.defaults,t),this.axis=this.options.horizontal?"horizontal":"vertical",this.waypoints=[],this.element=this.options.element,this.createWaypoints()}var i=window.Waypoint;e.prototype.createWaypoints=function(){for(var t={vertical:[{down:"enter",up:"exited",offset:"100%"},{down:"entered",up:"exit",offset:"bottom-in-view"},{down:"exit",up:"entered",offset:0},{down:"exited",up:"enter",offset:function(){return-this.adapter.outerHeight()}}],horizontal:[{right:"enter",left:"exited",offset:"100%"},{right:"entered",left:"exit",offset:"right-in-view"},{right:"exit",left:"entered",offset:0},{right:"exited",left:"enter",offset:function(){return-this.adapter.outerWidth()}}]},e=0,i=t[this.axis].length;i>e;e++){var n=t[this.axis][e];this.createWaypoint(n)}},e.prototype.createWaypoint=function(t){var e=this;this.waypoints.push(new i({context:this.options.context,element:this.options.element,enabled:this.options.enabled,handler:function(t){return function(i){e.options[t[i]].call(e,i)}}(t),offset:t.offset,horizontal:this.options.horizontal}))},e.prototype.destroy=function(){for(var t=0,e=this.waypoints.length;e>t;t++)this.waypoints[t].destroy();this.waypoints=[]},e.prototype.disable=function(){for(var t=0,e=this.waypoints.length;e>t;t++)this.waypoints[t].disable()},e.prototype.enable=function(){for(var t=0,e=this.waypoints.length;e>t;t++)this.waypoints[t].enable()},e.defaults={context:window,enabled:!0,enter:t,entered:t,exit:t,exited:t},i.Inview=e}();

// Check for jQuery.
if ( typeof(jQuery) === 'undefined' ) {
	var jQuery;
	// Check if require is a defined function.
	if ( typeof(require) === 'function' ) {
		jQuery = $ = require( 'jquery' );
		// Else use the dollar sign alias.
	} else {
		jQuery = $;
	}
}
;/*
 * jQuery Easing v1.4.1 - http://gsgd.co.uk/sandbox/jquery/easing/
 * Open source under the BSD License.
 * Copyright © 2008 George McGinley Smith
 * All rights reserved.
 * https://raw.github.com/gdsmith/jquery-easing/master/LICENSE
 */

(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define( [ 'jquery' ], function( $ ) {
			return factory( $ );
		} );
	} else {
		if ( typeof module === "object" && typeof module.exports === "object" ) {
			exports = factory( require( 'jquery' ) );
		} else {
			factory( jQuery );
		}
	}
})( function( $ ) {

	// Preserve the original jQuery "swing" easing as "jswing"
	$.easing.jswing = $.easing.swing;

	var pow = Math.pow,
		sqrt = Math.sqrt,
		sin = Math.sin,
		cos = Math.cos,
		PI = Math.PI,
		c1 = 1.70158,
		c2 = c1 * 1.525,
		c3 = c1 + 1,
		c4 = ( 2 * PI ) / 3,
		c5 = ( 2 * PI ) / 4.5;

	// x is the fraction of animation progress, in the range 0..1
	function bounceOut( x ) {
		var n1 = 7.5625,
			d1 = 2.75;
		if ( x < 1 / d1 ) {
			return n1 * x * x;
		} else {
			if ( x < 2 / d1 ) {
				return n1 * (x -= (1.5 / d1)) * x + 0.75;
			} else {
				if ( x < 2.5 / d1 ) {
					return n1 * (x -= (2.25 / d1)) * x + 0.9375;
				} else {
					return n1 * (x -= (2.625 / d1)) * x + 0.984375;
				}
			}
		}
	}

	$.extend( $.easing,
		{
			def: 'easeOutQuad',
			swing: function( x ) {
				return $.easing[ $.easing.def ]( x );
			},
			easeInQuad: function( x ) {
				return x * x;
			},
			easeOutQuad: function( x ) {
				return 1 - ( 1 - x ) * ( 1 - x );
			},
			easeInOutQuad: function( x ) {
				return x < 0.5 ?
					   2 * x * x :
					   1 - pow( - 2 * x + 2, 2 ) / 2;
			},
			easeInCubic: function( x ) {
				return x * x * x;
			},
			easeOutCubic: function( x ) {
				return 1 - pow( 1 - x, 3 );
			},
			easeInOutCubic: function( x ) {
				return x < 0.5 ?
					   4 * x * x * x :
					   1 - pow( - 2 * x + 2, 3 ) / 2;
			},
			easeInQuart: function( x ) {
				return x * x * x * x;
			},
			easeOutQuart: function( x ) {
				return 1 - pow( 1 - x, 4 );
			},
			easeInOutQuart: function( x ) {
				return x < 0.5 ?
					   8 * x * x * x * x :
					   1 - pow( - 2 * x + 2, 4 ) / 2;
			},
			easeInQuint: function( x ) {
				return x * x * x * x * x;
			},
			easeOutQuint: function( x ) {
				return 1 - pow( 1 - x, 5 );
			},
			easeInOutQuint: function( x ) {
				return x < 0.5 ?
					   16 * x * x * x * x * x :
					   1 - pow( - 2 * x + 2, 5 ) / 2;
			},
			easeInSine: function( x ) {
				return 1 - cos( x * PI / 2 );
			},
			easeOutSine: function( x ) {
				return sin( x * PI / 2 );
			},
			easeInOutSine: function( x ) {
				return - ( cos( PI * x ) - 1 ) / 2;
			},
			easeInExpo: function( x ) {
				return x === 0 ? 0 : pow( 2, 10 * x - 10 );
			},
			easeOutExpo: function( x ) {
				return x === 1 ? 1 : 1 - pow( 2, - 10 * x );
			},
			easeInOutExpo: function( x ) {
				return x === 0 ? 0 : x === 1 ? 1 : x < 0.5 ?
												   pow( 2, 20 * x - 10 ) / 2 :
												   ( 2 - pow( 2, - 20 * x + 10 ) ) / 2;
			},
			easeInCirc: function( x ) {
				return 1 - sqrt( 1 - pow( x, 2 ) );
			},
			easeOutCirc: function( x ) {
				return sqrt( 1 - pow( x - 1, 2 ) );
			},
			easeInOutCirc: function( x ) {
				return x < 0.5 ?
					   ( 1 - sqrt( 1 - pow( 2 * x, 2 ) ) ) / 2 :
					   ( sqrt( 1 - pow( - 2 * x + 2, 2 ) ) + 1 ) / 2;
			},
			easeInElastic: function( x ) {
				return x === 0 ? 0 : x === 1 ? 1 :
									 - pow( 2, 10 * x - 10 ) * sin( ( x * 10 - 10.75 ) * c4 );
			},
			easeOutElastic: function( x ) {
				return x === 0 ? 0 : x === 1 ? 1 :
									 pow( 2, - 10 * x ) * sin( ( x * 10 - 0.75 ) * c4 ) + 1;
			},
			easeInOutElastic: function( x ) {
				return x === 0 ? 0 : x === 1 ? 1 : x < 0.5 ?
												   - ( pow( 2, 20 * x - 10 ) * sin( ( 20 * x - 11.125 ) * c5 )) / 2 :
												   pow( 2, - 20 * x + 10 ) * sin( ( 20 * x - 11.125 ) * c5 ) / 2 + 1;
			},
			easeInBack: function( x ) {
				return c3 * x * x * x - c1 * x * x;
			},
			easeOutBack: function( x ) {
				return 1 + c3 * pow( x - 1, 3 ) + c1 * pow( x - 1, 2 );
			},
			easeInOutBack: function( x ) {
				return x < 0.5 ?
					   ( pow( 2 * x, 2 ) * ( ( c2 + 1 ) * 2 * x - c2 ) ) / 2 :
					   ( pow( 2 * x - 2, 2 ) * ( ( c2 + 1 ) * ( x * 2 - 2 ) + c2 ) + 2 ) / 2;
			},
			easeInBounce: function( x ) {
				return 1 - bounceOut( 1 - x );
			},
			easeOutBounce: bounceOut,
			easeInOutBounce: function( x ) {
				return x < 0.5 ?
					   ( 1 - bounceOut( 1 - 2 * x ) ) / 2 :
					   ( 1 + bounceOut( 2 * x - 1 ) ) / 2;
			}
		} );

} );
;    // Custom Easing
jQuery.extend( jQuery.easing,
	{
		easeInOutMaterial: function( x, t, b, c, d ) {
			if ( (t /= d / 2) < 1 ) {
				return c / 2 * t * t + b;
			}
			return c / 4 * ((t -= 2) * t * t + 2) + b;
		}
	} );

;/*! VelocityJS.org (1.2.3). (C) 2014 Julian Shapiro. MIT @license: en.wikipedia.org/wiki/MIT_License */
/*! VelocityJS.org jQuery Shim (1.0.1). (C) 2014 The jQuery Foundation. MIT @license: en.wikipedia.org/wiki/MIT_License. */
/*! Note that this has been modified by Materialize to confirm that Velocity is not already being imported. */
jQuery.Velocity ? console.log( "Velocity is already loaded. You may be needlessly importing Velocity again; note that Materialize includes Velocity." ) : (! function( e ) {
	function t( e ) {
		var t = e.length, a = r.type( e );
		return "function" === a || r.isWindow( e ) ? ! 1 : 1 === e.nodeType && t ? ! 0 : "array" === a || 0 === t || "number" == typeof t && t > 0 && t - 1 in e
	}

	if ( ! e.jQuery ) {
		var r = function( e, t ) {
			return new r.fn.init( e, t )
		};
		r.isWindow = function( e ) {
			return null != e && e == e.window
		}, r.type = function( e ) {
			return null == e ? e + "" : "object" == typeof e || "function" == typeof e ? n[ i.call( e ) ] || "object" : typeof e
		}, r.isArray = Array.isArray || function( e ) {
				return "array" === r.type( e )
			}, r.isPlainObject = function( e ) {
			var t;
			if ( ! e || "object" !== r.type( e ) || e.nodeType || r.isWindow( e ) ) {
				return ! 1;
			}
			try {
				if ( e.constructor && ! o.call( e, "constructor" ) && ! o.call( e.constructor.prototype, "isPrototypeOf" ) ) {
					return ! 1
				}
			} catch ( a ) {
				return ! 1
			}
			for ( t in e );
			return void 0 === t || o.call( e, t )
		}, r.each = function( e, r, a ) {
			var n, o = 0, i = e.length, s = t( e );
			if ( a ) {
				if ( s ) {
					for ( ; i > o && (n = r.apply( e[ o ], a ), n !== ! 1); o ++ );
				} else {
					for ( o in e )if ( n = r.apply( e[ o ], a ), n === ! 1 ) {
						break
					}
				}
			} else {
				if ( s ) {
					for ( ; i > o && (n = r.call( e[ o ], o, e[ o ] ), n !== ! 1); o ++ );
				} else {
					for ( o in e )if ( n = r.call( e[ o ], o, e[ o ] ), n === ! 1 ) {
						break;
					}
				}
			}
			return e
		}, r.data = function( e, t, n ) {
			if ( void 0 === n ) {
				var o = e[ r.expando ], i = o && a[ o ];
				if ( void 0 === t ) {
					return i;
				}
				if ( i && t in i ) {
					return i[ t ]
				}
			} else {
				if ( void 0 !== t ) {
					var o = e[ r.expando ] || (e[ r.expando ] = ++ r.uuid);
					return a[ o ] = a[ o ] || {}, a[ o ][ t ] = n, n
				}
			}
		}, r.removeData = function( e, t ) {
			var n = e[ r.expando ], o = n && a[ n ];
			o && r.each( t, function( e, t ) {
				delete o[ t ]
			} )
		}, r.extend = function() {
			var e, t, a, n, o, i, s = arguments[ 0 ] || {}, l = 1, u = arguments.length, c = ! 1;
			for ( "boolean" == typeof s && (c = s, s = arguments[ l ] || {}, l ++), "object" != typeof s && "function" !== r.type( s ) && (s = {}), l === u && (s = this, l --); u > l; l ++ )if ( null != (o = arguments[ l ]) ) {
				for ( n in o )e = s[ n ], a = o[ n ], s !== a && (c && a && (r.isPlainObject( a ) || (t = r.isArray( a ))) ? (t ? (t = ! 1, i = e && r.isArray( e ) ? e : []) : i = e && r.isPlainObject( e ) ? e : {}, s[ n ] = r.extend( c, i, a )) : void 0 !== a && (s[ n ] = a));
			}
			return s
		}, r.queue = function( e, a, n ) {
			function o( e, r ) {
				var a = r || [];
				return null != e && (t( Object( e ) ) ? ! function( e, t ) {
					for ( var r = + t.length, a = 0, n = e.length; r > a; )e[ n ++ ] = t[ a ++ ];
					if ( r !== r ) {
						for ( ; void 0 !== t[ a ]; )e[ n ++ ] = t[ a ++ ];
					}
					return e.length = n, e
				}( a, "string" == typeof e ? [ e ] : e ) : [].push.call( a, e )), a
			}

			if ( e ) {
				a = (a || "fx") + "queue";
				var i = r.data( e, a );
				return n ? (! i || r.isArray( n ) ? i = r.data( e, a, o( n ) ) : i.push( n ), i) : i || []
			}
		}, r.dequeue = function( e, t ) {
			r.each( e.nodeType ? [ e ] : e, function( e, a ) {
				t = t || "fx";
				var n = r.queue( a, t ), o = n.shift();
				"inprogress" === o && (o = n.shift()), o && ("fx" === t && n.unshift( "inprogress" ), o.call( a, function() {
					r.dequeue( a, t )
				} ))
			} )
		}, r.fn = r.prototype = {
			init: function( e ) {
				if ( e.nodeType ) {
					return this[ 0 ] = e, this;
				}
				throw new Error( "Not a DOM node." )
			}, offset: function() {
				var t = this[ 0 ].getBoundingClientRect ? this[ 0 ].getBoundingClientRect() : {
					top: 0,
					left: 0
				};
				return {
					top: t.top + (e.pageYOffset || document.scrollTop || 0) - (document.clientTop || 0),
					left: t.left + (e.pageXOffset || document.scrollLeft || 0) - (document.clientLeft || 0)
				}
			}, position: function() {
				function e() {
					for ( var e = this.offsetParent || document; e && "html" === ! e.nodeType.toLowerCase && "static" === e.style.position; )e = e.offsetParent;
					return e || document
				}

				var t = this[ 0 ], e = e.apply( t ), a = this.offset(), n = /^(?:body|html)$/i.test( e.nodeName ) ? {
					top: 0,
					left: 0
				} : r( e ).offset();
				return a.top -= parseFloat( t.style.marginTop ) || 0, a.left -= parseFloat( t.style.marginLeft ) || 0, e.style && (n.top += parseFloat( e.style.borderTopWidth ) || 0, n.left += parseFloat( e.style.borderLeftWidth ) || 0), {
					top: a.top - n.top,
					left: a.left - n.left
				}
			}
		};
		var a = {};
		r.expando = "velocity" + (new Date).getTime(), r.uuid = 0;
		for ( var n = {}, o = n.hasOwnProperty, i = n.toString, s = "Boolean Number String Function Array Date RegExp Object Error".split( " " ), l = 0; l < s.length; l ++ )n[ "[object " + s[ l ] + "]" ] = s[ l ].toLowerCase();
		r.fn.init.prototype = r.fn, e.Velocity = { Utilities: r }
	}
}( window ), function( e ) {
	"object" == typeof module && "object" == typeof module.exports ? module.exports = e() : "function" == typeof define && define.amd ? define( e ) : e()
}( function() {
	return function( e, t, r, a ) {
		function n( e ) {
			for ( var t = - 1, r = e ? e.length : 0, a = []; ++ t < r; ) {
				var n = e[ t ];
				n && a.push( n )
			}
			return a
		}

		function o( e ) {
			return m.isWrapped( e ) ? e = [].slice.call( e ) : m.isNode( e ) && (e = [ e ]), e
		}

		function i( e ) {
			var t = f.data( e, "velocity" );
			return null === t ? a : t
		}

		function s( e ) {
			return function( t ) {
				return Math.round( t * e ) * (1 / e)
			}
		}

		function l( e, r, a, n ) {
			function o( e, t ) {
				return 1 - 3 * t + 3 * e
			}

			function i( e, t ) {
				return 3 * t - 6 * e
			}

			function s( e ) {
				return 3 * e
			}

			function l( e, t, r ) {
				return ((o( t, r ) * e + i( t, r )) * e + s( t )) * e
			}

			function u( e, t, r ) {
				return 3 * o( t, r ) * e * e + 2 * i( t, r ) * e + s( t )
			}

			function c( t, r ) {
				for ( var n = 0; m > n; ++ n ) {
					var o = u( r, e, a );
					if ( 0 === o ) {
						return r;
					}
					var i = l( r, e, a ) - t;
					r -= i / o
				}
				return r
			}

			function p() {
				for ( var t = 0; b > t; ++ t )w[ t ] = l( t * x, e, a )
			}

			function f( t, r, n ) {
				var o, i, s = 0;
				do i = r + (n - r) / 2, o = l( i, e, a ) - t, o > 0 ? n = i : r = i; while ( Math.abs( o ) > h && ++ s < v );
				return i
			}

			function d( t ) {
				for ( var r = 0, n = 1, o = b - 1; n != o && w[ n ] <= t; ++ n )r += x;
				-- n;
				var i = (t - w[ n ]) / (w[ n + 1 ] - w[ n ]), s = r + i * x, l = u( s, e, a );
				return l >= y ? c( t, s ) : 0 == l ? s : f( t, r, r + x )
			}

			function g() {
				V = ! 0, (e != r || a != n) && p()
			}

			var m = 4, y = .001, h = 1e-7, v = 10, b = 11, x = 1 / (b - 1), S = "Float32Array" in t;
			if ( 4 !== arguments.length ) {
				return ! 1;
			}
			for ( var P = 0; 4 > P; ++ P )if ( "number" != typeof arguments[ P ] || isNaN( arguments[ P ] ) || ! isFinite( arguments[ P ] ) ) {
				return ! 1;
			}
			e = Math.min( e, 1 ), a = Math.min( a, 1 ), e = Math.max( e, 0 ), a = Math.max( a, 0 );
			var w = S ? new Float32Array( b ) : new Array( b ), V = ! 1, C = function( t ) {
				return V || g(), e === r && a === n ? t : 0 === t ? 0 : 1 === t ? 1 : l( d( t ), r, n )
			};
			C.getControlPoints = function() {
				return [ { x: e, y: r }, { x: a, y: n } ]
			};
			var T = "generateBezier(" + [ e, r, a, n ] + ")";
			return C.toString = function() {
				return T
			}, C
		}

		function u( e, t ) {
			var r = e;
			return m.isString( e ) ? b.Easings[ e ] || (r = ! 1) : r = m.isArray( e ) && 1 === e.length ? s.apply( null, e ) : m.isArray( e ) && 2 === e.length ? x.apply( null, e.concat( [ t ] ) ) : m.isArray( e ) && 4 === e.length ? l.apply( null, e ) : ! 1, r === ! 1 && (r = b.Easings[ b.defaults.easing ] ? b.defaults.easing : v), r
		}

		function c( e ) {
			if ( e ) {
				var t = (new Date).getTime(), r = b.State.calls.length;
				r > 1e4 && (b.State.calls = n( b.State.calls ));
				for ( var o = 0; r > o; o ++ )if ( b.State.calls[ o ] ) {
					var s = b.State.calls[ o ], l = s[ 0 ], u = s[ 2 ], d = s[ 3 ], g = ! ! d, y = null;
					d || (d = b.State.calls[ o ][ 3 ] = t - 16);
					for ( var h = Math.min( (t - d) / u.duration, 1 ), v = 0, x = l.length; x > v; v ++ ) {
						var P = l[ v ], V = P.element;
						if ( i( V ) ) {
							var C = ! 1;
							if ( u.display !== a && null !== u.display && "none" !== u.display ) {
								if ( "flex" === u.display ) {
									var T = [ "-webkit-box", "-moz-box", "-ms-flexbox", "-webkit-flex" ];
									f.each( T, function( e, t ) {
										S.setPropertyValue( V, "display", t )
									} )
								}
								S.setPropertyValue( V, "display", u.display )
							}
							u.visibility !== a && "hidden" !== u.visibility && S.setPropertyValue( V, "visibility", u.visibility );
							for ( var k in P )if ( "element" !== k ) {
								var A, F = P[ k ], j = m.isString( F.easing ) ? b.Easings[ F.easing ] : F.easing;
								if ( 1 === h ) {
									A = F.endValue;
								} else {
									var E = F.endValue - F.startValue;
									if ( A = F.startValue + E * j( h, u, E ), ! g && A === F.currentValue ) {
										continue
									}
								}
								if ( F.currentValue = A, "tween" === k ) {
									y = A;
								} else {
									if ( S.Hooks.registered[ k ] ) {
										var H = S.Hooks.getRoot( k ), N = i( V ).rootPropertyValueCache[ H ];
										N && (F.rootPropertyValue = N)
									}
									var L = S.setPropertyValue( V, k, F.currentValue + (0 === parseFloat( A ) ? "" : F.unitType), F.rootPropertyValue, F.scrollData );
									S.Hooks.registered[ k ] && (i( V ).rootPropertyValueCache[ H ] = S.Normalizations.registered[ H ] ? S.Normalizations.registered[ H ]( "extract", null, L[ 1 ] ) : L[ 1 ]), "transform" === L[ 0 ] && (C = ! 0)
								}
							}
							u.mobileHA && i( V ).transformCache.translate3d === a && (i( V ).transformCache.translate3d = "(0px, 0px, 0px)", C = ! 0), C && S.flushTransformCache( V )
						}
					}
					u.display !== a && "none" !== u.display && (b.State.calls[ o ][ 2 ].display = ! 1), u.visibility !== a && "hidden" !== u.visibility && (b.State.calls[ o ][ 2 ].visibility = ! 1), u.progress && u.progress.call( s[ 1 ], s[ 1 ], h, Math.max( 0, d + u.duration - t ), d, y ), 1 === h && p( o )
				}
			}
			b.State.isTicking && w( c )
		}

		function p( e, t ) {
			if ( ! b.State.calls[ e ] ) {
				return ! 1;
			}
			for ( var r = b.State.calls[ e ][ 0 ], n = b.State.calls[ e ][ 1 ], o = b.State.calls[ e ][ 2 ], s = b.State.calls[ e ][ 4 ], l = ! 1, u = 0, c = r.length; c > u; u ++ ) {
				var p = r[ u ].element;
				if ( t || o.loop || ("none" === o.display && S.setPropertyValue( p, "display", o.display ), "hidden" === o.visibility && S.setPropertyValue( p, "visibility", o.visibility )), o.loop !== ! 0 && (f.queue( p )[ 1 ] === a || ! /\.velocityQueueEntryFlag/i.test( f.queue( p )[ 1 ] )) && i( p ) ) {
					i( p ).isAnimating = ! 1, i( p ).rootPropertyValueCache = {};
					var d = ! 1;
					f.each( S.Lists.transforms3D, function( e, t ) {
						var r = /^scale/.test( t ) ? 1 : 0, n = i( p ).transformCache[ t ];
						i( p ).transformCache[ t ] !== a && new RegExp( "^\\(" + r + "[^.]" ).test( n ) && (d = ! 0, delete i( p ).transformCache[ t ])
					} ), o.mobileHA && (d = ! 0, delete i( p ).transformCache.translate3d), d && S.flushTransformCache( p ), S.Values.removeClass( p, "velocity-animating" )
				}
				if ( ! t && o.complete && ! o.loop && u === c - 1 ) {
					try {
						o.complete.call( n, n )
					} catch ( g ) {
						setTimeout( function() {
							throw g
						}, 1 )
					}
				}
				s && o.loop !== ! 0 && s( n ), i( p ) && o.loop === ! 0 && ! t && (f.each( i( p ).tweensContainer, function( e, t ) {
					/^rotate/.test( e ) && 360 === parseFloat( t.endValue ) && (t.endValue = 0, t.startValue = 360), /^backgroundPosition/.test( e ) && 100 === parseFloat( t.endValue ) && "%" === t.unitType && (t.endValue = 0, t.startValue = 100)
				} ), b( p, "reverse", {
					loop: ! 0,
					delay: o.delay
				} )), o.queue !== ! 1 && f.dequeue( p, o.queue )
			}
			b.State.calls[ e ] = ! 1;
			for ( var m = 0, y = b.State.calls.length; y > m; m ++ )if ( b.State.calls[ m ] !== ! 1 ) {
				l = ! 0;
				break
			}
			l === ! 1 && (b.State.isTicking = ! 1, delete b.State.calls, b.State.calls = [])
		}

		var f, d = function() {
			if ( r.documentMode ) {
				return r.documentMode;
			}
			for ( var e = 7; e > 4; e -- ) {
				var t = r.createElement( "div" );
				if ( t.innerHTML = "<!--[if IE " + e + "]><span></span><![endif]-->", t.getElementsByTagName( "span" ).length ) {
					return t = null, e
				}
			}
			return a
		}(), g = function() {
			var e = 0;
			return t.webkitRequestAnimationFrame || t.mozRequestAnimationFrame || function( t ) {
					var r, a = (new Date).getTime();
					return r = Math.max( 0, 16 - (a - e) ), e = a + r, setTimeout( function() {
						t( a + r )
					}, r )
				}
		}(), m = {
			isString: function( e ) {
				return "string" == typeof e
			}, isArray: Array.isArray || function( e ) {
				return "[object Array]" === Object.prototype.toString.call( e )
			}, isFunction: function( e ) {
				return "[object Function]" === Object.prototype.toString.call( e )
			}, isNode: function( e ) {
				return e && e.nodeType
			}, isNodeList: function( e ) {
				return "object" == typeof e && /^\[object (HTMLCollection|NodeList|Object)\]$/.test( Object.prototype.toString.call( e ) ) && e.length !== a && (0 === e.length || "object" == typeof e[ 0 ] && e[ 0 ].nodeType > 0)
			}, isWrapped: function( e ) {
				return e && (e.jquery || t.Zepto && t.Zepto.zepto.isZ( e ))
			}, isSVG: function( e ) {
				return t.SVGElement && e instanceof t.SVGElement
			}, isEmptyObject: function( e ) {
				for ( var t in e )return ! 1;
				return ! 0
			}
		}, y = ! 1;
		if ( e.fn && e.fn.jquery ? (f = e, y = ! 0) : f = t.Velocity.Utilities, 8 >= d && ! y ) {
			throw new Error( "Velocity: IE8 and below require jQuery to be loaded before Velocity." );
		}
		if ( 7 >= d ) {
			return void(jQuery.fn.velocity = jQuery.fn.animate);
		}
		var h = 400, v = "swing", b = {
			State: {
				isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test( navigator.userAgent ),
				isAndroid: /Android/i.test( navigator.userAgent ),
				isGingerbread: /Android 2\.3\.[3-7]/i.test( navigator.userAgent ),
				isChrome: t.chrome,
				isFirefox: /Firefox/i.test( navigator.userAgent ),
				prefixElement: r.createElement( "div" ),
				prefixMatches: {},
				scrollAnchor: null,
				scrollPropertyLeft: null,
				scrollPropertyTop: null,
				isTicking: ! 1,
				calls: []
			},
			CSS: {},
			Utilities: f,
			Redirects: {},
			Easings: {},
			Promise: t.Promise,
			defaults: {
				queue: "",
				duration: h,
				easing: v,
				begin: a,
				complete: a,
				progress: a,
				display: a,
				visibility: a,
				loop: ! 1,
				delay: ! 1,
				mobileHA: ! 0,
				_cacheValues: ! 0
			},
			init: function( e ) {
				f.data( e, "velocity", {
					isSVG: m.isSVG( e ),
					isAnimating: ! 1,
					computedStyle: null,
					tweensContainer: null,
					rootPropertyValueCache: {},
					transformCache: {}
				} )
			},
			hook: null,
			mock: ! 1,
			version: { major: 1, minor: 2, patch: 2 },
			debug: ! 1
		};
		t.pageYOffset !== a ? (b.State.scrollAnchor = t, b.State.scrollPropertyLeft = "pageXOffset", b.State.scrollPropertyTop = "pageYOffset") : (b.State.scrollAnchor = r.documentElement || r.body.parentNode || r.body, b.State.scrollPropertyLeft = "scrollLeft", b.State.scrollPropertyTop = "scrollTop");
		var x = function() {
			function e( e ) {
				return - e.tension * e.x - e.friction * e.v
			}

			function t( t, r, a ) {
				var n = {
					x: t.x + a.dx * r,
					v: t.v + a.dv * r,
					tension: t.tension,
					friction: t.friction
				};
				return { dx: n.v, dv: e( n ) }
			}

			function r( r, a ) {
				var n = {
					dx: r.v,
					dv: e( r )
				}, o = t( r, .5 * a, n ), i = t( r, .5 * a, o ), s = t( r, a, i ), l = 1 / 6 * (n.dx + 2 * (o.dx + i.dx) + s.dx), u = 1 / 6 * (n.dv + 2 * (o.dv + i.dv) + s.dv);
				return r.x = r.x + l * a, r.v = r.v + u * a, r
			}

			return function a( e, t, n ) {
				var o, i, s, l = {
					x: - 1,
					v: 0,
					tension: null,
					friction: null
				}, u = [ 0 ], c = 0, p = 1e-4, f = .016;
				for ( e = parseFloat( e ) || 500, t = parseFloat( t ) || 20, n = n || null, l.tension = e, l.friction = t, o = null !== n, o ? (c = a( e, t ), i = c / n * f) : i = f; s = r( s || l, i ), u.push( 1 + s.x ), c += 16, Math.abs( s.x ) > p && Math.abs( s.v ) > p; );
				return o ? function( e ) {
					return u[ e * (u.length - 1) | 0 ]
				} : c
			}
		}();
		b.Easings = {
			linear: function( e ) {
				return e
			}, swing: function( e ) {
				return .5 - Math.cos( e * Math.PI ) / 2
			}, spring: function( e ) {
				return 1 - Math.cos( 4.5 * e * Math.PI ) * Math.exp( 6 * - e )
			}
		}, f.each( [ [ "ease", [ .25, .1, .25, 1 ] ], [ "ease-in", [ .42, 0, 1, 1 ] ], [ "ease-out", [ 0, 0, .58, 1 ] ], [ "ease-in-out", [ .42, 0, .58, 1 ] ], [ "easeInSine", [ .47, 0, .745, .715 ] ], [ "easeOutSine", [ .39, .575, .565, 1 ] ], [ "easeInOutSine", [ .445, .05, .55, .95 ] ], [ "easeInQuad", [ .55, .085, .68, .53 ] ], [ "easeOutQuad", [ .25, .46, .45, .94 ] ], [ "easeInOutQuad", [ .455, .03, .515, .955 ] ], [ "easeInCubic", [ .55, .055, .675, .19 ] ], [ "easeOutCubic", [ .215, .61, .355, 1 ] ], [ "easeInOutCubic", [ .645, .045, .355, 1 ] ], [ "easeInQuart", [ .895, .03, .685, .22 ] ], [ "easeOutQuart", [ .165, .84, .44, 1 ] ], [ "easeInOutQuart", [ .77, 0, .175, 1 ] ], [ "easeInQuint", [ .755, .05, .855, .06 ] ], [ "easeOutQuint", [ .23, 1, .32, 1 ] ], [ "easeInOutQuint", [ .86, 0, .07, 1 ] ], [ "easeInExpo", [ .95, .05, .795, .035 ] ], [ "easeOutExpo", [ .19, 1, .22, 1 ] ], [ "easeInOutExpo", [ 1, 0, 0, 1 ] ], [ "easeInCirc", [ .6, .04, .98, .335 ] ], [ "easeOutCirc", [ .075, .82, .165, 1 ] ], [ "easeInOutCirc", [ .785, .135, .15, .86 ] ] ], function( e, t ) {
			b.Easings[ t[ 0 ] ] = l.apply( null, t[ 1 ] )
		} );
		var S = b.CSS = {
			RegEx: {
				isHex: /^#([A-f\d]{3}){1,2}$/i,
				valueUnwrap: /^[A-z]+\((.*)\)$/i,
				wrappedValueAlreadyExtracted: /[0-9.]+ [0-9.]+ [0-9.]+( [0-9.]+)?/,
				valueSplit: /([A-z]+\(.+\))|(([A-z0-9#-.]+?)(?=\s|$))/gi
			},
			Lists: {
				colors: [ "fill", "stroke", "stopColor", "color", "backgroundColor", "borderColor", "borderTopColor", "borderRightColor", "borderBottomColor", "borderLeftColor", "outlineColor" ],
				transformsBase: [ "translateX", "translateY", "scale", "scaleX", "scaleY", "skewX", "skewY", "rotateZ" ],
				transforms3D: [ "transformPerspective", "translateZ", "scaleZ", "rotateX", "rotateY" ]
			},
			Hooks: {
				templates: {
					textShadow: [ "Color X Y Blur", "black 0px 0px 0px" ],
					boxShadow: [ "Color X Y Blur Spread", "black 0px 0px 0px 0px" ],
					clip: [ "Top Right Bottom Left", "0px 0px 0px 0px" ],
					backgroundPosition: [ "X Y", "0% 0%" ],
					transformOrigin: [ "X Y Z", "50% 50% 0px" ],
					perspectiveOrigin: [ "X Y", "50% 50%" ]
				}, registered: {}, register: function() {
					for ( var e = 0; e < S.Lists.colors.length; e ++ ) {
						var t = "color" === S.Lists.colors[ e ] ? "0 0 0 1" : "255 255 255 1";
						S.Hooks.templates[ S.Lists.colors[ e ] ] = [ "Red Green Blue Alpha", t ]
					}
					var r, a, n;
					if ( d ) {
						for ( r in S.Hooks.templates ) {
							a = S.Hooks.templates[ r ], n = a[ 0 ].split( " " );
							var o = a[ 1 ].match( S.RegEx.valueSplit );
							"Color" === n[ 0 ] && (n.push( n.shift() ), o.push( o.shift() ), S.Hooks.templates[ r ] = [ n.join( " " ), o.join( " " ) ])
						}
					}
					for ( r in S.Hooks.templates ) {
						a = S.Hooks.templates[ r ], n = a[ 0 ].split( " " );
						for ( var e in n ) {
							var i = r + n[ e ], s = e;
							S.Hooks.registered[ i ] = [ r, s ]
						}
					}
				}, getRoot: function( e ) {
					var t = S.Hooks.registered[ e ];
					return t ? t[ 0 ] : e
				}, cleanRootPropertyValue: function( e, t ) {
					return S.RegEx.valueUnwrap.test( t ) && (t = t.match( S.RegEx.valueUnwrap )[ 1 ]), S.Values.isCSSNullValue( t ) && (t = S.Hooks.templates[ e ][ 1 ]), t
				}, extractValue: function( e, t ) {
					var r = S.Hooks.registered[ e ];
					if ( r ) {
						var a = r[ 0 ], n = r[ 1 ];
						return t = S.Hooks.cleanRootPropertyValue( a, t ), t.toString().match( S.RegEx.valueSplit )[ n ]
					}
					return t
				}, injectValue: function( e, t, r ) {
					var a = S.Hooks.registered[ e ];
					if ( a ) {
						var n, o, i = a[ 0 ], s = a[ 1 ];
						return r = S.Hooks.cleanRootPropertyValue( i, r ), n = r.toString().match( S.RegEx.valueSplit ), n[ s ] = t, o = n.join( " " )
					}
					return r
				}
			},
			Normalizations: {
				registered: {
					clip: function( e, t, r ) {
						switch ( e ) {
							case"name":
								return "clip";
							case"extract":
								var a;
								return S.RegEx.wrappedValueAlreadyExtracted.test( r ) ? a = r : (a = r.toString().match( S.RegEx.valueUnwrap ), a = a ? a[ 1 ].replace( /,(\s+)?/g, " " ) : r), a;
							case"inject":
								return "rect(" + r + ")"
						}
					}, blur: function( e, t, r ) {
						switch ( e ) {
							case"name":
								return b.State.isFirefox ? "filter" : "-webkit-filter";
							case"extract":
								var a = parseFloat( r );
								if ( ! a && 0 !== a ) {
									var n = r.toString().match( /blur\(([0-9]+[A-z]+)\)/i );
									a = n ? n[ 1 ] : 0
								}
								return a;
							case"inject":
								return parseFloat( r ) ? "blur(" + r + ")" : "none"
						}
					}, opacity: function( e, t, r ) {
						if ( 8 >= d ) {
							switch ( e ) {
								case"name":
									return "filter";
								case"extract":
									var a = r.toString().match( /alpha\(opacity=(.*)\)/i );
									return r = a ? a[ 1 ] / 100 : 1;
								case"inject":
									return t.style.zoom = 1, parseFloat( r ) >= 1 ? "" : "alpha(opacity=" + parseInt( 100 * parseFloat( r ), 10 ) + ")"
							}
						} else {
							switch ( e ) {
								case"name":
									return "opacity";
								case"extract":
									return r;
								case"inject":
									return r
							}
						}
					}
				}, register: function() {
					9 >= d || b.State.isGingerbread || (S.Lists.transformsBase = S.Lists.transformsBase.concat( S.Lists.transforms3D ));
					for ( var e = 0; e < S.Lists.transformsBase.length; e ++ )! function() {
						var t = S.Lists.transformsBase[ e ];
						S.Normalizations.registered[ t ] = function( e, r, n ) {
							switch ( e ) {
								case"name":
									return "transform";
								case"extract":
									return i( r ) === a || i( r ).transformCache[ t ] === a ? /^scale/i.test( t ) ? 1 : 0 : i( r ).transformCache[ t ].replace( /[()]/g, "" );
								case"inject":
									var o = ! 1;
									switch ( t.substr( 0, t.length - 1 ) ) {
										case"translate":
											o = ! /(%|px|em|rem|vw|vh|\d)$/i.test( n );
											break;
										case"scal":
										case"scale":
											b.State.isAndroid && i( r ).transformCache[ t ] === a && 1 > n && (n = 1), o = ! /(\d)$/i.test( n );
											break;
										case"skew":
											o = ! /(deg|\d)$/i.test( n );
											break;
										case"rotate":
											o = ! /(deg|\d)$/i.test( n )
									}
									return o || (i( r ).transformCache[ t ] = "(" + n + ")"), i( r ).transformCache[ t ]
							}
						}
					}();
					for ( var e = 0; e < S.Lists.colors.length; e ++ )! function() {
						var t = S.Lists.colors[ e ];
						S.Normalizations.registered[ t ] = function( e, r, n ) {
							switch ( e ) {
								case"name":
									return t;
								case"extract":
									var o;
									if ( S.RegEx.wrappedValueAlreadyExtracted.test( n ) ) {
										o = n;
									} else {
										var i, s = {
											black: "rgb(0, 0, 0)",
											blue: "rgb(0, 0, 255)",
											gray: "rgb(128, 128, 128)",
											green: "rgb(0, 128, 0)",
											red: "rgb(255, 0, 0)",
											white: "rgb(255, 255, 255)"
										};
										/^[A-z]+$/i.test( n ) ? i = s[ n ] !== a ? s[ n ] : s.black : S.RegEx.isHex.test( n ) ? i = "rgb(" + S.Values.hexToRgb( n ).join( " " ) + ")" : /^rgba?\(/i.test( n ) || (i = s.black), o = (i || n).toString().match( S.RegEx.valueUnwrap )[ 1 ].replace( /,(\s+)?/g, " " )
									}
									return 8 >= d || 3 !== o.split( " " ).length || (o += " 1"), o;
								case"inject":
									return 8 >= d ? 4 === n.split( " " ).length && (n = n.split( /\s+/ ).slice( 0, 3 ).join( " " )) : 3 === n.split( " " ).length && (n += " 1"), (8 >= d ? "rgb" : "rgba") + "(" + n.replace( /\s+/g, "," ).replace( /\.(\d)+(?=,)/g, "" ) + ")"
							}
						}
					}()
				}
			},
			Names: {
				camelCase: function( e ) {
					return e.replace( /-(\w)/g, function( e, t ) {
						return t.toUpperCase()
					} )
				}, SVGAttribute: function( e ) {
					var t = "width|height|x|y|cx|cy|r|rx|ry|x1|x2|y1|y2";
					return (d || b.State.isAndroid && ! b.State.isChrome) && (t += "|transform"), new RegExp( "^(" + t + ")$", "i" ).test( e )
				}, prefixCheck: function( e ) {
					if ( b.State.prefixMatches[ e ] ) {
						return [ b.State.prefixMatches[ e ], ! 0 ];
					}
					for ( var t = [ "", "Webkit", "Moz", "ms", "O" ], r = 0, a = t.length; a > r; r ++ ) {
						var n;
						if ( n = 0 === r ? e : t[ r ] + e.replace( /^\w/, function( e ) {
								return e.toUpperCase()
							} ), m.isString( b.State.prefixElement.style[ n ] ) ) {
							return b.State.prefixMatches[ e ] = n, [ n, ! 0 ]
						}
					}
					return [ e, ! 1 ]
				}
			},
			Values: {
				hexToRgb: function( e ) {
					var t, r = /^#?([a-f\d])([a-f\d])([a-f\d])$/i, a = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i;
					return e = e.replace( r, function( e, t, r, a ) {
						return t + t + r + r + a + a
					} ), t = a.exec( e ), t ? [ parseInt( t[ 1 ], 16 ), parseInt( t[ 2 ], 16 ), parseInt( t[ 3 ], 16 ) ] : [ 0, 0, 0 ]
				}, isCSSNullValue: function( e ) {
					return 0 == e || /^(none|auto|transparent|(rgba\(0, ?0, ?0, ?0\)))$/i.test( e )
				}, getUnitType: function( e ) {
					return /^(rotate|skew)/i.test( e ) ? "deg" : /(^(scale|scaleX|scaleY|scaleZ|alpha|flexGrow|flexHeight|zIndex|fontWeight)$)|((opacity|red|green|blue|alpha)$)/i.test( e ) ? "" : "px"
				}, getDisplayType: function( e ) {
					var t = e && e.tagName.toString().toLowerCase();
					return /^(b|big|i|small|tt|abbr|acronym|cite|code|dfn|em|kbd|strong|samp|var|a|bdo|br|img|map|object|q|script|span|sub|sup|button|input|label|select|textarea)$/i.test( t ) ? "inline" : /^(li)$/i.test( t ) ? "list-item" : /^(tr)$/i.test( t ) ? "table-row" : /^(table)$/i.test( t ) ? "table" : /^(tbody)$/i.test( t ) ? "table-row-group" : "block"
				}, addClass: function( e, t ) {
					e.classList ? e.classList.add( t ) : e.className += (e.className.length ? " " : "") + t
				}, removeClass: function( e, t ) {
					e.classList ? e.classList.remove( t ) : e.className = e.className.toString().replace( new RegExp( "(^|\\s)" + t.split( " " ).join( "|" ) + "(\\s|$)", "gi" ), " " )
				}
			},
			getPropertyValue: function( e, r, n, o ) {
				function s( e, r ) {
					function n() {
						u && S.setPropertyValue( e, "display", "none" )
					}

					var l = 0;
					if ( 8 >= d ) {
						l = f.css( e, r );
					} else {
						var u = ! 1;
						if ( /^(width|height)$/.test( r ) && 0 === S.getPropertyValue( e, "display" ) && (u = ! 0, S.setPropertyValue( e, "display", S.Values.getDisplayType( e ) )), ! o ) {
							if ( "height" === r && "border-box" !== S.getPropertyValue( e, "boxSizing" ).toString().toLowerCase() ) {
								var c = e.offsetHeight - (parseFloat( S.getPropertyValue( e, "borderTopWidth" ) ) || 0) - (parseFloat( S.getPropertyValue( e, "borderBottomWidth" ) ) || 0) - (parseFloat( S.getPropertyValue( e, "paddingTop" ) ) || 0) - (parseFloat( S.getPropertyValue( e, "paddingBottom" ) ) || 0);
								return n(), c
							}
							if ( "width" === r && "border-box" !== S.getPropertyValue( e, "boxSizing" ).toString().toLowerCase() ) {
								var p = e.offsetWidth - (parseFloat( S.getPropertyValue( e, "borderLeftWidth" ) ) || 0) - (parseFloat( S.getPropertyValue( e, "borderRightWidth" ) ) || 0) - (parseFloat( S.getPropertyValue( e, "paddingLeft" ) ) || 0) - (parseFloat( S.getPropertyValue( e, "paddingRight" ) ) || 0);
								return n(), p
							}
						}
						var g;
						g = i( e ) === a ? t.getComputedStyle( e, null ) : i( e ).computedStyle ? i( e ).computedStyle : i( e ).computedStyle = t.getComputedStyle( e, null ), "borderColor" === r && (r = "borderTopColor"), l = 9 === d && "filter" === r ? g.getPropertyValue( r ) : g[ r ], ("" === l || null === l) && (l = e.style[ r ]), n()
					}
					if ( "auto" === l && /^(top|right|bottom|left)$/i.test( r ) ) {
						var m = s( e, "position" );
						("fixed" === m || "absolute" === m && /top|left/i.test( r )) && (l = f( e ).position()[ r ] + "px")
					}
					return l
				}

				var l;
				if ( S.Hooks.registered[ r ] ) {
					var u = r, c = S.Hooks.getRoot( u );
					n === a && (n = S.getPropertyValue( e, S.Names.prefixCheck( c )[ 0 ] )), S.Normalizations.registered[ c ] && (n = S.Normalizations.registered[ c ]( "extract", e, n )), l = S.Hooks.extractValue( u, n )
				} else {
					if ( S.Normalizations.registered[ r ] ) {
						var p, g;
						p = S.Normalizations.registered[ r ]( "name", e ), "transform" !== p && (g = s( e, S.Names.prefixCheck( p )[ 0 ] ), S.Values.isCSSNullValue( g ) && S.Hooks.templates[ r ] && (g = S.Hooks.templates[ r ][ 1 ])), l = S.Normalizations.registered[ r ]( "extract", e, g )
					}
				}
				if ( ! /^[\d-]/.test( l ) ) {
					if ( i( e ) && i( e ).isSVG && S.Names.SVGAttribute( r ) ) {
						if ( /^(height|width)$/i.test( r ) ) {
							try {
								l = e.getBBox()[ r ]
							} catch ( m ) {
								l = 0
							}
						} else {
							l = e.getAttribute( r );
						}
					} else {
						l = s( e, S.Names.prefixCheck( r )[ 0 ] );
					}
				}
				return S.Values.isCSSNullValue( l ) && (l = 0), b.debug >= 2 && console.log( "Get " + r + ": " + l ), l
			},
			setPropertyValue: function( e, r, a, n, o ) {
				var s = r;
				if ( "scroll" === r ) {
					o.container ? o.container[ "scroll" + o.direction ] = a : "Left" === o.direction ? t.scrollTo( a, o.alternateValue ) : t.scrollTo( o.alternateValue, a );
				} else {
					if ( S.Normalizations.registered[ r ] && "transform" === S.Normalizations.registered[ r ]( "name", e ) ) {
						S.Normalizations.registered[ r ]( "inject", e, a ), s = "transform", a = i( e ).transformCache[ r ];
					} else {
						if ( S.Hooks.registered[ r ] ) {
							var l = r, u = S.Hooks.getRoot( r );
							n = n || S.getPropertyValue( e, u ), a = S.Hooks.injectValue( l, a, n ), r = u
						}
						if ( S.Normalizations.registered[ r ] && (a = S.Normalizations.registered[ r ]( "inject", e, a ), r = S.Normalizations.registered[ r ]( "name", e )), s = S.Names.prefixCheck( r )[ 0 ], 8 >= d ) {
							try {
								e.style[ s ] = a
							} catch ( c ) {
								b.debug && console.log( "Browser does not support [" + a + "] for [" + s + "]" )
							}
						} else {
							i( e ) && i( e ).isSVG && S.Names.SVGAttribute( r ) ? e.setAttribute( r, a ) : e.style[ s ] = a;
						}
						b.debug >= 2 && console.log( "Set " + r + " (" + s + "): " + a )
					}
				}
				return [ s, a ]
			},
			flushTransformCache: function( e ) {
				function t( t ) {
					return parseFloat( S.getPropertyValue( e, t ) )
				}

				var r = "";
				if ( (d || b.State.isAndroid && ! b.State.isChrome) && i( e ).isSVG ) {
					var a = {
						translate: [ t( "translateX" ), t( "translateY" ) ],
						skewX: [ t( "skewX" ) ],
						skewY: [ t( "skewY" ) ],
						scale: 1 !== t( "scale" ) ? [ t( "scale" ), t( "scale" ) ] : [ t( "scaleX" ), t( "scaleY" ) ],
						rotate: [ t( "rotateZ" ), 0, 0 ]
					};
					f.each( i( e ).transformCache, function( e ) {
						/^translate/i.test( e ) ? e = "translate" : /^scale/i.test( e ) ? e = "scale" : /^rotate/i.test( e ) && (e = "rotate"), a[ e ] && (r += e + "(" + a[ e ].join( " " ) + ") ", delete a[ e ])
					} )
				} else {
					var n, o;
					f.each( i( e ).transformCache, function( t ) {
						return n = i( e ).transformCache[ t ], "transformPerspective" === t ? (o = n, ! 0) : (9 === d && "rotateZ" === t && (t = "rotate"), void(r += t + n + " "))
					} ), o && (r = "perspective" + o + " " + r)
				}
				S.setPropertyValue( e, "transform", r )
			}
		};
		S.Hooks.register(), S.Normalizations.register(), b.hook = function( e, t, r ) {
			var n = a;
			return e = o( e ), f.each( e, function( e, o ) {
				if ( i( o ) === a && b.init( o ), r === a ) {
					n === a && (n = b.CSS.getPropertyValue( o, t ));
				} else {
					var s = b.CSS.setPropertyValue( o, t, r );
					"transform" === s[ 0 ] && b.CSS.flushTransformCache( o ), n = s
				}
			} ), n
		};
		var P = function() {
			function e() {
				return s ? k.promise || null : l
			}

			function n() {
				function e( e ) {
					function p( e, t ) {
						var r = a, n = a, i = a;
						return m.isArray( e ) ? (r = e[ 0 ], ! m.isArray( e[ 1 ] ) && /^[\d-]/.test( e[ 1 ] ) || m.isFunction( e[ 1 ] ) || S.RegEx.isHex.test( e[ 1 ] ) ? i = e[ 1 ] : (m.isString( e[ 1 ] ) && ! S.RegEx.isHex.test( e[ 1 ] ) || m.isArray( e[ 1 ] )) && (n = t ? e[ 1 ] : u( e[ 1 ], s.duration ), e[ 2 ] !== a && (i = e[ 2 ]))) : r = e, t || (n = n || s.easing), m.isFunction( r ) && (r = r.call( o, V, w )), m.isFunction( i ) && (i = i.call( o, V, w )), [ r || 0, n, i ]
					}

					function d( e, t ) {
						var r, a;
						return a = (t || "0").toString().toLowerCase().replace( /[%A-z]+$/, function( e ) {
							return r = e, ""
						} ), r || (r = S.Values.getUnitType( e )), [ a, r ]
					}

					function h() {
						var e = {
							myParent: o.parentNode || r.body,
							position: S.getPropertyValue( o, "position" ),
							fontSize: S.getPropertyValue( o, "fontSize" )
						}, a = e.position === L.lastPosition && e.myParent === L.lastParent, n = e.fontSize === L.lastFontSize;
						L.lastParent = e.myParent, L.lastPosition = e.position, L.lastFontSize = e.fontSize;
						var s = 100, l = {};
						if ( n && a ) {
							l.emToPx = L.lastEmToPx, l.percentToPxWidth = L.lastPercentToPxWidth, l.percentToPxHeight = L.lastPercentToPxHeight;
						} else {
							var u = i( o ).isSVG ? r.createElementNS( "http://www.w3.org/2000/svg", "rect" ) : r.createElement( "div" );
							b.init( u ), e.myParent.appendChild( u ), f.each( [ "overflow", "overflowX", "overflowY" ], function( e, t ) {
								b.CSS.setPropertyValue( u, t, "hidden" )
							} ), b.CSS.setPropertyValue( u, "position", e.position ), b.CSS.setPropertyValue( u, "fontSize", e.fontSize ), b.CSS.setPropertyValue( u, "boxSizing", "content-box" ), f.each( [ "minWidth", "maxWidth", "width", "minHeight", "maxHeight", "height" ], function( e, t ) {
								b.CSS.setPropertyValue( u, t, s + "%" )
							} ), b.CSS.setPropertyValue( u, "paddingLeft", s + "em" ), l.percentToPxWidth = L.lastPercentToPxWidth = (parseFloat( S.getPropertyValue( u, "width", null, ! 0 ) ) || 1) / s, l.percentToPxHeight = L.lastPercentToPxHeight = (parseFloat( S.getPropertyValue( u, "height", null, ! 0 ) ) || 1) / s, l.emToPx = L.lastEmToPx = (parseFloat( S.getPropertyValue( u, "paddingLeft" ) ) || 1) / s, e.myParent.removeChild( u )
						}
						return null === L.remToPx && (L.remToPx = parseFloat( S.getPropertyValue( r.body, "fontSize" ) ) || 16), null === L.vwToPx && (L.vwToPx = parseFloat( t.innerWidth ) / 100, L.vhToPx = parseFloat( t.innerHeight ) / 100), l.remToPx = L.remToPx, l.vwToPx = L.vwToPx, l.vhToPx = L.vhToPx, b.debug >= 1 && console.log( "Unit ratios: " + JSON.stringify( l ), o ), l
					}

					if ( s.begin && 0 === V ) {
						try {
							s.begin.call( g, g )
						} catch ( x ) {
							setTimeout( function() {
								throw x
							}, 1 )
						}
					}
					if ( "scroll" === A ) {
						var P, C, T, F = /^x$/i.test( s.axis ) ? "Left" : "Top", j = parseFloat( s.offset ) || 0;
						s.container ? m.isWrapped( s.container ) || m.isNode( s.container ) ? (s.container = s.container[ 0 ] || s.container, P = s.container[ "scroll" + F ], T = P + f( o ).position()[ F.toLowerCase() ] + j) : s.container = null : (P = b.State.scrollAnchor[ b.State[ "scrollProperty" + F ] ], C = b.State.scrollAnchor[ b.State[ "scrollProperty" + ("Left" === F ? "Top" : "Left") ] ], T = f( o ).offset()[ F.toLowerCase() ] + j), l = {
							scroll: {
								rootPropertyValue: ! 1,
								startValue: P,
								currentValue: P,
								endValue: T,
								unitType: "",
								easing: s.easing,
								scrollData: {
									container: s.container,
									direction: F,
									alternateValue: C
								}
							}, element: o
						}, b.debug && console.log( "tweensContainer (scroll): ", l.scroll, o )
					} else {
						if ( "reverse" === A ) {
							if ( ! i( o ).tweensContainer ) {
								return void f.dequeue( o, s.queue );
							}
							"none" === i( o ).opts.display && (i( o ).opts.display = "auto"), "hidden" === i( o ).opts.visibility && (i( o ).opts.visibility = "visible"), i( o ).opts.loop = ! 1, i( o ).opts.begin = null, i( o ).opts.complete = null, v.easing || delete s.easing, v.duration || delete s.duration, s = f.extend( {}, i( o ).opts, s );
							var E = f.extend( ! 0, {}, i( o ).tweensContainer );
							for ( var H in E )if ( "element" !== H ) {
								var N = E[ H ].startValue;
								E[ H ].startValue = E[ H ].currentValue = E[ H ].endValue, E[ H ].endValue = N, m.isEmptyObject( v ) || (E[ H ].easing = s.easing), b.debug && console.log( "reverse tweensContainer (" + H + "): " + JSON.stringify( E[ H ] ), o )
							}
							l = E
						} else {
							if ( "start" === A ) {
								var E;
								i( o ).tweensContainer && i( o ).isAnimating === ! 0 && (E = i( o ).tweensContainer), f.each( y, function( e, t ) {
									if ( RegExp( "^" + S.Lists.colors.join( "$|^" ) + "$" ).test( e ) ) {
										var r = p( t, ! 0 ), n = r[ 0 ], o = r[ 1 ], i = r[ 2 ];
										if ( S.RegEx.isHex.test( n ) ) {
											for ( var s = [ "Red", "Green", "Blue" ], l = S.Values.hexToRgb( n ), u = i ? S.Values.hexToRgb( i ) : a, c = 0; c < s.length; c ++ ) {
												var f = [ l[ c ] ];
												o && f.push( o ), u !== a && f.push( u[ c ] ), y[ e + s[ c ] ] = f
											}
											delete y[ e ]
										}
									}
								} );
								for ( var z in y ) {
									var O = p( y[ z ] ), q = O[ 0 ], $ = O[ 1 ], M = O[ 2 ];
									z = S.Names.camelCase( z );
									var I = S.Hooks.getRoot( z ), B = ! 1;
									if ( i( o ).isSVG || "tween" === I || S.Names.prefixCheck( I )[ 1 ] !== ! 1 || S.Normalizations.registered[ I ] !== a ) {
										(s.display !== a && null !== s.display && "none" !== s.display || s.visibility !== a && "hidden" !== s.visibility) && /opacity|filter/.test( z ) && ! M && 0 !== q && (M = 0), s._cacheValues && E && E[ z ] ? (M === a && (M = E[ z ].endValue + E[ z ].unitType), B = i( o ).rootPropertyValueCache[ I ]) : S.Hooks.registered[ z ] ? M === a ? (B = S.getPropertyValue( o, I ), M = S.getPropertyValue( o, z, B )) : B = S.Hooks.templates[ I ][ 1 ] : M === a && (M = S.getPropertyValue( o, z ));
										var W, G, Y, D = ! 1;
										if ( W = d( z, M ), M = W[ 0 ], Y = W[ 1 ], W = d( z, q ), q = W[ 0 ].replace( /^([+-\/*])=/, function( e, t ) {
												return D = t, ""
											} ), G = W[ 1 ], M = parseFloat( M ) || 0, q = parseFloat( q ) || 0, "%" === G && (/^(fontSize|lineHeight)$/.test( z ) ? (q /= 100, G = "em") : /^scale/.test( z ) ? (q /= 100, G = "") : /(Red|Green|Blue)$/i.test( z ) && (q = q / 100 * 255, G = "")), /[\/*]/.test( D ) ) {
											G = Y;
										} else {
											if ( Y !== G && 0 !== M ) {
												if ( 0 === q ) {
													G = Y;
												} else {
													n = n || h();
													var Q = /margin|padding|left|right|width|text|word|letter/i.test( z ) || /X$/.test( z ) || "x" === z ? "x" : "y";
													switch ( Y ) {
														case"%":
															M *= "x" === Q ? n.percentToPxWidth : n.percentToPxHeight;
															break;
														case"px":
															break;
														default:
															M *= n[ Y + "ToPx" ]
													}
													switch ( G ) {
														case"%":
															M *= 1 / ("x" === Q ? n.percentToPxWidth : n.percentToPxHeight);
															break;
														case"px":
															break;
														default:
															M *= 1 / n[ G + "ToPx" ]
													}
												}
											}
										}
										switch ( D ) {
											case"+":
												q = M + q;
												break;
											case"-":
												q = M - q;
												break;
											case"*":
												q = M * q;
												break;
											case"/":
												q = M / q
										}
										l[ z ] = {
											rootPropertyValue: B,
											startValue: M,
											currentValue: M,
											endValue: q,
											unitType: G,
											easing: $
										}, b.debug && console.log( "tweensContainer (" + z + "): " + JSON.stringify( l[ z ] ), o )
									} else {
										b.debug && console.log( "Skipping [" + I + "] due to a lack of browser support." )
									}
								}
								l.element = o
							}
						}
					}
					l.element && (S.Values.addClass( o, "velocity-animating" ), R.push( l ), "" === s.queue && (i( o ).tweensContainer = l, i( o ).opts = s), i( o ).isAnimating = ! 0, V === w - 1 ? (b.State.calls.push( [ R, g, s, null, k.resolver ] ), b.State.isTicking === ! 1 && (b.State.isTicking = ! 0, c())) : V ++)
				}

				var n, o = this, s = f.extend( {}, b.defaults, v ), l = {};
				switch ( i( o ) === a && b.init( o ), parseFloat( s.delay ) && s.queue !== ! 1 && f.queue( o, s.queue, function( e ) {
					b.velocityQueueEntryFlag = ! 0, i( o ).delayTimer = {
						setTimeout: setTimeout( e, parseFloat( s.delay ) ),
						next: e
					}
				} ), s.duration.toString().toLowerCase() ) {
					case"fast":
						s.duration = 200;
						break;
					case"normal":
						s.duration = h;
						break;
					case"slow":
						s.duration = 600;
						break;
					default:
						s.duration = parseFloat( s.duration ) || 1
				}
				b.mock !== ! 1 && (b.mock === ! 0 ? s.duration = s.delay = 1 : (s.duration *= parseFloat( b.mock ) || 1, s.delay *= parseFloat( b.mock ) || 1)), s.easing = u( s.easing, s.duration ), s.begin && ! m.isFunction( s.begin ) && (s.begin = null), s.progress && ! m.isFunction( s.progress ) && (s.progress = null), s.complete && ! m.isFunction( s.complete ) && (s.complete = null), s.display !== a && null !== s.display && (s.display = s.display.toString().toLowerCase(), "auto" === s.display && (s.display = b.CSS.Values.getDisplayType( o ))), s.visibility !== a && null !== s.visibility && (s.visibility = s.visibility.toString().toLowerCase()), s.mobileHA = s.mobileHA && b.State.isMobile && ! b.State.isGingerbread, s.queue === ! 1 ? s.delay ? setTimeout( e, s.delay ) : e() : f.queue( o, s.queue, function( t, r ) {
					return r === ! 0 ? (k.promise && k.resolver( g ), ! 0) : (b.velocityQueueEntryFlag = ! 0, void e( t ))
				} ), "" !== s.queue && "fx" !== s.queue || "inprogress" === f.queue( o )[ 0 ] || f.dequeue( o )
			}

			var s, l, d, g, y, v, x = arguments[ 0 ] && (arguments[ 0 ].p || f.isPlainObject( arguments[ 0 ].properties ) && ! arguments[ 0 ].properties.names || m.isString( arguments[ 0 ].properties ));
			if ( m.isWrapped( this ) ? (s = ! 1, d = 0, g = this, l = this) : (s = ! 0, d = 1, g = x ? arguments[ 0 ].elements || arguments[ 0 ].e : arguments[ 0 ]), g = o( g ) ) {
				x ? (y = arguments[ 0 ].properties || arguments[ 0 ].p, v = arguments[ 0 ].options || arguments[ 0 ].o) : (y = arguments[ d ], v = arguments[ d + 1 ]);
				var w = g.length, V = 0;
				if ( ! /^(stop|finish)$/i.test( y ) && ! f.isPlainObject( v ) ) {
					var C = d + 1;
					v = {};
					for ( var T = C; T < arguments.length; T ++ )m.isArray( arguments[ T ] ) || ! /^(fast|normal|slow)$/i.test( arguments[ T ] ) && ! /^\d/.test( arguments[ T ] ) ? m.isString( arguments[ T ] ) || m.isArray( arguments[ T ] ) ? v.easing = arguments[ T ] : m.isFunction( arguments[ T ] ) && (v.complete = arguments[ T ]) : v.duration = arguments[ T ]
				}
				var k = { promise: null, resolver: null, rejecter: null };
				s && b.Promise && (k.promise = new b.Promise( function( e, t ) {
					k.resolver = e, k.rejecter = t
				} ));
				var A;
				switch ( y ) {
					case"scroll":
						A = "scroll";
						break;
					case"reverse":
						A = "reverse";
						break;
					case"finish":
					case"stop":
						f.each( g, function( e, t ) {
							i( t ) && i( t ).delayTimer && (clearTimeout( i( t ).delayTimer.setTimeout ), i( t ).delayTimer.next && i( t ).delayTimer.next(), delete i( t ).delayTimer)
						} );
						var F = [];
						return f.each( b.State.calls, function( e, t ) {
							t && f.each( t[ 1 ], function( r, n ) {
								var o = v === a ? "" : v;
								return o === ! 0 || t[ 2 ].queue === o || v === a && t[ 2 ].queue === ! 1 ? void f.each( g, function( r, a ) {
									a === n && ((v === ! 0 || m.isString( v )) && (f.each( f.queue( a, m.isString( v ) ? v : "" ), function( e, t ) {
										m.isFunction( t ) && t( null, ! 0 )
									} ), f.queue( a, m.isString( v ) ? v : "", [] )), "stop" === y ? (i( a ) && i( a ).tweensContainer && o !== ! 1 && f.each( i( a ).tweensContainer, function( e, t ) {
										t.endValue = t.currentValue
									} ), F.push( e )) : "finish" === y && (t[ 2 ].duration = 1))
								} ) : ! 0
							} )
						} ), "stop" === y && (f.each( F, function( e, t ) {
							p( t, ! 0 )
						} ), k.promise && k.resolver( g )), e();
					default:
						if ( ! f.isPlainObject( y ) || m.isEmptyObject( y ) ) {
							if ( m.isString( y ) && b.Redirects[ y ] ) {
								var j = f.extend( {}, v ), E = j.duration, H = j.delay || 0;
								return j.backwards === ! 0 && (g = f.extend( ! 0, [], g ).reverse()), f.each( g, function( e, t ) {
									parseFloat( j.stagger ) ? j.delay = H + parseFloat( j.stagger ) * e : m.isFunction( j.stagger ) && (j.delay = H + j.stagger.call( t, e, w )), j.drag && (j.duration = parseFloat( E ) || (/^(callout|transition)/.test( y ) ? 1e3 : h), j.duration = Math.max( j.duration * (j.backwards ? 1 - e / w : (e + 1) / w), .75 * j.duration, 200 )), b.Redirects[ y ].call( t, t, j || {}, e, w, g, k.promise ? k : a )
								} ), e()
							}
							var N = "Velocity: First argument (" + y + ") was not a property map, a known action, or a registered redirect. Aborting.";
							return k.promise ? k.rejecter( new Error( N ) ) : console.log( N ), e()
						}
						A = "start"
				}
				var L = {
					lastParent: null,
					lastPosition: null,
					lastFontSize: null,
					lastPercentToPxWidth: null,
					lastPercentToPxHeight: null,
					lastEmToPx: null,
					remToPx: null,
					vwToPx: null,
					vhToPx: null
				}, R = [];
				f.each( g, function( e, t ) {
					m.isNode( t ) && n.call( t )
				} );
				var z, j = f.extend( {}, b.defaults, v );
				if ( j.loop = parseInt( j.loop ), z = 2 * j.loop - 1, j.loop ) {
					for ( var O = 0; z > O; O ++ ) {
						var q = { delay: j.delay, progress: j.progress };
						O === z - 1 && (q.display = j.display, q.visibility = j.visibility, q.complete = j.complete), P( g, "reverse", q )
					}
				}
				return e()
			}
		};
		b = f.extend( P, b ), b.animate = P;
		var w = t.requestAnimationFrame || g;
		return b.State.isMobile || r.hidden === a || r.addEventListener( "visibilitychange", function() {
			r.hidden ? (w = function( e ) {
				return setTimeout( function() {
					e( ! 0 )
				}, 16 )
			}, c()) : w = t.requestAnimationFrame || g
		} ), e.Velocity = b, e !== t && (e.fn.velocity = P, e.fn.velocity.defaults = b.defaults), f.each( [ "Down", "Up" ], function( e, t ) {
			b.Redirects[ "slide" + t ] = function( e, r, n, o, i, s ) {
				var l = f.extend( {}, r ), u = l.begin, c = l.complete, p = {
					height: "",
					marginTop: "",
					marginBottom: "",
					paddingTop: "",
					paddingBottom: ""
				}, d = {};
				l.display === a && (l.display = "Down" === t ? "inline" === b.CSS.Values.getDisplayType( e ) ? "inline-block" : "block" : "none"), l.begin = function() {
					u && u.call( i, i );
					for ( var r in p ) {
						d[ r ] = e.style[ r ];
						var a = b.CSS.getPropertyValue( e, r );
						p[ r ] = "Down" === t ? [ a, 0 ] : [ 0, a ]
					}
					d.overflow = e.style.overflow, e.style.overflow = "hidden"
				}, l.complete = function() {
					for ( var t in d )e.style[ t ] = d[ t ];
					c && c.call( i, i ), s && s.resolver( i )
				}, b( e, p, l )
			}
		} ), f.each( [ "In", "Out" ], function( e, t ) {
			b.Redirects[ "fade" + t ] = function( e, r, n, o, i, s ) {
				var l = f.extend( {}, r ), u = { opacity: "In" === t ? 1 : 0 }, c = l.complete;
				l.complete = n !== o - 1 ? l.begin = null : function() {
					c && c.call( i, i ), s && s.resolver( i )
				}, l.display === a && (l.display = "In" === t ? "auto" : "none"), b( this, u, l )
			}
		} ), b
	}( window.jQuery || window.Zepto || window, window, document )
} ));
;! function( a, b, c, d ) {
	"use strict";
	function k( a, b, c ) {
		return setTimeout( q( a, c ), b )
	}

	function l( a, b, c ) {
		return Array.isArray( a ) ? (m( a, c[ b ], c ), ! 0) : ! 1
	}

	function m( a, b, c ) {
		var e;
		if ( a ) {
			if ( a.forEach ) {
				a.forEach( b, c );
			} else {
				if ( a.length !== d ) {
					for ( e = 0; e < a.length; )b.call( c, a[ e ], e, a ), e ++;
				} else {
					for ( e in a )a.hasOwnProperty( e ) && b.call( c, a[ e ], e, a )
				}
			}
		}
	}

	function n( a, b, c ) {
		for ( var e = Object.keys( b ), f = 0; f < e.length; )(! c || c && a[ e[ f ] ] === d) && (a[ e[ f ] ] = b[ e[ f ] ]), f ++;
		return a
	}

	function o( a, b ) {
		return n( a, b, ! 0 )
	}

	function p( a, b, c ) {
		var e, d = b.prototype;
		e = a.prototype = Object.create( d ), e.constructor = a, e._super = d, c && n( e, c )
	}

	function q( a, b ) {
		return function() {
			return a.apply( b, arguments )
		}
	}

	function r( a, b ) {
		return typeof a == g ? a.apply( b ? b[ 0 ] || d : d, b ) : a
	}

	function s( a, b ) {
		return a === d ? b : a
	}

	function t( a, b, c ) {
		m( x( b ), function( b ) {
			a.addEventListener( b, c, ! 1 )
		} )
	}

	function u( a, b, c ) {
		m( x( b ), function( b ) {
			a.removeEventListener( b, c, ! 1 )
		} )
	}

	function v( a, b ) {
		for ( ; a; ) {
			if ( a == b ) {
				return ! 0;
			}
			a = a.parentNode
		}
		return ! 1
	}

	function w( a, b ) {
		return a.indexOf( b ) > - 1
	}

	function x( a ) {
		return a.trim().split( /\s+/g )
	}

	function y( a, b, c ) {
		if ( a.indexOf && ! c ) {
			return a.indexOf( b );
		}
		for ( var d = 0; d < a.length; ) {
			if ( c && a[ d ][ c ] == b || ! c && a[ d ] === b ) {
				return d;
			}
			d ++
		}
		return - 1
	}

	function z( a ) {
		return Array.prototype.slice.call( a, 0 )
	}

	function A( a, b, c ) {
		for ( var d = [], e = [], f = 0; f < a.length; ) {
			var g = b ? a[ f ][ b ] : a[ f ];
			y( e, g ) < 0 && d.push( a[ f ] ), e[ f ] = g, f ++
		}
		return c && (d = b ? d.sort( function( a, c ) {
			return a[ b ] > c[ b ]
		} ) : d.sort()), d
	}

	function B( a, b ) {
		for ( var c, f, g = b[ 0 ].toUpperCase() + b.slice( 1 ), h = 0; h < e.length; ) {
			if ( c = e[ h ], f = c ? c + g : b, f in a ) {
				return f;
			}
			h ++
		}
		return d
	}

	function D() {
		return C ++
	}

	function E( a ) {
		var b = a.ownerDocument;
		return b.defaultView || b.parentWindow
	}

	function ab( a, b ) {
		var c = this;
		this.manager = a, this.callback = b, this.element = a.element, this.target = a.options.inputTarget, this.domHandler = function( b ) {
			r( a.options.enable, [ a ] ) && c.handler( b )
		}, this.init()
	}

	function bb( a ) {
		var b, c = a.options.inputClass;
		return b = c ? c : H ? wb : I ? Eb : G ? Gb : rb, new b( a, cb )
	}

	function cb( a, b, c ) {
		var d = c.pointers.length, e = c.changedPointers.length, f = b & O && 0 === d - e, g = b & (Q | R) && 0 === d - e;
		c.isFirst = ! ! f, c.isFinal = ! ! g, f && (a.session = {}), c.eventType = b, db( a, c ), a.emit( "hammer.input", c ), a.recognize( c ), a.session.prevInput = c
	}

	function db( a, b ) {
		var c = a.session, d = b.pointers, e = d.length;
		c.firstInput || (c.firstInput = gb( b )), e > 1 && ! c.firstMultiple ? c.firstMultiple = gb( b ) : 1 === e && (c.firstMultiple = ! 1);
		var f = c.firstInput, g = c.firstMultiple, h = g ? g.center : f.center, i = b.center = hb( d );
		b.timeStamp = j(), b.deltaTime = b.timeStamp - f.timeStamp, b.angle = lb( h, i ), b.distance = kb( h, i ), eb( c, b ), b.offsetDirection = jb( b.deltaX, b.deltaY ), b.scale = g ? nb( g.pointers, d ) : 1, b.rotation = g ? mb( g.pointers, d ) : 0, fb( c, b );
		var k = a.element;
		v( b.srcEvent.target, k ) && (k = b.srcEvent.target), b.target = k
	}

	function eb( a, b ) {
		var c = b.center, d = a.offsetDelta || {}, e = a.prevDelta || {}, f = a.prevInput || {};
		(b.eventType === O || f.eventType === Q) && (e = a.prevDelta = {
			x: f.deltaX || 0,
			y: f.deltaY || 0
		}, d = a.offsetDelta = {
			x: c.x,
			y: c.y
		}), b.deltaX = e.x + (c.x - d.x), b.deltaY = e.y + (c.y - d.y)
	}

	function fb( a, b ) {
		var f, g, h, j, c = a.lastInterval || b, e = b.timeStamp - c.timeStamp;
		if ( b.eventType != R && (e > N || c.velocity === d) ) {
			var k = c.deltaX - b.deltaX, l = c.deltaY - b.deltaY, m = ib( e, k, l );
			g = m.x, h = m.y, f = i( m.x ) > i( m.y ) ? m.x : m.y, j = jb( k, l ), a.lastInterval = b
		} else {
			f = c.velocity, g = c.velocityX, h = c.velocityY, j = c.direction;
		}
		b.velocity = f, b.velocityX = g, b.velocityY = h, b.direction = j
	}

	function gb( a ) {
		for ( var b = [], c = 0; c < a.pointers.length; )b[ c ] = {
			clientX: h( a.pointers[ c ].clientX ),
			clientY: h( a.pointers[ c ].clientY )
		}, c ++;
		return { timeStamp: j(), pointers: b, center: hb( b ), deltaX: a.deltaX, deltaY: a.deltaY }
	}

	function hb( a ) {
		var b = a.length;
		if ( 1 === b ) {
			return { x: h( a[ 0 ].clientX ), y: h( a[ 0 ].clientY ) };
		}
		for ( var c = 0, d = 0, e = 0; b > e; )c += a[ e ].clientX, d += a[ e ].clientY, e ++;
		return { x: h( c / b ), y: h( d / b ) }
	}

	function ib( a, b, c ) {
		return { x: b / a || 0, y: c / a || 0 }
	}

	function jb( a, b ) {
		return a === b ? S : i( a ) >= i( b ) ? a > 0 ? T : U : b > 0 ? V : W
	}

	function kb( a, b, c ) {
		c || (c = $);
		var d = b[ c[ 0 ] ] - a[ c[ 0 ] ], e = b[ c[ 1 ] ] - a[ c[ 1 ] ];
		return Math.sqrt( d * d + e * e )
	}

	function lb( a, b, c ) {
		c || (c = $);
		var d = b[ c[ 0 ] ] - a[ c[ 0 ] ], e = b[ c[ 1 ] ] - a[ c[ 1 ] ];
		return 180 * Math.atan2( e, d ) / Math.PI
	}

	function mb( a, b ) {
		return lb( b[ 1 ], b[ 0 ], _ ) - lb( a[ 1 ], a[ 0 ], _ )
	}

	function nb( a, b ) {
		return kb( b[ 0 ], b[ 1 ], _ ) / kb( a[ 0 ], a[ 1 ], _ )
	}

	function rb() {
		this.evEl = pb, this.evWin = qb, this.allow = ! 0, this.pressed = ! 1, ab.apply( this, arguments )
	}

	function wb() {
		this.evEl = ub, this.evWin = vb, ab.apply( this, arguments ), this.store = this.manager.session.pointerEvents = []
	}

	function Ab() {
		this.evTarget = yb, this.evWin = zb, this.started = ! 1, ab.apply( this, arguments )
	}

	function Bb( a, b ) {
		var c = z( a.touches ), d = z( a.changedTouches );
		return b & (Q | R) && (c = A( c.concat( d ), "identifier", ! 0 )), [ c, d ]
	}

	function Eb() {
		this.evTarget = Db, this.targetIds = {}, ab.apply( this, arguments )
	}

	function Fb( a, b ) {
		var c = z( a.touches ), d = this.targetIds;
		if ( b & (O | P) && 1 === c.length ) {
			return d[ c[ 0 ].identifier ] = ! 0, [ c, c ];
		}
		var e, f, g = z( a.changedTouches ), h = [], i = this.target;
		if ( f = c.filter( function( a ) {
				return v( a.target, i )
			} ), b === O ) {
			for ( e = 0; e < f.length; )d[ f[ e ].identifier ] = ! 0, e ++;
		}
		for ( e = 0; e < g.length; )d[ g[ e ].identifier ] && h.push( g[ e ] ), b & (Q | R) && delete d[ g[ e ].identifier ], e ++;
		return h.length ? [ A( f.concat( h ), "identifier", ! 0 ), h ] : void 0
	}

	function Gb() {
		ab.apply( this, arguments );
		var a = q( this.handler, this );
		this.touch = new Eb( this.manager, a ), this.mouse = new rb( this.manager, a )
	}

	function Pb( a, b ) {
		this.manager = a, this.set( b )
	}

	function Qb( a ) {
		if ( w( a, Mb ) ) {
			return Mb;
		}
		var b = w( a, Nb ), c = w( a, Ob );
		return b && c ? Nb + " " + Ob : b || c ? b ? Nb : Ob : w( a, Lb ) ? Lb : Kb
	}

	function Yb( a ) {
		this.id = D(), this.manager = null, this.options = o( a || {}, this.defaults ), this.options.enable = s( this.options.enable, ! 0 ), this.state = Rb, this.simultaneous = {}, this.requireFail = []
	}

	function Zb( a ) {
		return a & Wb ? "cancel" : a & Ub ? "end" : a & Tb ? "move" : a & Sb ? "start" : ""
	}

	function $b( a ) {
		return a == W ? "down" : a == V ? "up" : a == T ? "left" : a == U ? "right" : ""
	}

	function _b( a, b ) {
		var c = b.manager;
		return c ? c.get( a ) : a
	}

	function ac() {
		Yb.apply( this, arguments )
	}

	function bc() {
		ac.apply( this, arguments ), this.pX = null, this.pY = null
	}

	function cc() {
		ac.apply( this, arguments )
	}

	function dc() {
		Yb.apply( this, arguments ), this._timer = null, this._input = null
	}

	function ec() {
		ac.apply( this, arguments )
	}

	function fc() {
		ac.apply( this, arguments )
	}

	function gc() {
		Yb.apply( this, arguments ), this.pTime = ! 1, this.pCenter = ! 1, this._timer = null, this._input = null, this.count = 0
	}

	function hc( a, b ) {
		return b = b || {}, b.recognizers = s( b.recognizers, hc.defaults.preset ), new kc( a, b )
	}

	function kc( a, b ) {
		b = b || {}, this.options = o( b, hc.defaults ), this.options.inputTarget = this.options.inputTarget || a, this.handlers = {}, this.session = {}, this.recognizers = [], this.element = a, this.input = bb( this ), this.touchAction = new Pb( this, this.options.touchAction ), lc( this, ! 0 ), m( b.recognizers, function( a ) {
			var b = this.add( new a[ 0 ]( a[ 1 ] ) );
			a[ 2 ] && b.recognizeWith( a[ 2 ] ), a[ 3 ] && b.requireFailure( a[ 3 ] )
		}, this )
	}

	function lc( a, b ) {
		var c = a.element;
		m( a.options.cssProps, function( a, d ) {
			c.style[ B( c.style, d ) ] = b ? a : ""
		} )
	}

	function mc( a, c ) {
		var d = b.createEvent( "Event" );
		d.initEvent( a, ! 0, ! 0 ), d.gesture = c, c.target.dispatchEvent( d )
	}

	var e = [ "", "webkit", "moz", "MS", "ms", "o" ], f = b.createElement( "div" ), g = "function", h = Math.round, i = Math.abs, j = Date.now, C = 1, F = /mobile|tablet|ip(ad|hone|od)|android/i, G = "ontouchstart" in a, H = B( a, "PointerEvent" ) !== d, I = G && F.test( navigator.userAgent ), J = "touch", K = "pen", L = "mouse", M = "kinect", N = 25, O = 1, P = 2, Q = 4, R = 8, S = 1, T = 2, U = 4, V = 8, W = 16, X = T | U, Y = V | W, Z = X | Y, $ = [ "x", "y" ], _ = [ "clientX", "clientY" ];
	ab.prototype = {
		handler: function() {
		}, init: function() {
			this.evEl && t( this.element, this.evEl, this.domHandler ), this.evTarget && t( this.target, this.evTarget, this.domHandler ), this.evWin && t( E( this.element ), this.evWin, this.domHandler )
		}, destroy: function() {
			this.evEl && u( this.element, this.evEl, this.domHandler ), this.evTarget && u( this.target, this.evTarget, this.domHandler ), this.evWin && u( E( this.element ), this.evWin, this.domHandler )
		}
	};
	var ob = {
		mousedown: O,
		mousemove: P,
		mouseup: Q
	}, pb = "mousedown", qb = "mousemove mouseup";
	p( rb, ab, {
		handler: function( a ) {
			var b = ob[ a.type ];
			b & O && 0 === a.button && (this.pressed = ! 0), b & P && 1 !== a.which && (b = Q), this.pressed && this.allow && (b & Q && (this.pressed = ! 1), this.callback( this.manager, b, {
				pointers: [ a ],
				changedPointers: [ a ],
				pointerType: L,
				srcEvent: a
			} ))
		}
	} );
	var sb = {
		pointerdown: O,
		pointermove: P,
		pointerup: Q,
		pointercancel: R,
		pointerout: R
	}, tb = {
		2: J,
		3: K,
		4: L,
		5: M
	}, ub = "pointerdown", vb = "pointermove pointerup pointercancel";
	a.MSPointerEvent && (ub = "MSPointerDown", vb = "MSPointerMove MSPointerUp MSPointerCancel"), p( wb, ab, {
		handler: function( a ) {
			var b = this.store, c = ! 1, d = a.type.toLowerCase().replace( "ms", "" ), e = sb[ d ], f = tb[ a.pointerType ] || a.pointerType, g = f == J, h = y( b, a.pointerId, "pointerId" );
			e & O && (0 === a.button || g) ? 0 > h && (b.push( a ), h = b.length - 1) : e & (Q | R) && (c = ! 0), 0 > h || (b[ h ] = a, this.callback( this.manager, e, {
				pointers: b,
				changedPointers: [ a ],
				pointerType: f,
				srcEvent: a
			} ), c && b.splice( h, 1 ))
		}
	} );
	var xb = {
		touchstart: O,
		touchmove: P,
		touchend: Q,
		touchcancel: R
	}, yb = "touchstart", zb = "touchstart touchmove touchend touchcancel";
	p( Ab, ab, {
		handler: function( a ) {
			var b = xb[ a.type ];
			if ( b === O && (this.started = ! 0), this.started ) {
				var c = Bb.call( this, a, b );
				b & (Q | R) && 0 === c[ 0 ].length - c[ 1 ].length && (this.started = ! 1), this.callback( this.manager, b, {
					pointers: c[ 0 ],
					changedPointers: c[ 1 ],
					pointerType: J,
					srcEvent: a
				} )
			}
		}
	} );
	var Cb = {
		touchstart: O,
		touchmove: P,
		touchend: Q,
		touchcancel: R
	}, Db = "touchstart touchmove touchend touchcancel";
	p( Eb, ab, {
		handler: function( a ) {
			var b = Cb[ a.type ], c = Fb.call( this, a, b );
			c && this.callback( this.manager, b, {
				pointers: c[ 0 ],
				changedPointers: c[ 1 ],
				pointerType: J,
				srcEvent: a
			} )
		}
	} ), p( Gb, ab, {
		handler: function( a, b, c ) {
			var d = c.pointerType == J, e = c.pointerType == L;
			if ( d ) {
				this.mouse.allow = ! 1;
			} else {
				if ( e && ! this.mouse.allow ) {
					return;
				}
			}
			b & (Q | R) && (this.mouse.allow = ! 0), this.callback( a, b, c )
		}, destroy: function() {
			this.touch.destroy(), this.mouse.destroy()
		}
	} );
	var Hb = B( f.style, "touchAction" ), Ib = Hb !== d, Jb = "compute", Kb = "auto", Lb = "manipulation", Mb = "none", Nb = "pan-x", Ob = "pan-y";
	Pb.prototype = {
		set: function( a ) {
			a == Jb && (a = this.compute()), Ib && (this.manager.element.style[ Hb ] = a), this.actions = a.toLowerCase().trim()
		}, update: function() {
			this.set( this.manager.options.touchAction )
		}, compute: function() {
			var a = [];
			return m( this.manager.recognizers, function( b ) {
				r( b.options.enable, [ b ] ) && (a = a.concat( b.getTouchAction() ))
			} ), Qb( a.join( " " ) )
		}, preventDefaults: function( a ) {
			if ( ! Ib ) {
				var b = a.srcEvent, c = a.offsetDirection;
				if ( this.manager.session.prevented ) {
					return b.preventDefault(), void 0;
				}
				var d = this.actions, e = w( d, Mb ), f = w( d, Ob ), g = w( d, Nb );
				return e || f && c & X || g && c & Y ? this.preventSrc( b ) : void 0
			}
		}, preventSrc: function( a ) {
			this.manager.session.prevented = ! 0, a.preventDefault()
		}
	};
	var Rb = 1, Sb = 2, Tb = 4, Ub = 8, Vb = Ub, Wb = 16, Xb = 32;
	Yb.prototype = {
		defaults: {}, set: function( a ) {
			return n( this.options, a ), this.manager && this.manager.touchAction.update(), this
		}, recognizeWith: function( a ) {
			if ( l( a, "recognizeWith", this ) ) {
				return this;
			}
			var b = this.simultaneous;
			return a = _b( a, this ), b[ a.id ] || (b[ a.id ] = a, a.recognizeWith( this )), this
		}, dropRecognizeWith: function( a ) {
			return l( a, "dropRecognizeWith", this ) ? this : (a = _b( a, this ), delete this.simultaneous[ a.id ], this)
		}, requireFailure: function( a ) {
			if ( l( a, "requireFailure", this ) ) {
				return this;
			}
			var b = this.requireFail;
			return a = _b( a, this ), - 1 === y( b, a ) && (b.push( a ), a.requireFailure( this )), this
		}, dropRequireFailure: function( a ) {
			if ( l( a, "dropRequireFailure", this ) ) {
				return this;
			}
			a = _b( a, this );
			var b = y( this.requireFail, a );
			return b > - 1 && this.requireFail.splice( b, 1 ), this
		}, hasRequireFailures: function() {
			return this.requireFail.length > 0
		}, canRecognizeWith: function( a ) {
			return ! ! this.simultaneous[ a.id ]
		}, emit: function( a ) {
			function d( d ) {
				b.manager.emit( b.options.event + (d ? Zb( c ) : ""), a )
			}

			var b = this, c = this.state;
			Ub > c && d( ! 0 ), d(), c >= Ub && d( ! 0 )
		}, tryEmit: function( a ) {
			return this.canEmit() ? this.emit( a ) : (this.state = Xb, void 0)
		}, canEmit: function() {
			for ( var a = 0; a < this.requireFail.length; ) {
				if ( ! (this.requireFail[ a ].state & (Xb | Rb)) ) {
					return ! 1;
				}
				a ++
			}
			return ! 0
		}, recognize: function( a ) {
			var b = n( {}, a );
			return r( this.options.enable, [ this, b ] ) ? (this.state & (Vb | Wb | Xb) && (this.state = Rb), this.state = this.process( b ), this.state & (Sb | Tb | Ub | Wb) && this.tryEmit( b ), void 0) : (this.reset(), this.state = Xb, void 0)
		}, process: function() {
		}, getTouchAction: function() {
		}, reset: function() {
		}
	}, p( ac, Yb, {
		defaults: { pointers: 1 }, attrTest: function( a ) {
			var b = this.options.pointers;
			return 0 === b || a.pointers.length === b
		}, process: function( a ) {
			var b = this.state, c = a.eventType, d = b & (Sb | Tb), e = this.attrTest( a );
			return d && (c & R || ! e) ? b | Wb : d || e ? c & Q ? b | Ub : b & Sb ? b | Tb : Sb : Xb
		}
	} ), p( bc, ac, {
		defaults: { event: "pan", threshold: 10, pointers: 1, direction: Z },
		getTouchAction: function() {
			var a = this.options.direction, b = [];
			return a & X && b.push( Ob ), a & Y && b.push( Nb ), b
		},
		directionTest: function( a ) {
			var b = this.options, c = ! 0, d = a.distance, e = a.direction, f = a.deltaX, g = a.deltaY;
			return e & b.direction || (b.direction & X ? (e = 0 === f ? S : 0 > f ? T : U, c = f != this.pX, d = Math.abs( a.deltaX )) : (e = 0 === g ? S : 0 > g ? V : W, c = g != this.pY, d = Math.abs( a.deltaY ))), a.direction = e, c && d > b.threshold && e & b.direction
		},
		attrTest: function( a ) {
			return ac.prototype.attrTest.call( this, a ) && (this.state & Sb || ! (this.state & Sb) && this.directionTest( a ))
		},
		emit: function( a ) {
			this.pX = a.deltaX, this.pY = a.deltaY;
			var b = $b( a.direction );
			b && this.manager.emit( this.options.event + b, a ), this._super.emit.call( this, a )
		}
	} ), p( cc, ac, {
		defaults: { event: "pinch", threshold: 0, pointers: 2 },
		getTouchAction: function() {
			return [ Mb ]
		},
		attrTest: function( a ) {
			return this._super.attrTest.call( this, a ) && (Math.abs( a.scale - 1 ) > this.options.threshold || this.state & Sb)
		},
		emit: function( a ) {
			if ( this._super.emit.call( this, a ), 1 !== a.scale ) {
				var b = a.scale < 1 ? "in" : "out";
				this.manager.emit( this.options.event + b, a )
			}
		}
	} ), p( dc, Yb, {
		defaults: { event: "press", pointers: 1, time: 500, threshold: 5 },
		getTouchAction: function() {
			return [ Kb ]
		},
		process: function( a ) {
			var b = this.options, c = a.pointers.length === b.pointers, d = a.distance < b.threshold, e = a.deltaTime > b.time;
			if ( this._input = a, ! d || ! c || a.eventType & (Q | R) && ! e ) {
				this.reset();
			} else {
				if ( a.eventType & O ) {
					this.reset(), this._timer = k( function() {
						this.state = Vb, this.tryEmit()
					}, b.time, this );
				} else {
					if ( a.eventType & Q ) {
						return Vb;
					}
				}
			}
			return Xb
		},
		reset: function() {
			clearTimeout( this._timer )
		},
		emit: function( a ) {
			this.state === Vb && (a && a.eventType & Q ? this.manager.emit( this.options.event + "up", a ) : (this._input.timeStamp = j(), this.manager.emit( this.options.event, this._input )))
		}
	} ), p( ec, ac, {
		defaults: { event: "rotate", threshold: 0, pointers: 2 },
		getTouchAction: function() {
			return [ Mb ]
		},
		attrTest: function( a ) {
			return this._super.attrTest.call( this, a ) && (Math.abs( a.rotation ) > this.options.threshold || this.state & Sb)
		}
	} ), p( fc, ac, {
		defaults: {
			event: "swipe",
			threshold: 10,
			velocity: .65,
			direction: X | Y,
			pointers: 1
		}, getTouchAction: function() {
			return bc.prototype.getTouchAction.call( this )
		}, attrTest: function( a ) {
			var c, b = this.options.direction;
			return b & (X | Y) ? c = a.velocity : b & X ? c = a.velocityX : b & Y && (c = a.velocityY), this._super.attrTest.call( this, a ) && b & a.direction && a.distance > this.options.threshold && i( c ) > this.options.velocity && a.eventType & Q
		}, emit: function( a ) {
			var b = $b( a.direction );
			b && this.manager.emit( this.options.event + b, a ), this.manager.emit( this.options.event, a )
		}
	} ), p( gc, Yb, {
		defaults: {
			event: "tap",
			pointers: 1,
			taps: 1,
			interval: 300,
			time: 250,
			threshold: 2,
			posThreshold: 10
		}, getTouchAction: function() {
			return [ Lb ]
		}, process: function( a ) {
			var b = this.options, c = a.pointers.length === b.pointers, d = a.distance < b.threshold, e = a.deltaTime < b.time;
			if ( this.reset(), a.eventType & O && 0 === this.count ) {
				return this.failTimeout();
			}
			if ( d && e && c ) {
				if ( a.eventType != Q ) {
					return this.failTimeout();
				}
				var f = this.pTime ? a.timeStamp - this.pTime < b.interval : ! 0, g = ! this.pCenter || kb( this.pCenter, a.center ) < b.posThreshold;
				this.pTime = a.timeStamp, this.pCenter = a.center, g && f ? this.count += 1 : this.count = 1, this._input = a;
				var h = this.count % b.taps;
				if ( 0 === h ) {
					return this.hasRequireFailures() ? (this._timer = k( function() {
						this.state = Vb, this.tryEmit()
					}, b.interval, this ), Sb) : Vb
				}
			}
			return Xb
		}, failTimeout: function() {
			return this._timer = k( function() {
				this.state = Xb
			}, this.options.interval, this ), Xb
		}, reset: function() {
			clearTimeout( this._timer )
		}, emit: function() {
			this.state == Vb && (this._input.tapCount = this.count, this.manager.emit( this.options.event, this._input ))
		}
	} ), hc.VERSION = "2.0.4", hc.defaults = {
		domEvents: ! 1,
		touchAction: Jb,
		enable: ! 0,
		inputTarget: null,
		inputClass: null,
		preset: [ [ ec, { enable: ! 1 } ], [ cc, { enable: ! 1 }, [ "rotate" ] ], [ fc, { direction: X } ], [ bc, { direction: X }, [ "swipe" ] ], [ gc ], [ gc, {
			event: "doubletap",
			taps: 2
		}, [ "tap" ] ], [ dc ] ],
		cssProps: {
			userSelect: "default",
			touchSelect: "none",
			touchCallout: "none",
			contentZooming: "none",
			userDrag: "none",
			tapHighlightColor: "rgba(0,0,0,0)"
		}
	};
	var ic = 1, jc = 2;
	kc.prototype = {
		set: function( a ) {
			return n( this.options, a ), a.touchAction && this.touchAction.update(), a.inputTarget && (this.input.destroy(), this.input.target = a.inputTarget, this.input.init()), this
		}, stop: function( a ) {
			this.session.stopped = a ? jc : ic
		}, recognize: function( a ) {
			var b = this.session;
			if ( ! b.stopped ) {
				this.touchAction.preventDefaults( a );
				var c, d = this.recognizers, e = b.curRecognizer;
				(! e || e && e.state & Vb) && (e = b.curRecognizer = null);
				for ( var f = 0; f < d.length; )c = d[ f ], b.stopped === jc || e && c != e && ! c.canRecognizeWith( e ) ? c.reset() : c.recognize( a ), ! e && c.state & (Sb | Tb | Ub) && (e = b.curRecognizer = c), f ++
			}
		}, get: function( a ) {
			if ( a instanceof Yb ) {
				return a;
			}
			for ( var b = this.recognizers, c = 0; c < b.length; c ++ )if ( b[ c ].options.event == a ) {
				return b[ c ];
			}
			return null
		}, add: function( a ) {
			if ( l( a, "add", this ) ) {
				return this;
			}
			var b = this.get( a.options.event );
			return b && this.remove( b ), this.recognizers.push( a ), a.manager = this, this.touchAction.update(), a
		}, remove: function( a ) {
			if ( l( a, "remove", this ) ) {
				return this;
			}
			var b = this.recognizers;
			return a = this.get( a ), b.splice( y( b, a ), 1 ), this.touchAction.update(), this
		}, on: function( a, b ) {
			var c = this.handlers;
			return m( x( a ), function( a ) {
				c[ a ] = c[ a ] || [], c[ a ].push( b )
			} ), this
		}, off: function( a, b ) {
			var c = this.handlers;
			return m( x( a ), function( a ) {
				b ? c[ a ].splice( y( c[ a ], b ), 1 ) : delete c[ a ]
			} ), this
		}, emit: function( a, b ) {
			this.options.domEvents && mc( a, b );
			var c = this.handlers[ a ] && this.handlers[ a ].slice();
			if ( c && c.length ) {
				b.type = a, b.preventDefault = function() {
					b.srcEvent.preventDefault()
				};
				for ( var d = 0; d < c.length; )c[ d ]( b ), d ++
			}
		}, destroy: function() {
			this.element && lc( this, ! 1 ), this.handlers = {}, this.session = {}, this.input.destroy(), this.element = null
		}
	}, n( hc, {
		INPUT_START: O,
		INPUT_MOVE: P,
		INPUT_END: Q,
		INPUT_CANCEL: R,
		STATE_POSSIBLE: Rb,
		STATE_BEGAN: Sb,
		STATE_CHANGED: Tb,
		STATE_ENDED: Ub,
		STATE_RECOGNIZED: Vb,
		STATE_CANCELLED: Wb,
		STATE_FAILED: Xb,
		DIRECTION_NONE: S,
		DIRECTION_LEFT: T,
		DIRECTION_RIGHT: U,
		DIRECTION_UP: V,
		DIRECTION_DOWN: W,
		DIRECTION_HORIZONTAL: X,
		DIRECTION_VERTICAL: Y,
		DIRECTION_ALL: Z,
		Manager: kc,
		Input: ab,
		TouchAction: Pb,
		TouchInput: Eb,
		MouseInput: rb,
		PointerEventInput: wb,
		TouchMouseInput: Gb,
		SingleTouchInput: Ab,
		Recognizer: Yb,
		AttrRecognizer: ac,
		Tap: gc,
		Pan: bc,
		Swipe: fc,
		Pinch: cc,
		Rotate: ec,
		Press: dc,
		on: t,
		off: u,
		each: m,
		merge: o,
		extend: n,
		inherit: p,
		bindFn: q,
		prefixed: B
	} ), typeof define == g && define.amd ? define( function() {
		return hc
	} ) : "undefined" != typeof module && module.exports ? module.exports = hc : a[ c ] = hc
}( window, document, "Hammer" );
;(function( factory ) {
	if ( typeof define === 'function' && define.amd ) {
		define( [ 'jquery', 'hammerjs' ], factory );
	} else {
		if ( typeof exports === 'object' ) {
			factory( require( 'jquery' ), require( 'hammerjs' ) );
		} else {
			factory( jQuery, Hammer );
		}
	}
}( function( $, Hammer ) {
	function hammerify( el, options ) {
		var $el = $( el );
		if ( ! $el.data( "hammer" ) ) {
			$el.data( "hammer", new Hammer( $el[ 0 ], options ) );
		}
	}

	$.fn.hammer = function( options ) {
		return this.each( function() {
			hammerify( this, options );
		} );
	};

	// extend the emit method to also trigger jQuery events
	Hammer.Manager.prototype.emit = (function( originalEmit ) {
		return function( type, data ) {
			originalEmit.call( this, type, data );
			$( this.element ).trigger( {
				type: type,
				gesture: data
			} );
		};
	})( Hammer.Manager.prototype.emit );
} ));
;// Required for Meteor package, the use of window prevents export by Meteor
(function( window ) {
	if ( window.Package ) {
		Materialize = {};
	} else {
		window.Materialize = {};
	}
})( window );


// Unique ID
Materialize.guid = (function() {
	function s4() {
		return Math.floor( (1 + Math.random()) * 0x10000 ).toString( 16 ).substring( 1 );
	}

	return function() {
		return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
			s4() + '-' + s4() + s4() + s4();
	};
})();

Materialize.elementOrParentIsFixed = function( element ) {
	var $element = $( element );
	var $checkElements = $element.add( $element.parents() );
	var isFixed = false;
	$checkElements.each( function() {
		if ( $( this ).css( "position" ) === "fixed" ) {
			isFixed = true;
			return false;
		}
	} );
	return isFixed;
};

// Velocity has conflicts when loaded with jQuery, this will check for it
var Vel;
if ( $ ) {
	Vel = $.Velocity;
} else {
	if ( jQuery ) {
		Vel = jQuery.Velocity;
	} else {
		Vel = Velocity;
	}
}
;(function( $ ) {
	$.fn.collapsible = function( options ) {
		var defaults = {
			accordion: undefined
		};

		options = $.extend( defaults, options );


		return this.each( function() {

			var $this = $( this );

			var $panel_headers = $( this ).find( '> li > .collapsible-header, > a > .collapsible-header' );

			var collapsible_type = $this.data( "collapsible" );

			// Turn off any existing event handlers
			$this.off( 'click.collapse', '> li > .collapsible-header, > a > .collapsible-header' );
			$panel_headers.off( 'click.collapse' );


			/****************
			 Helper Functions
			 ****************/

			// Accordion Open
			function accordionOpen( object ) {
				$panel_headers = $this.find( '> li > .collapsible-header, > a > .collapsible-header' );
				if ( object.hasClass( 'active' ) ) {
					object.parent().addClass( 'active' );
				}
				else {
					object.parent().removeClass( 'active' );
				}
				if ( object.parent().hasClass( 'active' ) ) {
					object.siblings( '.collapsible-body' ).stop( true, false ).slideDown( {
						duration: 350,
						easing: "easeOutQuart",
						queue: true,
						complete: function() {
							$( this ).css( 'height', '' );
						}
					} );
				}
				else {
					object.siblings( '.collapsible-body' ).stop( true, false ).slideUp( {
						duration: 350,
						easing: "easeOutQuart",
						queue: true,
						complete: function() {
							$( this ).css( 'height', '' );
						}
					} );
				}

				$panel_headers.not( object ).removeClass( 'active' ).parent().removeClass( 'active' );
				$panel_headers.not( object ).parent().children( '.collapsible-body' ).stop( true, false ).slideUp(
					{
						duration: 350,
						easing: "easeOutQuart",
						queue: true,
						complete: function() {
							$( this ).css( 'height', '' );
						}
					} );
			}

			// Expandable Open
			function expandableOpen( object ) {
				if ( object.hasClass( 'active' ) ) {
					object.parent().addClass( 'active' );
				}
				else {
					object.parent().removeClass( 'active' );
				}
				if ( object.parent().hasClass( 'active' ) ) {
					object.siblings( '.collapsible-body' ).stop( true, false ).slideDown( {
						duration: 350,
						easing: "easeOutQuart",
						queue: true,
						complete: function() {
							$( this ).css( 'height', '' );
						}
					} );
				}
				else {
					object.siblings( '.collapsible-body' ).stop( true, false ).slideUp( {
						duration: 350,
						easing: "easeOutQuart",
						queue: true,
						complete: function() {
							$( this ).css( 'height', '' );
						}
					} );
				}
			}

			/**
			 * Check if object is children of panel header
			 * @param  {Object}  object Jquery object
			 * @return {Boolean} true if it is children
			 */
			function isChildrenOfPanelHeader( object ) {

				var panelHeader = getPanelHeader( object );

				return panelHeader.length > 0;
			}

			/**
			 * Get panel header from a children element
			 * @param  {Object} object Jquery object
			 * @return {Object} panel header object
			 */
			function getPanelHeader( object ) {

				return object.closest( 'li > .collapsible-header, a > .collapsible-header' );
			}

			/*****  End Helper Functions  *****/



			// Add click handler to only direct collapsible header children
			$this.on( 'click.collapse', '> li > .collapsible-header, > a > .collapsible-header', function( e ) {
				var $header = $( this ),
					element = $( e.target );

				if ( isChildrenOfPanelHeader( element ) ) {
					element = getPanelHeader( element );
				}

				element.toggleClass( 'active' );

				if ( options.accordion || collapsible_type === "accordion" || collapsible_type === undefined ) { // Handle Accordion
					accordionOpen( element );
				} else { // Handle Expandables
					expandableOpen( element );

					if ( $header.hasClass( 'active' ) ) {
						expandableOpen( $header );
					}
				}
			} );

			// Open first active
			var $panel_headers = $this.find( '> li > .collapsible-header, > a > .collapsible-header' );
			if ( options.accordion || collapsible_type === "accordion" || collapsible_type === undefined ) { // Handle Accordion
				accordionOpen( $panel_headers.filter( '.active' ).first() );
			}
			else { // Handle Expandables
				$panel_headers.filter( '.active' ).each( function() {
					expandableOpen( $( this ) );
				} );
			}

		} );
	};

	$( document ).ready( function() {
		$( '.collapsible' ).collapsible();
	} );
}( jQuery ));
;(function( $ ) {

	// Add posibility to scroll to selected option
	// usefull for select for example
	$.fn.scrollTo = function( elem ) {
		$( this ).scrollTop( $( this ).scrollTop() - $( this ).offset().top + $( elem ).offset().top );
		return this;
	};

	$.fn.dropdown = function( options ) {
		var defaults = {
			inDuration: 300,
			outDuration: 225,
			constrain_width: true, // Constrains width of dropdown to the activator
			hover: false,
			gutter: 0, // Spacing from edge
			belowOrigin: false,
			alignment: 'left',
			stopPropagation: false
		};

		// Open dropdown.
		if ( options === "open" ) {
			this.each( function() {
				$( this ).trigger( 'open' );
			} );
			return false;
		}

		// Close dropdown.
		if ( options === "close" ) {
			this.each( function() {
				$( this ).trigger( 'close' );
			} );
			return false;
		}

		this.each( function() {
			var origin = $( this );
			var options = $.extend( {}, defaults, options );
			var isFocused = false;

			// Dropdown menu
			var activates = $( "#" + origin.attr( 'data-activates' ) );

			function updateOptions() {
				if ( origin.data( 'induration' ) !== undefined ) {
					options.inDuration = origin.data( 'induration' );
				}
				if ( origin.data( 'outduration' ) !== undefined ) {
					options.outDuration = origin.data( 'outduration' );
				}
				if ( origin.data( 'constrainwidth' ) !== undefined ) {
					options.constrain_width = origin.data( 'constrainwidth' );
				}
				if ( origin.data( 'hover' ) !== undefined ) {
					options.hover = origin.data( 'hover' );
				}
				if ( origin.data( 'gutter' ) !== undefined ) {
					options.gutter = origin.data( 'gutter' );
				}
				if ( origin.data( 'beloworigin' ) !== undefined ) {
					options.belowOrigin = origin.data( 'beloworigin' );
				}
				if ( origin.data( 'alignment' ) !== undefined ) {
					options.alignment = origin.data( 'alignment' );
				}
				if ( origin.data( 'stoppropagation' ) !== undefined ) {
					options.stopPropagation = origin.data( 'stoppropagation' );
				}
			}

			updateOptions();

			// Attach dropdown to its activator
			origin.after( activates );

			/*
			 Helper function to position and resize dropdown.
			 Used in hover and click handler.
			 */
			function placeDropdown( eventType ) {
				// Check for simultaneous focus and click events.
				if ( eventType === 'focus' ) {
					isFocused = true;
				}

				// Check html data attributes
				updateOptions();

				// Set Dropdown state
				activates.addClass( 'active' );
				origin.addClass( 'active' );

				// Constrain width
				if ( options.constrain_width === true ) {
					activates.css( 'width', origin.outerWidth() );

				} else {
					activates.css( 'white-space', 'nowrap' );
				}

				// Offscreen detection
				var windowHeight = window.innerHeight;
				var originHeight = origin.innerHeight();
				var offsetLeft = origin.offset().left;
				var offsetTop = origin.offset().top - $( window ).scrollTop();
				var currAlignment = options.alignment;
				var gutterSpacing = 0;
				var leftPosition = 0;

				// Below Origin
				var verticalOffset = 0;
				if ( options.belowOrigin === true ) {
					verticalOffset = originHeight;
				}

				// Check for scrolling positioned container.
				var scrollYOffset = 0;
				var scrollXOffset = 0;
				var wrapper = origin.parent();
				if ( ! wrapper.is( 'body' ) ) {
					if ( wrapper[ 0 ].scrollHeight > wrapper[ 0 ].clientHeight ) {
						scrollYOffset = wrapper[ 0 ].scrollTop;
					}
					if ( wrapper[ 0 ].scrollWidth > wrapper[ 0 ].clientWidth ) {
						scrollXOffset = wrapper[ 0 ].scrollLeft;
					}
				}


				if ( offsetLeft + activates.innerWidth() > $( window ).width() ) {
					// Dropdown goes past screen on right, force right alignment
					currAlignment = 'right';

				} else {
					if ( offsetLeft - activates.innerWidth() + origin.innerWidth() < 0 ) {
						// Dropdown goes past screen on left, force left alignment
						currAlignment = 'left';
					}
				}
				// Vertical bottom offscreen detection
				if ( offsetTop + activates.innerHeight() > windowHeight ) {
					// If going upwards still goes offscreen, just crop height of dropdown.
					if ( offsetTop + originHeight - activates.innerHeight() < 0 ) {
						var adjustedHeight = windowHeight - offsetTop - verticalOffset;
						activates.css( 'max-height', adjustedHeight );
					} else {
						// Flow upwards.
						if ( ! verticalOffset ) {
							verticalOffset += originHeight;
						}
						verticalOffset -= activates.innerHeight();
					}
				}

				// Handle edge alignment
				if ( currAlignment === 'left' ) {
					gutterSpacing = options.gutter;
					leftPosition = origin.position().left + gutterSpacing;
				}
				else {
					if ( currAlignment === 'right' ) {
						var offsetRight = origin.position().left + origin.outerWidth() - activates.outerWidth();
						gutterSpacing = - options.gutter;
						leftPosition = offsetRight + gutterSpacing;
					}
				}

				// Position dropdown
				activates.css( {
					position: 'absolute',
					top: origin.position().top + verticalOffset + scrollYOffset,
					left: leftPosition + scrollXOffset
				} );


				// Show dropdown
				activates.stop( true, true ).css( 'opacity', 0 ).slideDown( {
					queue: false,
					duration: options.inDuration,
					easing: 'easeOutCubic',
					complete: function() {
						$( this ).css( 'height', '' );
					}
				} ).animate( { opacity: 1 }, {
					queue: false,
					duration: options.inDuration,
					easing: 'easeOutSine'
				} );
			}

			function hideDropdown() {
				// Check for simultaneous focus and click events.
				isFocused = false;
				activates.fadeOut( options.outDuration );
				activates.removeClass( 'active' );
				origin.removeClass( 'active' );
				setTimeout( function() {
					activates.css( 'max-height', '' );
				}, options.outDuration );
			}

			// Hover
			if ( options.hover ) {
				var open = false;
				origin.unbind( 'click.' + origin.attr( 'id' ) );
				// Hover handler to show dropdown
				origin.on( 'mouseenter', function( e ) { // Mouse over
					if ( open === false ) {
						placeDropdown();
						open = true;
					}
				} );
				origin.on( 'mouseleave', function( e ) {
					// If hover on origin then to something other than dropdown content, then close
					var toEl = e.toElement || e.relatedTarget; // added browser compatibility for
															   // target element
					if ( ! $( toEl ).closest( '.dropdown-content' ).is( activates ) ) {
						activates.stop( true, true );
						hideDropdown();
						open = false;
					}
				} );

				activates.on( 'mouseleave', function( e ) { // Mouse out
					var toEl = e.toElement || e.relatedTarget;
					if ( ! $( toEl ).closest( '.dropdown-button' ).is( origin ) ) {
						activates.stop( true, true );
						hideDropdown();
						open = false;
					}
				} );

				// Click
			} else {
				// Click handler to show dropdown
				origin.unbind( 'click.' + origin.attr( 'id' ) );
				origin.bind( 'click.' + origin.attr( 'id' ), function( e ) {
					if ( ! isFocused ) {
						if ( origin[ 0 ] == e.currentTarget && ! origin.hasClass( 'active' ) &&
							($( e.target ).closest( '.dropdown-content' ).length === 0) ) {
							e.preventDefault(); // Prevents button click from moving window
							if ( options.stopPropagation ) {
								e.stopPropagation();
							}
							placeDropdown( 'click' );
						}
						// If origin is clicked and menu is open, close menu
						else {
							if ( origin.hasClass( 'active' ) ) {
								hideDropdown();
								$( document ).unbind( 'click.' + activates.attr( 'id' ) + ' touchstart.' + activates.attr( 'id' ) );
							}
						}
						// If menu open, add click close handler to document
						if ( activates.hasClass( 'active' ) ) {
							$( document ).bind( 'click.' + activates.attr( 'id' ) + ' touchstart.' + activates.attr( 'id' ), function( e ) {
								if ( ! activates.is( e.target ) && ! origin.is( e.target ) && (! origin.find( e.target ).length) ) {
									hideDropdown();
									$( document ).unbind( 'click.' + activates.attr( 'id' ) + ' touchstart.' + activates.attr( 'id' ) );
								}
							} );
						}
					}
				} );

			} // End else

			// Listen to open and close event - useful for select component
			origin.on( 'open', function( e, eventType ) {
				placeDropdown( eventType );
			} );
			origin.on( 'close', hideDropdown );


		} );
	}; // End dropdown plugin

	$( document ).ready( function() {
		$( '.dropdown-button' ).dropdown();
	} );
}( jQuery ));
;(function( $ ) {
	var _stack = 0,
		_lastID = 0,
		_generateID = function() {
			_lastID ++;
			return 'materialize-lean-overlay-' + _lastID;
		};

	$.fn.extend( {
		openModal: function( options ) {

			var $body = $( 'body' );
			var oldWidth = $body.innerWidth();
			$body.css( 'overflow', 'hidden' );
			$body.width( oldWidth );

			var defaults = {
				opacity: 0.5,
				in_duration: 350,
				out_duration: 250,
				ready: undefined,
				complete: undefined,
				dismissible: true,
				starting_top: '4%',
				ending_top: '10%'
			};
			var $modal = $( this );

			if ( $modal.hasClass( 'open' ) ) {
				return;
			}

			var overlayID = _generateID();
			var $overlay = $( '<div class="lean-overlay"></div>' );
			lStack = (++ _stack);

			// Store a reference of the overlay
			$overlay.attr( 'id', overlayID ).css( 'z-index', 1000 + lStack * 2 );
			$modal.data( 'overlay-id', overlayID ).css( 'z-index', 1000 + lStack * 2 + 1 );
			$modal.addClass( 'open' );

			$( "body" ).append( $overlay );

			// Override defaults
			options = $.extend( defaults, options );

			if ( options.dismissible ) {
				$overlay.click( function() {
					$modal.closeModal( options );
				} );
				// Return on ESC
				$( document ).on( 'keyup.leanModal' + overlayID, function( e ) {
					if ( e.keyCode === 27 ) {   // ESC key
						$modal.closeModal( options );
					}
				} );
			}

			$modal.find( ".modal-close" ).on( 'click.close', function( e ) {
				$modal.closeModal( options );
			} );

			$overlay.css( { display: "block", opacity: 0 } );

			$modal.css( {
				display: "block",
				opacity: 0
			} );

			$overlay.velocity( { opacity: options.opacity }, {
				duration: options.in_duration,
				queue: false,
				ease: "easeOutCubic"
			} );
			$modal.data( 'associated-overlay', $overlay[ 0 ] );

			// Define Bottom Sheet animation
			if ( $modal.hasClass( 'bottom-sheet' ) ) {
				$modal.velocity( { bottom: "0", opacity: 1 }, {
					duration: options.in_duration,
					queue: false,
					ease: "easeOutCubic",
					// Handle modal ready callback
					complete: function() {
						if ( typeof(options.ready) === "function" ) {
							options.ready();
						}
					}
				} );
			}
			else {
				$.Velocity.hook( $modal, "scaleX", 0.7 );
				$modal.css( { top: options.starting_top } );
				$modal.velocity( { top: options.ending_top, opacity: 1, scaleX: '1' }, {
					duration: options.in_duration,
					queue: false,
					ease: "easeOutCubic",
					// Handle modal ready callback
					complete: function() {
						if ( typeof(options.ready) === "function" ) {
							options.ready();
						}
					}
				} );
			}


		}
	} );

	$.fn.extend( {
		closeModal: function( options ) {
			var defaults = {
				out_duration: 250,
				complete: undefined
			};
			var $modal = $( this );
			var overlayID = $modal.data( 'overlay-id' );
			var $overlay = $( '#' + overlayID );
			$modal.removeClass( 'open' );

			options = $.extend( defaults, options );

			// Enable scrolling
			$( 'body' ).css( {
				overflow: '',
				width: ''
			} );

			$modal.find( '.modal-close' ).off( 'click.close' );
			$( document ).off( 'keyup.leanModal' + overlayID );

			$overlay.velocity( { opacity: 0 }, {
				duration: options.out_duration,
				queue: false,
				ease: "easeOutQuart"
			} );


			// Define Bottom Sheet animation
			if ( $modal.hasClass( 'bottom-sheet' ) ) {
				$modal.velocity( { bottom: "-100%", opacity: 0 }, {
					duration: options.out_duration,
					queue: false,
					ease: "easeOutCubic",
					// Handle modal ready callback
					complete: function() {
						$overlay.css( { display: "none" } );

						// Call complete callback
						if ( typeof(options.complete) === "function" ) {
							options.complete();
						}
						$overlay.remove();
						_stack --;
					}
				} );
			}
			else {
				$modal.velocity(
					{ top: options.starting_top, opacity: 0, scaleX: 0.7 }, {
						duration: options.out_duration,
						complete: function() {

							$( this ).css( 'display', 'none' );
							// Call complete callback
							if ( typeof(options.complete) === "function" ) {
								options.complete();
							}
							$overlay.remove();
							_stack --;
						}
					}
				);
			}
		}
	} );

	$.fn.extend( {
		leanModal: function( option ) {
			return this.each( function() {

				var defaults = {
						starting_top: '4%'
					},
					// Override defaults
					options = $.extend( defaults, option );

				// Close Handlers
				$( this ).click( function( e ) {
					options.starting_top = ($( this ).offset().top - $( window ).scrollTop()) / 1.15;
					var modal_id = $( this ).attr( "href" ) || '#' + $( this ).data( 'target' );
					$( modal_id ).openModal( options );
					e.preventDefault();
				} ); // done set on click
			} ); // done return
		}
	} );
})( jQuery );
;(function( $ ) {

	$.fn.materialbox = function() {

		return this.each( function() {

			if ( $( this ).hasClass( 'initialized' ) ) {
				return;
			}

			$( this ).addClass( 'initialized' );

			var overlayActive = false;
			var doneAnimating = true;
			var inDuration = 275;
			var outDuration = 200;
			var origin = $( this );
			var placeholder = $( '<div></div>' ).addClass( 'material-placeholder' );
			var originalWidth = 0;
			var originalHeight = 0;
			var ancestorsChanged;
			var ancestor;
			origin.wrap( placeholder );


			origin.on( 'click', function() {
				var placeholder = origin.parent( '.material-placeholder' );
				var windowWidth = window.innerWidth;
				var windowHeight = window.innerHeight;
				var originalWidth = origin.width();
				var originalHeight = origin.height();


				// If already modal, return to original
				if ( doneAnimating === false ) {
					returnToOriginal();
					return false;
				}
				else {
					if ( overlayActive && doneAnimating === true ) {
						returnToOriginal();
						return false;
					}
				}


				// Set states
				doneAnimating = false;
				origin.addClass( 'active' );
				overlayActive = true;

				// Set positioning for placeholder
				placeholder.css( {
					width: placeholder[ 0 ].getBoundingClientRect().width,
					height: placeholder[ 0 ].getBoundingClientRect().height,
					position: 'relative',
					top: 0,
					left: 0
				} );

				// Find ancestor with overflow: hidden; and remove it
				ancestorsChanged = undefined;
				ancestor = placeholder[ 0 ].parentNode;
				var count = 0;
				while ( ancestor !== null && ! $( ancestor ).is( document ) ) {
					var curr = $( ancestor );
					if ( curr.css( 'overflow' ) !== 'visible' ) {
						curr.css( 'overflow', 'visible' );
						if ( ancestorsChanged === undefined ) {
							ancestorsChanged = curr;
						}
						else {
							ancestorsChanged = ancestorsChanged.add( curr );
						}
					}
					ancestor = ancestor.parentNode;
				}

				// Set css on origin
				origin.css( {
					position: 'absolute',
					'z-index': 1000
				} ).data( 'width', originalWidth ).data( 'height', originalHeight );

				// Add overlay
				var overlay = $( '<div id="materialbox-overlay"></div>' ).css( {
					opacity: 0
				} ).click( function() {
					if ( doneAnimating === true ) {
						returnToOriginal();
					}
				} );
				// Animate Overlay
				// Put before in origin image to preserve z-index layering.
				origin.before( overlay );
				overlay.velocity( { opacity: 1 },
					{ duration: inDuration, queue: false, easing: 'easeOutQuad' } );

				// Add and animate caption if it exists
				if ( origin.data( 'caption' ) !== "" ) {
					var $photo_caption = $( '<div class="materialbox-caption"></div>' );
					$photo_caption.text( origin.data( 'caption' ) );
					$( 'body' ).append( $photo_caption );
					$photo_caption.css( { "display": "inline" } );
					$photo_caption.velocity( { opacity: 1 }, {
						duration: inDuration,
						queue: false,
						easing: 'easeOutQuad'
					} );
				}

				// Resize Image
				var ratio = 0;
				var widthPercent = originalWidth / windowWidth;
				var heightPercent = originalHeight / windowHeight;
				var newWidth = 0;
				var newHeight = 0;

				if ( widthPercent > heightPercent ) {
					ratio = originalHeight / originalWidth;
					newWidth = windowWidth * 0.9;
					newHeight = windowWidth * 0.9 * ratio;
				}
				else {
					ratio = originalWidth / originalHeight;
					newWidth = (windowHeight * 0.9) * ratio;
					newHeight = windowHeight * 0.9;
				}

				// Animate image + set z-index
				if ( origin.hasClass( 'responsive-img' ) ) {
					origin.velocity( { 'max-width': newWidth, 'width': originalWidth }, {
						duration: 0, queue: false,
						complete: function() {
							origin.css( { left: 0, top: 0 } ).velocity(
								{
									height: newHeight,
									width: newWidth,
									left: $( document ).scrollLeft() + windowWidth / 2 - origin.parent( '.material-placeholder' ).offset().left - newWidth / 2,
									top: $( document ).scrollTop() + windowHeight / 2 - origin.parent( '.material-placeholder' ).offset().top - newHeight / 2
								},
								{
									duration: inDuration,
									queue: false,
									easing: 'easeOutQuad',
									complete: function() {
										doneAnimating = true;
									}
								}
							);
						} // End Complete
					} ); // End Velocity
				}
				else {
					origin.css( 'left', 0 ).css( 'top', 0 ).velocity(
						{
							height: newHeight,
							width: newWidth,
							left: $( document ).scrollLeft() + windowWidth / 2 - origin.parent( '.material-placeholder' ).offset().left - newWidth / 2,
							top: $( document ).scrollTop() + windowHeight / 2 - origin.parent( '.material-placeholder' ).offset().top - newHeight / 2
						},
						{
							duration: inDuration,
							queue: false,
							easing: 'easeOutQuad',
							complete: function() {
								doneAnimating = true;
							}
						}
					); // End Velocity
				}

			} ); // End origin on click


			// Return on scroll
			$( window ).scroll( function() {
				if ( overlayActive ) {
					returnToOriginal();
				}
			} );

			// Return on ESC
			$( document ).keyup( function( e ) {

				if ( e.keyCode === 27 && doneAnimating === true ) {   // ESC key
					if ( overlayActive ) {
						returnToOriginal();
					}
				}
			} );


			// This function returns the modaled image to the original spot
			function returnToOriginal() {

				doneAnimating = false;

				var placeholder = origin.parent( '.material-placeholder' );
				var windowWidth = window.innerWidth;
				var windowHeight = window.innerHeight;
				var originalWidth = origin.data( 'width' );
				var originalHeight = origin.data( 'height' );

				origin.velocity( "stop", true );
				$( '#materialbox-overlay' ).velocity( "stop", true );
				$( '.materialbox-caption' ).velocity( "stop", true );


				$( '#materialbox-overlay' ).velocity( { opacity: 0 }, {
					duration: outDuration, // Delay prevents animation overlapping
					queue: false, easing: 'easeOutQuad',
					complete: function() {
						// Remove Overlay
						overlayActive = false;
						$( this ).remove();
					}
				} );

				// Resize Image
				origin.velocity(
					{
						width: originalWidth,
						height: originalHeight,
						left: 0,
						top: 0
					},
					{
						duration: outDuration,
						queue: false, easing: 'easeOutQuad'
					}
				);

				// Remove Caption + reset css settings on image
				$( '.materialbox-caption' ).velocity( { opacity: 0 }, {
					duration: outDuration, // Delay prevents animation overlapping
					queue: false, easing: 'easeOutQuad',
					complete: function() {
						placeholder.css( {
							height: '',
							width: '',
							position: '',
							top: '',
							left: ''
						} );

						origin.css( {
							height: '',
							top: '',
							left: '',
							width: '',
							'max-width': '',
							position: '',
							'z-index': ''
						} );

						// Remove class
						origin.removeClass( 'active' );
						doneAnimating = true;
						$( this ).remove();

						// Remove overflow overrides on ancestors
						if ( ancestorsChanged ) {
							ancestorsChanged.css( 'overflow', '' );
						}
					}
				} );

			}
		} );
	};

	$( document ).ready( function() {
		$( '.materialboxed' ).materialbox();
	} );

}( jQuery ));
;(function( $ ) {

	$.fn.parallax = function() {
		var window_width = $( window ).width();
		// Parallax Scripts
		return this.each( function( i ) {
			var $this = $( this );
			$this.addClass( 'parallax' );

			function updateParallax( initial ) {
				var container_height;
				if ( window_width < 601 ) {
					container_height = ($this.height() > 0) ? $this.height() : $this.children( "img" ).height();
				}
				else {
					container_height = ($this.height() > 0) ? $this.height() : 500;
				}
				var $img = $this.children( "img" ).first();
				var img_height = $img.height();
				var parallax_dist = img_height - container_height;
				var bottom = $this.offset().top + container_height;
				var top = $this.offset().top;
				var scrollTop = $( window ).scrollTop();
				var windowHeight = window.innerHeight;
				var windowBottom = scrollTop + windowHeight;
				var percentScrolled = (windowBottom - top) / (container_height + windowHeight);
				var parallax = Math.round( (parallax_dist * percentScrolled) );

				if ( initial ) {
					$img.css( 'display', 'block' );
				}
				if ( (bottom > scrollTop) && (top < (scrollTop + windowHeight)) ) {
					$img.css( 'transform', "translate3D(-50%," + parallax + "px, 0)" );
				}

			}

			// Wait for image load
			$this.children( "img" ).one( "load", function() {
				updateParallax( true );
			} ).each( function() {
				if ( this.complete ) {
					$( this ).load();
				}
			} );

			$( window ).scroll( function() {
				window_width = $( window ).width();
				updateParallax( false );
			} );

			$( window ).resize( function() {
				window_width = $( window ).width();
				updateParallax( false );
			} );

		} );

	};
}( jQuery ));
;(function( $ ) {

	var methods = {
		init: function( options ) {
			var defaults = {
				onShow: null
			};
			options = $.extend( defaults, options );

			return this.each( function() {

				// For each set of tabs, we want to keep track of
				// which tab is active and its associated content
				var $this = $( this ),
					window_width = $( window ).width();

				$this.width( '100%' );
				var $active, $content, $links = $this.find( 'li.tab a' ),
					$tabs_width = $this.width(),
					$tab_width = Math.max( $tabs_width, $this[ 0 ].scrollWidth ) / $links.length,
					$index = 0;

				// If the location.hash matches one of the links, use that as the active tab.
				$active = $( $links.filter( '[href="' + location.hash + '"]' ) );

				// If no match is found, use the first link or any with class 'active' as the
				// initial active tab.
				if ( $active.length === 0 ) {
					$active = $( this ).find( 'li.tab a.active' ).first();
				}
				if ( $active.length === 0 ) {
					$active = $( this ).find( 'li.tab a' ).first();
				}

				$active.addClass( 'active' );
				$index = $links.index( $active );
				if ( $index < 0 ) {
					$index = 0;
				}

				if ( $active[ 0 ] !== undefined ) {
					$content = $( $active[ 0 ].hash );
				}

				// append indicator then set indicator width to tab width
				$this.append( '<div class="indicator"></div>' );
				var $indicator = $this.find( '.indicator' );
				if ( $this.is( ":visible" ) ) {
					$indicator.css( { "right": $tabs_width - (($index + 1) * $tab_width) } );
					$indicator.css( { "left": $index * $tab_width } );
				}
				$( window ).resize( function() {
					$tabs_width = $this.width();
					$tab_width = Math.max( $tabs_width, $this[ 0 ].scrollWidth ) / $links.length;
					if ( $index < 0 ) {
						$index = 0;
					}
					if ( $tab_width !== 0 && $tabs_width !== 0 ) {
						$indicator.css( { "right": $tabs_width - (($index + 1) * $tab_width) } );
						$indicator.css( { "left": $index * $tab_width } );
					}
				} );

				// Hide the remaining content
				$links.not( $active ).each( function() {
					$( this.hash ).hide();
				} );


				// Bind the click event handler
				$this.on( 'click.materialize', 'a', function( e ) {
					if ( $( this ).parent().hasClass( 'disabled' ) ) {
						e.preventDefault();
						return;
					}

					// Act as regular link if target attribute is specified.
					if ( ! ! $( this ).attr( "target" ) ) {
						return;
					}

					$tabs_width = $this.width();
					$tab_width = Math.max( $tabs_width, $this[ 0 ].scrollWidth ) / $links.length;

					// Make the old tab inactive.
					$active.removeClass( 'active' );
					if ( $content !== undefined ) {
						$content.hide();
					}

					// Update the variables with the new link and content
					$active = $( this );
					$content = $( this.hash );
					$links = $this.find( 'li.tab a' );

					// Make the tab active.
					$active.addClass( 'active' );
					var $prev_index = $index;
					$index = $links.index( $( this ) );
					if ( $index < 0 ) {
						$index = 0;
					}
					// Change url to current tab
					// window.location.hash = $active.attr('href');

					if ( $content !== undefined ) {
						$content.show();
						if ( typeof(options.onShow) === "function" ) {
							options.onShow.call( this, $content );
						}
					}

					// Update indicator
					if ( ($index - $prev_index) >= 0 ) {
						$indicator.velocity( { "right": $tabs_width - (($index + 1) * $tab_width) }, {
							duration: 300,
							queue: false,
							easing: 'easeOutQuad'
						} );
						$indicator.velocity( { "left": $index * $tab_width }, {
							duration: 300,
							queue: false,
							easing: 'easeOutQuad',
							delay: 90
						} );

					}
					else {
						$indicator.velocity( { "left": $index * $tab_width }, {
							duration: 300,
							queue: false,
							easing: 'easeOutQuad'
						} );
						$indicator.velocity( { "right": $tabs_width - (($index + 1) * $tab_width) }, {
							duration: 300,
							queue: false,
							easing: 'easeOutQuad',
							delay: 90
						} );
					}

					// Prevent the anchor's default click action
					e.preventDefault();
				} );
			} );

		},
		select_tab: function( id ) {
			this.find( 'a[href="#' + id + '"]' ).trigger( 'click' );
		}
	};

	$.fn.tabs = function( methodOrOptions ) {
		if ( methods[ methodOrOptions ] ) {
			return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ) );
		} else {
			if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
				// Default to "init"
				return methods.init.apply( this, arguments );
			} else {
				$.error( 'Method ' + methodOrOptions + ' does not exist on jQuery.tooltip' );
			}
		}
	};

	$( document ).ready( function() {
		$( 'ul.tabs' ).tabs();
	} );
}( jQuery ));
;(function( $ ) {
	$.fn.tooltip = function( options ) {
		var timeout = null,
			margin = 5;

		// Defaults
		var defaults = {
			delay: 350,
			tooltip: '',
			position: 'bottom',
			html: false
		};

		// Remove tooltip from the activator
		if ( options === "remove" ) {
			this.each( function() {
				$( '#' + $( this ).attr( 'data-tooltip-id' ) ).remove();
				$( this ).off( 'mouseenter.tooltip mouseleave.tooltip' );
			} );
			return false;
		}

		options = $.extend( defaults, options );

		return this.each( function() {
			var tooltipId = Materialize.guid();
			var origin = $( this );
			origin.attr( 'data-tooltip-id', tooltipId );

			// Get attributes.
			var allowHtml,
				tooltipDelay,
				tooltipPosition,
				tooltipText,
				tooltipEl,
				backdrop;
			var setAttributes = function() {
				allowHtml = origin.attr( 'data-html' ) ? origin.attr( 'data-html' ) === 'true' : options.html;
				tooltipDelay = origin.attr( 'data-delay' );
				tooltipDelay = (tooltipDelay === undefined || tooltipDelay === '') ?
							   options.delay : tooltipDelay;
				tooltipPosition = origin.attr( 'data-position' );
				tooltipPosition = (tooltipPosition === undefined || tooltipPosition === '') ?
								  options.position : tooltipPosition;
				tooltipText = origin.attr( 'data-tooltip' );
				tooltipText = (tooltipText === undefined || tooltipText === '') ?
							  options.tooltip : tooltipText;
			};
			setAttributes();

			var renderTooltipEl = function() {
				var tooltip = $( '<div class="material-tooltip"></div>' );

				// Create Text span
				if ( allowHtml ) {
					tooltipText = $( '<span></span>' ).html( tooltipText );
				} else {
					tooltipText = $( '<span></span>' ).text( tooltipText );
				}

				// Create tooltip
				tooltip.append( tooltipText ).appendTo( $( 'body' ) ).attr( 'id', tooltipId );

				// Create backdrop
				backdrop = $( '<div class="backdrop"></div>' );
				backdrop.appendTo( tooltip );
				return tooltip;
			};
			tooltipEl = renderTooltipEl();

			// Destroy previously binded events
			origin.off( 'mouseenter.tooltip mouseleave.tooltip' );
			// Mouse In
			var started = false, timeoutRef;
			origin.on( {
				'mouseenter.tooltip': function( e ) {
					var showTooltip = function() {
						setAttributes();
						started = true;
						tooltipEl.velocity( 'stop' );
						backdrop.velocity( 'stop' );
						tooltipEl.css( { display: 'block', left: '0px', top: '0px' } );

						// Tooltip positioning
						var originWidth = origin.outerWidth();
						var originHeight = origin.outerHeight();

						var tooltipHeight = tooltipEl.outerHeight();
						var tooltipWidth = tooltipEl.outerWidth();
						var tooltipVerticalMovement = '0px';
						var tooltipHorizontalMovement = '0px';
						var scaleXFactor = 8;
						var scaleYFactor = 8;
						var targetTop, targetLeft, newCoordinates;

						if ( tooltipPosition === "top" ) {
							// Top Position
							targetTop = origin.offset().top - tooltipHeight - margin;
							targetLeft = origin.offset().left + originWidth / 2 - tooltipWidth / 2;
							newCoordinates = repositionWithinScreen( targetLeft, targetTop, tooltipWidth, tooltipHeight );

							tooltipVerticalMovement = '-10px';
							backdrop.css( {
								bottom: 0,
								left: 0,
								borderRadius: '14px 14px 0 0',
								transformOrigin: '50% 100%',
								marginTop: tooltipHeight,
								marginLeft: (tooltipWidth / 2) - (backdrop.width() / 2)
							} );
						}
						// Left Position
						else {
							if ( tooltipPosition === "left" ) {
								targetTop = origin.offset().top + originHeight / 2 - tooltipHeight / 2;
								targetLeft = origin.offset().left - tooltipWidth - margin;
								newCoordinates = repositionWithinScreen( targetLeft, targetTop, tooltipWidth, tooltipHeight );

								tooltipHorizontalMovement = '-10px';
								backdrop.css( {
									top: '-7px',
									right: 0,
									width: '14px',
									height: '14px',
									borderRadius: '14px 0 0 14px',
									transformOrigin: '95% 50%',
									marginTop: tooltipHeight / 2,
									marginLeft: tooltipWidth
								} );
							}
							// Right Position
							else {
								if ( tooltipPosition === "right" ) {
									targetTop = origin.offset().top + originHeight / 2 - tooltipHeight / 2;
									targetLeft = origin.offset().left + originWidth + margin;
									newCoordinates = repositionWithinScreen( targetLeft, targetTop, tooltipWidth, tooltipHeight );

									tooltipHorizontalMovement = '+10px';
									backdrop.css( {
										top: '-7px',
										left: 0,
										width: '14px',
										height: '14px',
										borderRadius: '0 14px 14px 0',
										transformOrigin: '5% 50%',
										marginTop: tooltipHeight / 2,
										marginLeft: '0px'
									} );
								}
								else {
									// Bottom Position
									targetTop = origin.offset().top + origin.outerHeight() + margin;
									targetLeft = origin.offset().left + originWidth / 2 - tooltipWidth / 2;
									newCoordinates = repositionWithinScreen( targetLeft, targetTop, tooltipWidth, tooltipHeight );
									tooltipVerticalMovement = '+10px';
									backdrop.css( {
										top: 0,
										left: 0,
										marginLeft: (tooltipWidth / 2) - (backdrop.width() / 2)
									} );
								}
							}
						}

						// Set tooptip css placement
						tooltipEl.css( {
							top: newCoordinates.y,
							left: newCoordinates.x
						} );

						// Calculate Scale to fill
						scaleXFactor = Math.SQRT2 * tooltipWidth / parseInt( backdrop.css( 'width' ) );
						scaleYFactor = Math.SQRT2 * tooltipHeight / parseInt( backdrop.css( 'height' ) );

						tooltipEl.velocity( {
							marginTop: tooltipVerticalMovement,
							marginLeft: tooltipHorizontalMovement
						}, {
							duration: 350,
							queue: false
						} ).velocity( { opacity: 1 }, { duration: 300, delay: 50, queue: false } );
						backdrop.css( { display: 'block' } ).velocity( { opacity: 1 }, {
							duration: 55,
							delay: 0,
							queue: false
						} ).velocity( {
							scaleX: scaleXFactor,
							scaleY: scaleYFactor
						}, { duration: 300, delay: 0, queue: false, easing: 'easeInOutQuad' } );
					};

					timeoutRef = setTimeout( showTooltip, tooltipDelay ); // End Interval

					// Mouse Out
				},
				'mouseleave.tooltip': function() {
					// Reset State
					started = false;
					clearTimeout( timeoutRef );

					// Animate back
					setTimeout( function() {
						if ( started !== true ) {
							tooltipEl.velocity( {
								opacity: 0, marginTop: 0, marginLeft: 0
							}, { duration: 225, queue: false } );
							backdrop.velocity( { opacity: 0, scaleX: 1, scaleY: 1 }, {
								duration: 225,
								queue: false,
								complete: function() {
									backdrop.css( 'display', 'none' );
									tooltipEl.css( 'display', 'none' );
									started = false;
								}
							} );
						}
					}, 225 );
				}
			} );
		} );
	};

	var repositionWithinScreen = function( x, y, width, height ) {
		var newX = x;
		var newY = y;

		if ( newX < 0 ) {
			newX = 4;
		} else {
			if ( newX + width > window.innerWidth ) {
				newX -= newX + width - window.innerWidth;
			}
		}

		if ( newY < 0 ) {
			newY = 4;
		} else {
			if ( newY + height > window.innerHeight + $( window ).scrollTop ) {
				newY -= newY + height - window.innerHeight;
			}
		}

		return { x: newX, y: newY };
	};

	$( document ).ready( function() {
		$( '.tooltipped' ).tooltip();
	} );
}( jQuery ));
;/*!
 * Waves v0.6.4
 * http://fian.my.id/Waves
 *
 * Copyright 2014 Alfiana E. Sibuea and other contributors
 * Released under the MIT license
 * https://github.com/fians/Waves/blob/master/LICENSE
 */

;(function( window ) {
	'use strict';

	var Waves = Waves || {};
	var $$ = document.querySelectorAll.bind( document );

	// Find exact position of element
	function isWindow( obj ) {
		return obj !== null && obj === obj.window;
	}

	function getWindow( elem ) {
		return isWindow( elem ) ? elem : elem.nodeType === 9 && elem.defaultView;
	}

	function offset( elem ) {
		var docElem, win,
			box = { top: 0, left: 0 },
			doc = elem && elem.ownerDocument;

		docElem = doc.documentElement;

		if ( typeof elem.getBoundingClientRect !== typeof undefined ) {
			box = elem.getBoundingClientRect();
		}
		win = getWindow( doc );
		return {
			top: box.top + win.pageYOffset - docElem.clientTop,
			left: box.left + win.pageXOffset - docElem.clientLeft
		};
	}

	function convertStyle( obj ) {
		var style = '';

		for ( var a in obj ) {
			if ( obj.hasOwnProperty( a ) ) {
				style += (a + ':' + obj[ a ] + ';');
			}
		}

		return style;
	}

	var Effect = {

		// Effect delay
		duration: 750,

		show: function( e, element ) {

			// Disable right click
			if ( e.button === 2 ) {
				return false;
			}

			var el = element || this;

			// Create ripple
			var ripple = document.createElement( 'div' );
			ripple.className = 'waves-ripple';
			el.appendChild( ripple );

			// Get click coordinate and element witdh
			var pos = offset( el );
			var relativeY = (e.pageY - pos.top);
			var relativeX = (e.pageX - pos.left);
			var scale = 'scale(' + ((el.clientWidth / 100) * 10) + ')';

			// Support for touch devices
			if ( 'touches' in e ) {
				relativeY = (e.touches[ 0 ].pageY - pos.top);
				relativeX = (e.touches[ 0 ].pageX - pos.left);
			}

			// Attach data to element
			ripple.setAttribute( 'data-hold', Date.now() );
			ripple.setAttribute( 'data-scale', scale );
			ripple.setAttribute( 'data-x', relativeX );
			ripple.setAttribute( 'data-y', relativeY );

			// Set ripple position
			var rippleStyle = {
				'top': relativeY + 'px',
				'left': relativeX + 'px'
			};

			ripple.className = ripple.className + ' waves-notransition';
			ripple.setAttribute( 'style', convertStyle( rippleStyle ) );
			ripple.className = ripple.className.replace( 'waves-notransition', '' );

			// Scale the ripple
			rippleStyle[ '-webkit-transform' ] = scale;
			rippleStyle[ '-moz-transform' ] = scale;
			rippleStyle[ '-ms-transform' ] = scale;
			rippleStyle[ '-o-transform' ] = scale;
			rippleStyle.transform = scale;
			rippleStyle.opacity = '1';

			rippleStyle[ '-webkit-transition-duration' ] = Effect.duration + 'ms';
			rippleStyle[ '-moz-transition-duration' ] = Effect.duration + 'ms';
			rippleStyle[ '-o-transition-duration' ] = Effect.duration + 'ms';
			rippleStyle[ 'transition-duration' ] = Effect.duration + 'ms';

			rippleStyle[ '-webkit-transition-timing-function' ] = 'cubic-bezier(0.250, 0.460, 0.450, 0.940)';
			rippleStyle[ '-moz-transition-timing-function' ] = 'cubic-bezier(0.250, 0.460, 0.450, 0.940)';
			rippleStyle[ '-o-transition-timing-function' ] = 'cubic-bezier(0.250, 0.460, 0.450, 0.940)';
			rippleStyle[ 'transition-timing-function' ] = 'cubic-bezier(0.250, 0.460, 0.450, 0.940)';

			ripple.setAttribute( 'style', convertStyle( rippleStyle ) );
		},

		hide: function( e ) {
			TouchHandler.touchup( e );

			var el = this;
			var width = el.clientWidth * 1.4;

			// Get first ripple
			var ripple = null;
			var ripples = el.getElementsByClassName( 'waves-ripple' );
			if ( ripples.length > 0 ) {
				ripple = ripples[ ripples.length - 1 ];
			} else {
				return false;
			}

			var relativeX = ripple.getAttribute( 'data-x' );
			var relativeY = ripple.getAttribute( 'data-y' );
			var scale = ripple.getAttribute( 'data-scale' );

			// Get delay beetween mousedown and mouse leave
			var diff = Date.now() - Number( ripple.getAttribute( 'data-hold' ) );
			var delay = 350 - diff;

			if ( delay < 0 ) {
				delay = 0;
			}

			// Fade out ripple after delay
			setTimeout( function() {
				var style = {
					'top': relativeY + 'px',
					'left': relativeX + 'px',
					'opacity': '0',

					// Duration
					'-webkit-transition-duration': Effect.duration + 'ms',
					'-moz-transition-duration': Effect.duration + 'ms',
					'-o-transition-duration': Effect.duration + 'ms',
					'transition-duration': Effect.duration + 'ms',
					'-webkit-transform': scale,
					'-moz-transform': scale,
					'-ms-transform': scale,
					'-o-transform': scale,
					'transform': scale,
				};

				ripple.setAttribute( 'style', convertStyle( style ) );

				setTimeout( function() {
					try {
						el.removeChild( ripple );
					} catch ( e ) {
						return false;
					}
				}, Effect.duration );
			}, delay );
		},

		// Little hack to make <input> can perform waves effect
		wrapInput: function( elements ) {
			for ( var a = 0; a < elements.length; a ++ ) {
				var el = elements[ a ];

				if ( el.tagName.toLowerCase() === 'input' ) {
					var parent = el.parentNode;

					// If input already have parent just pass through
					if ( parent.tagName.toLowerCase() === 'i' && parent.className.indexOf( 'waves-effect' ) !== - 1 ) {
						continue;
					}

					// Put element class and style to the specified parent
					var wrapper = document.createElement( 'i' );
					wrapper.className = el.className + ' waves-input-wrapper';

					var elementStyle = el.getAttribute( 'style' );

					if ( ! elementStyle ) {
						elementStyle = '';
					}

					wrapper.setAttribute( 'style', elementStyle );

					el.className = 'waves-button-input';
					el.removeAttribute( 'style' );

					// Put element as child
					parent.replaceChild( wrapper, el );
					wrapper.appendChild( el );
				}
			}
		}
	};


	/**
	 * Disable mousedown event for 500ms during and after touch
	 */
	var TouchHandler = {
		/* uses an integer rather than bool so there's no issues with
		 * needing to clear timeouts if another touch event occurred
		 * within the 500ms. Cannot mouseup between touchstart and
		 * touchend, nor in the 500ms after touchend. */
		touches: 0,
		allowEvent: function( e ) {
			var allow = true;

			if ( e.type === 'touchstart' ) {
				TouchHandler.touches += 1; //push
			} else {
				if ( e.type === 'touchend' || e.type === 'touchcancel' ) {
					setTimeout( function() {
						if ( TouchHandler.touches > 0 ) {
							TouchHandler.touches -= 1; //pop after 500ms
						}
					}, 500 );
				} else {
					if ( e.type === 'mousedown' && TouchHandler.touches > 0 ) {
						allow = false;
					}
				}
			}

			return allow;
		},
		touchup: function( e ) {
			TouchHandler.allowEvent( e );
		}
	};


	/**
	 * Delegated click handler for .waves-effect element.
	 * returns null when .waves-effect element not in "click tree"
	 */
	function getWavesEffectElement( e ) {
		if ( TouchHandler.allowEvent( e ) === false ) {
			return null;
		}

		var element = null;
		var target = e.target || e.srcElement;

		while ( target.parentElement !== null ) {
			if ( ! (target instanceof SVGElement) && target.className.indexOf( 'waves-effect' ) !== - 1 ) {
				element = target;
				break;
			} else {
				if ( target.classList.contains( 'waves-effect' ) ) {
					element = target;
					break;
				}
			}
			target = target.parentElement;
		}

		return element;
	}

	/**
	 * Bubble the click and show effect if .waves-effect elem was found
	 */
	function showEffect( e ) {
		var element = getWavesEffectElement( e );

		if ( element !== null ) {
			Effect.show( e, element );

			if ( 'ontouchstart' in window ) {
				element.addEventListener( 'touchend', Effect.hide, false );
				element.addEventListener( 'touchcancel', Effect.hide, false );
			}

			element.addEventListener( 'mouseup', Effect.hide, false );
			element.addEventListener( 'mouseleave', Effect.hide, false );
		}
	}

	Waves.displayEffect = function( options ) {
		options = options || {};

		if ( 'duration' in options ) {
			Effect.duration = options.duration;
		}

		//Wrap input inside <i> tag
		Effect.wrapInput( $$( '.waves-effect' ) );

		if ( 'ontouchstart' in window ) {
			document.body.addEventListener( 'touchstart', showEffect, false );
		}

		document.body.addEventListener( 'mousedown', showEffect, false );
	};

	/**
	 * Attach Waves to an input element (or any element which doesn't
	 * bubble mouseup/mousedown events).
	 *   Intended to be used with dynamically loaded forms/inputs, or
	 * where the user doesn't want a delegated click handler.
	 */
	Waves.attach = function( element ) {
		//FUTURE: automatically add waves classes and allow users
		// to specify them with an options param? Eg. light/classic/button
		if ( element.tagName.toLowerCase() === 'input' ) {
			Effect.wrapInput( [ element ] );
			element = element.parentElement;
		}

		if ( 'ontouchstart' in window ) {
			element.addEventListener( 'touchstart', showEffect, false );
		}

		element.addEventListener( 'mousedown', showEffect, false );
	};

	window.Waves = Waves;

	document.addEventListener( 'DOMContentLoaded', function() {
		Waves.displayEffect();
	}, false );

})( window );
;Materialize.toast = function( message, displayLength, className, completeCallback ) {
	className = className || "";

	var container = document.getElementById( 'toast-container' );

	// Create toast container if it does not exist
	if ( container === null ) {
		// create notification container
		container = document.createElement( 'div' );
		container.id = 'toast-container';
		document.body.appendChild( container );
	}

	// Select and append toast
	var newToast = createToast( message );

	// only append toast if message is not undefined
	if ( message ) {
		container.appendChild( newToast );
	}

	newToast.style.top = '35px';
	newToast.style.opacity = 0;

	// Animate toast in
	Vel( newToast, { "top": "0px", opacity: 1 }, {
		duration: 300,
		easing: 'easeOutCubic',
		queue: false
	} );

	// Allows timer to be pause while being panned
	var timeLeft = displayLength;
	var counterInterval = setInterval( function() {


		if ( newToast.parentNode === null ) {
			window.clearInterval( counterInterval );
		}

		// If toast is not being dragged, decrease its time remaining
		if ( ! newToast.classList.contains( 'panning' ) ) {
			timeLeft -= 20;
		}

		if ( timeLeft <= 0 ) {
			// Animate toast out
			Vel( newToast, { "opacity": 0, marginTop: '-40px' }, {
				duration: 375,
				easing: 'easeOutExpo',
				queue: false,
				complete: function() {
					// Call the optional callback
					if ( typeof(completeCallback) === "function" ) {
						completeCallback();
					}
					// Remove toast after it times out
					this[ 0 ].parentNode.removeChild( this[ 0 ] );
				}
			} );
			window.clearInterval( counterInterval );
		}
	}, 20 );



	function createToast( html ) {

		// Create toast
		var toast = document.createElement( 'div' );
		toast.classList.add( 'toast' );
		if ( className ) {
			var classes = className.split( ' ' );

			for ( var i = 0, count = classes.length; i < count; i ++ ) {
				toast.classList.add( classes[ i ] );
			}
		}
		// If type of parameter is HTML Element
		if ( typeof HTMLElement === "object" ? html instanceof HTMLElement : html && typeof html === "object" && html !== null && html.nodeType === 1 && typeof html.nodeName === "string"
		) {
			toast.appendChild( html );
		}
		else {
			if ( html instanceof jQuery ) {
				// Check if it is jQuery object
				toast.appendChild( html[ 0 ] );
			}
			else {
				// Insert as text;
				toast.innerHTML = html;
			}
		}
		// Bind hammer
		var hammerHandler = new Hammer( toast, { prevent_default: false } );
		hammerHandler.on( 'pan', function( e ) {
			var deltaX = e.deltaX;
			var activationDistance = 80;

			// Change toast state
			if ( ! toast.classList.contains( 'panning' ) ) {
				toast.classList.add( 'panning' );
			}

			var opacityPercent = 1 - Math.abs( deltaX / activationDistance );
			if ( opacityPercent < 0 ) {
				opacityPercent = 0;
			}

			Vel( toast, { left: deltaX, opacity: opacityPercent }, {
				duration: 50,
				queue: false,
				easing: 'easeOutQuad'
			} );

		} );

		hammerHandler.on( 'panend', function( e ) {
			var deltaX = e.deltaX;
			var activationDistance = 80;

			// If toast dragged past activation point
			if ( Math.abs( deltaX ) > activationDistance ) {
				Vel( toast, { marginTop: '-40px' }, {
					duration: 375,
					easing: 'easeOutExpo',
					queue: false,
					complete: function() {
						if ( typeof(completeCallback) === "function" ) {
							completeCallback();
						}
						toast.parentNode.removeChild( toast );
					}
				} );

			} else {
				toast.classList.remove( 'panning' );
				// Put toast back into original position
				Vel( toast, { left: 0, opacity: 1 }, {
					duration: 300,
					easing: 'easeOutExpo',
					queue: false
				} );

			}
		} );

		return toast;
	}
};
;(function( $ ) {

	var methods = {
		init: function( options ) {
			var defaults = {
				menuWidth: 300,
				edge: 'left',
				closeOnClick: false
			};
			options = $.extend( defaults, options );

			$( this ).each( function() {
				var $this = $( this );
				var menu_id = $( "#" + $this.attr( 'data-activates' ) );

				// Set to width
				if ( options.menuWidth != 300 ) {
					menu_id.css( 'width', options.menuWidth );
				}

				// Add Touch Area
				var dragTarget = $( '<div class="drag-target"></div>' );
				$( 'body' ).append( dragTarget );

				if ( options.edge == 'left' ) {
					menu_id.css( 'transform', 'translateX(-100%)' );
					dragTarget.css( { 'left': 0 } ); // Add Touch Area
				}
				else {
					menu_id.addClass( 'right-aligned' ) // Change text-alignment to right
						.css( 'transform', 'translateX(100%)' );
					dragTarget.css( { 'right': 0 } ); // Add Touch Area
				}

				// If fixed sidenav, bring menu out
				if ( menu_id.hasClass( 'fixed' ) ) {
					if ( window.innerWidth > 992 ) {
						menu_id.css( 'transform', 'translateX(0)' );
					}
				}

				// Window resize to reset on large screens fixed
				if ( menu_id.hasClass( 'fixed' ) ) {
					$( window ).resize( function() {
						if ( window.innerWidth > 992 ) {
							// Close menu if window is resized bigger than 992 and user has fixed
							// sidenav
							if ( $( '#sidenav-overlay' ).length !== 0 && menuOut ) {
								removeMenu( true );
							}
							else {
								// menu_id.removeAttr('style');
								menu_id.css( 'transform', 'translateX(0%)' );
								// menu_id.css('width', options.menuWidth);
							}
						}
						else {
							if ( menuOut === false ) {
								if ( options.edge === 'left' ) {
									menu_id.css( 'transform', 'translateX(-100%)' );
								} else {
									menu_id.css( 'transform', 'translateX(100%)' );
								}

							}
						}

					} );
				}

				// if closeOnClick, then add close event for all a tags in side sideNav
				if ( options.closeOnClick === true ) {
					menu_id.on( "click.itemclick", "a:not(.collapsible-header)", function() {
						removeMenu();
					} );
				}

				function removeMenu( restoreNav ) {
					panning = false;
					menuOut = false;
					// Reenable scrolling
					$( 'body' ).css( {
						overflow: '',
						width: ''
					} );

					$( '#sidenav-overlay' ).velocity( { opacity: 0 }, {
						duration: 200,
						queue: false, easing: 'easeOutQuad',
						complete: function() {
							$( this ).remove();
						}
					} );
					if ( options.edge === 'left' ) {
						// Reset phantom div
						dragTarget.css( { width: '', right: '', left: '0' } );
						menu_id.velocity(
							{ 'translateX': '-100%' },
							{
								duration: 200,
								queue: false,
								easing: 'easeOutCubic',
								complete: function() {
									if ( restoreNav === true ) {
										// Restore Fixed sidenav
										menu_id.removeAttr( 'style' );
										menu_id.css( 'width', options.menuWidth );
									}
								}

							} );
					}
					else {
						// Reset phantom div
						dragTarget.css( { width: '', right: '0', left: '' } );
						menu_id.velocity(
							{ 'translateX': '100%' },
							{
								duration: 200,
								queue: false,
								easing: 'easeOutCubic',
								complete: function() {
									if ( restoreNav === true ) {
										// Restore Fixed sidenav
										menu_id.removeAttr( 'style' );
										menu_id.css( 'width', options.menuWidth );
									}
								}
							} );
					}
				}



				// Touch Event
				var panning = false;
				var menuOut = false;

				dragTarget.on( 'click', function() {
					if ( menuOut ) {
						removeMenu();
					}
				} );

				dragTarget.hammer( {
					prevent_default: false
				} ).bind( 'pan', function( e ) {

					if ( e.gesture.pointerType == "touch" ) {

						var direction = e.gesture.direction;
						var x = e.gesture.center.x;
						var y = e.gesture.center.y;
						var velocityX = e.gesture.velocityX;

						// Disable Scrolling
						var $body = $( 'body' );
						var oldWidth = $body.innerWidth();
						$body.css( 'overflow', 'hidden' );
						$body.width( oldWidth );

						// If overlay does not exist, create one and if it is clicked, close menu
						if ( $( '#sidenav-overlay' ).length === 0 ) {
							var overlay = $( '<div id="sidenav-overlay"></div>' );
							overlay.css( 'opacity', 0 ).click( function() {
								removeMenu();
							} );
							$( 'body' ).append( overlay );
						}

						// Keep within boundaries
						if ( options.edge === 'left' ) {
							if ( x > options.menuWidth ) {
								x = options.menuWidth;
							}
							else {
								if ( x < 0 ) {
									x = 0;
								}
							}
						}

						if ( options.edge === 'left' ) {
							// Left Direction
							if ( x < (options.menuWidth / 2) ) {
								menuOut = false;
							}
							// Right Direction
							else {
								if ( x >= (options.menuWidth / 2) ) {
									menuOut = true;
								}
							}
							menu_id.css( 'transform', 'translateX(' + (x - options.menuWidth) + 'px)' );
						}
						else {
							// Left Direction
							if ( x < (window.innerWidth - options.menuWidth / 2) ) {
								menuOut = true;
							}
							// Right Direction
							else {
								if ( x >= (window.innerWidth - options.menuWidth / 2) ) {
									menuOut = false;
								}
							}
							var rightPos = (x - options.menuWidth / 2);
							if ( rightPos < 0 ) {
								rightPos = 0;
							}

							menu_id.css( 'transform', 'translateX(' + rightPos + 'px)' );
						}


						// Percentage overlay
						var overlayPerc;
						if ( options.edge === 'left' ) {
							overlayPerc = x / options.menuWidth;
							$( '#sidenav-overlay' ).velocity( { opacity: overlayPerc }, {
								duration: 10,
								queue: false,
								easing: 'easeOutQuad'
							} );
						}
						else {
							overlayPerc = Math.abs( (x - window.innerWidth) / options.menuWidth );
							$( '#sidenav-overlay' ).velocity( { opacity: overlayPerc }, {
								duration: 10,
								queue: false,
								easing: 'easeOutQuad'
							} );
						}
					}

				} ).bind( 'panend', function( e ) {

					if ( e.gesture.pointerType == "touch" ) {
						var velocityX = e.gesture.velocityX;
						var x = e.gesture.center.x;
						var leftPos = x - options.menuWidth;
						var rightPos = x - options.menuWidth / 2;
						if ( leftPos > 0 ) {
							leftPos = 0;
						}
						if ( rightPos < 0 ) {
							rightPos = 0;
						}
						panning = false;

						if ( options.edge === 'left' ) {
							// If velocityX <= 0.3 then the user is flinging the menu closed so
							// ignore menuOut
							if ( (menuOut && velocityX <= 0.3) || velocityX < - 0.5 ) {
								// Return menu to open
								if ( leftPos !== 0 ) {
									menu_id.velocity( { 'translateX': [ 0, leftPos ] }, {
										duration: 300,
										queue: false,
										easing: 'easeOutQuad'
									} );
								}

								$( '#sidenav-overlay' ).velocity( { opacity: 1 }, {
									duration: 50,
									queue: false,
									easing: 'easeOutQuad'
								} );
								dragTarget.css( { width: '50%', right: 0, left: '' } );
								menuOut = true;
							}
							else {
								if ( ! menuOut || velocityX > 0.3 ) {
									// Enable Scrolling
									$( 'body' ).css( {
										overflow: '',
										width: ''
									} );
									// Slide menu closed
									menu_id.velocity( { 'translateX': [ - 1 * options.menuWidth - 10, leftPos ] }, {
										duration: 200,
										queue: false,
										easing: 'easeOutQuad'
									} );
									$( '#sidenav-overlay' ).velocity( { opacity: 0 }, {
										duration: 200, queue: false, easing: 'easeOutQuad',
										complete: function() {
											$( this ).remove();
										}
									} );
									dragTarget.css( { width: '10px', right: '', left: 0 } );
								}
							}
						}
						else {
							if ( (menuOut && velocityX >= - 0.3) || velocityX > 0.5 ) {
								// Return menu to open
								if ( rightPos !== 0 ) {
									menu_id.velocity( { 'translateX': [ 0, rightPos ] }, {
										duration: 300,
										queue: false,
										easing: 'easeOutQuad'
									} );
								}

								$( '#sidenav-overlay' ).velocity( { opacity: 1 }, {
									duration: 50,
									queue: false,
									easing: 'easeOutQuad'
								} );
								dragTarget.css( { width: '50%', right: '', left: 0 } );
								menuOut = true;
							}
							else {
								if ( ! menuOut || velocityX < - 0.3 ) {
									// Enable Scrolling
									$( 'body' ).css( {
										overflow: '',
										width: ''
									} );

									// Slide menu closed
									menu_id.velocity( { 'translateX': [ options.menuWidth + 10, rightPos ] }, {
										duration: 200,
										queue: false,
										easing: 'easeOutQuad'
									} );
									$( '#sidenav-overlay' ).velocity( { opacity: 0 }, {
										duration: 200, queue: false, easing: 'easeOutQuad',
										complete: function() {
											$( this ).remove();
										}
									} );
									dragTarget.css( { width: '10px', right: 0, left: '' } );
								}
							}
						}

					}
				} );

				$this.click( function() {
					if ( menuOut === true ) {
						menuOut = false;
						panning = false;
						removeMenu();
					}
					else {

						// Disable Scrolling
						var $body = $( 'body' );
						var oldWidth = $body.innerWidth();
						$body.css( 'overflow', 'hidden' );
						$body.width( oldWidth );

						// Push current drag target on top of DOM tree
						$( 'body' ).append( dragTarget );

						if ( options.edge === 'left' ) {
							dragTarget.css( { width: '50%', right: 0, left: '' } );
							menu_id.velocity( { 'translateX': [ 0, - 1 * options.menuWidth ] }, {
								duration: 300,
								queue: false,
								easing: 'easeOutQuad'
							} );
						}
						else {
							dragTarget.css( { width: '50%', right: '', left: 0 } );
							menu_id.velocity( { 'translateX': [ 0, options.menuWidth ] }, {
								duration: 300,
								queue: false,
								easing: 'easeOutQuad'
							} );
						}

						var overlay = $( '<div id="sidenav-overlay"></div>' );
						overlay.css( 'opacity', 0 ).click( function() {
							menuOut = false;
							panning = false;
							removeMenu();
							overlay.velocity( { opacity: 0 }, {
								duration: 300, queue: false, easing: 'easeOutQuad',
								complete: function() {
									$( this ).remove();
								}
							} );

						} );
						$( 'body' ).append( overlay );
						overlay.velocity( { opacity: 1 }, {
							duration: 300, queue: false, easing: 'easeOutQuad',
							complete: function() {
								menuOut = true;
								panning = false;
							}
						} );
					}

					return false;
				} );
			} );


		},
		show: function() {
			this.trigger( 'click' );
		},
		hide: function() {
			$( '#sidenav-overlay' ).trigger( 'click' );
		}
	};


	$.fn.sideNav = function( methodOrOptions ) {
		if ( methods[ methodOrOptions ] ) {
			return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ) );
		} else {
			if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
				// Default to "init"
				return methods.init.apply( this, arguments );
			} else {
				$.error( 'Method ' + methodOrOptions + ' does not exist on jQuery.sideNav' );
			}
		}
	}; // Plugin end
}( jQuery ));
;/**
 * Extend jquery with a scrollspy plugin.
 * This watches the window scroll and fires events when elements are scrolled into viewport.
 *
 * throttle() and getTime() taken from Underscore.js
 * https://github.com/jashkenas/underscore
 *
 * @author Copyright 2013 John Smart
 * @license https://raw.github.com/thesmart/jquery-scrollspy/master/LICENSE
 * @see https://github.com/thesmart
 * @version 0.1.2
 */
(function( $ ) {

	var jWindow = $( window );
	var elements = [];
	var elementsInView = [];
	var isSpying = false;
	var ticks = 0;
	var unique_id = 1;
	var offset = {
		top: 0,
		right: 0,
		bottom: 0,
		left: 0,
	}

	/**
	 * Find elements that are within the boundary
	 * @param {number} top
	 * @param {number} right
	 * @param {number} bottom
	 * @param {number} left
	 * @return {jQuery}        A collection of elements
	 */
	function findElements( top, right, bottom, left ) {
		var hits = $();
		$.each( elements, function( i, element ) {
			if ( element.height() > 0 ) {
				var elTop = element.offset().top,
					elLeft = element.offset().left,
					elRight = elLeft + element.width(),
					elBottom = elTop + element.height();

				var isIntersect = ! (elLeft > right ||
				elRight < left ||
				elTop > bottom ||
				elBottom < top);

				if ( isIntersect ) {
					hits.push( element );
				}
			}
		} );

		return hits;
	}


	/**
	 * Called when the user scrolls the window
	 */
	function onScroll() {
		// unique tick id
		++ ticks;

		// viewport rectangle
		var top = jWindow.scrollTop(),
			left = jWindow.scrollLeft(),
			right = left + jWindow.width(),
			bottom = top + jWindow.height();

		// determine which elements are in view
		//        + 60 accounts for fixed nav
		var intersections = findElements( top + offset.top + 200, right + offset.right, bottom + offset.bottom, left + offset.left );
		$.each( intersections, function( i, element ) {

			var lastTick = element.data( 'scrollSpy:ticks' );
			if ( typeof lastTick != 'number' ) {
				// entered into view
				element.triggerHandler( 'scrollSpy:enter' );
			}

			// update tick id
			element.data( 'scrollSpy:ticks', ticks );
		} );

		// determine which elements are no longer in view
		$.each( elementsInView, function( i, element ) {
			var lastTick = element.data( 'scrollSpy:ticks' );
			if ( typeof lastTick == 'number' && lastTick !== ticks ) {
				// exited from view
				element.triggerHandler( 'scrollSpy:exit' );
				element.data( 'scrollSpy:ticks', null );
			}
		} );

		// remember elements in view for next tick
		elementsInView = intersections;
	}

	/**
	 * Called when window is resized
	 */
	function onWinSize() {
		jWindow.trigger( 'scrollSpy:winSize' );
	}

	/**
	 * Get time in ms
	 * @license https://raw.github.com/jashkenas/underscore/master/LICENSE
	 * @type {function}
	 * @return {number}
	 */
	var getTime = (Date.now || function() {
		return new Date().getTime();
	});

	/**
	 * Returns a function, that, when invoked, will only be triggered at most once
	 * during a given window of time. Normally, the throttled function will run
	 * as much as it can, without ever going more than once per `wait` duration;
	 * but if you'd like to disable the execution on the leading edge, pass
	 * `{leading: false}`. To disable execution on the trailing edge, ditto.
	 * @license https://raw.github.com/jashkenas/underscore/master/LICENSE
	 * @param {function} func
	 * @param {number} wait
	 * @param {Object=} options
	 * @returns {Function}
	 */
	function throttle( func, wait, options ) {
		var context, args, result;
		var timeout = null;
		var previous = 0;
		options || (options = {});
		var later = function() {
			previous = options.leading === false ? 0 : getTime();
			timeout = null;
			result = func.apply( context, args );
			context = args = null;
		};
		return function() {
			var now = getTime();
			if ( ! previous && options.leading === false ) {
				previous = now;
			}
			var remaining = wait - (now - previous);
			context = this;
			args = arguments;
			if ( remaining <= 0 ) {
				clearTimeout( timeout );
				timeout = null;
				previous = now;
				result = func.apply( context, args );
				context = args = null;
			} else {
				if ( ! timeout && options.trailing !== false ) {
					timeout = setTimeout( later, remaining );
				}
			}
			return result;
		};
	};

	/**
	 * Enables ScrollSpy using a selector
	 * @param {jQuery|string} selector  The elements collection, or a selector
	 * @param {Object=} options    Optional.
	 throttle : number -> scrollspy throttling. Default: 100 ms
	 offsetTop : number -> offset from top. Default: 0
	 offsetRight : number -> offset from right. Default: 0
	 offsetBottom : number -> offset from bottom. Default: 0
	 offsetLeft : number -> offset from left. Default: 0
	 * @returns {jQuery}
	 */
	$.scrollSpy = function( selector, options ) {
		var defaults = {
			throttle: 100,
			scrollOffset: 200 // offset - 200 allows elements near bottom of page to scroll
		};
		options = $.extend( defaults, options );

		var visible = [];
		selector = $( selector );
		selector.each( function( i, element ) {
			elements.push( $( element ) );
			$( element ).data( "scrollSpy:id", i );
			// Smooth scroll to section
			$( 'a[href="#' + $( element ).attr( 'id' ) + '"]' ).click( function( e ) {
				e.preventDefault();
				var offset = $( this.hash ).offset().top + 1;
				$( 'html, body' ).animate( { scrollTop: offset - options.scrollOffset }, {
					duration: 400,
					queue: false,
					easing: 'easeOutCubic'
				} );
			} );
		} );

		offset.top = options.offsetTop || 0;
		offset.right = options.offsetRight || 0;
		offset.bottom = options.offsetBottom || 0;
		offset.left = options.offsetLeft || 0;

		var throttledScroll = throttle( onScroll, options.throttle || 100 );
		var readyScroll = function() {
			$( document ).ready( throttledScroll );
		};

		if ( ! isSpying ) {
			jWindow.on( 'scroll', readyScroll );
			jWindow.on( 'resize', readyScroll );
			isSpying = true;
		}

		// perform a scan once, after current execution context, and after dom is ready
		setTimeout( readyScroll, 0 );


		selector.on( 'scrollSpy:enter', function() {
			visible = $.grep( visible, function( value ) {
				return value.height() != 0;
			} );

			var $this = $( this );

			if ( visible[ 0 ] ) {
				$( 'a[href="#' + visible[ 0 ].attr( 'id' ) + '"]' ).removeClass( 'active' );
				if ( $this.data( 'scrollSpy:id' ) < visible[ 0 ].data( 'scrollSpy:id' ) ) {
					visible.unshift( $( this ) );
				}
				else {
					visible.push( $( this ) );
				}
			}
			else {
				visible.push( $( this ) );
			}


			$( 'a[href="#' + visible[ 0 ].attr( 'id' ) + '"]' ).addClass( 'active' );
		} );
		selector.on( 'scrollSpy:exit', function() {
			visible = $.grep( visible, function( value ) {
				return value.height() != 0;
			} );

			if ( visible[ 0 ] ) {
				$( 'a[href="#' + visible[ 0 ].attr( 'id' ) + '"]' ).removeClass( 'active' );
				var $this = $( this );
				visible = $.grep( visible, function( value ) {
					return value.attr( 'id' ) != $this.attr( 'id' );
				} );
				if ( visible[ 0 ] ) { // Check if empty
					$( 'a[href="#' + visible[ 0 ].attr( 'id' ) + '"]' ).addClass( 'active' );
				}
			}
		} );

		return selector;
	};

	/**
	 * Listen for window resize events
	 * @param {Object=} options                        Optional. Set { throttle: number } to
	 *     change throttling. Default: 100 ms
	 * @returns {jQuery}        $(window)
	 */
	$.winSizeSpy = function( options ) {
		$.winSizeSpy = function() {
			return jWindow;
		}; // lock from multiple calls
		options = options || {
				throttle: 100
			};
		return jWindow.on( 'resize', throttle( onWinSize, options.throttle || 100 ) );
	};

	/**
	 * Enables ScrollSpy on a collection of elements
	 * e.g. $('.scrollSpy').scrollSpy()
	 * @param {Object=} options    Optional.
	 throttle : number -> scrollspy throttling. Default: 100 ms
	 offsetTop : number -> offset from top. Default: 0
	 offsetRight : number -> offset from right. Default: 0
	 offsetBottom : number -> offset from bottom. Default: 0
	 offsetLeft : number -> offset from left. Default: 0
	 * @returns {jQuery}
	 */
	$.fn.scrollSpy = function( options ) {
		return $.scrollSpy( $( this ), options );
	};

})( jQuery );
;(function( $ ) {
	$( document ).ready( function() {

		// Function to update labels of text fields
		Materialize.updateTextFields = function() {
			var input_selector = 'input[type=text], input[type=password], input[type=email], input[type=url], input[type=tel], input[type=number], input[type=search], textarea';
			$( input_selector ).each( function( index, element ) {
				if ( $( element ).val().length > 0 || element.autofocus || $( this ).attr( 'placeholder' ) !== undefined || $( element )[ 0 ].validity.badInput === true ) {
					$( this ).siblings( 'label' ).addClass( 'active' );
				}
				else {
					$( this ).siblings( 'label' ).removeClass( 'active' );
				}
			} );
		};

		// Text based inputs
		var input_selector = 'input[type=text], input[type=password], input[type=email], input[type=url], input[type=tel], input[type=number], input[type=search], textarea';

		// Add active if form auto complete
		$( document ).on( 'change', input_selector, function() {
			if ( $( this ).val().length !== 0 || $( this ).attr( 'placeholder' ) !== undefined ) {
				$( this ).siblings( 'label' ).addClass( 'active' );
			}
			validate_field( $( this ) );
		} );

		// Add active if input element has been pre-populated on document ready
		$( document ).ready( function() {
			Materialize.updateTextFields();
		} );

		// HTML DOM FORM RESET handling
		$( document ).on( 'reset', function( e ) {
			var formReset = $( e.target );
			if ( formReset.is( 'form' ) ) {
				formReset.find( input_selector ).removeClass( 'valid' ).removeClass( 'invalid' );
				formReset.find( input_selector ).each( function() {
					if ( $( this ).attr( 'value' ) === '' ) {
						$( this ).siblings( 'label' ).removeClass( 'active' );
					}
				} );

				// Reset select
				formReset.find( 'select.initialized' ).each( function() {
					var reset_text = formReset.find( 'option[selected]' ).text();
					formReset.siblings( 'input.select-dropdown' ).val( reset_text );
				} );
			}
		} );

		// Add active when element has focus
		$( document ).on( 'focus', input_selector, function() {
			$( this ).siblings( 'label, .prefix' ).addClass( 'active' );
		} );

		$( document ).on( 'blur', input_selector, function() {
			var $inputElement = $( this );
			var selector = ".prefix";

			if ( $inputElement.val().length === 0 && $inputElement[ 0 ].validity.badInput !== true && $inputElement.attr( 'placeholder' ) === undefined ) {
				selector += ", label";
			}

			$inputElement.siblings( selector ).removeClass( 'active' );

			validate_field( $inputElement );
		} );

		window.validate_field = function( object ) {
			var hasLength = object.attr( 'length' ) !== undefined;
			var lenAttr = parseInt( object.attr( 'length' ) );
			var len = object.val().length;

			if ( object.val().length === 0 && object[ 0 ].validity.badInput === false ) {
				if ( object.hasClass( 'validate' ) ) {
					object.removeClass( 'valid' );
					object.removeClass( 'invalid' );
				}
			}
			else {
				if ( object.hasClass( 'validate' ) ) {
					// Check for character counter attributes
					if ( (object.is( ':valid' ) && hasLength && (len <= lenAttr)) || (object.is( ':valid' ) && ! hasLength) ) {
						object.removeClass( 'invalid' );
						object.addClass( 'valid' );
					}
					else {
						object.removeClass( 'valid' );
						object.addClass( 'invalid' );
					}
				}
			}
		};

		// Radio and Checkbox focus class
		var radio_checkbox = 'input[type=radio], input[type=checkbox]';
		$( document ).on( 'keyup.radio', radio_checkbox, function( e ) {
			// TAB, check if tabbing to radio or checkbox.
			if ( e.which === 9 ) {
				$( this ).addClass( 'tabbed' );
				var $this = $( this );
				$this.one( 'blur', function( e ) {

					$( this ).removeClass( 'tabbed' );
				} );
				return;
			}
		} );

		// Textarea Auto Resize
		var hiddenDiv = $( '.hiddendiv' ).first();
		if ( ! hiddenDiv.length ) {
			hiddenDiv = $( '<div class="hiddendiv common"></div>' );
			$( 'body' ).append( hiddenDiv );
		}
		var text_area_selector = '.materialize-textarea';

		function textareaAutoResize( $textarea ) {
			// Set font properties of hiddenDiv

			var fontFamily = $textarea.css( 'font-family' );
			var fontSize = $textarea.css( 'font-size' );
			var lineHeight = $textarea.css( 'line-height' );

			if ( fontSize ) {
				hiddenDiv.css( 'font-size', fontSize );
			}
			if ( fontFamily ) {
				hiddenDiv.css( 'font-family', fontFamily );
			}
			if ( lineHeight ) {
				hiddenDiv.css( 'line-height', lineHeight );
			}

			if ( $textarea.attr( 'wrap' ) === "off" ) {
				hiddenDiv.css( 'overflow-wrap', "normal" ).css( 'white-space', "pre" );
			}

			hiddenDiv.text( $textarea.val() + '\n' );
			var content = hiddenDiv.html().replace( /\n/g, '<br>' );
			hiddenDiv.html( content );


			// When textarea is hidden, width goes crazy.
			// Approximate with half of window size

			if ( $textarea.is( ':visible' ) ) {
				hiddenDiv.css( 'width', $textarea.width() );
			}
			else {
				hiddenDiv.css( 'width', $( window ).width() / 2 );
			}

			$textarea.css( 'height', hiddenDiv.height() );
		}

		$( text_area_selector ).each( function() {
			var $textarea = $( this );
			if ( $textarea.val().length ) {
				textareaAutoResize( $textarea );
			}
		} );

		$( 'body' ).on( 'keyup keydown autoresize', text_area_selector, function() {
			textareaAutoResize( $( this ) );
		} );

		// File Input Path
		$( document ).on( 'change', '.file-field input[type="file"]', function() {
			var file_field = $( this ).closest( '.file-field' );
			var path_input = file_field.find( 'input.file-path' );
			var files = $( this )[ 0 ].files;
			var file_names = [];
			for ( var i = 0; i < files.length; i ++ ) {
				file_names.push( files[ i ].name );
			}
			path_input.val( file_names.join( ", " ) );
			path_input.trigger( 'change' );
		} );

		/****************
		 *  Range Input  *
		 ****************/

		var range_type = 'input[type=range]';
		var range_mousedown = false;
		var left;

		$( range_type ).each( function() {
			var thumb = $( '<span class="thumb"><span class="value"></span></span>' );
			$( this ).after( thumb );
		} );

		var range_wrapper = '.range-field';
		$( document ).on( 'change', range_type, function( e ) {
			var thumb = $( this ).siblings( '.thumb' );
			thumb.find( '.value' ).html( $( this ).val() );
		} );

		$( document ).on( 'input mousedown touchstart', range_type, function( e ) {
			var thumb = $( this ).siblings( '.thumb' );
			var width = $( this ).outerWidth();

			// If thumb indicator does not exist yet, create it
			if ( thumb.length <= 0 ) {
				thumb = $( '<span class="thumb"><span class="value"></span></span>' );
				$( this ).after( thumb );
			}

			// Set indicator value
			thumb.find( '.value' ).html( $( this ).val() );

			range_mousedown = true;
			$( this ).addClass( 'active' );

			if ( ! thumb.hasClass( 'active' ) ) {
				thumb.velocity( {
					height: "30px",
					width: "30px",
					top: "-20px",
					marginLeft: "-15px"
				}, { duration: 300, easing: 'easeOutExpo' } );
			}

			if ( e.type !== 'input' ) {
				if ( e.pageX === undefined || e.pageX === null ) {//mobile
					left = e.originalEvent.touches[ 0 ].pageX - $( this ).offset().left;
				}
				else { // desktop
					left = e.pageX - $( this ).offset().left;
				}
				if ( left < 0 ) {
					left = 0;
				}
				else {
					if ( left > width ) {
						left = width;
					}
				}
				thumb.addClass( 'active' ).css( 'left', left );
			}

			thumb.find( '.value' ).html( $( this ).val() );
		} );

		$( document ).on( 'mouseup touchend', range_wrapper, function() {
			range_mousedown = false;
			$( this ).removeClass( 'active' );
		} );

		$( document ).on( 'mousemove touchmove', range_wrapper, function( e ) {
			var thumb = $( this ).children( '.thumb' );
			var left;
			if ( range_mousedown ) {
				if ( ! thumb.hasClass( 'active' ) ) {
					thumb.velocity( {
						height: '30px',
						width: '30px',
						top: '-20px',
						marginLeft: '-15px'
					}, { duration: 300, easing: 'easeOutExpo' } );
				}
				if ( e.pageX === undefined || e.pageX === null ) { //mobile
					left = e.originalEvent.touches[ 0 ].pageX - $( this ).offset().left;
				}
				else { // desktop
					left = e.pageX - $( this ).offset().left;
				}
				var width = $( this ).outerWidth();

				if ( left < 0 ) {
					left = 0;
				}
				else {
					if ( left > width ) {
						left = width;
					}
				}
				thumb.addClass( 'active' ).css( 'left', left );
				thumb.find( '.value' ).html( thumb.siblings( range_type ).val() );
			}
		} );

		$( document ).on( 'mouseout touchleave', range_wrapper, function() {
			if ( ! range_mousedown ) {

				var thumb = $( this ).children( '.thumb' );

				if ( thumb.hasClass( 'active' ) ) {
					thumb.velocity( {
						height: '0',
						width: '0',
						top: '10px',
						marginLeft: '-6px'
					}, { duration: 100 } );
				}
				thumb.removeClass( 'active' );
			}
		} );

		/**************************
		 * Auto complete plugin  *
		 *************************/
		$.fn.autocomplete = function( options ) {
			// Defaults
			var defaults = {
				data: {}
			};

			options = $.extend( defaults, options );

			return this.each( function() {
				var $input = $( this );
				var data = options.data,
					$inputDiv = $input.closest( '.input-field' ); // Div to append on

				// Check if data isn't empty
				if ( ! $.isEmptyObject( data ) ) {
					// Create autocomplete element
					var $autocomplete = $( '<ul class="autocomplete-content dropdown-content"></ul>' );

					// Append autocomplete element
					if ( $inputDiv.length ) {
						$inputDiv.append( $autocomplete ); // Set ul in body
					} else {
						$input.after( $autocomplete );
					}

					var highlight = function( string, $el ) {
						var img = $el.find( 'img' );
						var matchStart = $el.text().toLowerCase().indexOf( "" + string.toLowerCase() + "" ),
							matchEnd = matchStart + string.length - 1,
							beforeMatch = $el.text().slice( 0, matchStart ),
							matchText = $el.text().slice( matchStart, matchEnd + 1 ),
							afterMatch = $el.text().slice( matchEnd + 1 );
						$el.html( "<span>" + beforeMatch + "<span class='highlight'>" + matchText + "</span>" + afterMatch + "</span>" );
						if ( img.length ) {
							$el.prepend( img );
						}
					};

					// Perform search
					$input.on( 'keyup', function( e ) {
						// Capture Enter
						if ( e.which === 13 ) {
							$autocomplete.find( 'li' ).first().click();
							return;
						}

						var val = $input.val().toLowerCase();
						$autocomplete.empty();

						// Check if the input isn't empty
						if ( val !== '' ) {
							for ( var key in data ) {
								if ( data.hasOwnProperty( key ) &&
									key.toLowerCase().indexOf( val ) !== - 1 &&
									key.toLowerCase() !== val ) {
									var autocompleteOption = $( '<li></li>' );
									if ( ! ! data[ key ] ) {
										autocompleteOption.append( '<img src="' + data[ key ] + '" class="right circle"><span>' + key + '</span>' );
									} else {
										autocompleteOption.append( '<span>' + key + '</span>' );
									}
									$autocomplete.append( autocompleteOption );

									highlight( val, autocompleteOption );
								}
							}
						}
					} );

					// Set input value
					$autocomplete.on( 'click', 'li', function() {
						$input.val( $( this ).text().trim() );
						$autocomplete.empty();
					} );
				}
			} );
		};

	} ); // End of $(document).ready

	/*******************
	 *  Select Plugin  *
	 ******************/
	$.fn.material_select = function( callback ) {
		$( this ).each( function() {
			var $select = $( this );

			if ( $select.hasClass( 'browser-default' ) ) {
				return; // Continue to next (return false breaks out of entire loop)
			}

			var multiple = $select.attr( 'multiple' ) ? true : false,
				lastID = $select.data( 'select-id' ); // Tear down structure if Select needs to be
													  // rebuilt

			if ( lastID ) {
				$select.parent().find( 'span.caret' ).remove();
				$select.parent().find( 'input' ).remove();

				$select.unwrap();
				$( 'ul#select-options-' + lastID ).remove();
			}

			// If destroying the select, remove the selelct-id and reset it to it's uninitialized
			// state.
			if ( callback === 'destroy' ) {
				$select.data( 'select-id', null ).removeClass( 'initialized' );
				return;
			}

			var uniqueID = Materialize.guid();
			$select.data( 'select-id', uniqueID );
			var wrapper = $( '<div class="select-wrapper"></div>' );
			wrapper.addClass( $select.attr( 'class' ) );
			var options = $( '<ul id="select-options-' + uniqueID + '" class="dropdown-content select-dropdown ' + (multiple ? 'multiple-select-dropdown' : '') + '"></ul>' ),
				selectChildren = $select.children( 'option, optgroup' ),
				valuesSelected = [],
				optionsHover = false;

			var label = $select.find( 'option:selected' ).html() || $select.find( 'option:first' ).html() || "";

			// Function that renders and appends the option taking into
			// account type and possible image icon.
			var appendOptionWithIcon = function( select, option, type ) {
				// Add disabled attr if disabled
				var disabledClass = (option.is( ':disabled' )) ? 'disabled ' : '';
				var optgroupClass = (type === 'optgroup-option') ? 'optgroup-option ' : '';

				// add icons
				var icon_url = option.data( 'icon' );
				var classes = option.attr( 'class' );
				if ( ! ! icon_url ) {
					var classString = '';
					if ( ! ! classes ) {
						classString = ' class="' + classes + '"';
					}

					// Check for multiple type.
					if ( type === 'multiple' ) {
						options.append( $( '<li class="' + disabledClass + '"><img src="' + icon_url + '"' + classString + '><span><input type="checkbox"' + disabledClass + '/><label></label>' + option.html() + '</span></li>' ) );
					} else {
						options.append( $( '<li class="' + disabledClass + optgroupClass + '"><img src="' + icon_url + '"' + classString + '><span>' + option.html() + '</span></li>' ) );
					}
					return true;
				}

				// Check for multiple type.
				if ( type === 'multiple' ) {
					options.append( $( '<li class="' + disabledClass + '"><span><input type="checkbox"' + disabledClass + '/><label></label>' + option.html() + '</span></li>' ) );
				} else {
					options.append( $( '<li class="' + disabledClass + optgroupClass + '"><span>' + option.html() + '</span></li>' ) );
				}
			};

			/* Create dropdown structure. */
			if ( selectChildren.length ) {
				selectChildren.each( function() {
					if ( $( this ).is( 'option' ) ) {
						// Direct descendant option.
						if ( multiple ) {
							appendOptionWithIcon( $select, $( this ), 'multiple' );

						} else {
							appendOptionWithIcon( $select, $( this ) );
						}
					} else {
						if ( $( this ).is( 'optgroup' ) ) {
							// Optgroup.
							var selectOptions = $( this ).children( 'option' );
							options.append( $( '<li class="optgroup"><span>' + $( this ).attr( 'label' ) + '</span></li>' ) );

							selectOptions.each( function() {
								appendOptionWithIcon( $select, $( this ), 'optgroup-option' );
							} );
						}
					}
				} );
			}

			options.find( 'li:not(.optgroup)' ).each( function( i ) {
				$( this ).click( function( e ) {
					// Check if option element is disabled
					if ( ! $( this ).hasClass( 'disabled' ) && ! $( this ).hasClass( 'optgroup' ) ) {
						var selected = true;

						if ( multiple ) {
							$( 'input[type="checkbox"]', this ).prop( 'checked', function( i, v ) {
								return ! v;
							} );
							selected = toggleEntryFromArray( valuesSelected, $( this ).index(), $select );
							$newSelect.trigger( 'focus' );
						} else {
							options.find( 'li' ).removeClass( 'active' );
							$( this ).toggleClass( 'active' );
							$newSelect.val( $( this ).text() );
						}

						activateOption( options, $( this ) );
						$select.find( 'option' ).eq( i ).prop( 'selected', selected );
						// Trigger onchange() event
						$select.trigger( 'change' );
						if ( typeof callback !== 'undefined' ) {
							callback();
						}
					}

					e.stopPropagation();
				} );
			} );

			// Wrap Elements
			$select.wrap( wrapper );
			// Add Select Display Element
			var dropdownIcon = $( '<span class="caret">&#9660;</span>' );
			if ( $select.is( ':disabled' ) ) {
				dropdownIcon.addClass( 'disabled' );
			}

			// escape double quotes
			var sanitizedLabelHtml = label.replace( /"/g, '&quot;' );

			var $newSelect = $( '<input type="text" class="select-dropdown" readonly="true" ' + (($select.is( ':disabled' )) ? 'disabled' : '') + ' data-activates="select-options-' + uniqueID + '" value="' + sanitizedLabelHtml + '"/>' );
			$select.before( $newSelect );
			$newSelect.before( dropdownIcon );

			$newSelect.after( options );
			// Check if section element is disabled
			if ( ! $select.is( ':disabled' ) ) {
				$newSelect.dropdown( { 'hover': false, 'closeOnClick': false } );
			}

			// Copy tabindex
			if ( $select.attr( 'tabindex' ) ) {
				$( $newSelect[ 0 ] ).attr( 'tabindex', $select.attr( 'tabindex' ) );
			}

			$select.addClass( 'initialized' );

			$newSelect.on( {
				'focus': function() {
					if ( $( 'ul.select-dropdown' ).not( options[ 0 ] ).is( ':visible' ) ) {
						$( 'input.select-dropdown' ).trigger( 'close' );
					}
					if ( ! options.is( ':visible' ) ) {
						$( this ).trigger( 'open', [ 'focus' ] );
						var label = $( this ).val();
						var selectedOption = options.find( 'li' ).filter( function() {
							return $( this ).text().toLowerCase() === label.toLowerCase();
						} )[ 0 ];
						activateOption( options, selectedOption );
					}
				},
				'click': function( e ) {
					e.stopPropagation();
				}
			} );

			$newSelect.on( 'blur', function() {
				if ( ! multiple ) {
					$( this ).trigger( 'close' );
				}
				options.find( 'li.selected' ).removeClass( 'selected' );
			} );

			options.hover( function() {
				optionsHover = true;
			}, function() {
				optionsHover = false;
			} );

			$( window ).on( {
				'click': function() {
					multiple && (optionsHover || $newSelect.trigger( 'close' ));
				}
			} );

			// Add initial multiple selections.
			if ( multiple ) {
				$select.find( "option:selected:not(:disabled)" ).each( function() {
					var index = $( this ).index();

					toggleEntryFromArray( valuesSelected, index, $select );
					options.find( "li" ).eq( index ).find( ":checkbox" ).prop( "checked", true );
				} );
			}

			// Make option as selected and scroll to selected position
			var activateOption = function( collection, newOption ) {
				if ( newOption ) {
					collection.find( 'li.selected' ).removeClass( 'selected' );
					var option = $( newOption );
					option.addClass( 'selected' );
					options.scrollTo( option );
				}
			};

			// Allow user to search by typing
			// this array is cleared after 1 second
			var filterQuery = [],
				onKeyDown = function( e ) {
					// TAB - switch to another input
					if ( e.which == 9 ) {
						$newSelect.trigger( 'close' );
						return;
					}

					// ARROW DOWN WHEN SELECT IS CLOSED - open select options
					if ( e.which == 40 && ! options.is( ':visible' ) ) {
						$newSelect.trigger( 'open' );
						return;
					}

					// ENTER WHEN SELECT IS CLOSED - submit form
					if ( e.which == 13 && ! options.is( ':visible' ) ) {
						return;
					}

					e.preventDefault();

					// CASE WHEN USER TYPE LETTERS
					var letter = String.fromCharCode( e.which ).toLowerCase(),
						nonLetters = [ 9, 13, 27, 38, 40 ];
					if ( letter && (nonLetters.indexOf( e.which ) === - 1) ) {
						filterQuery.push( letter );

						var string = filterQuery.join( '' ),
							newOption = options.find( 'li' ).filter( function() {
								return $( this ).text().toLowerCase().indexOf( string ) === 0;
							} )[ 0 ];

						if ( newOption ) {
							activateOption( options, newOption );
						}
					}

					// ENTER - select option and close when select options are opened
					if ( e.which == 13 ) {
						var activeOption = options.find( 'li.selected:not(.disabled)' )[ 0 ];
						if ( activeOption ) {
							$( activeOption ).trigger( 'click' );
							if ( ! multiple ) {
								$newSelect.trigger( 'close' );
							}
						}
					}

					// ARROW DOWN - move to next not disabled option
					if ( e.which == 40 ) {
						if ( options.find( 'li.selected' ).length ) {
							newOption = options.find( 'li.selected' ).next( 'li:not(.disabled)' )[ 0 ];
						} else {
							newOption = options.find( 'li:not(.disabled)' )[ 0 ];
						}
						activateOption( options, newOption );
					}

					// ESC - close options
					if ( e.which == 27 ) {
						$newSelect.trigger( 'close' );
					}

					// ARROW UP - move to previous not disabled option
					if ( e.which == 38 ) {
						newOption = options.find( 'li.selected' ).prev( 'li:not(.disabled)' )[ 0 ];
						if ( newOption ) {
							activateOption( options, newOption );
						}
					}

					// Automaticaly clean filter query so user can search again by starting letters
					setTimeout( function() {
						filterQuery = [];
					}, 1000 );
				};

			$newSelect.on( 'keydown', onKeyDown );
		} );

		function toggleEntryFromArray( entriesArray, entryIndex, select ) {
			var index = entriesArray.indexOf( entryIndex ),
				notAdded = index === - 1;

			if ( notAdded ) {
				entriesArray.push( entryIndex );
			} else {
				entriesArray.splice( index, 1 );
			}

			select.siblings( 'ul.dropdown-content' ).find( 'li' ).eq( entryIndex ).toggleClass( 'active' );

			// use notAdded instead of true (to detect if the option is selected or not)
			select.find( 'option' ).eq( entryIndex ).prop( 'selected', notAdded );
			setValueToInput( entriesArray, select );

			return notAdded;
		}

		function setValueToInput( entriesArray, select ) {
			var value = '';

			for ( var i = 0, count = entriesArray.length; i < count; i ++ ) {
				var text = select.find( 'option' ).eq( entriesArray[ i ] ).text();

				i === 0 ? value += text : value += ', ' + text;
			}

			if ( value === '' ) {
				value = select.find( 'option:disabled' ).eq( 0 ).text();
			}

			select.siblings( 'input.select-dropdown' ).val( value );
		}
	};

}( jQuery ));
;(function( $ ) {

	var methods = {

		init: function( options ) {
			var defaults = {
				indicators: true,
				height: 400,
				transition: 500,
				interval: 6000
			};
			options = $.extend( defaults, options );

			return this.each( function() {

				// For each slider, we want to keep track of
				// which slide is active and its associated content
				var $this = $( this );
				var $slider = $this.find( 'ul.slides' ).first();
				var $slides = $slider.find( '> li' );
				var $active_index = $slider.find( '.active' ).index();
				var $active, $indicators, $interval;
				if ( $active_index != - 1 ) {
					$active = $slides.eq( $active_index );
				}

				// Transitions the caption depending on alignment
				function captionTransition( caption, duration ) {
					if ( caption.hasClass( "center-align" ) ) {
						caption.velocity( { opacity: 0, translateY: - 100 }, {
							duration: duration,
							queue: false
						} );
					}
					else {
						if ( caption.hasClass( "right-align" ) ) {
							caption.velocity( {
								opacity: 0,
								translateX: 100
							}, { duration: duration, queue: false } );
						}
						else {
							if ( caption.hasClass( "left-align" ) ) {
								caption.velocity( {
									opacity: 0,
									translateX: - 100
								}, { duration: duration, queue: false } );
							}
						}
					}
				}

				// This function will transition the slide to any index of the next slide
				function moveToSlide( index ) {
					// Wrap around indices.
					if ( index >= $slides.length ) {
						index = 0;
					} else {
						if ( index < 0 ) {
							index = $slides.length - 1;
						}
					}

					$active_index = $slider.find( '.active' ).index();

					// Only do if index changes
					if ( $active_index != index ) {
						$active = $slides.eq( $active_index );
						$caption = $active.find( '.caption' );

						$active.removeClass( 'active' );
						$active.velocity( { opacity: 0 }, {
							duration: options.transition, queue: false, easing: 'easeOutQuad',
							complete: function() {
								$slides.not( '.active' ).velocity( {
									opacity: 0,
									translateX: 0,
									translateY: 0
								}, { duration: 0, queue: false } );
							}
						} );
						captionTransition( $caption, options.transition );


						// Update indicators
						if ( options.indicators ) {
							$indicators.eq( $active_index ).removeClass( 'active' );
						}

						$slides.eq( index ).velocity( { opacity: 1 }, {
							duration: options.transition,
							queue: false,
							easing: 'easeOutQuad'
						} );
						$slides.eq( index ).find( '.caption' ).velocity( {
							opacity: 1,
							translateX: 0,
							translateY: 0
						}, {
							duration: options.transition,
							delay: options.transition,
							queue: false,
							easing: 'easeOutQuad'
						} );
						$slides.eq( index ).addClass( 'active' );


						// Update indicators
						if ( options.indicators ) {
							$indicators.eq( index ).addClass( 'active' );
						}
					}
				}

				// Set height of slider
				// If fullscreen, do nothing
				if ( ! $this.hasClass( 'fullscreen' ) ) {
					if ( options.indicators ) {
						// Add height if indicators are present
						$this.height( options.height + 40 );
					}
					else {
						$this.height( options.height );
					}
					$slider.height( options.height );
				}


				// Set initial positions of captions
				$slides.find( '.caption' ).each( function() {
					captionTransition( $( this ), 0 );
				} );

				// Move img src into background-image
				$slides.find( 'img' ).each( function() {
					var placeholderBase64 = 'data:image/gif;base64,R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
					if ( $( this ).attr( 'src' ) !== placeholderBase64 ) {
						$( this ).css( 'background-image', 'url(' + $( this ).attr( 'src' ) + ')' );
						$( this ).attr( 'src', placeholderBase64 );
					}
				} );

				// dynamically add indicators
				if ( options.indicators ) {
					$indicators = $( '<ul class="indicators"></ul>' );
					$slides.each( function( index ) {
						var $indicator = $( '<li class="indicator-item"></li>' );

						// Handle clicks on indicators
						$indicator.click( function() {
							var $parent = $slider.parent();
							var curr_index = $parent.find( $( this ) ).index();
							moveToSlide( curr_index );

							// reset interval
							clearInterval( $interval );
							$interval = setInterval(
								function() {
									$active_index = $slider.find( '.active' ).index();
									if ( $slides.length == $active_index + 1 ) {
										$active_index = 0;
									}// loop to start
									else {
										$active_index += 1;
									}

									moveToSlide( $active_index );

								}, options.transition + options.interval
							);
						} );
						$indicators.append( $indicator );
					} );
					$this.append( $indicators );
					$indicators = $this.find( 'ul.indicators' ).find( 'li.indicator-item' );
				}

				if ( $active ) {
					$active.show();
				}
				else {
					$slides.first().addClass( 'active' ).velocity( { opacity: 1 }, {
						duration: options.transition,
						queue: false,
						easing: 'easeOutQuad'
					} );

					$active_index = 0;
					$active = $slides.eq( $active_index );

					// Update indicators
					if ( options.indicators ) {
						$indicators.eq( $active_index ).addClass( 'active' );
					}
				}

				// Adjust height to current slide
				$active.find( 'img' ).each( function() {
					$active.find( '.caption' ).velocity( {
						opacity: 1,
						translateX: 0,
						translateY: 0
					}, { duration: options.transition, queue: false, easing: 'easeOutQuad' } );
				} );

				// auto scroll
				$interval = setInterval(
					function() {
						$active_index = $slider.find( '.active' ).index();
						moveToSlide( $active_index + 1 );

					}, options.transition + options.interval
				);


				// HammerJS, Swipe navigation

				// Touch Event
				var panning = false;
				var swipeLeft = false;
				var swipeRight = false;

				$this.hammer( {
					prevent_default: false
				} ).bind( 'pan', function( e ) {
					if ( e.gesture.pointerType === "touch" ) {

						// reset interval
						clearInterval( $interval );

						var direction = e.gesture.direction;
						var x = e.gesture.deltaX;
						var velocityX = e.gesture.velocityX;

						$curr_slide = $slider.find( '.active' );
						$curr_slide.velocity( {
							translateX: x
						}, { duration: 50, queue: false, easing: 'easeOutQuad' } );

						// Swipe Left
						if ( direction === 4 && (x > ($this.innerWidth() / 2) || velocityX < - 0.65) ) {
							swipeRight = true;
						}
						// Swipe Right
						else {
							if ( direction === 2 && (x < (- 1 * $this.innerWidth() / 2) || velocityX > 0.65) ) {
								swipeLeft = true;
							}
						}

						// Make Slide Behind active slide visible
						var next_slide;
						if ( swipeLeft ) {
							next_slide = $curr_slide.next();
							if ( next_slide.length === 0 ) {
								next_slide = $slides.first();
							}
							next_slide.velocity( {
								opacity: 1
							}, { duration: 300, queue: false, easing: 'easeOutQuad' } );
						}
						if ( swipeRight ) {
							next_slide = $curr_slide.prev();
							if ( next_slide.length === 0 ) {
								next_slide = $slides.last();
							}
							next_slide.velocity( {
								opacity: 1
							}, { duration: 300, queue: false, easing: 'easeOutQuad' } );
						}


					}

				} ).bind( 'panend', function( e ) {
					if ( e.gesture.pointerType === "touch" ) {

						$curr_slide = $slider.find( '.active' );
						panning = false;
						curr_index = $slider.find( '.active' ).index();

						if ( ! swipeRight && ! swipeLeft || $slides.length <= 1 ) {
							// Return to original spot
							$curr_slide.velocity( {
								translateX: 0
							}, { duration: 300, queue: false, easing: 'easeOutQuad' } );
						}
						else {
							if ( swipeLeft ) {
								moveToSlide( curr_index + 1 );
								$curr_slide.velocity( { translateX: - 1 * $this.innerWidth() }, {
									duration: 300, queue: false, easing: 'easeOutQuad',
									complete: function() {
										$curr_slide.velocity( {
											opacity: 0,
											translateX: 0
										}, { duration: 0, queue: false } );
									}
								} );
							}
							else {
								if ( swipeRight ) {
									moveToSlide( curr_index - 1 );
									$curr_slide.velocity( { translateX: $this.innerWidth() }, {
										duration: 300, queue: false, easing: 'easeOutQuad',
										complete: function() {
											$curr_slide.velocity( {
												opacity: 0,
												translateX: 0
											}, { duration: 0, queue: false } );
										}
									} );
								}
							}
						}
						swipeLeft = false;
						swipeRight = false;

						// Restart interval
						clearInterval( $interval );
						$interval = setInterval(
							function() {
								$active_index = $slider.find( '.active' ).index();
								if ( $slides.length == $active_index + 1 ) {
									$active_index = 0;
								}// loop to start
								else {
									$active_index += 1;
								}

								moveToSlide( $active_index );

							}, options.transition + options.interval
						);
					}
				} );

				$this.on( 'sliderPause', function() {
					clearInterval( $interval );
				} );

				$this.on( 'sliderStart', function() {
					clearInterval( $interval );
					$interval = setInterval(
						function() {
							$active_index = $slider.find( '.active' ).index();
							if ( $slides.length == $active_index + 1 ) {
								$active_index = 0;
							}// loop to start
							else {
								$active_index += 1;
							}

							moveToSlide( $active_index );

						}, options.transition + options.interval
					);
				} );

				$this.on( 'sliderNext', function() {
					$active_index = $slider.find( '.active' ).index();
					moveToSlide( $active_index + 1 );
				} );

				$this.on( 'sliderPrev', function() {
					$active_index = $slider.find( '.active' ).index();
					moveToSlide( $active_index - 1 );
				} );

			} );



		},
		pause: function() {
			$( this ).trigger( 'sliderPause' );
		},
		start: function() {
			$( this ).trigger( 'sliderStart' );
		},
		next: function() {
			$( this ).trigger( 'sliderNext' );
		},
		prev: function() {
			$( this ).trigger( 'sliderPrev' );
		}
	};


	$.fn.slider = function( methodOrOptions ) {
		if ( methods[ methodOrOptions ] ) {
			return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ) );
		} else {
			if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
				// Default to "init"
				return methods.init.apply( this, arguments );
			} else {
				$.error( 'Method ' + methodOrOptions + ' does not exist on jQuery.tooltip' );
			}
		}
	}; // Plugin end
}( jQuery ));
;(function( $ ) {
	$( document ).ready( function() {

		$( document ).on( 'click.card', '.card', function( e ) {
			if ( $( this ).find( '> .card-reveal' ).length ) {
				if ( $( e.target ).is( $( '.card-reveal .card-title' ) ) || $( e.target ).is( $( '.card-reveal .card-title i' ) ) ) {
					// Make Reveal animate down and display none
					$( this ).find( '.card-reveal' ).velocity(
						{ translateY: 0 }, {
							duration: 225,
							queue: false,
							easing: 'easeInOutQuad',
							complete: function() {
								$( this ).css( { display: 'none' } );
							}
						}
					);
				}
				else {
					if ( $( e.target ).is( $( '.card .activator' ) ) ||
						$( e.target ).is( $( '.card .activator i' ) ) ) {
						$( e.target ).closest( '.card' ).css( 'overflow', 'hidden' );
						$( this ).find( '.card-reveal' ).css( { display: 'block' } ).velocity( "stop", false ).velocity( { translateY: '-100%' }, {
							duration: 300,
							queue: false,
							easing: 'easeInOutQuad'
						} );
					}
				}
			}
		} );

	} );
}( jQuery ));
;(function( $ ) {
	var chipsHandleEvents = false;
	var materialChipsDefaults = {
		data: [],
		placeholder: '',
		secondaryPlaceholder: '',
	};

	$( document ).ready( function() {
		// Handle removal of static chips.
		$( document ).on( 'click', '.chip .close', function( e ) {
			var $chips = $( this ).closest( '.chips' );
			if ( $chips.data( 'initialized' ) ) {
				return;
			}
			$( this ).closest( '.chip' ).remove();
		} );
	} );

	$.fn.material_chip = function( options ) {
		var self = this;
		this.$el = $( this );
		this.$document = $( document );
		this.SELS = {
			CHIPS: '.chips',
			CHIP: '.chip',
			INPUT: 'input',
			DELETE: '.material-icons',
			SELECTED_CHIP: '.selected',
		};

		if ( 'data' === options ) {
			return this.$el.data( 'chips' );
		}

		if ( 'options' === options ) {
			return this.$el.data( 'options' );
		}

		this.$el.data( 'options', $.extend( {}, materialChipsDefaults, options ) );

		// Initialize
		this.init = function() {
			var i = 0;
			var chips;
			self.$el.each( function() {
				var $chips = $( this );
				if ( $chips.data( 'initialized' ) ) {
					// Prevent double initialization.
					return;
				}
				var options = $chips.data( 'options' );
				if ( ! options.data || ! options.data instanceof Array ) {
					options.data = [];
				}
				$chips.data( 'chips', options.data );
				$chips.data( 'index', i );
				$chips.data( 'initialized', true );

				if ( ! $chips.hasClass( self.SELS.CHIPS ) ) {
					$chips.addClass( 'chips' );
				}

				self.chips( $chips );
				i ++;
			} );
		};

		this.handleEvents = function() {
			var SELS = self.SELS;

			self.$document.on( 'click', SELS.CHIPS, function( e ) {
				$( e.target ).find( SELS.INPUT ).focus();
			} );

			self.$document.on( 'click', SELS.CHIP, function( e ) {
				$( SELS.CHIP ).removeClass( 'selected' );
				$( this ).toggleClass( 'selected' );
			} );

			self.$document.on( 'keydown', function( e ) {
				if ( $( e.target ).is( 'input, textarea' ) ) {
					return;
				}

				// delete
				var $chip = self.$document.find( SELS.CHIP + SELS.SELECTED_CHIP );
				var $chips = $chip.closest( SELS.CHIPS );
				var length = $chip.siblings( SELS.CHIP ).length;
				var index;

				if ( ! $chip.length ) {
					return;
				}

				if ( e.which === 8 || e.which === 46 ) {
					e.preventDefault();
					var chipsIndex = $chips.data( 'index' );

					index = $chip.index();
					self.deleteChip( chipsIndex, index, $chips );

					var selectIndex = null;
					if ( (index + 1) < length ) {
						selectIndex = index;
					} else {
						if ( index === length || (index + 1) === length ) {
							selectIndex = length - 1;
						}
					}

					if ( selectIndex < 0 ) {
						selectIndex = null;
					}

					if ( null !== selectIndex ) {
						self.selectChip( chipsIndex, selectIndex, $chips );
					}
					if ( ! length ) {
						$chips.find( 'input' ).focus();
					}

					// left
				} else {
					if ( e.which === 37 ) {
						index = $chip.index() - 1;
						if ( index < 0 ) {
							return;
						}
						$( SELS.CHIP ).removeClass( 'selected' );
						self.selectChip( $chips.data( 'index' ), index, $chips );

						// right
					} else {
						if ( e.which === 39 ) {
							index = $chip.index() + 1;
							$( SELS.CHIP ).removeClass( 'selected' );
							if ( index > length ) {
								$chips.find( 'input' ).focus();
								return;
							}
							self.selectChip( $chips.data( 'index' ), index, $chips );
						}
					}
				}
			} );

			self.$document.on( 'focusin', SELS.CHIPS + ' ' + SELS.INPUT, function( e ) {
				$( e.target ).closest( SELS.CHIPS ).addClass( 'focus' );
				$( SELS.CHIP ).removeClass( 'selected' );
			} );

			self.$document.on( 'focusout', SELS.CHIPS + ' ' + SELS.INPUT, function( e ) {
				$( e.target ).closest( SELS.CHIPS ).removeClass( 'focus' );
			} );

			self.$document.on( 'keydown', SELS.CHIPS + ' ' + SELS.INPUT, function( e ) {
				var $target = $( e.target );
				var $chips = $target.closest( SELS.CHIPS );
				var chipsIndex = $chips.data( 'index' );
				var chipsLength = $chips.children( SELS.CHIP ).length;

				// enter
				if ( 13 === e.which ) {
					e.preventDefault();
					self.addChip( chipsIndex, { tag: $target.val() }, $chips );
					$target.val( '' );
					return;
				}

				// delete or left
				if ( (8 === e.keyCode || 37 === e.keyCode) && '' === $target.val() && chipsLength ) {
					self.selectChip( chipsIndex, chipsLength - 1, $chips );
					$target.blur();
					return;
				}
			} );

			self.$document.on( 'click', SELS.CHIPS + ' ' + SELS.DELETE, function( e ) {
				var $target = $( e.target );
				var $chips = $target.closest( SELS.CHIPS );
				var $chip = $target.closest( SELS.CHIP );
				e.stopPropagation();
				self.deleteChip(
					$chips.data( 'index' ),
					$chip.index(),
					$chips
				);
				$chips.find( 'input' ).focus();
			} );
		};

		this.chips = function( $chips ) {
			var html = '';
			var options = $chips.data( 'options' );
			$chips.data( 'chips' ).forEach( function( elem ) {
				html += self.renderChip( elem );
			} );
			html += '<input class="input" placeholder="">';
			$chips.html( html );
			self.setPlaceholder( $chips );
		};

		this.renderChip = function( elem ) {
			if ( ! elem.tag ) {
				return;
			}

			var html = '<div class="chip">' + elem.tag;
			if ( elem.image ) {
				html += ' <img src="' + elem.image + '"> ';
			}
			html += '<i class="material-icons close">close</i>';
			html += '</div>';
			return html;
		};

		this.setPlaceholder = function( $chips ) {
			var options = $chips.data( 'options' );
			if ( $chips.data( 'chips' ).length && options.placeholder ) {
				$chips.find( 'input' ).prop( 'placeholder', options.placeholder );
			} else {
				if ( ! $chips.data( 'chips' ).length && options.secondaryPlaceholder ) {
					$chips.find( 'input' ).prop( 'placeholder', options.secondaryPlaceholder );
				}
			}
		};

		this.isValid = function( $chips, elem ) {
			var chips = $chips.data( 'chips' );
			var exists = false;
			for ( var i = 0; i < chips.length; i ++ ) {
				if ( chips[ i ].tag === elem.tag ) {
					exists = true;
					return;
				}
			}
			return '' !== elem.tag && ! exists;
		};

		this.addChip = function( chipsIndex, elem, $chips ) {
			if ( ! self.isValid( $chips, elem ) ) {
				return;
			}
			var options = $chips.data( 'options' );
			var chipHtml = self.renderChip( elem );
			$chips.data( 'chips' ).push( elem );
			$( chipHtml ).insertBefore( $chips.find( 'input' ) );
			$chips.trigger( 'chip.add', elem );
			self.setPlaceholder( $chips );
		};

		this.deleteChip = function( chipsIndex, chipIndex, $chips ) {
			var chip = $chips.data( 'chips' )[ chipIndex ];
			$chips.find( '.chip' ).eq( chipIndex ).remove();
			$chips.data( 'chips' ).splice( chipIndex, 1 );
			$chips.trigger( 'chip.delete', chip );
			self.setPlaceholder( $chips );
		};

		this.selectChip = function( chipsIndex, chipIndex, $chips ) {
			var $chip = $chips.find( '.chip' ).eq( chipIndex );
			if ( $chip && false === $chip.hasClass( 'selected' ) ) {
				$chip.addClass( 'selected' );
				$chips.trigger( 'chip.select', $chips.data( 'chips' )[ chipIndex ] );
			}
		};

		this.getChipsElement = function( index, $chips ) {
			return $chips.eq( index );
		};

		// init
		this.init();

		if ( ! chipsHandleEvents ) {
			this.handleEvents();
			chipsHandleEvents = true;
		}
	};
}( jQuery ));
;(function( $ ) {
	$.fn.pushpin = function( options ) {
		// Defaults
		var defaults = {
			top: 0,
			bottom: Infinity,
			offset: 0
		};

		// Remove pushpin event and classes
		if ( options === "remove" ) {
			this.each( function() {
				if ( id = $( this ).data( 'pushpin-id' ) ) {
					$( window ).off( 'scroll.' + id );
					$( this ).removeData( 'pushpin-id' ).removeClass( 'pin-top pinned pin-bottom' ).removeAttr( 'style' );
				}
			} );
			return false;
		}

		options = $.extend( defaults, options );


		$index = 0;
		return this.each( function() {
			var $uniqueId = Materialize.guid(),
				$this = $( this ),
				$original_offset = $( this ).offset().top;

			function removePinClasses( object ) {
				object.removeClass( 'pin-top' );
				object.removeClass( 'pinned' );
				object.removeClass( 'pin-bottom' );
			}

			function updateElements( objects, scrolled ) {
				objects.each( function() {
					// Add position fixed (because its between top and bottom)
					if ( options.top <= scrolled && options.bottom >= scrolled && ! $( this ).hasClass( 'pinned' ) ) {
						removePinClasses( $( this ) );
						$( this ).css( 'top', options.offset );
						$( this ).addClass( 'pinned' );
					}

					// Add pin-top (when scrolled position is above top)
					if ( scrolled < options.top && ! $( this ).hasClass( 'pin-top' ) ) {
						removePinClasses( $( this ) );
						$( this ).css( 'top', 0 );
						$( this ).addClass( 'pin-top' );
					}

					// Add pin-bottom (when scrolled position is below bottom)
					if ( scrolled > options.bottom && ! $( this ).hasClass( 'pin-bottom' ) ) {
						removePinClasses( $( this ) );
						$( this ).addClass( 'pin-bottom' );
						$( this ).css( 'top', options.bottom - $original_offset );
					}
				} );
			}

			$( this ).data( 'pushpin-id', $uniqueId );
			updateElements( $this, $( window ).scrollTop() );
			$( window ).on( 'scroll.' + $uniqueId, function() {
				var $scrolled = $( window ).scrollTop() + options.offset;
				updateElements( $this, $scrolled );
			} );

		} );

	};
}( jQuery ));
;(function( $ ) {
	$( document ).ready( function() {

		// jQuery reverse
		$.fn.reverse = [].reverse;

		// Hover behaviour: make sure this doesn't work on .click-to-toggle FABs!
		$( document ).on( 'mouseenter.fixedActionBtn', '.fixed-action-btn:not(.click-to-toggle)', function( e ) {
			var $this = $( this );
			openFABMenu( $this );
		} );
		$( document ).on( 'mouseleave.fixedActionBtn', '.fixed-action-btn:not(.click-to-toggle)', function( e ) {
			var $this = $( this );
			closeFABMenu( $this );
		} );

		// Toggle-on-click behaviour.
		$( document ).on( 'click.fixedActionBtn', '.fixed-action-btn.click-to-toggle > a', function( e ) {
			var $this = $( this );
			var $menu = $this.parent();
			if ( $menu.hasClass( 'active' ) ) {
				closeFABMenu( $menu );
			} else {
				openFABMenu( $menu );
			}
		} );

	} );

	$.fn.extend( {
		openFAB: function() {
			openFABMenu( $( this ) );
		},
		closeFAB: function() {
			closeFABMenu( $( this ) );
		}
	} );


	var openFABMenu = function( btn ) {
		$this = btn;
		if ( $this.hasClass( 'active' ) === false ) {

			// Get direction option
			var horizontal = $this.hasClass( 'horizontal' );
			var offsetY, offsetX;

			if ( horizontal === true ) {
				offsetX = 40;
			} else {
				offsetY = 40;
			}

			$this.addClass( 'active' );
			$this.find( 'ul .btn-floating' ).velocity(
				{
					scaleY: ".4",
					scaleX: ".4",
					translateY: offsetY + 'px',
					translateX: offsetX + 'px'
				},
				{ duration: 0 } );

			var time = 0;
			$this.find( 'ul .btn-floating' ).reverse().each( function() {
				$( this ).velocity(
					{ opacity: "1", scaleX: "1", scaleY: "1", translateY: "0", translateX: '0' },
					{ duration: 80, delay: time } );
				time += 40;
			} );
		}
	};

	var closeFABMenu = function( btn ) {
		$this = btn;
		// Get direction option
		var horizontal = $this.hasClass( 'horizontal' );
		var offsetY, offsetX;

		if ( horizontal === true ) {
			offsetX = 40;
		} else {
			offsetY = 40;
		}

		$this.removeClass( 'active' );
		var time = 0;
		$this.find( 'ul .btn-floating' ).velocity( "stop", true );
		$this.find( 'ul .btn-floating' ).velocity(
			{
				opacity: "0",
				scaleX: ".4",
				scaleY: ".4",
				translateY: offsetY + 'px',
				translateX: offsetX + 'px'
			},
			{ duration: 80 }
		);
	};


}( jQuery ));
;(function( $ ) {
	// Image transition function
	Materialize.fadeInImage = function( selectorOrEl ) {
		var element;
		if ( typeof(selectorOrEl) === 'string' ) {
			element = $( selectorOrEl );
		} else {
			if ( typeof(selectorOrEl) === 'object' ) {
				element = selectorOrEl;
			} else {
				return;
			}
		}
		element.css( { opacity: 0 } );
		$( element ).velocity( { opacity: 1 }, {
			duration: 650,
			queue: false,
			easing: 'easeOutSine'
		} );
		$( element ).velocity( { opacity: 1 }, {
			duration: 1300,
			queue: false,
			easing: 'swing',
			step: function( now, fx ) {
				fx.start = 100;
				var grayscale_setting = now / 100;
				var brightness_setting = 150 - (100 - now) / 1.75;

				if ( brightness_setting < 100 ) {
					brightness_setting = 100;
				}
				if ( now >= 0 ) {
					$( this ).css( {
						"-webkit-filter": "grayscale(" + grayscale_setting + ")" + "brightness(" + brightness_setting + "%)",
						"filter": "grayscale(" + grayscale_setting + ")" + "brightness(" + brightness_setting + "%)"
					} );
				}
			}
		} );
	};

	// Horizontal staggered list
	Materialize.showStaggeredList = function( selectorOrEl ) {
		var element;
		if ( typeof(selectorOrEl) === 'string' ) {
			element = $( selectorOrEl );
		} else {
			if ( typeof(selectorOrEl) === 'object' ) {
				element = selectorOrEl;
			} else {
				return;
			}
		}
		var time = 0;
		element.find( 'li, a' ).velocity(
			{ translateX: "-100px" },
			{ duration: 0 } );

		element.find( 'li, a' ).each( function() {
			$( this ).velocity(
				{ opacity: "1", translateX: "0" },
				{ duration: 800, delay: time, easing: [ 60, 10 ] } );
			time += 120;
		} );
	};


	$( document ).ready( function() {
		// Hardcoded .staggered-list scrollFire
		// var staggeredListOptions = [];
		// $('ul.staggered-list').each(function (i) {

		//   var label = 'scrollFire-' + i;
		//   $(this).addClass(label);
		//   staggeredListOptions.push(
		//     {selector: 'ul.staggered-list.' + label,
		//      offset: 200,
		//      callback: 'showStaggeredList("ul.staggered-list.' + label + '")'});
		// });
		// scrollFire(staggeredListOptions);

		// HammerJS, Swipe navigation

		// Touch Event
		var swipeLeft = false;
		var swipeRight = false;


		// Dismissible Collections
		$( '.dismissable' ).each( function() {
			$( this ).hammer( {
				prevent_default: false
			} ).bind( 'pan', function( e ) {
				if ( e.gesture.pointerType === "touch" ) {
					var $this = $( this );
					var direction = e.gesture.direction;
					var x = e.gesture.deltaX;
					var velocityX = e.gesture.velocityX;

					$this.velocity( {
						translateX: x
					}, { duration: 50, queue: false, easing: 'easeOutQuad' } );

					// Swipe Left
					if ( direction === 4 && (x > ($this.innerWidth() / 2) || velocityX < - 0.75) ) {
						swipeLeft = true;
					}

					// Swipe Right
					if ( direction === 2 && (x < (- 1 * $this.innerWidth() / 2) || velocityX > 0.75) ) {
						swipeRight = true;
					}
				}
			} ).bind( 'panend', function( e ) {
				// Reset if collection is moved back into original position
				if ( Math.abs( e.gesture.deltaX ) < ($( this ).innerWidth() / 2) ) {
					swipeRight = false;
					swipeLeft = false;
				}

				if ( e.gesture.pointerType === "touch" ) {
					var $this = $( this );
					if ( swipeLeft || swipeRight ) {
						var fullWidth;
						if ( swipeLeft ) {
							fullWidth = $this.innerWidth();
						}
						else {
							fullWidth = - 1 * $this.innerWidth();
						}

						$this.velocity( {
							translateX: fullWidth,
						}, {
							duration: 100,
							queue: false,
							easing: 'easeOutQuad',
							complete: function() {
								$this.css( 'border', 'none' );
								$this.velocity( {
									height: 0, padding: 0,
								}, {
									duration: 200,
									queue: false,
									easing: 'easeOutQuad',
									complete: function() {
										$this.remove();
									}
								} );
							}
						} );
					}
					else {
						$this.velocity( {
							translateX: 0,
						}, { duration: 100, queue: false, easing: 'easeOutQuad' } );
					}
					swipeLeft = false;
					swipeRight = false;
				}
			} );

		} );


		// time = 0
		// // Vertical Staggered list
		// $('ul.staggered-list.vertical li').velocity(
		//     { translateY: "100px"},
		//     { duration: 0 });

		// $('ul.staggered-list.vertical li').each(function() {
		//   $(this).velocity(
		//     { opacity: "1", translateY: "0"},
		//     { duration: 800, delay: time, easing: [60, 25] });
		//   time += 120;
		// });

		// // Fade in and Scale
		// $('.fade-in.scale').velocity(
		//     { scaleX: .4, scaleY: .4, translateX: -600},
		//     { duration: 0});
		// $('.fade-in').each(function() {
		//   $(this).velocity(
		//     { opacity: "1", scaleX: 1, scaleY: 1, translateX: 0},
		//     { duration: 800, easing: [60, 10] });
		// });
	} );
}( jQuery ));
;(function( $ ) {

	// Input: Array of JSON objects {selector, offset, callback}

	Materialize.scrollFire = function( options ) {

		var didScroll = false;

		window.addEventListener( "scroll", function() {
			didScroll = true;
		} );

		// Rate limit to 100ms
		setInterval( function() {
			if ( didScroll ) {
				didScroll = false;

				var windowScroll = window.pageYOffset + window.innerHeight;

				for ( var i = 0; i < options.length; i ++ ) {
					// Get options from each line
					var value = options[ i ];
					var selector = value.selector,
						offset = value.offset,
						callback = value.callback;

					var currentElement = document.querySelector( selector );
					if ( currentElement !== null ) {
						var elementOffset = currentElement.getBoundingClientRect().top + window.pageYOffset;

						if ( windowScroll > (elementOffset + offset) ) {
							if ( value.done !== true ) {
								if ( typeof(callback) === 'function' ) {
									callback.call( this, currentElement );
								} else {
									if ( typeof(callback) === 'string' ) {
										var callbackFunc = new Function( callback );
										callbackFunc( currentElement );
									}
								}
								value.done = true;
							}
						}
					}
				}
			}
		}, 100 );
	};

})( jQuery );
;/*!
 * pickadate.js v3.5.0, 2014/04/13
 * By Amsul, http://amsul.ca
 * Hosted on http://amsul.github.io/pickadate.js
 * Licensed under MIT
 */

(function( factory ) {

	// AMD.
	if ( typeof define == 'function' && define.amd ) {
		define( 'picker', [ 'jquery' ], factory )
	}// Node.js/browserify.
	else {
		if ( typeof exports == 'object' ) {
			module.exports = factory( require( 'jquery' ) )
		}// Browser globals.
		else {
			this.Picker = factory( jQuery )
		}
	}

}( function( $ ) {

	var $window = $( window )
	var $document = $( document )
	var $html = $( document.documentElement )


	/**
	 * The picker constructor that creates a blank picker.
	 */
	function PickerConstructor( ELEMENT, NAME, COMPONENT, OPTIONS ) {

		// If there’s no element, return the picker constructor.
		if ( ! ELEMENT ) {
			return PickerConstructor
		}


		var
			IS_DEFAULT_THEME = false,


			// The state of the picker.
			STATE = {
				id: ELEMENT.id || 'P' + Math.abs( ~ ~ (Math.random() * new Date()) )
			},


			// Merge the defaults and options passed.
			SETTINGS = COMPONENT ? $.extend( true, {}, COMPONENT.defaults, OPTIONS ) : OPTIONS || {},


			// Merge the default classes with the settings classes.
			CLASSES = $.extend( {}, PickerConstructor.klasses(), SETTINGS.klass ),


			// The element node wrapper into a jQuery object.
			$ELEMENT = $( ELEMENT ),


			// Pseudo picker constructor.
			PickerInstance = function() {
				return this.start()
			},


			// The picker prototype.
			P = PickerInstance.prototype = {

				constructor: PickerInstance,

				$node: $ELEMENT,


				/**
				 * Initialize everything
				 */
				start: function() {

					// If it’s already started, do nothing.
					if ( STATE && STATE.start ) {
						return P
					}


					// Update the picker states.
					STATE.methods = {}
					STATE.start = true
					STATE.open = false
					STATE.type = ELEMENT.type


					// Confirm focus state, convert into text input to remove UA stylings,
					// and set as readonly to prevent keyboard popup.
					ELEMENT.autofocus = ELEMENT == getActiveElement()
					ELEMENT.readOnly = ! SETTINGS.editable
					ELEMENT.id = ELEMENT.id || STATE.id
					if ( ELEMENT.type != 'text' ) {
						ELEMENT.type = 'text'
					}


					// Create a new picker component with the settings.
					P.component = new COMPONENT( P, SETTINGS )


					// Create the picker root with a holder and then prepare it.
					P.$root = $( PickerConstructor._.node( 'div', createWrappedComponent(), CLASSES.picker, 'id="' + ELEMENT.id + '_root" tabindex="0"' ) )
					prepareElementRoot()


					// If there’s a format for the hidden input element, create the element.
					if ( SETTINGS.formatSubmit ) {
						prepareElementHidden()
					}


					// Prepare the input element.
					prepareElement()


					// Insert the root as specified in the settings.
					if ( SETTINGS.container ) {
						$( SETTINGS.container ).append( P.$root )
					} else {
						$ELEMENT.after( P.$root )
					}


					// Bind the default component and settings events.
					P.on( {
						start: P.component.onStart,
						render: P.component.onRender,
						stop: P.component.onStop,
						open: P.component.onOpen,
						close: P.component.onClose,
						set: P.component.onSet
					} ).on( {
						start: SETTINGS.onStart,
						render: SETTINGS.onRender,
						stop: SETTINGS.onStop,
						open: SETTINGS.onOpen,
						close: SETTINGS.onClose,
						set: SETTINGS.onSet
					} )


					// Once we’re all set, check the theme in use.
					IS_DEFAULT_THEME = isUsingDefaultTheme( P.$root.children()[ 0 ] )


					// If the element has autofocus, open the picker.
					if ( ELEMENT.autofocus ) {
						P.open()
					}


					// Trigger queued the “start” and “render” events.
					return P.trigger( 'start' ).trigger( 'render' )
				}, //start


				/**
				 * Render a new picker
				 */
				render: function( entireComponent ) {

					// Insert a new component holder in the root or box.
					if ( entireComponent ) {
						P.$root.html( createWrappedComponent() )
					} else {
						P.$root.find( '.' + CLASSES.box ).html( P.component.nodes( STATE.open ) )
					}

					// Trigger the queued “render” events.
					return P.trigger( 'render' )
				}, //render


				/**
				 * Destroy everything
				 */
				stop: function() {

					// If it’s already stopped, do nothing.
					if ( ! STATE.start ) {
						return P
					}

					// Then close the picker.
					P.close()

					// Remove the hidden field.
					if ( P._hidden ) {
						P._hidden.parentNode.removeChild( P._hidden )
					}

					// Remove the root.
					P.$root.remove()

					// Remove the input class, remove the stored data, and unbind
					// the events (after a tick for IE - see `P.close`).
					$ELEMENT.removeClass( CLASSES.input ).removeData( NAME )
					setTimeout( function() {
						$ELEMENT.off( '.' + STATE.id )
					}, 0 )

					// Restore the element state
					ELEMENT.type = STATE.type
					ELEMENT.readOnly = false

					// Trigger the queued “stop” events.
					P.trigger( 'stop' )

					// Reset the picker states.
					STATE.methods = {}
					STATE.start = false

					return P
				}, //stop


				/**
				 * Open up the picker
				 */
				open: function( dontGiveFocus ) {

					// If it’s already open, do nothing.
					if ( STATE.open ) {
						return P
					}

					// Add the “active” class.
					$ELEMENT.addClass( CLASSES.active )
					aria( ELEMENT, 'expanded', true )

					// * A Firefox bug, when `html` has `overflow:hidden`, results in
					//   killing transitions :(. So add the “opened” state on the next tick.
					//   Bug: https://bugzilla.mozilla.org/show_bug.cgi?id=625289
					setTimeout( function() {

						// Add the “opened” class to the picker root.
						P.$root.addClass( CLASSES.opened )
						aria( P.$root[ 0 ], 'hidden', false )

					}, 0 )

					// If we have to give focus, bind the element and doc events.
					if ( dontGiveFocus !== false ) {

						// Set it as open.
						STATE.open = true

						// Prevent the page from scrolling.
						if ( IS_DEFAULT_THEME ) {
							$html.
								css( 'overflow', 'hidden' ).
								css( 'padding-right', '+=' + getScrollbarWidth() )
						}

						// Pass focus to the root element’s jQuery object.
						// * Workaround for iOS8 to bring the picker’s root into view.
						P.$root.eq( 0 ).focus()

						// Bind the document events.
						$document.on( 'click.' + STATE.id + ' focusin.' + STATE.id, function( event ) {

							var target = event.target

							// If the target of the event is not the element, close the picker
							// picker. * Don’t worry about clicks or focusins on the root because
							// those don’t bubble up. Also, for Firefox, a click on an `option`
							// element bubbles up directly to the doc. So make sure the target
							// wasn't the doc. * In Firefox stopPropagation() doesn’t prevent
							// right-click events from bubbling, which causes the picker to
							// unexpectedly close when right-clicking it. So make sure the event
							// wasn’t a right-click.
							if ( target != ELEMENT && target != document && event.which != 3 ) {

								// If the target was the holder that covers the screen,
								// keep the element focused to maintain tabindex.
								P.close( target === P.$root.children()[ 0 ] )
							}

						} ).on( 'keydown.' + STATE.id, function( event ) {

							var
								// Get the keycode.
								keycode = event.keyCode,

								// Translate that to a selection change.
								keycodeToMove = P.component.key[ keycode ],

								// Grab the target.
								target = event.target


							// On escape, close the picker and give focus.
							if ( keycode == 27 ) {
								P.close( true )
							}


							// Check if there is a key movement or “enter” keypress on the element.
							else {
								if ( target == P.$root[ 0 ] && ( keycodeToMove || keycode == 13 ) ) {

									// Prevent the default action to stop page movement.
									event.preventDefault()

									// Trigger the key movement action.
									if ( keycodeToMove ) {
										PickerConstructor._.trigger( P.component.key.go, P, [ PickerConstructor._.trigger( keycodeToMove ) ] )
									}

									// On “enter”, if the highlighted item isn’t disabled, set the
									// value and close.
									else {
										if ( ! P.$root.find( '.' + CLASSES.highlighted ).hasClass( CLASSES.disabled ) ) {
											P.set( 'select', P.component.item.highlight ).close()
										}
									}
								}


								// If the target is within the root and “enter” is pressed,
								// prevent the default action and trigger a click on the target
								// instead.
								else {
									if ( $.contains( P.$root[ 0 ], target ) && keycode == 13 ) {
										event.preventDefault()
										target.click()
									}
								}
							}
						} )
					}

					// Trigger the queued “open” events.
					return P.trigger( 'open' )
				}, //open


				/**
				 * Close the picker
				 */
				close: function( giveFocus ) {

					// If we need to give focus, do it before changing states.
					if ( giveFocus ) {
						// ....ah yes! It would’ve been incomplete without a crazy workaround for
						// IE :| The focus is triggered *after* the close has completed - causing
						// it to open again. So unbind and rebind the event at the next tick.
						P.$root.off( 'focus.toOpen' ).eq( 0 ).focus()
						setTimeout( function() {
							P.$root.on( 'focus.toOpen', handleFocusToOpenEvent )
						}, 0 )
					}

					// Remove the “active” class.
					$ELEMENT.removeClass( CLASSES.active )
					aria( ELEMENT, 'expanded', false )

					// * A Firefox bug, when `html` has `overflow:hidden`, results in
					//   killing transitions :(. So remove the “opened” state on the next tick.
					//   Bug: https://bugzilla.mozilla.org/show_bug.cgi?id=625289
					setTimeout( function() {

						// Remove the “opened” and “focused” class from the picker root.
						P.$root.removeClass( CLASSES.opened + ' ' + CLASSES.focused )
						aria( P.$root[ 0 ], 'hidden', true )

					}, 0 )

					// If it’s already closed, do nothing more.
					if ( ! STATE.open ) {
						return P
					}

					// Set it as closed.
					STATE.open = false

					// Allow the page to scroll.
					if ( IS_DEFAULT_THEME ) {
						$html.
							css( 'overflow', '' ).
							css( 'padding-right', '-=' + getScrollbarWidth() )
					}

					// Unbind the document events.
					$document.off( '.' + STATE.id )

					// Trigger the queued “close” events.
					return P.trigger( 'close' )
				}, //close


				/**
				 * Clear the values
				 */
				clear: function( options ) {
					return P.set( 'clear', null, options )
				}, //clear


				/**
				 * Set something
				 */
				set: function( thing, value, options ) {

					var thingItem, thingValue,
						thingIsObject = $.isPlainObject( thing ),
						thingObject = thingIsObject ? thing : {}

					// Make sure we have usable options.
					options = thingIsObject && $.isPlainObject( value ) ? value : options || {}

					if ( thing ) {

						// If the thing isn’t an object, make it one.
						if ( ! thingIsObject ) {
							thingObject[ thing ] = value
						}

						// Go through the things of items to set.
						for ( thingItem in thingObject ) {

							// Grab the value of the thing.
							thingValue = thingObject[ thingItem ]

							// First, if the item exists and there’s a value, set it.
							if ( thingItem in P.component.item ) {
								if ( thingValue === undefined ) {
									thingValue = null
								}
								P.component.set( thingItem, thingValue, options )
							}

							// Then, check to update the element value and broadcast a change.
							if ( thingItem == 'select' || thingItem == 'clear' ) {
								$ELEMENT.
									val( thingItem == 'clear' ? '' : P.get( thingItem, SETTINGS.format ) ).
									trigger( 'change' )
							}
						}

						// Render a new picker.
						P.render()
					}

					// When the method isn’t muted, trigger queued “set” events and pass the
					// `thingObject`.
					return options.muted ? P : P.trigger( 'set', thingObject )
				}, //set


				/**
				 * Get something
				 */
				get: function( thing, format ) {

					// Make sure there’s something to get.
					thing = thing || 'value'

					// If a picker state exists, return that.
					if ( STATE[ thing ] != null ) {
						return STATE[ thing ]
					}

					// Return the submission value, if that.
					if ( thing == 'valueSubmit' ) {
						if ( P._hidden ) {
							return P._hidden.value
						}
						thing = 'value'
					}

					// Return the value, if that.
					if ( thing == 'value' ) {
						return ELEMENT.value
					}

					// Check if a component item exists, return that.
					if ( thing in P.component.item ) {
						if ( typeof format == 'string' ) {
							var thingValue = P.component.get( thing )
							return thingValue ?
								   PickerConstructor._.trigger(
									   P.component.formats.toString,
									   P.component,
									   [ format, thingValue ]
								   ) : ''
						}
						return P.component.get( thing )
					}
				}, //get



				/**
				 * Bind events on the things.
				 */
				on: function( thing, method, internal ) {

					var thingName, thingMethod,
						thingIsObject = $.isPlainObject( thing ),
						thingObject = thingIsObject ? thing : {}

					if ( thing ) {

						// If the thing isn’t an object, make it one.
						if ( ! thingIsObject ) {
							thingObject[ thing ] = method
						}

						// Go through the things to bind to.
						for ( thingName in thingObject ) {

							// Grab the method of the thing.
							thingMethod = thingObject[ thingName ]

							// If it was an internal binding, prefix it.
							if ( internal ) {
								thingName = '_' + thingName
							}

							// Make sure the thing methods collection exists.
							STATE.methods[ thingName ] = STATE.methods[ thingName ] || []

							// Add the method to the relative method collection.
							STATE.methods[ thingName ].push( thingMethod )
						}
					}

					return P
				}, //on



				/**
				 * Unbind events on the things.
				 */
				off: function() {
					var i, thingName,
						names = arguments;
					for ( i = 0, namesCount = names.length; i < namesCount; i += 1 ) {
						thingName = names[ i ]
						if ( thingName in STATE.methods ) {
							delete STATE.methods[ thingName ]
						}
					}
					return P
				},


				/**
				 * Fire off method events.
				 */
				trigger: function( name, data ) {
					var _trigger = function( name ) {
						var methodList = STATE.methods[ name ]
						if ( methodList ) {
							methodList.map( function( method ) {
								PickerConstructor._.trigger( method, P, [ data ] )
							} )
						}
					}
					_trigger( '_' + name )
					_trigger( name )
					return P
				} //trigger
			} //PickerInstance.prototype


		/**
		 * Wrap the picker holder components together.
		 */
		function createWrappedComponent() {

			// Create a picker wrapper holder
			return PickerConstructor._.node( 'div',

				// Create a picker wrapper node
				PickerConstructor._.node( 'div',

					// Create a picker frame
					PickerConstructor._.node( 'div',

						// Create a picker box node
						PickerConstructor._.node( 'div',

							// Create the components nodes.
							P.component.nodes( STATE.open ),

							// The picker box class
							CLASSES.box
						),

						// Picker wrap class
						CLASSES.wrap
					),

					// Picker frame class
					CLASSES.frame
				),

				// Picker holder class
				CLASSES.holder
			) //endreturn
		} //createWrappedComponent



		/**
		 * Prepare the input element with all bindings.
		 */
		function prepareElement() {

			$ELEMENT.

				// Store the picker data by component name.
				data( NAME, P ).

				// Add the “input” class name.
				addClass( CLASSES.input ).

				// Remove the tabindex.
				attr( 'tabindex', - 1 ).

				// If there’s a `data-value`, update the value of the element.
				val( $ELEMENT.data( 'value' ) ?
					 P.get( 'select', SETTINGS.format ) :
					 ELEMENT.value
				)


			// Only bind keydown events if the element isn’t editable.
			if ( ! SETTINGS.editable ) {

				$ELEMENT.

					// On focus/click, focus onto the root to open it up.
					on( 'focus.' + STATE.id + ' click.' + STATE.id, function( event ) {
						event.preventDefault()
						P.$root.eq( 0 ).focus()
					} ).

					// Handle keyboard event based on the picker being opened or not.
					on( 'keydown.' + STATE.id, handleKeydownEvent )
			}


			// Update the aria attributes.
			aria( ELEMENT, {
				haspopup: true,
				expanded: false,
				readonly: false,
				owns: ELEMENT.id + '_root'
			} )
		}


		/**
		 * Prepare the root picker element with all bindings.
		 */
		function prepareElementRoot() {

			P.$root.

				on( {

					// For iOS8.
					keydown: handleKeydownEvent,

					// When something within the root is focused, stop from bubbling
					// to the doc and remove the “focused” state from the root.
					focusin: function( event ) {
						P.$root.removeClass( CLASSES.focused )
						event.stopPropagation()
					},

					// When something within the root holder is clicked, stop it
					// from bubbling to the doc.
					'mousedown click': function( event ) {

						var target = event.target

						// Make sure the target isn’t the root holder so it can bubble up.
						if ( target != P.$root.children()[ 0 ] ) {

							event.stopPropagation()

							// * For mousedown events, cancel the default action in order to
							//   prevent cases where focus is shifted onto external elements
							//   when using things like jQuery mobile or MagnificPopup (ref: #249
							// & #120). Also, for Firefox, don’t prevent action on the `option`
							// element.
							if ( event.type == 'mousedown' && ! $( target ).is( 'input, select, textarea, button, option' ) ) {

								event.preventDefault()

								// Re-focus onto the root so that users can click away
								// from elements focused within the picker.
								P.$root.eq( 0 ).focus()
							}
						}
					}
				} ).

				// Add/remove the “target” class on focus and blur.
				on( {
					focus: function() {
						$ELEMENT.addClass( CLASSES.target )
					},
					blur: function() {
						$ELEMENT.removeClass( CLASSES.target )
					}
				} ).

				// Open the picker and adjust the root “focused” state
				on( 'focus.toOpen', handleFocusToOpenEvent ).

				// If there’s a click on an actionable element, carry out the actions.
				on( 'click', '[data-pick], [data-nav], [data-clear], [data-close]', function() {

					var $target = $( this ),
						targetData = $target.data(),
						targetDisabled = $target.hasClass( CLASSES.navDisabled ) || $target.hasClass( CLASSES.disabled ),

						// * For IE, non-focusable elements can be active elements as well
						//   (http://stackoverflow.com/a/2684561).
						activeElement = getActiveElement()
					activeElement = activeElement && ( activeElement.type || activeElement.href )

					// If it’s disabled or nothing inside is actively focused, re-focus the
					// element.
					if ( targetDisabled || activeElement && ! $.contains( P.$root[ 0 ], activeElement ) ) {
						P.$root.eq( 0 ).focus()
					}

					// If something is superficially changed, update the `highlight` based on the
					// `nav`.
					if ( ! targetDisabled && targetData.nav ) {
						P.set( 'highlight', P.component.item.highlight, { nav: targetData.nav } )
					}

					// If something is picked, set `select` then close with focus.
					else {
						if ( ! targetDisabled && 'pick' in targetData ) {
							P.set( 'select', targetData.pick )
						}

						// If a “clear” button is pressed, empty the values and close with focus.
						else {
							if ( targetData.clear ) {
								P.clear().close( true )
							}

							else {
								if ( targetData.close ) {
									P.close( true )
								}
							}
						}
					}

				} ) //P.$root

			aria( P.$root[ 0 ], 'hidden', true )
		}


		/**
		 * Prepare the hidden input element along with all bindings.
		 */
		function prepareElementHidden() {

			var name

			if ( SETTINGS.hiddenName === true ) {
				name = ELEMENT.name
				ELEMENT.name = ''
			}
			else {
				name = [
					typeof SETTINGS.hiddenPrefix == 'string' ? SETTINGS.hiddenPrefix : '',
					typeof SETTINGS.hiddenSuffix == 'string' ? SETTINGS.hiddenSuffix : '_submit'
				]
				name = name[ 0 ] + ELEMENT.name + name[ 1 ]
			}

			P._hidden = $(
				'<input ' +
				'type=hidden ' +

				// Create the name using the original input’s with a prefix and suffix.
				'name="' + name + '"' +

				// If the element has a value, set the hidden value as well.
				(
					$ELEMENT.data( 'value' ) || ELEMENT.value ?
					' value="' + P.get( 'select', SETTINGS.formatSubmit ) + '"' :
					''
				) +
				'>'
			)[ 0 ]

			$ELEMENT.

				// If the value changes, update the hidden input with the correct format.
				on( 'change.' + STATE.id, function() {
					P._hidden.value = ELEMENT.value ?
									  P.get( 'select', SETTINGS.formatSubmit ) :
									  ''
				} )


			// Insert the hidden input as specified in the settings.
			if ( SETTINGS.container ) {
				$( SETTINGS.container ).append( P._hidden )
			} else {
				$ELEMENT.after( P._hidden )
			}
		}


		// For iOS8.
		function handleKeydownEvent( event ) {

			var keycode = event.keyCode,

				// Check if one of the delete keys was pressed.
				isKeycodeDelete = /^(8|46)$/.test( keycode )

			// For some reason IE clears the input value on “escape”.
			if ( keycode == 27 ) {
				P.close()
				return false
			}

			// Check if `space` or `delete` was pressed or the picker is closed with a key
			// movement.
			if ( keycode == 32 || isKeycodeDelete || ! STATE.open && P.component.key[ keycode ] ) {

				// Prevent it from moving the page and bubbling to doc.
				event.preventDefault()
				event.stopPropagation()

				// If `delete` was pressed, clear the values and close the picker.
				// Otherwise open the picker.
				if ( isKeycodeDelete ) {
					P.clear().close()
				}
				else {
					P.open()
				}
			}
		}


		// Separated for IE
		function handleFocusToOpenEvent( event ) {

			// Stop the event from propagating to the doc.
			event.stopPropagation()

			// If it’s a focus event, add the “focused” class to the root.
			if ( event.type == 'focus' ) {
				P.$root.addClass( CLASSES.focused )
			}

			// And then finally open the picker.
			P.open()
		}


		// Return a new picker instance.
		return new PickerInstance()
	} //PickerConstructor



	/**
	 * The default classes and prefix to use for the HTML classes.
	 */
	PickerConstructor.klasses = function( prefix ) {
		prefix = prefix || 'picker'
		return {

			picker: prefix,
			opened: prefix + '--opened',
			focused: prefix + '--focused',

			input: prefix + '__input',
			active: prefix + '__input--active',
			target: prefix + '__input--target',

			holder: prefix + '__holder',

			frame: prefix + '__frame',
			wrap: prefix + '__wrap',

			box: prefix + '__box'
		}
	} //PickerConstructor.klasses



	/**
	 * Check if the default theme is being used.
	 */
	function isUsingDefaultTheme( element ) {

		var theme,
			prop = 'position'

		// For IE.
		if ( element.currentStyle ) {
			theme = element.currentStyle[ prop ]
		}

		// For normal browsers.
		else {
			if ( window.getComputedStyle ) {
				theme = getComputedStyle( element )[ prop ]
			}
		}

		return theme == 'fixed'
	}



	/**
	 * Get the width of the browser’s scrollbar.
	 * Taken from: https://github.com/VodkaBears/Remodal/blob/master/src/jquery.remodal.js
	 */
	function getScrollbarWidth() {

		if ( $html.height() <= $window.height() ) {
			return 0
		}

		var $outer = $( '<div style="visibility:hidden;width:100px" />' ).
			appendTo( 'body' )

		// Get the width without scrollbars.
		var widthWithoutScroll = $outer[ 0 ].offsetWidth

		// Force adding scrollbars.
		$outer.css( 'overflow', 'scroll' )

		// Add the inner div.
		var $inner = $( '<div style="width:100%" />' ).appendTo( $outer )

		// Get the width with scrollbars.
		var widthWithScroll = $inner[ 0 ].offsetWidth

		// Remove the divs.
		$outer.remove()

		// Return the difference between the widths.
		return widthWithoutScroll - widthWithScroll
	}



	/**
	 * PickerConstructor helper methods.
	 */
	PickerConstructor._ = {

		/**
		 * Create a group of nodes. Expects:
		 * `
		 {
            min:    {Integer},
            max:    {Integer},
            i:      {Integer},
            node:   {String},
            item:   {Function}
        }
		 * `
		 */
		group: function( groupObject ) {

			var
				// Scope for the looped object
				loopObjectScope,

				// Create the nodes list
				nodesList = '',

				// The counter starts from the `min`
				counter = PickerConstructor._.trigger( groupObject.min, groupObject )


			// Loop from the `min` to `max`, incrementing by `i`
			for ( ; counter <= PickerConstructor._.trigger( groupObject.max, groupObject, [ counter ] ); counter += groupObject.i ) {

				// Trigger the `item` function within scope of the object
				loopObjectScope = PickerConstructor._.trigger( groupObject.item, groupObject, [ counter ] )

				// Splice the subgroup and create nodes out of the sub nodes
				nodesList += PickerConstructor._.node(
					groupObject.node,
					loopObjectScope[ 0 ],   // the node
					loopObjectScope[ 1 ],   // the classes
					loopObjectScope[ 2 ]    // the attributes
				)
			}

			// Return the list of nodes
			return nodesList
		}, //group


		/**
		 * Create a dom node string
		 */
		node: function( wrapper, item, klass, attribute ) {

			// If the item is false-y, just return an empty string
			if ( ! item ) {
				return ''
			}

			// If the item is an array, do a join
			item = $.isArray( item ) ? item.join( '' ) : item

			// Check for the class
			klass = klass ? ' class="' + klass + '"' : ''

			// Check for any attributes
			attribute = attribute ? ' ' + attribute : ''

			// Return the wrapped item
			return '<' + wrapper + klass + attribute + '>' + item + '</' + wrapper + '>'
		}, //node


		/**
		 * Lead numbers below 10 with a zero.
		 */
		lead: function( number ) {
			return ( number < 10 ? '0' : '' ) + number
		},


		/**
		 * Trigger a function otherwise return the value.
		 */
		trigger: function( callback, scope, args ) {
			return typeof callback == 'function' ? callback.apply( scope, args || [] ) : callback
		},


		/**
		 * If the second character is a digit, length is 2 otherwise 1.
		 */
		digits: function( string ) {
			return ( /\d/ ).test( string[ 1 ] ) ? 2 : 1
		},


		/**
		 * Tell if something is a date object.
		 */
		isDate: function( value ) {
			return {}.toString.call( value ).indexOf( 'Date' ) > - 1 && this.isInteger( value.getDate() )
		},


		/**
		 * Tell if something is an integer.
		 */
		isInteger: function( value ) {
			return {}.toString.call( value ).indexOf( 'Number' ) > - 1 && value % 1 === 0
		},


		/**
		 * Create ARIA attribute strings.
		 */
		ariaAttr: ariaAttr
	} //PickerConstructor._



	/**
	 * Extend the picker with a component and defaults.
	 */
	PickerConstructor.extend = function( name, Component ) {

		// Extend jQuery.
		$.fn[ name ] = function( options, action ) {

			// Grab the component data.
			var componentData = this.data( name )

			// If the picker is requested, return the data object.
			if ( options == 'picker' ) {
				return componentData
			}

			// If the component data exists and `options` is a string, carry out the action.
			if ( componentData && typeof options == 'string' ) {
				return PickerConstructor._.trigger( componentData[ options ], componentData, [ action ] )
			}

			// Otherwise go through each matched element and if the component
			// doesn’t exist, create a new picker using `this` element
			// and merging the defaults and options with a deep copy.
			return this.each( function() {
				var $this = $( this )
				if ( ! $this.data( name ) ) {
					new PickerConstructor( this, name, Component, options )
				}
			} )
		}

		// Set the defaults.
		$.fn[ name ].defaults = Component.defaults
	} //PickerConstructor.extend



	function aria( element, attribute, value ) {
		if ( $.isPlainObject( attribute ) ) {
			for ( var key in attribute ) {
				ariaSet( element, key, attribute[ key ] )
			}
		}
		else {
			ariaSet( element, attribute, value )
		}
	}

	function ariaSet( element, attribute, value ) {
		element.setAttribute(
			(attribute == 'role' ? '' : 'aria-') + attribute,
			value
		)
	}

	function ariaAttr( attribute, data ) {
		if ( ! $.isPlainObject( attribute ) ) {
			attribute = { attribute: data }
		}
		data = ''
		for ( var key in attribute ) {
			var attr = (key == 'role' ? '' : 'aria-') + key,
				attrVal = attribute[ key ]
			data += attrVal == null ? '' : attr + '="' + attribute[ key ] + '"'
		}
		return data
	}

	// IE8 bug throws an error for activeElements within iframes.
	function getActiveElement() {
		try {
			return document.activeElement
		} catch ( err ) {
		}
	}



	// Expose the picker constructor.
	return PickerConstructor


} ));


;/*!
 * Date picker for pickadate.js v3.5.0
 * http://amsul.github.io/pickadate.js/date.htm
 */

(function( factory ) {

	// AMD.
	if ( typeof define == 'function' && define.amd ) {
		define( [ 'picker', 'jquery' ], factory )
	}// Node.js/browserify.
	else {
		if ( typeof exports == 'object' ) {
			module.exports = factory( require( './picker.js' ), require( 'jquery' ) )
		}// Browser globals.
		else {
			factory( Picker, jQuery )
		}
	}

}( function( Picker, $ ) {


	/**
	 * Globals and constants
	 */
	var DAYS_IN_WEEK = 7,
		WEEKS_IN_CALENDAR = 6,
		_ = Picker._



	/**
	 * The date picker constructor
	 */
	function DatePicker( picker, settings ) {

		var calendar = this,
			element = picker.$node[ 0 ],
			elementValue = element.value,
			elementDataValue = picker.$node.data( 'value' ),
			valueString = elementDataValue || elementValue,
			formatString = elementDataValue ? settings.formatSubmit : settings.format,
			isRTL = function() {

				return element.currentStyle ?

					// For IE.
					   element.currentStyle.direction == 'rtl' :

					// For normal browsers.
					   getComputedStyle( picker.$root[ 0 ] ).direction == 'rtl'
			}

		calendar.settings = settings
		calendar.$node = picker.$node

		// The queue of methods that will be used to build item objects.
		calendar.queue = {
			min: 'measure create',
			max: 'measure create',
			now: 'now create',
			select: 'parse create validate',
			highlight: 'parse navigate create validate',
			view: 'parse create validate viewset',
			disable: 'deactivate',
			enable: 'activate'
		}

		// The component's item object.
		calendar.item = {}

		calendar.item.clear = null
		calendar.item.disable = ( settings.disable || [] ).slice( 0 )
		calendar.item.enable = - (function( collectionDisabled ) {
			return collectionDisabled[ 0 ] === true ? collectionDisabled.shift() : - 1
		})( calendar.item.disable )

		calendar.
			set( 'min', settings.min ).
			set( 'max', settings.max ).
			set( 'now' )

		// When there’s a value, set the `select`, which in turn
		// also sets the `highlight` and `view`.
		if ( valueString ) {
			calendar.set( 'select', valueString, { format: formatString } )
		}

		// If there’s no value, default to highlighting “today”.
		else {
			calendar.
				set( 'select', null ).
				set( 'highlight', calendar.item.now )
		}


		// The keycode to movement mapping.
		calendar.key = {
			40: 7, // Down
			38: - 7, // Up
			39: function() {
				return isRTL() ? - 1 : 1
			}, // Right
			37: function() {
				return isRTL() ? 1 : - 1
			}, // Left
			go: function( timeChange ) {
				var highlightedObject = calendar.item.highlight,
					targetDate = new Date( highlightedObject.year, highlightedObject.month, highlightedObject.date + timeChange )
				calendar.set(
					'highlight',
					targetDate,
					{ interval: timeChange }
				)
				this.render()
			}
		}


		// Bind some picker events.
		picker.
			on( 'render', function() {
				picker.$root.find( '.' + settings.klass.selectMonth ).on( 'change', function() {
					var value = this.value
					if ( value ) {
						picker.set( 'highlight', [ picker.get( 'view' ).year, value, picker.get( 'highlight' ).date ] )
						picker.$root.find( '.' + settings.klass.selectMonth ).trigger( 'focus' )
					}
				} )
				picker.$root.find( '.' + settings.klass.selectYear ).on( 'change', function() {
					var value = this.value
					if ( value ) {
						picker.set( 'highlight', [ value, picker.get( 'view' ).month, picker.get( 'highlight' ).date ] )
						picker.$root.find( '.' + settings.klass.selectYear ).trigger( 'focus' )
					}
				} )
			}, 1 ).
			on( 'open', function() {
				var includeToday = ''
				if ( calendar.disabled( calendar.get( 'now' ) ) ) {
					includeToday = ':not(.' + settings.klass.buttonToday + ')'
				}
				picker.$root.find( 'button' + includeToday + ', select' ).attr( 'disabled', false )
			}, 1 ).
			on( 'close', function() {
				picker.$root.find( 'button, select' ).attr( 'disabled', true )
			}, 1 )

	} //DatePicker


	/**
	 * Set a datepicker item object.
	 */
	DatePicker.prototype.set = function( type, value, options ) {

		var calendar = this,
			calendarItem = calendar.item

		// If the value is `null` just set it immediately.
		if ( value === null ) {
			if ( type == 'clear' ) {
				type = 'select'
			}
			calendarItem[ type ] = value
			return calendar
		}

		// Otherwise go through the queue of methods, and invoke the functions.
		// Update this as the time unit, and set the final value as this item.
		// * In the case of `enable`, keep the queue but set `disable` instead.
		//   And in the case of `flip`, keep the queue but set `enable` instead.
		calendarItem[ ( type == 'enable' ? 'disable' : type == 'flip' ? 'enable' : type ) ] = calendar.queue[ type ].split( ' ' ).map( function( method ) {
			value = calendar[ method ]( type, value, options )
			return value
		} ).pop()

		// Check if we need to cascade through more updates.
		if ( type == 'select' ) {
			calendar.set( 'highlight', calendarItem.select, options )
		}
		else {
			if ( type == 'highlight' ) {
				calendar.set( 'view', calendarItem.highlight, options )
			}
			else {
				if ( type.match( /^(flip|min|max|disable|enable)$/ ) ) {
					if ( calendarItem.select && calendar.disabled( calendarItem.select ) ) {
						calendar.set( 'select', calendarItem.select, options )
					}
					if ( calendarItem.highlight && calendar.disabled( calendarItem.highlight ) ) {
						calendar.set( 'highlight', calendarItem.highlight, options )
					}
				}
			}
		}

		return calendar
	} //DatePicker.prototype.set


	/**
	 * Get a datepicker item object.
	 */
	DatePicker.prototype.get = function( type ) {
		return this.item[ type ]
	} //DatePicker.prototype.get


	/**
	 * Create a picker date object.
	 */
	DatePicker.prototype.create = function( type, value, options ) {

		var isInfiniteValue,
			calendar = this

		// If there’s no value, use the type as the value.
		value = value === undefined ? type : value


		// If it’s infinity, update the value.
		if ( value == - Infinity || value == Infinity ) {
			isInfiniteValue = value
		}

		// If it’s an object, use the native date object.
		else {
			if ( $.isPlainObject( value ) && _.isInteger( value.pick ) ) {
				value = value.obj
			}

			// If it’s an array, convert it into a date and make sure
			// that it’s a valid date – otherwise default to today.
			else {
				if ( $.isArray( value ) ) {
					value = new Date( value[ 0 ], value[ 1 ], value[ 2 ] )
					value = _.isDate( value ) ? value : calendar.create().obj
				}

				// If it’s a number or date object, make a normalized date.
				else {
					if ( _.isInteger( value ) || _.isDate( value ) ) {
						value = calendar.normalize( new Date( value ), options )
					}

					// If it’s a literal true or any other case, set it to now.
					else /*if ( value === true )*/ {
						value = calendar.now( type, value, options )
					}
				}
			}
		}

		// Return the compiled object.
		return {
			year: isInfiniteValue || value.getFullYear(),
			month: isInfiniteValue || value.getMonth(),
			date: isInfiniteValue || value.getDate(),
			day: isInfiniteValue || value.getDay(),
			obj: isInfiniteValue || value,
			pick: isInfiniteValue || value.getTime()
		}
	} //DatePicker.prototype.create


	/**
	 * Create a range limit object using an array, date object,
	 * literal “true”, or integer relative to another time.
	 */
	DatePicker.prototype.createRange = function( from, to ) {

		var calendar = this,
			createDate = function( date ) {
				if ( date === true || $.isArray( date ) || _.isDate( date ) ) {
					return calendar.create( date )
				}
				return date
			}

		// Create objects if possible.
		if ( ! _.isInteger( from ) ) {
			from = createDate( from )
		}
		if ( ! _.isInteger( to ) ) {
			to = createDate( to )
		}

		// Create relative dates.
		if ( _.isInteger( from ) && $.isPlainObject( to ) ) {
			from = [ to.year, to.month, to.date + from ];
		}
		else {
			if ( _.isInteger( to ) && $.isPlainObject( from ) ) {
				to = [ from.year, from.month, from.date + to ];
			}
		}

		return {
			from: createDate( from ),
			to: createDate( to )
		}
	} //DatePicker.prototype.createRange


	/**
	 * Check if a date unit falls within a date range object.
	 */
	DatePicker.prototype.withinRange = function( range, dateUnit ) {
		range = this.createRange( range.from, range.to )
		return dateUnit.pick >= range.from.pick && dateUnit.pick <= range.to.pick
	}


	/**
	 * Check if two date range objects overlap.
	 */
	DatePicker.prototype.overlapRanges = function( one, two ) {

		var calendar = this

		// Convert the ranges into comparable dates.
		one = calendar.createRange( one.from, one.to )
		two = calendar.createRange( two.from, two.to )

		return calendar.withinRange( one, two.from ) || calendar.withinRange( one, two.to ) ||
			calendar.withinRange( two, one.from ) || calendar.withinRange( two, one.to )
	}


	/**
	 * Get the date today.
	 */
	DatePicker.prototype.now = function( type, value, options ) {
		value = new Date()
		if ( options && options.rel ) {
			value.setDate( value.getDate() + options.rel )
		}
		return this.normalize( value, options )
	}


	/**
	 * Navigate to next/prev month.
	 */
	DatePicker.prototype.navigate = function( type, value, options ) {

		var targetDateObject,
			targetYear,
			targetMonth,
			targetDate,
			isTargetArray = $.isArray( value ),
			isTargetObject = $.isPlainObject( value ),
			viewsetObject = this.item.view
		/*,
		 safety = 100*/


		if ( isTargetArray || isTargetObject ) {

			if ( isTargetObject ) {
				targetYear = value.year
				targetMonth = value.month
				targetDate = value.date
			}
			else {
				targetYear = + value[ 0 ]
				targetMonth = + value[ 1 ]
				targetDate = + value[ 2 ]
			}

			// If we’re navigating months but the view is in a different
			// month, navigate to the view’s year and month.
			if ( options && options.nav && viewsetObject && viewsetObject.month !== targetMonth ) {
				targetYear = viewsetObject.year
				targetMonth = viewsetObject.month
			}

			// Figure out the expected target year and month.
			targetDateObject = new Date( targetYear, targetMonth + ( options && options.nav ? options.nav : 0 ), 1 )
			targetYear = targetDateObject.getFullYear()
			targetMonth = targetDateObject.getMonth()

			// If the month we’re going to doesn’t have enough days,
			// keep decreasing the date until we reach the month’s last date.
			while ( /*safety &&*/ new Date( targetYear, targetMonth, targetDate ).getMonth() !== targetMonth ) {
				targetDate -= 1
				/*safety -= 1
				 if ( !safety ) {
				 throw 'Fell into an infinite loop while navigating to ' + new Date( targetYear, targetMonth, targetDate ) + '.'
				 }*/
			}

			value = [ targetYear, targetMonth, targetDate ]
		}

		return value
	} //DatePicker.prototype.navigate


	/**
	 * Normalize a date by setting the hours to midnight.
	 */
	DatePicker.prototype.normalize = function( value/*, options*/ ) {
		value.setHours( 0, 0, 0, 0 )
		return value
	}


	/**
	 * Measure the range of dates.
	 */
	DatePicker.prototype.measure = function( type, value/*, options*/ ) {

		var calendar = this

		// If it’s anything false-y, remove the limits.
		if ( ! value ) {
			value = type == 'min' ? - Infinity : Infinity
		}

		// If it’s a string, parse it.
		else {
			if ( typeof value == 'string' ) {
				value = calendar.parse( type, value )
			}

			// If it's an integer, get a date relative to today.
			else {
				if ( _.isInteger( value ) ) {
					value = calendar.now( type, value, { rel: value } )
				}
			}
		}

		return value
	} ///DatePicker.prototype.measure


	/**
	 * Create a viewset object based on navigation.
	 */
	DatePicker.prototype.viewset = function( type, dateObject/*, options*/ ) {
		return this.create( [ dateObject.year, dateObject.month, 1 ] )
	}


	/**
	 * Validate a date as enabled and shift if needed.
	 */
	DatePicker.prototype.validate = function( type, dateObject, options ) {

		var calendar = this,

			// Keep a reference to the original date.
			originalDateObject = dateObject,

			// Make sure we have an interval.
			interval = options && options.interval ? options.interval : 1,

			// Check if the calendar enabled dates are inverted.
			isFlippedBase = calendar.item.enable === - 1,

			// Check if we have any enabled dates after/before now.
			hasEnabledBeforeTarget, hasEnabledAfterTarget,

			// The min & max limits.
			minLimitObject = calendar.item.min,
			maxLimitObject = calendar.item.max,

			// Check if we’ve reached the limit during shifting.
			reachedMin, reachedMax,

			// Check if the calendar is inverted and at least one weekday is enabled.
			hasEnabledWeekdays = isFlippedBase && calendar.item.disable.filter( function( value ) {

					// If there’s a date, check where it is relative to the target.
					if ( $.isArray( value ) ) {
						var dateTime = calendar.create( value ).pick
						if ( dateTime < dateObject.pick ) {
							hasEnabledBeforeTarget = true
						} else {
							if ( dateTime > dateObject.pick ) {
								hasEnabledAfterTarget = true
							}
						}
					}

					// Return only integers for enabled weekdays.
					return _.isInteger( value )
				} ).length
		/*,

		 safety = 100*/



		// Cases to validate for:
		// [1] Not inverted and date disabled.
		// [2] Inverted and some dates enabled.
		// [3] Not inverted and out of range.
		//
		// Cases to **not** validate for:
		// • Navigating months.
		// • Not inverted and date enabled.
		// • Inverted and all dates disabled.
		// • ..and anything else.
		if ( ! options || ! options.nav ) {
			if (
				/* 1 */ ( ! isFlippedBase && calendar.disabled( dateObject ) ) ||
			/* 2 */ ( isFlippedBase && calendar.disabled( dateObject ) && ( hasEnabledWeekdays || hasEnabledBeforeTarget || hasEnabledAfterTarget ) ) ||
			/* 3 */ ( ! isFlippedBase && (dateObject.pick <= minLimitObject.pick || dateObject.pick >= maxLimitObject.pick) )
			) {


				// When inverted, flip the direction if there aren’t any enabled weekdays
				// and there are no enabled dates in the direction of the interval.
				if ( isFlippedBase && ! hasEnabledWeekdays && ( ( ! hasEnabledAfterTarget && interval > 0 ) || ( ! hasEnabledBeforeTarget && interval < 0 ) ) ) {
					interval *= - 1
				}


				// Keep looping until we reach an enabled date.
				while ( /*safety &&*/ calendar.disabled( dateObject ) ) {

					/*safety -= 1
					 if ( !safety ) {
					 throw 'Fell into an infinite loop while validating ' + dateObject.obj + '.'
					 }*/


					// If we’ve looped into the next/prev month with a large interval, return to
					// the original date and flatten the interval.
					if ( Math.abs( interval ) > 1 && ( dateObject.month < originalDateObject.month || dateObject.month > originalDateObject.month ) ) {
						dateObject = originalDateObject
						interval = interval > 0 ? 1 : - 1
					}


					// If we’ve reached the min/max limit, reverse the direction, flatten the
					// interval and set it to the limit.
					if ( dateObject.pick <= minLimitObject.pick ) {
						reachedMin = true
						interval = 1
						dateObject = calendar.create( [
							minLimitObject.year,
							minLimitObject.month,
							minLimitObject.date + (dateObject.pick === minLimitObject.pick ? 0 : - 1)
						] )
					}
					else {
						if ( dateObject.pick >= maxLimitObject.pick ) {
							reachedMax = true
							interval = - 1
							dateObject = calendar.create( [
								maxLimitObject.year,
								maxLimitObject.month,
								maxLimitObject.date + (dateObject.pick === maxLimitObject.pick ? 0 : 1)
							] )
						}
					}


					// If we’ve reached both limits, just break out of the loop.
					if ( reachedMin && reachedMax ) {
						break
					}


					// Finally, create the shifted date using the interval and keep looping.
					dateObject = calendar.create( [ dateObject.year, dateObject.month, dateObject.date + interval ] )
				}

			}
		} //endif


		// Return the date object settled on.
		return dateObject
	} //DatePicker.prototype.validate


	/**
	 * Check if a date is disabled.
	 */
	DatePicker.prototype.disabled = function( dateToVerify ) {

		var
			calendar = this,

			// Filter through the disabled dates to check if this is one.
			isDisabledMatch = calendar.item.disable.filter( function( dateToDisable ) {

				// If the date is a number, match the weekday with 0index and `firstDay` check.
				if ( _.isInteger( dateToDisable ) ) {
					return dateToVerify.day === ( calendar.settings.firstDay ? dateToDisable : dateToDisable - 1 ) % 7
				}

				// If it’s an array or a native JS date, create and match the exact date.
				if ( $.isArray( dateToDisable ) || _.isDate( dateToDisable ) ) {
					return dateToVerify.pick === calendar.create( dateToDisable ).pick
				}

				// If it’s an object, match a date within the “from” and “to” range.
				if ( $.isPlainObject( dateToDisable ) ) {
					return calendar.withinRange( dateToDisable, dateToVerify )
				}
			} )

		// If this date matches a disabled date, confirm it’s not inverted.
		isDisabledMatch = isDisabledMatch.length && ! isDisabledMatch.filter( function( dateToDisable ) {
				return $.isArray( dateToDisable ) && dateToDisable[ 3 ] == 'inverted' ||
					$.isPlainObject( dateToDisable ) && dateToDisable.inverted
			} ).length

		// Check the calendar “enabled” flag and respectively flip the
		// disabled state. Then also check if it’s beyond the min/max limits.
		return calendar.item.enable === - 1 ? ! isDisabledMatch : isDisabledMatch ||
		dateToVerify.pick < calendar.item.min.pick ||
		dateToVerify.pick > calendar.item.max.pick

	} //DatePicker.prototype.disabled


	/**
	 * Parse a string into a usable type.
	 */
	DatePicker.prototype.parse = function( type, value, options ) {

		var calendar = this,
			parsingObject = {}

		// If it’s already parsed, we’re good.
		if ( ! value || typeof value != 'string' ) {
			return value
		}

		// We need a `.format` to parse the value with.
		if ( ! ( options && options.format ) ) {
			options = options || {}
			options.format = calendar.settings.format
		}

		// Convert the format into an array and then map through it.
		calendar.formats.toArray( options.format ).map( function( label ) {

			var
				// Grab the formatting label.
				formattingLabel = calendar.formats[ label ],

				// The format length is from the formatting label function or the
				// label length without the escaping exclamation (!) mark.
				formatLength = formattingLabel ? _.trigger( formattingLabel, calendar, [ value, parsingObject ] ) : label.replace( /^!/, '' ).length

			// If there's a format label, split the value up to the format length.
			// Then add it to the parsing object with appropriate label.
			if ( formattingLabel ) {
				parsingObject[ label ] = value.substr( 0, formatLength )
			}

			// Update the value as the substring from format length to end.
			value = value.substr( formatLength )
		} )

		// Compensate for month 0index.
		return [
			parsingObject.yyyy || parsingObject.yy,
			+ ( parsingObject.mm || parsingObject.m ) - 1,
			parsingObject.dd || parsingObject.d
		]
	} //DatePicker.prototype.parse


	/**
	 * Various formats to display the object in.
	 */
	DatePicker.prototype.formats = (function() {

		// Return the length of the first word in a collection.
		function getWordLengthFromCollection( string, collection, dateObject ) {

			// Grab the first word from the string.
			var word = string.match( /\w+/ )[ 0 ]

			// If there's no month index, add it to the date object
			if ( ! dateObject.mm && ! dateObject.m ) {
				dateObject.m = collection.indexOf( word ) + 1
			}

			// Return the length of the word.
			return word.length
		}

		// Get the length of the first word in a string.
		function getFirstWordLength( string ) {
			return string.match( /\w+/ )[ 0 ].length
		}

		return {

			d: function( string, dateObject ) {

				// If there's string, then get the digits length.
				// Otherwise return the selected date.
				return string ? _.digits( string ) : dateObject.date
			},
			dd: function( string, dateObject ) {

				// If there's a string, then the length is always 2.
				// Otherwise return the selected date with a leading zero.
				return string ? 2 : _.lead( dateObject.date )
			},
			ddd: function( string, dateObject ) {

				// If there's a string, then get the length of the first word.
				// Otherwise return the short selected weekday.
				return string ? getFirstWordLength( string ) : this.settings.weekdaysShort[ dateObject.day ]
			},
			dddd: function( string, dateObject ) {

				// If there's a string, then get the length of the first word.
				// Otherwise return the full selected weekday.
				return string ? getFirstWordLength( string ) : this.settings.weekdaysFull[ dateObject.day ]
			},
			m: function( string, dateObject ) {

				// If there's a string, then get the length of the digits
				// Otherwise return the selected month with 0index compensation.
				return string ? _.digits( string ) : dateObject.month + 1
			},
			mm: function( string, dateObject ) {

				// If there's a string, then the length is always 2.
				// Otherwise return the selected month with 0index and leading zero.
				return string ? 2 : _.lead( dateObject.month + 1 )
			},
			mmm: function( string, dateObject ) {

				var collection = this.settings.monthsShort

				// If there's a string, get length of the relevant month from the short
				// months collection. Otherwise return the selected month from that collection.
				return string ? getWordLengthFromCollection( string, collection, dateObject ) : collection[ dateObject.month ]
			},
			mmmm: function( string, dateObject ) {

				var collection = this.settings.monthsFull

				// If there's a string, get length of the relevant month from the full
				// months collection. Otherwise return the selected month from that collection.
				return string ? getWordLengthFromCollection( string, collection, dateObject ) : collection[ dateObject.month ]
			},
			yy: function( string, dateObject ) {

				// If there's a string, then the length is always 2.
				// Otherwise return the selected year by slicing out the first 2 digits.
				return string ? 2 : ( '' + dateObject.year ).slice( 2 )
			},
			yyyy: function( string, dateObject ) {

				// If there's a string, then the length is always 4.
				// Otherwise return the selected year.
				return string ? 4 : dateObject.year
			},

			// Create an array by splitting the formatting string passed.
			toArray: function( formatString ) {
				return formatString.split( /(d{1,4}|m{1,4}|y{4}|yy|!.)/g )
			},

			// Format an object into a string using the formatting options.
			toString: function( formatString, itemObject ) {
				var calendar = this
				return calendar.formats.toArray( formatString ).map( function( label ) {
					return _.trigger( calendar.formats[ label ], calendar, [ 0, itemObject ] ) || label.replace( /^!/, '' )
				} ).join( '' )
			}
		}
	})() //DatePicker.prototype.formats




	/**
	 * Check if two date units are the exact.
	 */
	DatePicker.prototype.isDateExact = function( one, two ) {

		var calendar = this

		// When we’re working with weekdays, do a direct comparison.
		if (
			( _.isInteger( one ) && _.isInteger( two ) ) ||
			( typeof one == 'boolean' && typeof two == 'boolean' )
		) {
			return one === two
		}

		// When we’re working with date representations, compare the “pick” value.
		if (
			( _.isDate( one ) || $.isArray( one ) ) &&
			( _.isDate( two ) || $.isArray( two ) )
		) {
			return calendar.create( one ).pick === calendar.create( two ).pick
		}

		// When we’re working with range objects, compare the “from” and “to”.
		if ( $.isPlainObject( one ) && $.isPlainObject( two ) ) {
			return calendar.isDateExact( one.from, two.from ) && calendar.isDateExact( one.to, two.to )
		}

		return false
	}


	/**
	 * Check if two date units overlap.
	 */
	DatePicker.prototype.isDateOverlap = function( one, two ) {

		var calendar = this,
			firstDay = calendar.settings.firstDay ? 1 : 0

		// When we’re working with a weekday index, compare the days.
		if ( _.isInteger( one ) && ( _.isDate( two ) || $.isArray( two ) ) ) {
			one = one % 7 + firstDay
			return one === calendar.create( two ).day + 1
		}
		if ( _.isInteger( two ) && ( _.isDate( one ) || $.isArray( one ) ) ) {
			two = two % 7 + firstDay
			return two === calendar.create( one ).day + 1
		}

		// When we’re working with range objects, check if the ranges overlap.
		if ( $.isPlainObject( one ) && $.isPlainObject( two ) ) {
			return calendar.overlapRanges( one, two )
		}

		return false
	}


	/**
	 * Flip the “enabled” state.
	 */
	DatePicker.prototype.flipEnable = function( val ) {
		var itemObject = this.item
		itemObject.enable = val || (itemObject.enable == - 1 ? 1 : - 1)
	}


	/**
	 * Mark a collection of dates as “disabled”.
	 */
	DatePicker.prototype.deactivate = function( type, datesToDisable ) {

		var calendar = this,
			disabledItems = calendar.item.disable.slice( 0 )


		// If we’re flipping, that’s all we need to do.
		if ( datesToDisable == 'flip' ) {
			calendar.flipEnable()
		}

		else {
			if ( datesToDisable === false ) {
				calendar.flipEnable( 1 )
				disabledItems = []
			}

			else {
				if ( datesToDisable === true ) {
					calendar.flipEnable( - 1 )
					disabledItems = []
				}

				// Otherwise go through the dates to disable.
				else {

					datesToDisable.map( function( unitToDisable ) {

						var matchFound

						// When we have disabled items, check for matches.
						// If something is matched, immediately break out.
						for ( var index = 0; index < disabledItems.length; index += 1 ) {
							if ( calendar.isDateExact( unitToDisable, disabledItems[ index ] ) ) {
								matchFound = true
								break
							}
						}

						// If nothing was found, add the validated unit to the collection.
						if ( ! matchFound ) {
							if (
								_.isInteger( unitToDisable ) ||
								_.isDate( unitToDisable ) ||
								$.isArray( unitToDisable ) ||
								( $.isPlainObject( unitToDisable ) && unitToDisable.from && unitToDisable.to )
							) {
								disabledItems.push( unitToDisable )
							}
						}
					} )
				}
			}
		}

		// Return the updated collection.
		return disabledItems
	} //DatePicker.prototype.deactivate


	/**
	 * Mark a collection of dates as “enabled”.
	 */
	DatePicker.prototype.activate = function( type, datesToEnable ) {

		var calendar = this,
			disabledItems = calendar.item.disable,
			disabledItemsCount = disabledItems.length

		// If we’re flipping, that’s all we need to do.
		if ( datesToEnable == 'flip' ) {
			calendar.flipEnable()
		}

		else {
			if ( datesToEnable === true ) {
				calendar.flipEnable( 1 )
				disabledItems = []
			}

			else {
				if ( datesToEnable === false ) {
					calendar.flipEnable( - 1 )
					disabledItems = []
				}

				// Otherwise go through the disabled dates.
				else {

					datesToEnable.map( function( unitToEnable ) {

						var matchFound,
							disabledUnit,
							index,
							isExactRange

						// Go through the disabled items and try to find a match.
						for ( index = 0; index < disabledItemsCount; index += 1 ) {

							disabledUnit = disabledItems[ index ]

							// When an exact match is found, remove it from the collection.
							if ( calendar.isDateExact( disabledUnit, unitToEnable ) ) {
								matchFound = disabledItems[ index ] = null
								isExactRange = true
								break
							}

							// When an overlapped match is found, add the “inverted” state to it.
							else {
								if ( calendar.isDateOverlap( disabledUnit, unitToEnable ) ) {
									if ( $.isPlainObject( unitToEnable ) ) {
										unitToEnable.inverted = true
										matchFound = unitToEnable
									}
									else {
										if ( $.isArray( unitToEnable ) ) {
											matchFound = unitToEnable
											if ( ! matchFound[ 3 ] ) {
												matchFound.push( 'inverted' )
											}
										}
										else {
											if ( _.isDate( unitToEnable ) ) {
												matchFound = [ unitToEnable.getFullYear(), unitToEnable.getMonth(), unitToEnable.getDate(), 'inverted' ]
											}
										}
									}
									break
								}
							}
						}

						// If a match was found, remove a previous duplicate entry.
						if ( matchFound ) {
							for ( index = 0; index < disabledItemsCount; index += 1 ) {
								if ( calendar.isDateExact( disabledItems[ index ], unitToEnable ) ) {
									disabledItems[ index ] = null
									break
								}
							}
						}

						// In the event that we’re dealing with an exact range of dates,
						// make sure there are no “inverted” dates because of it.
						if ( isExactRange ) {
							for ( index = 0; index < disabledItemsCount; index += 1 ) {
								if ( calendar.isDateOverlap( disabledItems[ index ], unitToEnable ) ) {
									disabledItems[ index ] = null
									break
								}
							}
						}

						// If something is still matched, add it into the collection.
						if ( matchFound ) {
							disabledItems.push( matchFound )
						}
					} )
				}
			}
		}

		// Return the updated collection.
		return disabledItems.filter( function( val ) {
			return val != null
		} )
	} //DatePicker.prototype.activate


	/**
	 * Create a string for the nodes in the picker.
	 */
	DatePicker.prototype.nodes = function( isOpen ) {

		var
			calendar = this,
			settings = calendar.settings,
			calendarItem = calendar.item,
			nowObject = calendarItem.now,
			selectedObject = calendarItem.select,
			highlightedObject = calendarItem.highlight,
			viewsetObject = calendarItem.view,
			disabledCollection = calendarItem.disable,
			minLimitObject = calendarItem.min,
			maxLimitObject = calendarItem.max,


			// Create the calendar table head using a copy of weekday labels collection.
			// * We do a copy so we don't mutate the original array.
			tableHead = (function( collection, fullCollection ) {

				// If the first day should be Monday, move Sunday to the end.
				if ( settings.firstDay ) {
					collection.push( collection.shift() )
					fullCollection.push( fullCollection.shift() )
				}

				// Create and return the table head group.
				return _.node(
					'thead',
					_.node(
						'tr',
						_.group( {
							min: 0,
							max: DAYS_IN_WEEK - 1,
							i: 1,
							node: 'th',
							item: function( counter ) {
								return [
									collection[ counter ],
									settings.klass.weekdays,
									'scope=col title="' + fullCollection[ counter ] + '"'
								]
							}
						} )
					)
				) //endreturn

				// Materialize modified
			})( ( settings.showWeekdaysFull ? settings.weekdaysFull : settings.weekdaysLetter ).slice( 0 ), settings.weekdaysFull.slice( 0 ) ), //tableHead


			// Create the nav for next/prev month.
			createMonthNav = function( next ) {

				// Otherwise, return the created month tag.
				return _.node(
					'div',
					' ',
					settings.klass[ 'nav' + ( next ? 'Next' : 'Prev' ) ] + (

						// If the focused month is outside the range, disabled the button.
						( next && viewsetObject.year >= maxLimitObject.year && viewsetObject.month >= maxLimitObject.month ) ||
						( ! next && viewsetObject.year <= minLimitObject.year && viewsetObject.month <= minLimitObject.month ) ?
						' ' + settings.klass.navDisabled : ''
					),
					'data-nav=' + ( next || - 1 ) + ' ' +
					_.ariaAttr( {
						role: 'button',
						controls: calendar.$node[ 0 ].id + '_table'
					} ) + ' ' +
					'title="' + (next ? settings.labelMonthNext : settings.labelMonthPrev ) + '"'
				) //endreturn
			}, //createMonthNav


			// Create the month label.
			//Materialize modified
			createMonthLabel = function( override ) {

				var monthsCollection = settings.showMonthsShort ? settings.monthsShort : settings.monthsFull

				// Materialize modified
				if ( override == "short_months" ) {
					monthsCollection = settings.monthsShort;
				}

				// If there are months to select, add a dropdown menu.
				if ( settings.selectMonths && override == undefined ) {

					return _.node( 'select',
						_.group( {
							min: 0,
							max: 11,
							i: 1,
							node: 'option',
							item: function( loopedMonth ) {

								return [

									// The looped month and no classes.
									monthsCollection[ loopedMonth ], 0,

									// Set the value and selected index.
									'value=' + loopedMonth +
									( viewsetObject.month == loopedMonth ? ' selected' : '' ) +
									(
										(
											( viewsetObject.year == minLimitObject.year && loopedMonth < minLimitObject.month ) ||
											( viewsetObject.year == maxLimitObject.year && loopedMonth > maxLimitObject.month )
										) ?
										' disabled' : ''
									)
								]
							}
						} ),
						settings.klass.selectMonth + ' browser-default',
						( isOpen ? '' : 'disabled' ) + ' ' +
						_.ariaAttr( { controls: calendar.$node[ 0 ].id + '_table' } ) + ' ' +
						'title="' + settings.labelMonthSelect + '"'
					)
				}

				// Materialize modified
				if ( override == "short_months" ) {
					if ( selectedObject != null ) {
						return _.node( 'div', monthsCollection[ selectedObject.month ] );
					} else {
						return _.node( 'div', monthsCollection[ viewsetObject.month ] );
					}
				}

				// If there's a need for a month selector
				return _.node( 'div', monthsCollection[ viewsetObject.month ], settings.klass.month )
			}, //createMonthLabel


			// Create the year label.
			// Materialize modified
			createYearLabel = function( override ) {

				var focusedYear = viewsetObject.year,

					// If years selector is set to a literal "true", set it to 5. Otherwise
					// divide in half to get half before and half after focused year.
					numberYears = settings.selectYears === true ? 5 : ~ ~ ( settings.selectYears / 2 )

				// If there are years to select, add a dropdown menu.
				if ( numberYears ) {

					var
						minYear = minLimitObject.year,
						maxYear = maxLimitObject.year,
						lowestYear = focusedYear - numberYears,
						highestYear = focusedYear + numberYears

					// If the min year is greater than the lowest year, increase the highest year
					// by the difference and set the lowest year to the min year.
					if ( minYear > lowestYear ) {
						highestYear += minYear - lowestYear
						lowestYear = minYear
					}

					// If the max year is less than the highest year, decrease the lowest year
					// by the lower of the two: available and needed years. Then set the
					// highest year to the max year.
					if ( maxYear < highestYear ) {

						var availableYears = lowestYear - minYear,
							neededYears = highestYear - maxYear

						lowestYear -= availableYears > neededYears ? neededYears : availableYears
						highestYear = maxYear
					}

					if ( settings.selectYears && override == undefined ) {
						return _.node( 'select',
							_.group( {
								min: lowestYear,
								max: highestYear,
								i: 1,
								node: 'option',
								item: function( loopedYear ) {
									return [

										// The looped year and no classes.
										loopedYear, 0,

										// Set the value and selected index.
										'value=' + loopedYear + ( focusedYear == loopedYear ? ' selected' : '' )
									]
								}
							} ),
							settings.klass.selectYear + ' browser-default',
							( isOpen ? '' : 'disabled' ) + ' ' + _.ariaAttr( { controls: calendar.$node[ 0 ].id + '_table' } ) + ' ' +
							'title="' + settings.labelYearSelect + '"'
						)
					}
				}

				// Materialize modified
				if ( override == "raw" ) {
					return _.node( 'div', focusedYear )
				}

				// Otherwise just return the year focused
				return _.node( 'div', focusedYear, settings.klass.year )
			} //createYearLabel


		// Materialize modified
		createDayLabel = function() {
			if ( selectedObject != null ) {
				return _.node( 'div', selectedObject.date )
			} else {
				return _.node( 'div', nowObject.date )
			}
		}
		createWeekdayLabel = function() {
			var display_day;

			if ( selectedObject != null ) {
				display_day = selectedObject.day;
			} else {
				display_day = nowObject.day;
			}
			var weekday = settings.weekdaysFull[ display_day ]
			return weekday
		}


		// Create and return the entire calendar.
		return _.node(
				// Date presentation View
				'div',
				_.node(
					'div',
					createWeekdayLabel(),
					"picker__weekday-display"
				) +
				_.node(
					// Div for short Month
					'div',
					createMonthLabel( "short_months" ),
					settings.klass.month_display
				) +
				_.node(
					// Div for Day
					'div',
					createDayLabel(),
					settings.klass.day_display
				) +
				_.node(
					// Div for Year
					'div',
					createYearLabel( "raw" ),
					settings.klass.year_display
				),
				settings.klass.date_display
			) +
			// Calendar container
			_.node( 'div',
				_.node( 'div',
					( settings.selectYears ? createMonthLabel() + createYearLabel() : createMonthLabel() + createYearLabel() ) +
					createMonthNav() + createMonthNav( 1 ),
					settings.klass.header
				) + _.node(
					'table',
					tableHead +
					_.node(
						'tbody',
						_.group( {
							min: 0,
							max: WEEKS_IN_CALENDAR - 1,
							i: 1,
							node: 'tr',
							item: function( rowCounter ) {

								// If Monday is the first day and the month starts on Sunday,
								// shift the date back a week.
								var shiftDateBy = settings.firstDay && calendar.create( [ viewsetObject.year, viewsetObject.month, 1 ] ).day === 0 ? - 7 : 0

								return [
									_.group( {
										min: DAYS_IN_WEEK * rowCounter - viewsetObject.day + shiftDateBy + 1, // Add 1 for weekday 0index
										max: function() {
											return this.min + DAYS_IN_WEEK - 1
										},
										i: 1,
										node: 'td',
										item: function( targetDate ) {

											// Convert the time date from a relative date to a
											// target date.
											targetDate = calendar.create( [ viewsetObject.year, viewsetObject.month, targetDate + ( settings.firstDay ? 1 : 0 ) ] )

											var isSelected = selectedObject && selectedObject.pick == targetDate.pick,
												isHighlighted = highlightedObject && highlightedObject.pick == targetDate.pick,
												isDisabled = disabledCollection && calendar.disabled( targetDate ) || targetDate.pick < minLimitObject.pick || targetDate.pick > maxLimitObject.pick,
												formattedDate = _.trigger( calendar.formats.toString, calendar, [ settings.format, targetDate ] )

											return [
												_.node(
													'div',
													targetDate.date,
													(function( klasses ) {

														// Add the `infocus` or `outfocus` classes
														// based on month in view.
														klasses.push( viewsetObject.month == targetDate.month ? settings.klass.infocus : settings.klass.outfocus )

														// Add the `today` class if needed.
														if ( nowObject.pick == targetDate.pick ) {
															klasses.push( settings.klass.now )
														}

														// Add the `selected` class if something's
														// selected and the time matches.
														if ( isSelected ) {
															klasses.push( settings.klass.selected )
														}

														// Add the `highlighted` class if
														// something's highlighted and the time
														// matches.
														if ( isHighlighted ) {
															klasses.push( settings.klass.highlighted )
														}

														// Add the `disabled` class if something's
														// disabled and the object matches.
														if ( isDisabled ) {
															klasses.push( settings.klass.disabled )
														}

														return klasses.join( ' ' )
													})( [ settings.klass.day ] ),
													'data-pick=' + targetDate.pick + ' ' + _.ariaAttr( {
														role: 'gridcell',
														label: formattedDate,
														selected: isSelected && calendar.$node.val() === formattedDate ? true : null,
														activedescendant: isHighlighted ? true : null,
														disabled: isDisabled ? true : null
													} )
												),
												'',
												_.ariaAttr( { role: 'presentation' } )
											] //endreturn
										}
									} )
								] //endreturn
							}
						} )
					),
					settings.klass.table,
					'id="' + calendar.$node[ 0 ].id + '_table' + '" ' + _.ariaAttr( {
						role: 'grid',
						controls: calendar.$node[ 0 ].id,
						readonly: true
					} )
				)
				, settings.klass.calendar_container ) // end calendar

			+

			// * For Firefox forms to submit, make sure to set the buttons’ `type` attributes as
			// “button”.
			_.node(
				'div',
				_.node( 'button', settings.today, "btn-flat picker__today",
					'type=button data-pick=' + nowObject.pick +
					( isOpen && ! calendar.disabled( nowObject ) ? '' : ' disabled' ) + ' ' +
					_.ariaAttr( { controls: calendar.$node[ 0 ].id } ) ) +
				_.node( 'button', settings.clear, "btn-flat picker__clear",
					'type=button data-clear=1' +
					( isOpen ? '' : ' disabled' ) + ' ' +
					_.ariaAttr( { controls: calendar.$node[ 0 ].id } ) ) +
				_.node( 'button', settings.close, "btn-flat picker__close",
					'type=button data-close=true ' +
					( isOpen ? '' : ' disabled' ) + ' ' +
					_.ariaAttr( { controls: calendar.$node[ 0 ].id } ) ),
				settings.klass.footer
			) //endreturn
	} //DatePicker.prototype.nodes




	/**
	 * The date picker defaults.
	 */
	DatePicker.defaults = (function( prefix ) {

		return {

			// The title label to use for the month nav buttons
			labelMonthNext: 'Next month',
			labelMonthPrev: 'Previous month',

			// The title label to use for the dropdown selectors
			labelMonthSelect: 'Select a month',
			labelYearSelect: 'Select a year',

			// Months and weekdays
			monthsFull: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ],
			monthsShort: [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ],
			weekdaysFull: [ 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' ],
			weekdaysShort: [ 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ],

			// Materialize modified
			weekdaysLetter: [ 'S', 'M', 'T', 'W', 'T', 'F', 'S' ],

			// Today and clear
			today: 'Today',
			clear: 'Clear',
			close: 'Close',

			// The format to show on the `input` element
			format: 'd mmmm, yyyy',

			// Classes
			klass: {

				table: prefix + 'table',

				header: prefix + 'header',


				// Materialize Added klasses
				date_display: prefix + 'date-display',
				day_display: prefix + 'day-display',
				month_display: prefix + 'month-display',
				year_display: prefix + 'year-display',
				calendar_container: prefix + 'calendar-container',
				// end



				navPrev: prefix + 'nav--prev',
				navNext: prefix + 'nav--next',
				navDisabled: prefix + 'nav--disabled',

				month: prefix + 'month',
				year: prefix + 'year',

				selectMonth: prefix + 'select--month',
				selectYear: prefix + 'select--year',

				weekdays: prefix + 'weekday',

				day: prefix + 'day',
				disabled: prefix + 'day--disabled',
				selected: prefix + 'day--selected',
				highlighted: prefix + 'day--highlighted',
				now: prefix + 'day--today',
				infocus: prefix + 'day--infocus',
				outfocus: prefix + 'day--outfocus',

				footer: prefix + 'footer',

				buttonClear: prefix + 'button--clear',
				buttonToday: prefix + 'button--today',
				buttonClose: prefix + 'button--close'
			}
		}
	})( Picker.klasses().picker + '__' )





	/**
	 * Extend the picker to add the date picker.
	 */
	Picker.extend( 'pickadate', DatePicker )


} ));


;(function( $ ) {

	$.fn.characterCounter = function() {
		return this.each( function() {
			var $input = $( this );
			var $counterElement = $input.parent().find( 'span[class="character-counter"]' );

			// character counter has already been added appended to the parent container
			if ( $counterElement.length ) {
				return;
			}

			var itHasLengthAttribute = $input.attr( 'length' ) !== undefined;

			if ( itHasLengthAttribute ) {
				$input.on( 'input', updateCounter );
				$input.on( 'focus', updateCounter );
				$input.on( 'blur', removeCounterElement );

				addCounterElement( $input );
			}

		} );
	};

	function updateCounter() {
		var maxLength = + $( this ).attr( 'length' ),
			actualLength = + $( this ).val().length,
			isValidLength = actualLength <= maxLength;

		$( this ).parent().find( 'span[class="character-counter"]' ).html( actualLength + '/' + maxLength );

		addInputStyle( isValidLength, $( this ) );
	}

	function addCounterElement( $input ) {
		var $counterElement = $input.parent().find( 'span[class="character-counter"]' );

		if ( $counterElement.length ) {
			return;
		}

		$counterElement = $( '<span/>' ).addClass( 'character-counter' ).css( 'float', 'right' ).css( 'font-size', '12px' ).css( 'height', 1 );

		$input.parent().append( $counterElement );
	}

	function removeCounterElement() {
		$( this ).parent().find( 'span[class="character-counter"]' ).html( '' );
	}

	function addInputStyle( isValidLength, $input ) {
		var inputHasInvalidClass = $input.hasClass( 'invalid' );
		if ( isValidLength && inputHasInvalidClass ) {
			$input.removeClass( 'invalid' );
		}
		else {
			if ( ! isValidLength && ! inputHasInvalidClass ) {
				$input.removeClass( 'valid' );
				$input.addClass( 'invalid' );
			}
		}
	}

	$( document ).ready( function() {
		$( 'input, textarea' ).characterCounter();
	} );

}( jQuery ));
;(function( $ ) {

	var methods = {

		init: function( options ) {
			var defaults = {
				time_constant: 200, // ms
				dist: - 100, // zoom scale TODO: make this more intuitive as an option
				shift: 0, // spacing for center image
				padding: 0, // Padding between non center items
				full_width: false, // Change to full width styles
				indicators: false, // Toggle indicators
				no_wrap: false // Don't wrap around and cycle through items.
			};
			options = $.extend( defaults, options );

			return this.each( function() {

				var images, offset, center, pressed, dim, count,
					reference, referenceY, amplitude, target, velocity,
					xform, frame, timestamp, ticker, dragged, vertical_dragged;
				var $indicators = $( '<ul class="indicators"></ul>' );


				// Initialize
				var view = $( this );
				var showIndicators = view.attr( 'data-indicators' ) || options.indicators;

				// Don't double initialize.
				if ( view.hasClass( 'initialized' ) ) {
					// Redraw carousel.
					$( this ).trigger( 'carouselNext', [ 0.000001 ] );
					return true;
				}


				// Options
				if ( options.full_width ) {
					options.dist = 0;
					var firstImage = view.find( '.carousel-item img' ).first();
					if ( firstImage.length ) {
						imageHeight = firstImage.load( function() {
							view.css( 'height', $( this ).height() );
						} );
					} else {
						imageHeight = view.find( '.carousel-item' ).first().height();
						view.css( 'height', imageHeight );
					}

					// Offset fixed items when indicators.
					if ( showIndicators ) {
						view.find( '.carousel-fixed-item' ).addClass( 'with-indicators' );
					}
				}


				view.addClass( 'initialized' );
				pressed = false;
				offset = target = 0;
				images = [];
				item_width = view.find( '.carousel-item' ).first().innerWidth();
				dim = item_width * 2 + options.padding;

				view.find( '.carousel-item' ).each( function( i ) {
					images.push( $( this )[ 0 ] );
					if ( showIndicators ) {
						var $indicator = $( '<li class="indicator-item"></li>' );

						// Add active to first by default.
						if ( i === 0 ) {
							$indicator.addClass( 'active' );
						}

						// Handle clicks on indicators.
						$indicator.click( function() {
							var index = $( this ).index();
							cycleTo( index );
						} );
						$indicators.append( $indicator );
					}
				} );

				if ( showIndicators ) {
					view.append( $indicators );
				}
				count = images.length;


				function setupEvents() {
					if ( typeof window.ontouchstart !== 'undefined' ) {
						view[ 0 ].addEventListener( 'touchstart', tap );
						view[ 0 ].addEventListener( 'touchmove', drag );
						view[ 0 ].addEventListener( 'touchend', release );
					}
					view[ 0 ].addEventListener( 'mousedown', tap );
					view[ 0 ].addEventListener( 'mousemove', drag );
					view[ 0 ].addEventListener( 'mouseup', release );
					view[ 0 ].addEventListener( 'mouseleave', release );
					view[ 0 ].addEventListener( 'click', click );
				}

				function xpos( e ) {
					// touch event
					if ( e.targetTouches && (e.targetTouches.length >= 1) ) {
						return e.targetTouches[ 0 ].clientX;
					}

					// mouse event
					return e.clientX;
				}

				function ypos( e ) {
					// touch event
					if ( e.targetTouches && (e.targetTouches.length >= 1) ) {
						return e.targetTouches[ 0 ].clientY;
					}

					// mouse event
					return e.clientY;
				}

				function wrap( x ) {
					return (x >= count) ? (x % count) : (x < 0) ? wrap( count + (x % count) ) : x;
				}

				function scroll( x ) {
					var i, half, delta, dir, tween, el, alignment, xTranslation;

					offset = (typeof x === 'number') ? x : offset;
					center = Math.floor( (offset + dim / 2) / dim );
					delta = offset - center * dim;
					dir = (delta < 0) ? 1 : - 1;
					tween = - dir * delta * 2 / dim;
					half = count >> 1;

					if ( ! options.full_width ) {
						alignment = 'translateX(' + (view[ 0 ].clientWidth - item_width) / 2 + 'px) ';
						alignment += 'translateY(' + (view[ 0 ].clientHeight - item_width) / 2 + 'px)';
					} else {
						alignment = 'translateX(0)';
					}

					// Set indicator active
					if ( showIndicators ) {
						var diff = (center % count);
						var activeIndicator = $indicators.find( '.indicator-item.active' );
						if ( activeIndicator.index() !== diff ) {
							activeIndicator.removeClass( 'active' );
							$indicators.find( '.indicator-item' ).eq( diff ).addClass( 'active' );
						}
					}

					// center
					// Don't show wrapped items.
					if ( ! options.no_wrap || (center >= 0 && center < count) ) {
						el = images[ wrap( center ) ];
						el.style[ xform ] = alignment +
							' translateX(' + (- delta / 2) + 'px)' +
							' translateX(' + (dir * options.shift * tween * i) + 'px)' +
							' translateZ(' + (options.dist * tween) + 'px)';
						el.style.zIndex = 0;
						if ( options.full_width ) {
							tweenedOpacity = 1;
						}
						else {
							tweenedOpacity = 1 - 0.2 * tween;
						}
						el.style.opacity = tweenedOpacity;
						el.style.display = 'block';
					}

					for ( i = 1; i <= half; ++ i ) {
						// right side
						if ( options.full_width ) {
							zTranslation = options.dist;
							tweenedOpacity = (i === half && delta < 0) ? 1 - tween : 1;
						} else {
							zTranslation = options.dist * (i * 2 + tween * dir);
							tweenedOpacity = 1 - 0.2 * (i * 2 + tween * dir);
						}
						// Don't show wrapped items.
						if ( ! options.no_wrap || center + i < count ) {
							el = images[ wrap( center + i ) ];
							el.style[ xform ] = alignment +
								' translateX(' + (options.shift + (dim * i - delta) / 2) + 'px)' +
								' translateZ(' + zTranslation + 'px)';
							el.style.zIndex = - i;
							el.style.opacity = tweenedOpacity;
							el.style.display = 'block';
						}


						// left side
						if ( options.full_width ) {
							zTranslation = options.dist;
							tweenedOpacity = (i === half && delta > 0) ? 1 - tween : 1;
						} else {
							zTranslation = options.dist * (i * 2 - tween * dir);
							tweenedOpacity = 1 - 0.2 * (i * 2 - tween * dir);
						}
						// Don't show wrapped items.
						if ( ! options.no_wrap || center - i >= 0 ) {
							el = images[ wrap( center - i ) ];
							el.style[ xform ] = alignment +
								' translateX(' + (- options.shift + (- dim * i - delta) / 2) + 'px)' +
								' translateZ(' + zTranslation + 'px)';
							el.style.zIndex = - i;
							el.style.opacity = tweenedOpacity;
							el.style.display = 'block';
						}
					}

					// center
					// Don't show wrapped items.
					if ( ! options.no_wrap || (center >= 0 && center < count) ) {
						el = images[ wrap( center ) ];
						el.style[ xform ] = alignment +
							' translateX(' + (- delta / 2) + 'px)' +
							' translateX(' + (dir * options.shift * tween) + 'px)' +
							' translateZ(' + (options.dist * tween) + 'px)';
						el.style.zIndex = 0;
						if ( options.full_width ) {
							tweenedOpacity = 1;
						}
						else {
							tweenedOpacity = 1 - 0.2 * tween;
						}
						el.style.opacity = tweenedOpacity;
						el.style.display = 'block';
					}
				}

				function track() {
					var now, elapsed, delta, v;

					now = Date.now();
					elapsed = now - timestamp;
					timestamp = now;
					delta = offset - frame;
					frame = offset;

					v = 1000 * delta / (1 + elapsed);
					velocity = 0.8 * v + 0.2 * velocity;
				}

				function autoScroll() {
					var elapsed, delta;

					if ( amplitude ) {
						elapsed = Date.now() - timestamp;
						delta = amplitude * Math.exp( - elapsed / options.time_constant );
						if ( delta > 2 || delta < - 2 ) {
							scroll( target - delta );
							requestAnimationFrame( autoScroll );
						} else {
							scroll( target );
						}
					}
				}

				function click( e ) {
					// Disable clicks if carousel was dragged.
					if ( dragged ) {
						e.preventDefault();
						e.stopPropagation();
						return false;

					} else {
						if ( ! options.full_width ) {
							var clickedIndex = $( e.target ).closest( '.carousel-item' ).index();
							var diff = (center % count) - clickedIndex;

							// Disable clicks if carousel was shifted by click
							if ( diff !== 0 ) {
								e.preventDefault();
								e.stopPropagation();
							}
							cycleTo( clickedIndex );
						}
					}
				}

				function cycleTo( n ) {
					var diff = (center % count) - n;

					// Account for wraparound.
					if ( ! options.no_wrap ) {
						if ( diff < 0 ) {
							if ( Math.abs( diff + count ) < Math.abs( diff ) ) {
								diff += count;
							}

						} else {
							if ( diff > 0 ) {
								if ( Math.abs( diff - count ) < diff ) {
									diff -= count;
								}
							}
						}
					}

					// Call prev or next accordingly.
					if ( diff < 0 ) {
						view.trigger( 'carouselNext', [ Math.abs( diff ) ] );

					} else {
						if ( diff > 0 ) {
							view.trigger( 'carouselPrev', [ diff ] );
						}
					}
				}

				function tap( e ) {
					pressed = true;
					dragged = false;
					vertical_dragged = false;
					reference = xpos( e );
					referenceY = ypos( e );

					velocity = amplitude = 0;
					frame = offset;
					timestamp = Date.now();
					clearInterval( ticker );
					ticker = setInterval( track, 100 );

				}

				function drag( e ) {
					var x, delta, deltaY;
					if ( pressed ) {
						x = xpos( e );
						y = ypos( e );
						delta = reference - x;
						deltaY = Math.abs( referenceY - y );
						if ( deltaY < 30 && ! vertical_dragged ) {
							// If vertical scrolling don't allow dragging.
							if ( delta > 2 || delta < - 2 ) {
								dragged = true;
								reference = x;
								scroll( offset + delta );
							}

						} else {
							if ( dragged ) {
								// If dragging don't allow vertical scroll.
								e.preventDefault();
								e.stopPropagation();
								return false;

							} else {
								// Vertical scrolling.
								vertical_dragged = true;
							}
						}
					}

					if ( dragged ) {
						// If dragging don't allow vertical scroll.
						e.preventDefault();
						e.stopPropagation();
						return false;
					}
				}

				function release( e ) {
					if ( pressed ) {
						pressed = false;
					} else {
						return;
					}

					clearInterval( ticker );
					target = offset;
					if ( velocity > 10 || velocity < - 10 ) {
						amplitude = 0.9 * velocity;
						target = offset + amplitude;
					}
					target = Math.round( target / dim ) * dim;

					// No wrap of items.
					if ( options.no_wrap ) {
						if ( target >= dim * (count - 1) ) {
							target = dim * (count - 1);
						} else {
							if ( target < 0 ) {
								target = 0;
							}
						}
					}
					amplitude = target - offset;
					timestamp = Date.now();
					requestAnimationFrame( autoScroll );

					if ( dragged ) {
						e.preventDefault();
						e.stopPropagation();
					}
					return false;
				}

				xform = 'transform';
				[ 'webkit', 'Moz', 'O', 'ms' ].every( function( prefix ) {
					var e = prefix + 'Transform';
					if ( typeof document.body.style[ e ] !== 'undefined' ) {
						xform = e;
						return false;
					}
					return true;
				} );



				window.onresize = scroll;

				setupEvents();
				scroll( offset );

				$( this ).on( 'carouselNext', function( e, n ) {
					if ( n === undefined ) {
						n = 1;
					}
					target = offset + dim * n;
					if ( offset !== target ) {
						amplitude = target - offset;
						timestamp = Date.now();
						requestAnimationFrame( autoScroll );
					}
				} );

				$( this ).on( 'carouselPrev', function( e, n ) {
					if ( n === undefined ) {
						n = 1;
					}
					target = offset - dim * n;
					if ( offset !== target ) {
						amplitude = target - offset;
						timestamp = Date.now();
						requestAnimationFrame( autoScroll );
					}
				} );

				$( this ).on( 'carouselSet', function( e, n ) {
					if ( n === undefined ) {
						n = 0;
					}
					cycleTo( n );
				} );

			} );



		},
		next: function( n ) {
			$( this ).trigger( 'carouselNext', [ n ] );
		},
		prev: function( n ) {
			$( this ).trigger( 'carouselPrev', [ n ] );
		},
		set: function( n ) {
			$( this ).trigger( 'carouselSet', [ n ] );
		}
	};


	$.fn.carousel = function( methodOrOptions ) {
		if ( methods[ methodOrOptions ] ) {
			return methods[ methodOrOptions ].apply( this, Array.prototype.slice.call( arguments, 1 ) );
		} else {
			if ( typeof methodOrOptions === 'object' || ! methodOrOptions ) {
				// Default to "init"
				return methods.init.apply( this, arguments );
			} else {
				$.error( 'Method ' + methodOrOptions + ' does not exist on jQuery.carousel' );
			}
		}
	}; // Plugin end
}( jQuery ));

window.tzones = {};
window.tzones.zones = {
	"countries": {
		"AD": {
			"name": "Andorra",
			"abbr": "AD",
			"zones": [
				"Europe/Andorra"
			]
		},
		"AE": {
			"name": "United Arab Emirates",
			"abbr": "AE",
			"zones": [
				"Asia/Dubai"
			]
		},
		"AF": {
			"name": "Afghanistan",
			"abbr": "AF",
			"zones": [
				"Asia/Kabul"
			]
		},
		"AG": {
			"name": "Antigua & Barbuda",
			"abbr": "AG",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"AI": {
			"name": "Anguilla",
			"abbr": "AI",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"AL": {
			"name": "Albania",
			"abbr": "AL",
			"zones": [
				"Europe/Tirane"
			]
		},
		"AM": {
			"name": "Armenia",
			"abbr": "AM",
			"zones": [
				"Asia/Yerevan"
			]
		},
		"AO": {
			"name": "Angola",
			"abbr": "AO",
			"zones": [
				"Africa/Lagos"
			]
		},
		"AQ": {
			"name": "Antarctica",
			"abbr": "AQ",
			"zones": [
				"Antarctica/Casey",
				"Antarctica/Davis",
				"Antarctica/DumontDUrville",
				"Antarctica/Mawson",
				"Antarctica/Palmer",
				"Antarctica/Rothera",
				"Antarctica/Syowa",
				"Antarctica/Troll",
				"Antarctica/Vostok",
				"Pacific/Auckland"
			]
		},
		"AR": {
			"name": "Argentina",
			"abbr": "AR",
			"zones": [
				"America/Argentina/Buenos_Aires",
				"America/Argentina/Cordoba",
				"America/Argentina/Salta",
				"America/Argentina/Jujuy",
				"America/Argentina/Tucuman",
				"America/Argentina/Catamarca",
				"America/Argentina/La_Rioja",
				"America/Argentina/San_Juan",
				"America/Argentina/Mendoza",
				"America/Argentina/San_Luis",
				"America/Argentina/Rio_Gallegos",
				"America/Argentina/Ushuaia"
			]
		},
		"AS": {
			"name": "Samoa (American)",
			"abbr": "AS",
			"zones": [
				"Pacific/Pago_Pago"
			]
		},
		"AT": {
			"name": "Austria",
			"abbr": "AT",
			"zones": [
				"Europe/Vienna"
			]
		},
		"AU": {
			"name": "Australia",
			"abbr": "AU",
			"zones": [
				"Australia/Lord_Howe",
				"Antarctica/Macquarie",
				"Australia/Hobart",
				"Australia/Currie",
				"Australia/Melbourne",
				"Australia/Sydney",
				"Australia/Broken_Hill",
				"Australia/Brisbane",
				"Australia/Lindeman",
				"Australia/Adelaide",
				"Australia/Darwin",
				"Australia/Perth",
				"Australia/Eucla"
			]
		},
		"AW": {
			"name": "Aruba",
			"abbr": "AW",
			"zones": [
				"America/Curacao"
			]
		},
		"AX": {
			"name": "Åland Islands",
			"abbr": "AX",
			"zones": [
				"Europe/Helsinki"
			]
		},
		"AZ": {
			"name": "Azerbaijan",
			"abbr": "AZ",
			"zones": [
				"Asia/Baku"
			]
		},
		"BA": {
			"name": "Bosnia & Herzegovina",
			"abbr": "BA",
			"zones": [
				"Europe/Belgrade"
			]
		},
		"BB": {
			"name": "Barbados",
			"abbr": "BB",
			"zones": [
				"America/Barbados"
			]
		},
		"BD": {
			"name": "Bangladesh",
			"abbr": "BD",
			"zones": [
				"Asia/Dhaka"
			]
		},
		"BE": {
			"name": "Belgium",
			"abbr": "BE",
			"zones": [
				"Europe/Brussels"
			]
		},
		"BF": {
			"name": "Burkina Faso",
			"abbr": "BF",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"BG": {
			"name": "Bulgaria",
			"abbr": "BG",
			"zones": [
				"Europe/Sofia"
			]
		},
		"BH": {
			"name": "Bahrain",
			"abbr": "BH",
			"zones": [
				"Asia/Qatar"
			]
		},
		"BI": {
			"name": "Burundi",
			"abbr": "BI",
			"zones": [
				"Africa/Maputo"
			]
		},
		"BJ": {
			"name": "Benin",
			"abbr": "BJ",
			"zones": [
				"Africa/Lagos"
			]
		},
		"BL": {
			"name": "St Barthelemy",
			"abbr": "BL",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"BM": {
			"name": "Bermuda",
			"abbr": "BM",
			"zones": [
				"Atlantic/Bermuda"
			]
		},
		"BN": {
			"name": "Brunei",
			"abbr": "BN",
			"zones": [
				"Asia/Brunei"
			]
		},
		"BO": {
			"name": "Bolivia",
			"abbr": "BO",
			"zones": [
				"America/La_Paz"
			]
		},
		"BQ": {
			"name": "Caribbean NL",
			"abbr": "BQ",
			"zones": [
				"America/Curacao"
			]
		},
		"BR": {
			"name": "Brazil",
			"abbr": "BR",
			"zones": [
				"America/Noronha",
				"America/Belem",
				"America/Fortaleza",
				"America/Recife",
				"America/Araguaina",
				"America/Maceio",
				"America/Bahia",
				"America/Sao_Paulo",
				"America/Campo_Grande",
				"America/Cuiaba",
				"America/Santarem",
				"America/Porto_Velho",
				"America/Boa_Vista",
				"America/Manaus",
				"America/Eirunepe",
				"America/Rio_Branco"
			]
		},
		"BS": {
			"name": "Bahamas",
			"abbr": "BS",
			"zones": [
				"America/Nassau"
			]
		},
		"BT": {
			"name": "Bhutan",
			"abbr": "BT",
			"zones": [
				"Asia/Thimphu"
			]
		},
		"BW": {
			"name": "Botswana",
			"abbr": "BW",
			"zones": [
				"Africa/Maputo"
			]
		},
		"BY": {
			"name": "Belarus",
			"abbr": "BY",
			"zones": [
				"Europe/Minsk"
			]
		},
		"BZ": {
			"name": "Belize",
			"abbr": "BZ",
			"zones": [
				"America/Belize"
			]
		},
		"CA": {
			"name": "Canada",
			"abbr": "CA",
			"zones": [
				"America/St_Johns",
				"America/Halifax",
				"America/Glace_Bay",
				"America/Moncton",
				"America/Goose_Bay",
				"America/Blanc-Sablon",
				"America/Toronto",
				"America/Nipigon",
				"America/Thunder_Bay",
				"America/Iqaluit",
				"America/Pangnirtung",
				"America/Atikokan",
				"America/Winnipeg",
				"America/Rainy_River",
				"America/Resolute",
				"America/Rankin_Inlet",
				"America/Regina",
				"America/Swift_Current",
				"America/Edmonton",
				"America/Cambridge_Bay",
				"America/Yellowknife",
				"America/Inuvik",
				"America/Creston",
				"America/Dawson_Creek",
				"America/Fort_Nelson",
				"America/Vancouver",
				"America/Whitehorse",
				"America/Dawson"
			]
		},
		"CC": {
			"name": "Cocos (Keeling) Islands",
			"abbr": "CC",
			"zones": [
				"Indian/Cocos"
			]
		},
		"CD": {
			"name": "Congo (Dem. Rep.)",
			"abbr": "CD",
			"zones": [
				"Africa/Maputo",
				"Africa/Lagos"
			]
		},
		"CF": {
			"name": "Central African Rep.",
			"abbr": "CF",
			"zones": [
				"Africa/Lagos"
			]
		},
		"CG": {
			"name": "Congo (Rep.)",
			"abbr": "CG",
			"zones": [
				"Africa/Lagos"
			]
		},
		"CH": {
			"name": "Switzerland",
			"abbr": "CH",
			"zones": [
				"Europe/Zurich"
			]
		},
		"CI": {
			"name": "Côte d'Ivoire",
			"abbr": "CI",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"CK": {
			"name": "Cook Islands",
			"abbr": "CK",
			"zones": [
				"Pacific/Rarotonga"
			]
		},
		"CL": {
			"name": "Chile",
			"abbr": "CL",
			"zones": [
				"America/Santiago",
				"Pacific/Easter"
			]
		},
		"CM": {
			"name": "Cameroon",
			"abbr": "CM",
			"zones": [
				"Africa/Lagos"
			]
		},
		"CN": {
			"name": "China",
			"abbr": "CN",
			"zones": [
				"Asia/Shanghai",
				"Asia/Urumqi"
			]
		},
		"CO": {
			"name": "Colombia",
			"abbr": "CO",
			"zones": [
				"America/Bogota"
			]
		},
		"CR": {
			"name": "Costa Rica",
			"abbr": "CR",
			"zones": [
				"America/Costa_Rica"
			]
		},
		"CU": {
			"name": "Cuba",
			"abbr": "CU",
			"zones": [
				"America/Havana"
			]
		},
		"CV": {
			"name": "Cape Verde",
			"abbr": "CV",
			"zones": [
				"Atlantic/Cape_Verde"
			]
		},
		"CW": {
			"name": "Curacao",
			"abbr": "CW",
			"zones": [
				"America/Curacao"
			]
		},
		"CX": {
			"name": "Christmas Island",
			"abbr": "CX",
			"zones": [
				"Indian/Christmas"
			]
		},
		"CY": {
			"name": "Cyprus",
			"abbr": "CY",
			"zones": [
				"Asia/Nicosia"
			]
		},
		"CZ": {
			"name": "Czech Republic",
			"abbr": "CZ",
			"zones": [
				"Europe/Prague"
			]
		},
		"DE": {
			"name": "Germany",
			"abbr": "DE",
			"zones": [
				"Europe/Zurich",
				"Europe/Berlin"
			]
		},
		"DJ": {
			"name": "Djibouti",
			"abbr": "DJ",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"DK": {
			"name": "Denmark",
			"abbr": "DK",
			"zones": [
				"Europe/Copenhagen"
			]
		},
		"DM": {
			"name": "Dominica",
			"abbr": "DM",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"DO": {
			"name": "Dominican Republic",
			"abbr": "DO",
			"zones": [
				"America/Santo_Domingo"
			]
		},
		"DZ": {
			"name": "Algeria",
			"abbr": "DZ",
			"zones": [
				"Africa/Algiers"
			]
		},
		"EC": {
			"name": "Ecuador",
			"abbr": "EC",
			"zones": [
				"America/Guayaquil",
				"Pacific/Galapagos"
			]
		},
		"EE": {
			"name": "Estonia",
			"abbr": "EE",
			"zones": [
				"Europe/Tallinn"
			]
		},
		"EG": {
			"name": "Egypt",
			"abbr": "EG",
			"zones": [
				"Africa/Cairo"
			]
		},
		"EH": {
			"name": "Western Sahara",
			"abbr": "EH",
			"zones": [
				"Africa/El_Aaiun"
			]
		},
		"ER": {
			"name": "Eritrea",
			"abbr": "ER",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"ES": {
			"name": "Spain",
			"abbr": "ES",
			"zones": [
				"Europe/Madrid",
				"Africa/Ceuta",
				"Atlantic/Canary"
			]
		},
		"ET": {
			"name": "Ethiopia",
			"abbr": "ET",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"FI": {
			"name": "Finland",
			"abbr": "FI",
			"zones": [
				"Europe/Helsinki"
			]
		},
		"FJ": {
			"name": "Fiji",
			"abbr": "FJ",
			"zones": [
				"Pacific/Fiji"
			]
		},
		"FK": {
			"name": "Falkland Islands",
			"abbr": "FK",
			"zones": [
				"Atlantic/Stanley"
			]
		},
		"FM": {
			"name": "Micronesia",
			"abbr": "FM",
			"zones": [
				"Pacific/Chuuk",
				"Pacific/Pohnpei",
				"Pacific/Kosrae"
			]
		},
		"FO": {
			"name": "Faroe Islands",
			"abbr": "FO",
			"zones": [
				"Atlantic/Faroe"
			]
		},
		"FR": {
			"name": "France",
			"abbr": "FR",
			"zones": [
				"Europe/Paris"
			]
		},
		"GA": {
			"name": "Gabon",
			"abbr": "GA",
			"zones": [
				"Africa/Lagos"
			]
		},
		"GB": {
			"name": "Britain (UK)",
			"abbr": "GB",
			"zones": [
				"Europe/London"
			]
		},
		"GD": {
			"name": "Grenada",
			"abbr": "GD",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"GE": {
			"name": "Georgia",
			"abbr": "GE",
			"zones": [
				"Asia/Tbilisi"
			]
		},
		"GF": {
			"name": "French Guiana",
			"abbr": "GF",
			"zones": [
				"America/Cayenne"
			]
		},
		"GG": {
			"name": "Guernsey",
			"abbr": "GG",
			"zones": [
				"Europe/London"
			]
		},
		"GH": {
			"name": "Ghana",
			"abbr": "GH",
			"zones": [
				"Africa/Accra"
			]
		},
		"GI": {
			"name": "Gibraltar",
			"abbr": "GI",
			"zones": [
				"Europe/Gibraltar"
			]
		},
		"GL": {
			"name": "Greenland",
			"abbr": "GL",
			"zones": [
				"America/Godthab",
				"America/Danmarkshavn",
				"America/Scoresbysund",
				"America/Thule"
			]
		},
		"GM": {
			"name": "Gambia",
			"abbr": "GM",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"GN": {
			"name": "Guinea",
			"abbr": "GN",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"GP": {
			"name": "Guadeloupe",
			"abbr": "GP",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"GQ": {
			"name": "Equatorial Guinea",
			"abbr": "GQ",
			"zones": [
				"Africa/Lagos"
			]
		},
		"GR": {
			"name": "Greece",
			"abbr": "GR",
			"zones": [
				"Europe/Athens"
			]
		},
		"GS": {
			"name": "South Georgia & the South Sandwich Islands",
			"abbr": "GS",
			"zones": [
				"Atlantic/South_Georgia"
			]
		},
		"GT": {
			"name": "Guatemala",
			"abbr": "GT",
			"zones": [
				"America/Guatemala"
			]
		},
		"GU": {
			"name": "Guam",
			"abbr": "GU",
			"zones": [
				"Pacific/Guam"
			]
		},
		"GW": {
			"name": "Guinea-Bissau",
			"abbr": "GW",
			"zones": [
				"Africa/Bissau"
			]
		},
		"GY": {
			"name": "Guyana",
			"abbr": "GY",
			"zones": [
				"America/Guyana"
			]
		},
		"HK": {
			"name": "Hong Kong",
			"abbr": "HK",
			"zones": [
				"Asia/Hong_Kong"
			]
		},
		"HN": {
			"name": "Honduras",
			"abbr": "HN",
			"zones": [
				"America/Tegucigalpa"
			]
		},
		"HR": {
			"name": "Croatia",
			"abbr": "HR",
			"zones": [
				"Europe/Belgrade"
			]
		},
		"HT": {
			"name": "Haiti",
			"abbr": "HT",
			"zones": [
				"America/Port-au-Prince"
			]
		},
		"HU": {
			"name": "Hungary",
			"abbr": "HU",
			"zones": [
				"Europe/Budapest"
			]
		},
		"ID": {
			"name": "Indonesia",
			"abbr": "ID",
			"zones": [
				"Asia/Jakarta",
				"Asia/Pontianak",
				"Asia/Makassar",
				"Asia/Jayapura"
			]
		},
		"IE": {
			"name": "Ireland",
			"abbr": "IE",
			"zones": [
				"Europe/Dublin"
			]
		},
		"IL": {
			"name": "Israel",
			"abbr": "IL",
			"zones": [
				"Asia/Jerusalem"
			]
		},
		"IM": {
			"name": "Isle of Man",
			"abbr": "IM",
			"zones": [
				"Europe/London"
			]
		},
		"IN": {
			"name": "India",
			"abbr": "IN",
			"zones": [
				"Asia/Kolkata"
			]
		},
		"IO": {
			"name": "British Indian Ocean Territory",
			"abbr": "IO",
			"zones": [
				"Indian/Chagos"
			]
		},
		"IQ": {
			"name": "Iraq",
			"abbr": "IQ",
			"zones": [
				"Asia/Baghdad"
			]
		},
		"IR": {
			"name": "Iran",
			"abbr": "IR",
			"zones": [
				"Asia/Tehran"
			]
		},
		"IS": {
			"name": "Iceland",
			"abbr": "IS",
			"zones": [
				"Atlantic/Reykjavik"
			]
		},
		"IT": {
			"name": "Italy",
			"abbr": "IT",
			"zones": [
				"Europe/Rome"
			]
		},
		"JE": {
			"name": "Jersey",
			"abbr": "JE",
			"zones": [
				"Europe/London"
			]
		},
		"JM": {
			"name": "Jamaica",
			"abbr": "JM",
			"zones": [
				"America/Jamaica"
			]
		},
		"JO": {
			"name": "Jordan",
			"abbr": "JO",
			"zones": [
				"Asia/Amman"
			]
		},
		"JP": {
			"name": "Japan",
			"abbr": "JP",
			"zones": [
				"Asia/Tokyo"
			]
		},
		"KE": {
			"name": "Kenya",
			"abbr": "KE",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"KG": {
			"name": "Kyrgyzstan",
			"abbr": "KG",
			"zones": [
				"Asia/Bishkek"
			]
		},
		"KH": {
			"name": "Cambodia",
			"abbr": "KH",
			"zones": [
				"Asia/Bangkok"
			]
		},
		"KI": {
			"name": "Kiribati",
			"abbr": "KI",
			"zones": [
				"Pacific/Tarawa",
				"Pacific/Enderbury",
				"Pacific/Kiritimati"
			]
		},
		"KM": {
			"name": "Comoros",
			"abbr": "KM",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"KN": {
			"name": "St Kitts & Nevis",
			"abbr": "KN",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"KP": {
			"name": "Korea (North)",
			"abbr": "KP",
			"zones": [
				"Asia/Pyongyang"
			]
		},
		"KR": {
			"name": "Korea (South)",
			"abbr": "KR",
			"zones": [
				"Asia/Seoul"
			]
		},
		"KW": {
			"name": "Kuwait",
			"abbr": "KW",
			"zones": [
				"Asia/Riyadh"
			]
		},
		"KY": {
			"name": "Cayman Islands",
			"abbr": "KY",
			"zones": [
				"America/Panama"
			]
		},
		"KZ": {
			"name": "Kazakhstan",
			"abbr": "KZ",
			"zones": [
				"Asia/Almaty",
				"Asia/Qyzylorda",
				"Asia/Aqtobe",
				"Asia/Aqtau",
				"Asia/Oral"
			]
		},
		"LA": {
			"name": "Laos",
			"abbr": "LA",
			"zones": [
				"Asia/Bangkok"
			]
		},
		"LB": {
			"name": "Lebanon",
			"abbr": "LB",
			"zones": [
				"Asia/Beirut"
			]
		},
		"LC": {
			"name": "St Lucia",
			"abbr": "LC",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"LI": {
			"name": "Liechtenstein",
			"abbr": "LI",
			"zones": [
				"Europe/Zurich"
			]
		},
		"LK": {
			"name": "Sri Lanka",
			"abbr": "LK",
			"zones": [
				"Asia/Colombo"
			]
		},
		"LR": {
			"name": "Liberia",
			"abbr": "LR",
			"zones": [
				"Africa/Monrovia"
			]
		},
		"LS": {
			"name": "Lesotho",
			"abbr": "LS",
			"zones": [
				"Africa/Johannesburg"
			]
		},
		"LT": {
			"name": "Lithuania",
			"abbr": "LT",
			"zones": [
				"Europe/Vilnius"
			]
		},
		"LU": {
			"name": "Luxembourg",
			"abbr": "LU",
			"zones": [
				"Europe/Luxembourg"
			]
		},
		"LV": {
			"name": "Latvia",
			"abbr": "LV",
			"zones": [
				"Europe/Riga"
			]
		},
		"LY": {
			"name": "Libya",
			"abbr": "LY",
			"zones": [
				"Africa/Tripoli"
			]
		},
		"MA": {
			"name": "Morocco",
			"abbr": "MA",
			"zones": [
				"Africa/Casablanca"
			]
		},
		"MC": {
			"name": "Monaco",
			"abbr": "MC",
			"zones": [
				"Europe/Monaco"
			]
		},
		"MD": {
			"name": "Moldova",
			"abbr": "MD",
			"zones": [
				"Europe/Chisinau"
			]
		},
		"ME": {
			"name": "Montenegro",
			"abbr": "ME",
			"zones": [
				"Europe/Belgrade"
			]
		},
		"MF": {
			"name": "St Martin (French)",
			"abbr": "MF",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"MG": {
			"name": "Madagascar",
			"abbr": "MG",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"MH": {
			"name": "Marshall Islands",
			"abbr": "MH",
			"zones": [
				"Pacific/Majuro",
				"Pacific/Kwajalein"
			]
		},
		"MK": {
			"name": "Macedonia",
			"abbr": "MK",
			"zones": [
				"Europe/Belgrade"
			]
		},
		"ML": {
			"name": "Mali",
			"abbr": "ML",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"MM": {
			"name": "Myanmar (Burma)",
			"abbr": "MM",
			"zones": [
				"Asia/Rangoon"
			]
		},
		"MN": {
			"name": "Mongolia",
			"abbr": "MN",
			"zones": [
				"Asia/Ulaanbaatar",
				"Asia/Hovd",
				"Asia/Choibalsan"
			]
		},
		"MO": {
			"name": "Macau",
			"abbr": "MO",
			"zones": [
				"Asia/Macau"
			]
		},
		"MP": {
			"name": "Northern Mariana Islands",
			"abbr": "MP",
			"zones": [
				"Pacific/Guam"
			]
		},
		"MQ": {
			"name": "Martinique",
			"abbr": "MQ",
			"zones": [
				"America/Martinique"
			]
		},
		"MR": {
			"name": "Mauritania",
			"abbr": "MR",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"MS": {
			"name": "Montserrat",
			"abbr": "MS",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"MT": {
			"name": "Malta",
			"abbr": "MT",
			"zones": [
				"Europe/Malta"
			]
		},
		"MU": {
			"name": "Mauritius",
			"abbr": "MU",
			"zones": [
				"Indian/Mauritius"
			]
		},
		"MV": {
			"name": "Maldives",
			"abbr": "MV",
			"zones": [
				"Indian/Maldives"
			]
		},
		"MW": {
			"name": "Malawi",
			"abbr": "MW",
			"zones": [
				"Africa/Maputo"
			]
		},
		"MX": {
			"name": "Mexico",
			"abbr": "MX",
			"zones": [
				"America/Mexico_City",
				"America/Cancun",
				"America/Merida",
				"America/Monterrey",
				"America/Matamoros",
				"America/Mazatlan",
				"America/Chihuahua",
				"America/Ojinaga",
				"America/Hermosillo",
				"America/Tijuana",
				"America/Bahia_Banderas"
			]
		},
		"MY": {
			"name": "Malaysia",
			"abbr": "MY",
			"zones": [
				"Asia/Kuala_Lumpur",
				"Asia/Kuching"
			]
		},
		"MZ": {
			"name": "Mozambique",
			"abbr": "MZ",
			"zones": [
				"Africa/Maputo"
			]
		},
		"NA": {
			"name": "Namibia",
			"abbr": "NA",
			"zones": [
				"Africa/Windhoek"
			]
		},
		"NC": {
			"name": "New Caledonia",
			"abbr": "NC",
			"zones": [
				"Pacific/Noumea"
			]
		},
		"NE": {
			"name": "Niger",
			"abbr": "NE",
			"zones": [
				"Africa/Lagos"
			]
		},
		"NF": {
			"name": "Norfolk Island",
			"abbr": "NF",
			"zones": [
				"Pacific/Norfolk"
			]
		},
		"NG": {
			"name": "Nigeria",
			"abbr": "NG",
			"zones": [
				"Africa/Lagos"
			]
		},
		"NI": {
			"name": "Nicaragua",
			"abbr": "NI",
			"zones": [
				"America/Managua"
			]
		},
		"NL": {
			"name": "Netherlands",
			"abbr": "NL",
			"zones": [
				"Europe/Amsterdam"
			]
		},
		"NO": {
			"name": "Norway",
			"abbr": "NO",
			"zones": [
				"Europe/Oslo"
			]
		},
		"NP": {
			"name": "Nepal",
			"abbr": "NP",
			"zones": [
				"Asia/Kathmandu"
			]
		},
		"NR": {
			"name": "Nauru",
			"abbr": "NR",
			"zones": [
				"Pacific/Nauru"
			]
		},
		"NU": {
			"name": "Niue",
			"abbr": "NU",
			"zones": [
				"Pacific/Niue"
			]
		},
		"NZ": {
			"name": "New Zealand",
			"abbr": "NZ",
			"zones": [
				"Pacific/Auckland",
				"Pacific/Chatham"
			]
		},
		"OM": {
			"name": "Oman",
			"abbr": "OM",
			"zones": [
				"Asia/Dubai"
			]
		},
		"PA": {
			"name": "Panama",
			"abbr": "PA",
			"zones": [
				"America/Panama"
			]
		},
		"PE": {
			"name": "Peru",
			"abbr": "PE",
			"zones": [
				"America/Lima"
			]
		},
		"PF": {
			"name": "French Polynesia",
			"abbr": "PF",
			"zones": [
				"Pacific/Tahiti",
				"Pacific/Marquesas",
				"Pacific/Gambier"
			]
		},
		"PG": {
			"name": "Papua New Guinea",
			"abbr": "PG",
			"zones": [
				"Pacific/Port_Moresby",
				"Pacific/Bougainville"
			]
		},
		"PH": {
			"name": "Philippines",
			"abbr": "PH",
			"zones": [
				"Asia/Manila"
			]
		},
		"PK": {
			"name": "Pakistan",
			"abbr": "PK",
			"zones": [
				"Asia/Karachi"
			]
		},
		"PL": {
			"name": "Poland",
			"abbr": "PL",
			"zones": [
				"Europe/Warsaw"
			]
		},
		"PM": {
			"name": "St Pierre & Miquelon",
			"abbr": "PM",
			"zones": [
				"America/Miquelon"
			]
		},
		"PN": {
			"name": "Pitcairn",
			"abbr": "PN",
			"zones": [
				"Pacific/Pitcairn"
			]
		},
		"PR": {
			"name": "Puerto Rico",
			"abbr": "PR",
			"zones": [
				"America/Puerto_Rico"
			]
		},
		"PS": {
			"name": "Palestine",
			"abbr": "PS",
			"zones": [
				"Asia/Gaza",
				"Asia/Hebron"
			]
		},
		"PT": {
			"name": "Portugal",
			"abbr": "PT",
			"zones": [
				"Europe/Lisbon",
				"Atlantic/Madeira",
				"Atlantic/Azores"
			]
		},
		"PW": {
			"name": "Palau",
			"abbr": "PW",
			"zones": [
				"Pacific/Palau"
			]
		},
		"PY": {
			"name": "Paraguay",
			"abbr": "PY",
			"zones": [
				"America/Asuncion"
			]
		},
		"QA": {
			"name": "Qatar",
			"abbr": "QA",
			"zones": [
				"Asia/Qatar"
			]
		},
		"RE": {
			"name": "Réunion",
			"abbr": "RE",
			"zones": [
				"Indian/Reunion"
			]
		},
		"RO": {
			"name": "Romania",
			"abbr": "RO",
			"zones": [
				"Europe/Bucharest"
			]
		},
		"RS": {
			"name": "Serbia",
			"abbr": "RS",
			"zones": [
				"Europe/Belgrade"
			]
		},
		"RU": {
			"name": "Russia",
			"abbr": "RU",
			"zones": [
				"Europe/Kaliningrad",
				"Europe/Moscow",
				"Europe/Simferopol",
				"Europe/Volgograd",
				"Europe/Kirov",
				"Europe/Astrakhan",
				"Europe/Samara",
				"Europe/Ulyanovsk",
				"Asia/Yekaterinburg",
				"Asia/Omsk",
				"Asia/Novosibirsk",
				"Asia/Barnaul",
				"Asia/Tomsk",
				"Asia/Novokuznetsk",
				"Asia/Krasnoyarsk",
				"Asia/Irkutsk",
				"Asia/Chita",
				"Asia/Yakutsk",
				"Asia/Khandyga",
				"Asia/Vladivostok",
				"Asia/Ust-Nera",
				"Asia/Magadan",
				"Asia/Sakhalin",
				"Asia/Srednekolymsk",
				"Asia/Kamchatka",
				"Asia/Anadyr"
			]
		},
		"RW": {
			"name": "Rwanda",
			"abbr": "RW",
			"zones": [
				"Africa/Maputo"
			]
		},
		"SA": {
			"name": "Saudi Arabia",
			"abbr": "SA",
			"zones": [
				"Asia/Riyadh"
			]
		},
		"SB": {
			"name": "Solomon Islands",
			"abbr": "SB",
			"zones": [
				"Pacific/Guadalcanal"
			]
		},
		"SC": {
			"name": "Seychelles",
			"abbr": "SC",
			"zones": [
				"Indian/Mahe"
			]
		},
		"SD": {
			"name": "Sudan",
			"abbr": "SD",
			"zones": [
				"Africa/Khartoum"
			]
		},
		"SE": {
			"name": "Sweden",
			"abbr": "SE",
			"zones": [
				"Europe/Stockholm"
			]
		},
		"SG": {
			"name": "Singapore",
			"abbr": "SG",
			"zones": [
				"Asia/Singapore"
			]
		},
		"SH": {
			"name": "St Helena",
			"abbr": "SH",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"SI": {
			"name": "Slovenia",
			"abbr": "SI",
			"zones": [
				"Europe/Belgrade"
			]
		},
		"SJ": {
			"name": "Svalbard & Jan Mayen",
			"abbr": "SJ",
			"zones": [
				"Europe/Oslo"
			]
		},
		"SK": {
			"name": "Slovakia",
			"abbr": "SK",
			"zones": [
				"Europe/Prague"
			]
		},
		"SL": {
			"name": "Sierra Leone",
			"abbr": "SL",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"SM": {
			"name": "San Marino",
			"abbr": "SM",
			"zones": [
				"Europe/Rome"
			]
		},
		"SN": {
			"name": "Senegal",
			"abbr": "SN",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"SO": {
			"name": "Somalia",
			"abbr": "SO",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"SR": {
			"name": "Suriname",
			"abbr": "SR",
			"zones": [
				"America/Paramaribo"
			]
		},
		"SS": {
			"name": "South Sudan",
			"abbr": "SS",
			"zones": [
				"Africa/Khartoum"
			]
		},
		"ST": {
			"name": "Sao Tome & Principe",
			"abbr": "ST",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"SV": {
			"name": "El Salvador",
			"abbr": "SV",
			"zones": [
				"America/El_Salvador"
			]
		},
		"SX": {
			"name": "St Maarten (Dutch)",
			"abbr": "SX",
			"zones": [
				"America/Curacao"
			]
		},
		"SY": {
			"name": "Syria",
			"abbr": "SY",
			"zones": [
				"Asia/Damascus"
			]
		},
		"SZ": {
			"name": "Swaziland",
			"abbr": "SZ",
			"zones": [
				"Africa/Johannesburg"
			]
		},
		"TC": {
			"name": "Turks & Caicos Is",
			"abbr": "TC",
			"zones": [
				"America/Grand_Turk"
			]
		},
		"TD": {
			"name": "Chad",
			"abbr": "TD",
			"zones": [
				"Africa/Ndjamena"
			]
		},
		"TF": {
			"name": "French Southern & Antarctic Lands",
			"abbr": "TF",
			"zones": [
				"Indian/Reunion",
				"Indian/Kerguelen"
			]
		},
		"TG": {
			"name": "Togo",
			"abbr": "TG",
			"zones": [
				"Africa/Abidjan"
			]
		},
		"TH": {
			"name": "Thailand",
			"abbr": "TH",
			"zones": [
				"Asia/Bangkok"
			]
		},
		"TJ": {
			"name": "Tajikistan",
			"abbr": "TJ",
			"zones": [
				"Asia/Dushanbe"
			]
		},
		"TK": {
			"name": "Tokelau",
			"abbr": "TK",
			"zones": [
				"Pacific/Fakaofo"
			]
		},
		"TL": {
			"name": "East Timor",
			"abbr": "TL",
			"zones": [
				"Asia/Dili"
			]
		},
		"TM": {
			"name": "Turkmenistan",
			"abbr": "TM",
			"zones": [
				"Asia/Ashgabat"
			]
		},
		"TN": {
			"name": "Tunisia",
			"abbr": "TN",
			"zones": [
				"Africa/Tunis"
			]
		},
		"TO": {
			"name": "Tonga",
			"abbr": "TO",
			"zones": [
				"Pacific/Tongatapu"
			]
		},
		"TR": {
			"name": "Turkey",
			"abbr": "TR",
			"zones": [
				"Europe/Istanbul"
			]
		},
		"TT": {
			"name": "Trinidad & Tobago",
			"abbr": "TT",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"TV": {
			"name": "Tuvalu",
			"abbr": "TV",
			"zones": [
				"Pacific/Funafuti"
			]
		},
		"TW": {
			"name": "Taiwan",
			"abbr": "TW",
			"zones": [
				"Asia/Taipei"
			]
		},
		"TZ": {
			"name": "Tanzania",
			"abbr": "TZ",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"UA": {
			"name": "Ukraine",
			"abbr": "UA",
			"zones": [
				"Europe/Kiev",
				"Europe/Uzhgorod",
				"Europe/Zaporozhye"
			]
		},
		"UG": {
			"name": "Uganda",
			"abbr": "UG",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"UM": {
			"name": "US minor outlying islands",
			"abbr": "UM",
			"zones": [
				"Pacific/Pago_Pago",
				"Pacific/Wake",
				"Pacific/Honolulu"
			]
		},
		"US": {
			"name": "United States",
			"abbr": "US",
			"zones": [
				"America/New_York",
				"America/Detroit",
				"America/Kentucky/Louisville",
				"America/Kentucky/Monticello",
				"America/Indiana/Indianapolis",
				"America/Indiana/Vincennes",
				"America/Indiana/Winamac",
				"America/Indiana/Marengo",
				"America/Indiana/Petersburg",
				"America/Indiana/Vevay",
				"America/Chicago",
				"America/Indiana/Tell_City",
				"America/Indiana/Knox",
				"America/Menominee",
				"America/North_Dakota/Center",
				"America/North_Dakota/New_Salem",
				"America/North_Dakota/Beulah",
				"America/Denver",
				"America/Boise",
				"America/Phoenix",
				"America/Los_Angeles",
				"America/Anchorage",
				"America/Juneau",
				"America/Sitka",
				"America/Metlakatla",
				"America/Yakutat",
				"America/Nome",
				"America/Adak",
				"Pacific/Honolulu"
			]
		},
		"UY": {
			"name": "Uruguay",
			"abbr": "UY",
			"zones": [
				"America/Montevideo"
			]
		},
		"UZ": {
			"name": "Uzbekistan",
			"abbr": "UZ",
			"zones": [
				"Asia/Samarkand",
				"Asia/Tashkent"
			]
		},
		"VA": {
			"name": "Vatican City",
			"abbr": "VA",
			"zones": [
				"Europe/Rome"
			]
		},
		"VC": {
			"name": "St Vincent",
			"abbr": "VC",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"VE": {
			"name": "Venezuela",
			"abbr": "VE",
			"zones": [
				"America/Caracas"
			]
		},
		"VG": {
			"name": "Virgin Islands (UK)",
			"abbr": "VG",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"VI": {
			"name": "Virgin Islands (US)",
			"abbr": "VI",
			"zones": [
				"America/Port_of_Spain"
			]
		},
		"VN": {
			"name": "Vietnam",
			"abbr": "VN",
			"zones": [
				"Asia/Bangkok",
				"Asia/Ho_Chi_Minh"
			]
		},
		"VU": {
			"name": "Vanuatu",
			"abbr": "VU",
			"zones": [
				"Pacific/Efate"
			]
		},
		"WF": {
			"name": "Wallis & Futuna",
			"abbr": "WF",
			"zones": [
				"Pacific/Wallis"
			]
		},
		"WS": {
			"name": "Samoa (western)",
			"abbr": "WS",
			"zones": [
				"Pacific/Apia"
			]
		},
		"YE": {
			"name": "Yemen",
			"abbr": "YE",
			"zones": [
				"Asia/Riyadh"
			]
		},
		"YT": {
			"name": "Mayotte",
			"abbr": "YT",
			"zones": [
				"Africa/Nairobi"
			]
		},
		"ZA": {
			"name": "South Africa",
			"abbr": "ZA",
			"zones": [
				"Africa/Johannesburg"
			]
		},
		"ZM": {
			"name": "Zambia",
			"abbr": "ZM",
			"zones": [
				"Africa/Maputo"
			]
		},
		"ZW": {
			"name": "Zimbabwe",
			"abbr": "ZW",
			"zones": [
				"Africa/Maputo"
			]
		}
	},
	"zones": {
		"Europe/Andorra": {
			"name": "Europe/Andorra",
			"lat": 42.5,
			"long": 1.5167,
			"countries": [
				"AD"
			],
			"comments": ""
		},
		"Asia/Dubai": {
			"name": "Asia/Dubai",
			"lat": 25.3,
			"long": 55.3,
			"countries": [
				"AE",
				"OM"
			],
			"comments": ""
		},
		"Asia/Kabul": {
			"name": "Asia/Kabul",
			"lat": 34.5167,
			"long": 69.2,
			"countries": [
				"AF"
			],
			"comments": ""
		},
		"Europe/Tirane": {
			"name": "Europe/Tirane",
			"lat": 41.3333,
			"long": 19.8333,
			"countries": [
				"AL"
			],
			"comments": ""
		},
		"Asia/Yerevan": {
			"name": "Asia/Yerevan",
			"lat": 40.1833,
			"long": 44.5,
			"countries": [
				"AM"
			],
			"comments": ""
		},
		"Antarctica/Casey": {
			"name": "Antarctica/Casey",
			"lat": - 65.7167,
			"long": 110.5167,
			"countries": [
				"AQ"
			],
			"comments": "Casey"
		},
		"Antarctica/Davis": {
			"name": "Antarctica/Davis",
			"lat": - 67.4167,
			"long": 77.9667,
			"countries": [
				"AQ"
			],
			"comments": "Davis"
		},
		"Antarctica/DumontDUrville": {
			"name": "Antarctica/DumontDUrville",
			"lat": - 65.3333,
			"long": 140.0167,
			"countries": [
				"AQ"
			],
			"comments": "Dumont-d'Urville"
		},
		"Antarctica/Mawson": {
			"name": "Antarctica/Mawson",
			"lat": - 66.4,
			"long": 62.8833,
			"countries": [
				"AQ"
			],
			"comments": "Mawson"
		},
		"Antarctica/Palmer": {
			"name": "Antarctica/Palmer",
			"lat": - 63.2,
			"long": - 63.9,
			"countries": [
				"AQ"
			],
			"comments": "Palmer"
		},
		"Antarctica/Rothera": {
			"name": "Antarctica/Rothera",
			"lat": - 66.4333,
			"long": - 67.8667,
			"countries": [
				"AQ"
			],
			"comments": "Rothera"
		},
		"Antarctica/Syowa": {
			"name": "Antarctica/Syowa",
			"lat": - 68.9939,
			"long": 39.59,
			"countries": [
				"AQ"
			],
			"comments": "Syowa"
		},
		"Antarctica/Troll": {
			"name": "Antarctica/Troll",
			"lat": - 71.9886,
			"long": 2.535,
			"countries": [
				"AQ"
			],
			"comments": "Troll"
		},
		"Antarctica/Vostok": {
			"name": "Antarctica/Vostok",
			"lat": - 77.6,
			"long": 106.9,
			"countries": [
				"AQ"
			],
			"comments": "Vostok"
		},
		"America/Argentina/Buenos_Aires": {
			"name": "America/Argentina/Buenos_Aires",
			"lat": - 33.4,
			"long": - 57.55,
			"countries": [
				"AR"
			],
			"comments": "Buenos Aires (BA, CF)"
		},
		"America/Argentina/Cordoba": {
			"name": "America/Argentina/Cordoba",
			"lat": - 30.6,
			"long": - 63.8167,
			"countries": [
				"AR"
			],
			"comments": "Argentina (most areas: CB, CC, CN, ER, FM, MN, SE, SF)"
		},
		"America/Argentina/Salta": {
			"name": "America/Argentina/Salta",
			"lat": - 23.2167,
			"long": - 64.5833,
			"countries": [
				"AR"
			],
			"comments": "Salta (SA, LP, NQ, RN)"
		},
		"America/Argentina/Jujuy": {
			"name": "America/Argentina/Jujuy",
			"lat": - 23.8167,
			"long": - 64.7,
			"countries": [
				"AR"
			],
			"comments": "Jujuy (JY)"
		},
		"America/Argentina/Tucuman": {
			"name": "America/Argentina/Tucuman",
			"lat": - 25.1833,
			"long": - 64.7833,
			"countries": [
				"AR"
			],
			"comments": "Tucumán (TM)"
		},
		"America/Argentina/Catamarca": {
			"name": "America/Argentina/Catamarca",
			"lat": - 27.5333,
			"long": - 64.2167,
			"countries": [
				"AR"
			],
			"comments": "Catamarca (CT); Chubut (CH)"
		},
		"America/Argentina/La_Rioja": {
			"name": "America/Argentina/La_Rioja",
			"lat": - 28.5667,
			"long": - 65.15,
			"countries": [
				"AR"
			],
			"comments": "La Rioja (LR)"
		},
		"America/Argentina/San_Juan": {
			"name": "America/Argentina/San_Juan",
			"lat": - 30.4667,
			"long": - 67.4833,
			"countries": [
				"AR"
			],
			"comments": "San Juan (SJ)"
		},
		"America/Argentina/Mendoza": {
			"name": "America/Argentina/Mendoza",
			"lat": - 31.1167,
			"long": - 67.1833,
			"countries": [
				"AR"
			],
			"comments": "Mendoza (MZ)"
		},
		"America/Argentina/San_Luis": {
			"name": "America/Argentina/San_Luis",
			"lat": - 32.6833,
			"long": - 65.65,
			"countries": [
				"AR"
			],
			"comments": "San Luis (SL)"
		},
		"America/Argentina/Rio_Gallegos": {
			"name": "America/Argentina/Rio_Gallegos",
			"lat": - 50.3667,
			"long": - 68.7833,
			"countries": [
				"AR"
			],
			"comments": "Santa Cruz (SC)"
		},
		"America/Argentina/Ushuaia": {
			"name": "America/Argentina/Ushuaia",
			"lat": - 53.2,
			"long": - 67.7,
			"countries": [
				"AR"
			],
			"comments": "Tierra del Fuego (TF)"
		},
		"Pacific/Pago_Pago": {
			"name": "Pacific/Pago_Pago",
			"lat": - 13.7333,
			"long": - 169.3,
			"countries": [
				"AS",
				"UM"
			],
			"comments": "Samoa, Midway"
		},
		"Europe/Vienna": {
			"name": "Europe/Vienna",
			"lat": 48.2167,
			"long": 16.3333,
			"countries": [
				"AT"
			],
			"comments": ""
		},
		"Australia/Lord_Howe": {
			"name": "Australia/Lord_Howe",
			"lat": - 30.45,
			"long": 159.0833,
			"countries": [
				"AU"
			],
			"comments": "Lord Howe Island"
		},
		"Antarctica/Macquarie": {
			"name": "Antarctica/Macquarie",
			"lat": - 53.5,
			"long": 158.95,
			"countries": [
				"AU"
			],
			"comments": "Macquarie Island"
		},
		"Australia/Hobart": {
			"name": "Australia/Hobart",
			"lat": - 41.1167,
			"long": 147.3167,
			"countries": [
				"AU"
			],
			"comments": "Tasmania (most areas)"
		},
		"Australia/Currie": {
			"name": "Australia/Currie",
			"lat": - 38.0667,
			"long": 143.8667,
			"countries": [
				"AU"
			],
			"comments": "Tasmania (King Island)"
		},
		"Australia/Melbourne": {
			"name": "Australia/Melbourne",
			"lat": - 36.1833,
			"long": 144.9667,
			"countries": [
				"AU"
			],
			"comments": "Victoria"
		},
		"Australia/Sydney": {
			"name": "Australia/Sydney",
			"lat": - 32.1333,
			"long": 151.2167,
			"countries": [
				"AU"
			],
			"comments": "New South Wales (most areas)"
		},
		"Australia/Broken_Hill": {
			"name": "Australia/Broken_Hill",
			"lat": - 30.05,
			"long": 141.45,
			"countries": [
				"AU"
			],
			"comments": "New South Wales (Yancowinna)"
		},
		"Australia/Brisbane": {
			"name": "Australia/Brisbane",
			"lat": - 26.5333,
			"long": 153.0333,
			"countries": [
				"AU"
			],
			"comments": "Queensland (most areas)"
		},
		"Australia/Lindeman": {
			"name": "Australia/Lindeman",
			"lat": - 19.7333,
			"long": 149,
			"countries": [
				"AU"
			],
			"comments": "Queensland (Whitsunday Islands)"
		},
		"Australia/Adelaide": {
			"name": "Australia/Adelaide",
			"lat": - 33.0833,
			"long": 138.5833,
			"countries": [
				"AU"
			],
			"comments": "South Australia"
		},
		"Australia/Darwin": {
			"name": "Australia/Darwin",
			"lat": - 11.5333,
			"long": 130.8333,
			"countries": [
				"AU"
			],
			"comments": "Northern Territory"
		},
		"Australia/Perth": {
			"name": "Australia/Perth",
			"lat": - 30.05,
			"long": 115.85,
			"countries": [
				"AU"
			],
			"comments": "Western Australia (most areas)"
		},
		"Australia/Eucla": {
			"name": "Australia/Eucla",
			"lat": - 30.2833,
			"long": 128.8667,
			"countries": [
				"AU"
			],
			"comments": "Western Australia (Eucla)"
		},
		"Asia/Baku": {
			"name": "Asia/Baku",
			"lat": 40.3833,
			"long": 49.85,
			"countries": [
				"AZ"
			],
			"comments": ""
		},
		"America/Barbados": {
			"name": "America/Barbados",
			"lat": 13.1,
			"long": - 58.3833,
			"countries": [
				"BB"
			],
			"comments": ""
		},
		"Asia/Dhaka": {
			"name": "Asia/Dhaka",
			"lat": 23.7167,
			"long": 90.4167,
			"countries": [
				"BD"
			],
			"comments": ""
		},
		"Europe/Brussels": {
			"name": "Europe/Brussels",
			"lat": 50.8333,
			"long": 4.3333,
			"countries": [
				"BE"
			],
			"comments": ""
		},
		"Europe/Sofia": {
			"name": "Europe/Sofia",
			"lat": 42.6833,
			"long": 23.3167,
			"countries": [
				"BG"
			],
			"comments": ""
		},
		"Atlantic/Bermuda": {
			"name": "Atlantic/Bermuda",
			"lat": 32.2833,
			"long": - 63.2333,
			"countries": [
				"BM"
			],
			"comments": ""
		},
		"Asia/Brunei": {
			"name": "Asia/Brunei",
			"lat": 4.9333,
			"long": 114.9167,
			"countries": [
				"BN"
			],
			"comments": ""
		},
		"America/La_Paz": {
			"name": "America/La_Paz",
			"lat": - 15.5,
			"long": - 67.85,
			"countries": [
				"BO"
			],
			"comments": ""
		},
		"America/Noronha": {
			"name": "America/Noronha",
			"lat": - 2.15,
			"long": - 31.5833,
			"countries": [
				"BR"
			],
			"comments": "Atlantic islands"
		},
		"America/Belem": {
			"name": "America/Belem",
			"lat": - 0.55,
			"long": - 47.5167,
			"countries": [
				"BR"
			],
			"comments": "Pará (east); Amapá"
		},
		"America/Fortaleza": {
			"name": "America/Fortaleza",
			"lat": - 2.2833,
			"long": - 37.5,
			"countries": [
				"BR"
			],
			"comments": "Brazil (northeast: MA, PI, CE, RN, PB)"
		},
		"America/Recife": {
			"name": "America/Recife",
			"lat": - 7.95,
			"long": - 33.1,
			"countries": [
				"BR"
			],
			"comments": "Pernambuco"
		},
		"America/Araguaina": {
			"name": "America/Araguaina",
			"lat": - 6.8,
			"long": - 47.8,
			"countries": [
				"BR"
			],
			"comments": "Tocantins"
		},
		"America/Maceio": {
			"name": "America/Maceio",
			"lat": - 8.3333,
			"long": - 34.2833,
			"countries": [
				"BR"
			],
			"comments": "Alagoas, Sergipe"
		},
		"America/Bahia": {
			"name": "America/Bahia",
			"lat": - 11.0167,
			"long": - 37.4833,
			"countries": [
				"BR"
			],
			"comments": "Bahia"
		},
		"America/Sao_Paulo": {
			"name": "America/Sao_Paulo",
			"lat": - 22.4667,
			"long": - 45.3833,
			"countries": [
				"BR"
			],
			"comments": "Brazil (southeast: GO, DF, MG, ES, RJ, SP, PR, SC, RS)"
		},
		"America/Campo_Grande": {
			"name": "America/Campo_Grande",
			"lat": - 19.55,
			"long": - 53.3833,
			"countries": [
				"BR"
			],
			"comments": "Mato Grosso do Sul"
		},
		"America/Cuiaba": {
			"name": "America/Cuiaba",
			"lat": - 14.4167,
			"long": - 55.9167,
			"countries": [
				"BR"
			],
			"comments": "Mato Grosso"
		},
		"America/Santarem": {
			"name": "America/Santarem",
			"lat": - 1.5667,
			"long": - 53.1333,
			"countries": [
				"BR"
			],
			"comments": "Pará (west)"
		},
		"America/Porto_Velho": {
			"name": "America/Porto_Velho",
			"lat": - 7.2333,
			"long": - 62.1,
			"countries": [
				"BR"
			],
			"comments": "Rondônia"
		},
		"America/Boa_Vista": {
			"name": "America/Boa_Vista",
			"lat": 2.8167,
			"long": - 59.3333,
			"countries": [
				"BR"
			],
			"comments": "Roraima"
		},
		"America/Manaus": {
			"name": "America/Manaus",
			"lat": - 2.8667,
			"long": - 59.9833,
			"countries": [
				"BR"
			],
			"comments": "Amazonas (east)"
		},
		"America/Eirunepe": {
			"name": "America/Eirunepe",
			"lat": - 5.3333,
			"long": - 68.1333,
			"countries": [
				"BR"
			],
			"comments": "Amazonas (west)"
		},
		"America/Rio_Branco": {
			"name": "America/Rio_Branco",
			"lat": - 8.0333,
			"long": - 66.2,
			"countries": [
				"BR"
			],
			"comments": "Acre"
		},
		"America/Nassau": {
			"name": "America/Nassau",
			"lat": 25.0833,
			"long": - 76.65,
			"countries": [
				"BS"
			],
			"comments": ""
		},
		"Asia/Thimphu": {
			"name": "Asia/Thimphu",
			"lat": 27.4667,
			"long": 89.65,
			"countries": [
				"BT"
			],
			"comments": ""
		},
		"Europe/Minsk": {
			"name": "Europe/Minsk",
			"lat": 53.9,
			"long": 27.5667,
			"countries": [
				"BY"
			],
			"comments": ""
		},
		"America/Belize": {
			"name": "America/Belize",
			"lat": 17.5,
			"long": - 87.8,
			"countries": [
				"BZ"
			],
			"comments": ""
		},
		"America/St_Johns": {
			"name": "America/St_Johns",
			"lat": 47.5667,
			"long": - 51.2833,
			"countries": [
				"CA"
			],
			"comments": "Newfoundland; Labrador (southeast)"
		},
		"America/Halifax": {
			"name": "America/Halifax",
			"lat": 44.65,
			"long": - 62.4,
			"countries": [
				"CA"
			],
			"comments": "Atlantic - NS (most areas); PE"
		},
		"America/Glace_Bay": {
			"name": "America/Glace_Bay",
			"lat": 46.2,
			"long": - 58.05,
			"countries": [
				"CA"
			],
			"comments": "Atlantic - NS (Cape Breton)"
		},
		"America/Moncton": {
			"name": "America/Moncton",
			"lat": 46.1,
			"long": - 63.2167,
			"countries": [
				"CA"
			],
			"comments": "Atlantic - New Brunswick"
		},
		"America/Goose_Bay": {
			"name": "America/Goose_Bay",
			"lat": 53.3333,
			"long": - 59.5833,
			"countries": [
				"CA"
			],
			"comments": "Atlantic - Labrador (most areas)"
		},
		"America/Blanc-Sablon": {
			"name": "America/Blanc-Sablon",
			"lat": 51.4167,
			"long": - 56.8833,
			"countries": [
				"CA"
			],
			"comments": "AST - QC (Lower North Shore)"
		},
		"America/Toronto": {
			"name": "America/Toronto",
			"lat": 43.65,
			"long": - 78.6167,
			"countries": [
				"CA"
			],
			"comments": "Eastern - ON, QC (most areas)"
		},
		"America/Nipigon": {
			"name": "America/Nipigon",
			"lat": 49.0167,
			"long": - 87.7333,
			"countries": [
				"CA"
			],
			"comments": "Eastern - ON, QC (no DST 1967-73)"
		},
		"America/Thunder_Bay": {
			"name": "America/Thunder_Bay",
			"lat": 48.3833,
			"long": - 88.75,
			"countries": [
				"CA"
			],
			"comments": "Eastern - ON (Thunder Bay)"
		},
		"America/Iqaluit": {
			"name": "America/Iqaluit",
			"lat": 63.7333,
			"long": - 67.5333,
			"countries": [
				"CA"
			],
			"comments": "Eastern - NU (most east areas)"
		},
		"America/Pangnirtung": {
			"name": "America/Pangnirtung",
			"lat": 66.1333,
			"long": - 64.2667,
			"countries": [
				"CA"
			],
			"comments": "Eastern - NU (Pangnirtung)"
		},
		"America/Atikokan": {
			"name": "America/Atikokan",
			"lat": 48.7586,
			"long": - 90.3783,
			"countries": [
				"CA"
			],
			"comments": "EST - ON (Atikokan); NU (Coral H)"
		},
		"America/Winnipeg": {
			"name": "America/Winnipeg",
			"lat": 49.8833,
			"long": - 96.85,
			"countries": [
				"CA"
			],
			"comments": "Central - ON (west); Manitoba"
		},
		"America/Rainy_River": {
			"name": "America/Rainy_River",
			"lat": 48.7167,
			"long": - 93.4333,
			"countries": [
				"CA"
			],
			"comments": "Central - ON (Rainy R, Ft Frances)"
		},
		"America/Resolute": {
			"name": "America/Resolute",
			"lat": 74.6956,
			"long": - 93.1708,
			"countries": [
				"CA"
			],
			"comments": "Central - NU (Resolute)"
		},
		"America/Rankin_Inlet": {
			"name": "America/Rankin_Inlet",
			"lat": 62.8167,
			"long": - 91.9169,
			"countries": [
				"CA"
			],
			"comments": "Central - NU (central)"
		},
		"America/Regina": {
			"name": "America/Regina",
			"lat": 50.4,
			"long": - 103.35,
			"countries": [
				"CA"
			],
			"comments": "CST - SK (most areas)"
		},
		"America/Swift_Current": {
			"name": "America/Swift_Current",
			"lat": 50.2833,
			"long": - 106.1667,
			"countries": [
				"CA"
			],
			"comments": "CST - SK (midwest)"
		},
		"America/Edmonton": {
			"name": "America/Edmonton",
			"lat": 53.55,
			"long": - 112.5333,
			"countries": [
				"CA"
			],
			"comments": "Mountain - AB; BC (E); SK (W)"
		},
		"America/Cambridge_Bay": {
			"name": "America/Cambridge_Bay",
			"lat": 69.1139,
			"long": - 104.9472,
			"countries": [
				"CA"
			],
			"comments": "Mountain - NU (west)"
		},
		"America/Yellowknife": {
			"name": "America/Yellowknife",
			"lat": 62.45,
			"long": - 113.65,
			"countries": [
				"CA"
			],
			"comments": "Mountain - NT (central)"
		},
		"America/Inuvik": {
			"name": "America/Inuvik",
			"lat": 68.3497,
			"long": - 132.2833,
			"countries": [
				"CA"
			],
			"comments": "Mountain - NT (west)"
		},
		"America/Creston": {
			"name": "America/Creston",
			"lat": 49.1,
			"long": - 115.4833,
			"countries": [
				"CA"
			],
			"comments": "MST - BC (Creston)"
		},
		"America/Dawson_Creek": {
			"name": "America/Dawson_Creek",
			"lat": 59.7667,
			"long": - 119.7667,
			"countries": [
				"CA"
			],
			"comments": "MST - BC (Dawson Cr, Ft St John)"
		},
		"America/Fort_Nelson": {
			"name": "America/Fort_Nelson",
			"lat": 58.8,
			"long": - 121.3,
			"countries": [
				"CA"
			],
			"comments": "MST - BC (Ft Nelson)"
		},
		"America/Vancouver": {
			"name": "America/Vancouver",
			"lat": 49.2667,
			"long": - 122.8833,
			"countries": [
				"CA"
			],
			"comments": "Pacific - BC (most areas)"
		},
		"America/Whitehorse": {
			"name": "America/Whitehorse",
			"lat": 60.7167,
			"long": - 134.95,
			"countries": [
				"CA"
			],
			"comments": "Pacific - Yukon (south)"
		},
		"America/Dawson": {
			"name": "America/Dawson",
			"lat": 64.0667,
			"long": - 138.5833,
			"countries": [
				"CA"
			],
			"comments": "Pacific - Yukon (north)"
		},
		"Indian/Cocos": {
			"name": "Indian/Cocos",
			"lat": - 11.8333,
			"long": 96.9167,
			"countries": [
				"CC"
			],
			"comments": ""
		},
		"Europe/Zurich": {
			"name": "Europe/Zurich",
			"lat": 47.3833,
			"long": 8.5333,
			"countries": [
				"CH",
				"DE",
				"LI"
			],
			"comments": "Swiss time"
		},
		"Africa/Abidjan": {
			"name": "Africa/Abidjan",
			"lat": 5.3167,
			"long": - 3.9667,
			"countries": [
				"CI",
				"BF",
				"GM",
				"GN",
				"ML",
				"MR",
				"SH",
				"SL",
				"SN",
				"ST",
				"TG"
			],
			"comments": ""
		},
		"Pacific/Rarotonga": {
			"name": "Pacific/Rarotonga",
			"lat": - 20.7667,
			"long": - 158.2333,
			"countries": [
				"CK"
			],
			"comments": ""
		},
		"America/Santiago": {
			"name": "America/Santiago",
			"lat": - 32.55,
			"long": - 69.3333,
			"countries": [
				"CL"
			],
			"comments": "Chile (most areas)"
		},
		"Pacific/Easter": {
			"name": "Pacific/Easter",
			"lat": - 26.85,
			"long": - 108.5667,
			"countries": [
				"CL"
			],
			"comments": "Easter Island"
		},
		"Asia/Shanghai": {
			"name": "Asia/Shanghai",
			"lat": 31.2333,
			"long": 121.4667,
			"countries": [
				"CN"
			],
			"comments": "Beijing Time"
		},
		"Asia/Urumqi": {
			"name": "Asia/Urumqi",
			"lat": 43.8,
			"long": 87.5833,
			"countries": [
				"CN"
			],
			"comments": "Xinjiang Time"
		},
		"America/Bogota": {
			"name": "America/Bogota",
			"lat": 4.6,
			"long": - 73.9167,
			"countries": [
				"CO"
			],
			"comments": ""
		},
		"America/Costa_Rica": {
			"name": "America/Costa_Rica",
			"lat": 9.9333,
			"long": - 83.9167,
			"countries": [
				"CR"
			],
			"comments": ""
		},
		"America/Havana": {
			"name": "America/Havana",
			"lat": 23.1333,
			"long": - 81.6333,
			"countries": [
				"CU"
			],
			"comments": ""
		},
		"Atlantic/Cape_Verde": {
			"name": "Atlantic/Cape_Verde",
			"lat": 14.9167,
			"long": - 22.4833,
			"countries": [
				"CV"
			],
			"comments": ""
		},
		"America/Curacao": {
			"name": "America/Curacao",
			"lat": 12.1833,
			"long": - 69,
			"countries": [
				"CW",
				"AW",
				"BQ",
				"SX"
			],
			"comments": ""
		},
		"Indian/Christmas": {
			"name": "Indian/Christmas",
			"lat": - 9.5833,
			"long": 105.7167,
			"countries": [
				"CX"
			],
			"comments": ""
		},
		"Asia/Nicosia": {
			"name": "Asia/Nicosia",
			"lat": 35.1667,
			"long": 33.3667,
			"countries": [
				"CY"
			],
			"comments": ""
		},
		"Europe/Prague": {
			"name": "Europe/Prague",
			"lat": 50.0833,
			"long": 14.4333,
			"countries": [
				"CZ",
				"SK"
			],
			"comments": ""
		},
		"Europe/Berlin": {
			"name": "Europe/Berlin",
			"lat": 52.5,
			"long": 13.3667,
			"countries": [
				"DE"
			],
			"comments": "Germany (most areas)"
		},
		"Europe/Copenhagen": {
			"name": "Europe/Copenhagen",
			"lat": 55.6667,
			"long": 12.5833,
			"countries": [
				"DK"
			],
			"comments": ""
		},
		"America/Santo_Domingo": {
			"name": "America/Santo_Domingo",
			"lat": 18.4667,
			"long": - 68.1,
			"countries": [
				"DO"
			],
			"comments": ""
		},
		"Africa/Algiers": {
			"name": "Africa/Algiers",
			"lat": 36.7833,
			"long": 3.05,
			"countries": [
				"DZ"
			],
			"comments": ""
		},
		"America/Guayaquil": {
			"name": "America/Guayaquil",
			"lat": - 1.8333,
			"long": - 78.1667,
			"countries": [
				"EC"
			],
			"comments": "Ecuador (mainland)"
		},
		"Pacific/Galapagos": {
			"name": "Pacific/Galapagos",
			"lat": 0.9,
			"long": - 88.4,
			"countries": [
				"EC"
			],
			"comments": "Galápagos Islands"
		},
		"Europe/Tallinn": {
			"name": "Europe/Tallinn",
			"lat": 59.4167,
			"long": 24.75,
			"countries": [
				"EE"
			],
			"comments": ""
		},
		"Africa/Cairo": {
			"name": "Africa/Cairo",
			"lat": 30.05,
			"long": 31.25,
			"countries": [
				"EG"
			],
			"comments": ""
		},
		"Africa/El_Aaiun": {
			"name": "Africa/El_Aaiun",
			"lat": 27.15,
			"long": - 12.8,
			"countries": [
				"EH"
			],
			"comments": ""
		},
		"Europe/Madrid": {
			"name": "Europe/Madrid",
			"lat": 40.4,
			"long": - 2.3167,
			"countries": [
				"ES"
			],
			"comments": "Spain (mainland)"
		},
		"Africa/Ceuta": {
			"name": "Africa/Ceuta",
			"lat": 35.8833,
			"long": - 4.6833,
			"countries": [
				"ES"
			],
			"comments": "Ceuta, Melilla"
		},
		"Atlantic/Canary": {
			"name": "Atlantic/Canary",
			"lat": 28.1,
			"long": - 14.6,
			"countries": [
				"ES"
			],
			"comments": "Canary Islands"
		},
		"Europe/Helsinki": {
			"name": "Europe/Helsinki",
			"lat": 60.1667,
			"long": 24.9667,
			"countries": [
				"FI",
				"AX"
			],
			"comments": ""
		},
		"Pacific/Fiji": {
			"name": "Pacific/Fiji",
			"lat": - 17.8667,
			"long": 178.4167,
			"countries": [
				"FJ"
			],
			"comments": ""
		},
		"Atlantic/Stanley": {
			"name": "Atlantic/Stanley",
			"lat": - 50.3,
			"long": - 56.15,
			"countries": [
				"FK"
			],
			"comments": ""
		},
		"Pacific/Chuuk": {
			"name": "Pacific/Chuuk",
			"lat": 7.4167,
			"long": 151.7833,
			"countries": [
				"FM"
			],
			"comments": "Chuuk/Truk, Yap"
		},
		"Pacific/Pohnpei": {
			"name": "Pacific/Pohnpei",
			"lat": 6.9667,
			"long": 158.2167,
			"countries": [
				"FM"
			],
			"comments": "Pohnpei/Ponape"
		},
		"Pacific/Kosrae": {
			"name": "Pacific/Kosrae",
			"lat": 5.3167,
			"long": 162.9833,
			"countries": [
				"FM"
			],
			"comments": "Kosrae"
		},
		"Atlantic/Faroe": {
			"name": "Atlantic/Faroe",
			"lat": 62.0167,
			"long": - 5.2333,
			"countries": [
				"FO"
			],
			"comments": ""
		},
		"Europe/Paris": {
			"name": "Europe/Paris",
			"lat": 48.8667,
			"long": 2.3333,
			"countries": [
				"FR"
			],
			"comments": ""
		},
		"Europe/London": {
			"name": "Europe/London",
			"lat": 51.5083,
			"long": 0.1253,
			"countries": [
				"GB",
				"GG",
				"IM",
				"JE"
			],
			"comments": ""
		},
		"Asia/Tbilisi": {
			"name": "Asia/Tbilisi",
			"lat": 41.7167,
			"long": 44.8167,
			"countries": [
				"GE"
			],
			"comments": ""
		},
		"America/Cayenne": {
			"name": "America/Cayenne",
			"lat": 4.9333,
			"long": - 51.6667,
			"countries": [
				"GF"
			],
			"comments": ""
		},
		"Africa/Accra": {
			"name": "Africa/Accra",
			"lat": 5.55,
			"long": 0.2167,
			"countries": [
				"GH"
			],
			"comments": ""
		},
		"Europe/Gibraltar": {
			"name": "Europe/Gibraltar",
			"lat": 36.1333,
			"long": - 4.65,
			"countries": [
				"GI"
			],
			"comments": ""
		},
		"America/Godthab": {
			"name": "America/Godthab",
			"lat": 64.1833,
			"long": - 50.2667,
			"countries": [
				"GL"
			],
			"comments": "Greenland (most areas)"
		},
		"America/Danmarkshavn": {
			"name": "America/Danmarkshavn",
			"lat": 76.7667,
			"long": - 17.3333,
			"countries": [
				"GL"
			],
			"comments": "National Park (east coast)"
		},
		"America/Scoresbysund": {
			"name": "America/Scoresbysund",
			"lat": 70.4833,
			"long": - 20.0333,
			"countries": [
				"GL"
			],
			"comments": "Scoresbysund/Ittoqqortoormiit"
		},
		"America/Thule": {
			"name": "America/Thule",
			"lat": 76.5667,
			"long": - 67.2167,
			"countries": [
				"GL"
			],
			"comments": "Thule/Pituffik"
		},
		"Europe/Athens": {
			"name": "Europe/Athens",
			"lat": 37.9667,
			"long": 23.7167,
			"countries": [
				"GR"
			],
			"comments": ""
		},
		"Atlantic/South_Georgia": {
			"name": "Atlantic/South_Georgia",
			"lat": - 53.7333,
			"long": - 35.4667,
			"countries": [
				"GS"
			],
			"comments": ""
		},
		"America/Guatemala": {
			"name": "America/Guatemala",
			"lat": 14.6333,
			"long": - 89.4833,
			"countries": [
				"GT"
			],
			"comments": ""
		},
		"Pacific/Guam": {
			"name": "Pacific/Guam",
			"lat": 13.4667,
			"long": 144.75,
			"countries": [
				"GU",
				"MP"
			],
			"comments": ""
		},
		"Africa/Bissau": {
			"name": "Africa/Bissau",
			"lat": 11.85,
			"long": - 14.4167,
			"countries": [
				"GW"
			],
			"comments": ""
		},
		"America/Guyana": {
			"name": "America/Guyana",
			"lat": 6.8,
			"long": - 57.8333,
			"countries": [
				"GY"
			],
			"comments": ""
		},
		"Asia/Hong_Kong": {
			"name": "Asia/Hong_Kong",
			"lat": 22.2833,
			"long": 114.15,
			"countries": [
				"HK"
			],
			"comments": ""
		},
		"America/Tegucigalpa": {
			"name": "America/Tegucigalpa",
			"lat": 14.1,
			"long": - 86.7833,
			"countries": [
				"HN"
			],
			"comments": ""
		},
		"America/Port-au-Prince": {
			"name": "America/Port-au-Prince",
			"lat": 18.5333,
			"long": - 71.6667,
			"countries": [
				"HT"
			],
			"comments": ""
		},
		"Europe/Budapest": {
			"name": "Europe/Budapest",
			"lat": 47.5,
			"long": 19.0833,
			"countries": [
				"HU"
			],
			"comments": ""
		},
		"Asia/Jakarta": {
			"name": "Asia/Jakarta",
			"lat": - 5.8333,
			"long": 106.8,
			"countries": [
				"ID"
			],
			"comments": "Java, Sumatra"
		},
		"Asia/Pontianak": {
			"name": "Asia/Pontianak",
			"lat": 0.0333,
			"long": 109.3333,
			"countries": [
				"ID"
			],
			"comments": "Borneo (west, central)"
		},
		"Asia/Makassar": {
			"name": "Asia/Makassar",
			"lat": - 4.8833,
			"long": 119.4,
			"countries": [
				"ID"
			],
			"comments": "Borneo (east, south); Sulawesi/Celebes, Bali, Nusa Tengarra; Timor (west)"
		},
		"Asia/Jayapura": {
			"name": "Asia/Jayapura",
			"lat": - 1.4667,
			"long": 140.7,
			"countries": [
				"ID"
			],
			"comments": "New Guinea (West Papua / Irian Jaya); Malukus/Moluccas"
		},
		"Europe/Dublin": {
			"name": "Europe/Dublin",
			"lat": 53.3333,
			"long": - 5.75,
			"countries": [
				"IE"
			],
			"comments": ""
		},
		"Asia/Jerusalem": {
			"name": "Asia/Jerusalem",
			"lat": 31.7806,
			"long": 35.2239,
			"countries": [
				"IL"
			],
			"comments": ""
		},
		"Asia/Kolkata": {
			"name": "Asia/Kolkata",
			"lat": 22.5333,
			"long": 88.3667,
			"countries": [
				"IN"
			],
			"comments": ""
		},
		"Indian/Chagos": {
			"name": "Indian/Chagos",
			"lat": - 6.6667,
			"long": 72.4167,
			"countries": [
				"IO"
			],
			"comments": ""
		},
		"Asia/Baghdad": {
			"name": "Asia/Baghdad",
			"lat": 33.35,
			"long": 44.4167,
			"countries": [
				"IQ"
			],
			"comments": ""
		},
		"Asia/Tehran": {
			"name": "Asia/Tehran",
			"lat": 35.6667,
			"long": 51.4333,
			"countries": [
				"IR"
			],
			"comments": ""
		},
		"Atlantic/Reykjavik": {
			"name": "Atlantic/Reykjavik",
			"lat": 64.15,
			"long": - 20.15,
			"countries": [
				"IS"
			],
			"comments": ""
		},
		"Europe/Rome": {
			"name": "Europe/Rome",
			"lat": 41.9,
			"long": 12.4833,
			"countries": [
				"IT",
				"SM",
				"VA"
			],
			"comments": ""
		},
		"America/Jamaica": {
			"name": "America/Jamaica",
			"lat": 17.9681,
			"long": - 75.2067,
			"countries": [
				"JM"
			],
			"comments": ""
		},
		"Asia/Amman": {
			"name": "Asia/Amman",
			"lat": 31.95,
			"long": 35.9333,
			"countries": [
				"JO"
			],
			"comments": ""
		},
		"Asia/Tokyo": {
			"name": "Asia/Tokyo",
			"lat": 35.6544,
			"long": 139.7447,
			"countries": [
				"JP"
			],
			"comments": ""
		},
		"Africa/Nairobi": {
			"name": "Africa/Nairobi",
			"lat": - 0.7167,
			"long": 36.8167,
			"countries": [
				"KE",
				"DJ",
				"ER",
				"ET",
				"KM",
				"MG",
				"SO",
				"TZ",
				"UG",
				"YT"
			],
			"comments": ""
		},
		"Asia/Bishkek": {
			"name": "Asia/Bishkek",
			"lat": 42.9,
			"long": 74.6,
			"countries": [
				"KG"
			],
			"comments": ""
		},
		"Pacific/Tarawa": {
			"name": "Pacific/Tarawa",
			"lat": 1.4167,
			"long": 173,
			"countries": [
				"KI"
			],
			"comments": "Gilbert Islands"
		},
		"Pacific/Enderbury": {
			"name": "Pacific/Enderbury",
			"lat": - 2.8667,
			"long": - 170.9167,
			"countries": [
				"KI"
			],
			"comments": "Phoenix Islands"
		},
		"Pacific/Kiritimati": {
			"name": "Pacific/Kiritimati",
			"lat": 1.8667,
			"long": - 156.6667,
			"countries": [
				"KI"
			],
			"comments": "Line Islands"
		},
		"Asia/Pyongyang": {
			"name": "Asia/Pyongyang",
			"lat": 39.0167,
			"long": 125.75,
			"countries": [
				"KP"
			],
			"comments": ""
		},
		"Asia/Seoul": {
			"name": "Asia/Seoul",
			"lat": 37.55,
			"long": 126.9667,
			"countries": [
				"KR"
			],
			"comments": ""
		},
		"Asia/Almaty": {
			"name": "Asia/Almaty",
			"lat": 43.25,
			"long": 76.95,
			"countries": [
				"KZ"
			],
			"comments": "Kazakhstan (most areas)"
		},
		"Asia/Qyzylorda": {
			"name": "Asia/Qyzylorda",
			"lat": 44.8,
			"long": 65.4667,
			"countries": [
				"KZ"
			],
			"comments": "Qyzylorda/Kyzylorda/Kzyl-Orda"
		},
		"Asia/Aqtobe": {
			"name": "Asia/Aqtobe",
			"lat": 50.2833,
			"long": 57.1667,
			"countries": [
				"KZ"
			],
			"comments": "Aqtobe/Aktobe"
		},
		"Asia/Aqtau": {
			"name": "Asia/Aqtau",
			"lat": 44.5167,
			"long": 50.2667,
			"countries": [
				"KZ"
			],
			"comments": "Atyrau/Atirau/Gur'yev, Mangghystau/Mankistau"
		},
		"Asia/Oral": {
			"name": "Asia/Oral",
			"lat": 51.2167,
			"long": 51.35,
			"countries": [
				"KZ"
			],
			"comments": "West Kazakhstan"
		},
		"Asia/Beirut": {
			"name": "Asia/Beirut",
			"lat": 33.8833,
			"long": 35.5,
			"countries": [
				"LB"
			],
			"comments": ""
		},
		"Asia/Colombo": {
			"name": "Asia/Colombo",
			"lat": 6.9333,
			"long": 79.85,
			"countries": [
				"LK"
			],
			"comments": ""
		},
		"Africa/Monrovia": {
			"name": "Africa/Monrovia",
			"lat": 6.3,
			"long": - 9.2167,
			"countries": [
				"LR"
			],
			"comments": ""
		},
		"Europe/Vilnius": {
			"name": "Europe/Vilnius",
			"lat": 54.6833,
			"long": 25.3167,
			"countries": [
				"LT"
			],
			"comments": ""
		},
		"Europe/Luxembourg": {
			"name": "Europe/Luxembourg",
			"lat": 49.6,
			"long": 6.15,
			"countries": [
				"LU"
			],
			"comments": ""
		},
		"Europe/Riga": {
			"name": "Europe/Riga",
			"lat": 56.95,
			"long": 24.1,
			"countries": [
				"LV"
			],
			"comments": ""
		},
		"Africa/Tripoli": {
			"name": "Africa/Tripoli",
			"lat": 32.9,
			"long": 13.1833,
			"countries": [
				"LY"
			],
			"comments": ""
		},
		"Africa/Casablanca": {
			"name": "Africa/Casablanca",
			"lat": 33.65,
			"long": - 6.4167,
			"countries": [
				"MA"
			],
			"comments": ""
		},
		"Europe/Monaco": {
			"name": "Europe/Monaco",
			"lat": 43.7,
			"long": 7.3833,
			"countries": [
				"MC"
			],
			"comments": ""
		},
		"Europe/Chisinau": {
			"name": "Europe/Chisinau",
			"lat": 47,
			"long": 28.8333,
			"countries": [
				"MD"
			],
			"comments": ""
		},
		"Pacific/Majuro": {
			"name": "Pacific/Majuro",
			"lat": 7.15,
			"long": 171.2,
			"countries": [
				"MH"
			],
			"comments": "Marshall Islands (most areas)"
		},
		"Pacific/Kwajalein": {
			"name": "Pacific/Kwajalein",
			"lat": 9.0833,
			"long": 167.3333,
			"countries": [
				"MH"
			],
			"comments": "Kwajalein"
		},
		"Asia/Rangoon": {
			"name": "Asia/Rangoon",
			"lat": 16.7833,
			"long": 96.1667,
			"countries": [
				"MM"
			],
			"comments": ""
		},
		"Asia/Ulaanbaatar": {
			"name": "Asia/Ulaanbaatar",
			"lat": 47.9167,
			"long": 106.8833,
			"countries": [
				"MN"
			],
			"comments": "Mongolia (most areas)"
		},
		"Asia/Hovd": {
			"name": "Asia/Hovd",
			"lat": 48.0167,
			"long": 91.65,
			"countries": [
				"MN"
			],
			"comments": "Bayan-Ölgii, Govi-Altai, Hovd, Uvs, Zavkhan"
		},
		"Asia/Choibalsan": {
			"name": "Asia/Choibalsan",
			"lat": 48.0667,
			"long": 114.5,
			"countries": [
				"MN"
			],
			"comments": "Dornod, Sükhbaatar"
		},
		"Asia/Macau": {
			"name": "Asia/Macau",
			"lat": 22.2333,
			"long": 113.5833,
			"countries": [
				"MO"
			],
			"comments": ""
		},
		"America/Martinique": {
			"name": "America/Martinique",
			"lat": 14.6,
			"long": - 60.9167,
			"countries": [
				"MQ"
			],
			"comments": ""
		},
		"Europe/Malta": {
			"name": "Europe/Malta",
			"lat": 35.9,
			"long": 14.5167,
			"countries": [
				"MT"
			],
			"comments": ""
		},
		"Indian/Mauritius": {
			"name": "Indian/Mauritius",
			"lat": - 19.8333,
			"long": 57.5,
			"countries": [
				"MU"
			],
			"comments": ""
		},
		"Indian/Maldives": {
			"name": "Indian/Maldives",
			"lat": 4.1667,
			"long": 73.5,
			"countries": [
				"MV"
			],
			"comments": ""
		},
		"America/Mexico_City": {
			"name": "America/Mexico_City",
			"lat": 19.4,
			"long": - 98.85,
			"countries": [
				"MX"
			],
			"comments": "Central Time"
		},
		"America/Cancun": {
			"name": "America/Cancun",
			"lat": 21.0833,
			"long": - 85.2333,
			"countries": [
				"MX"
			],
			"comments": "Eastern Standard Time - Quintana Roo"
		},
		"America/Merida": {
			"name": "America/Merida",
			"lat": 20.9667,
			"long": - 88.3833,
			"countries": [
				"MX"
			],
			"comments": "Central Time - Campeche, Yucatán"
		},
		"America/Monterrey": {
			"name": "America/Monterrey",
			"lat": 25.6667,
			"long": - 99.6833,
			"countries": [
				"MX"
			],
			"comments": "Central Time - Durango; Coahuila, Nuevo León, Tamaulipas (most areas)"
		},
		"America/Matamoros": {
			"name": "America/Matamoros",
			"lat": 25.8333,
			"long": - 96.5,
			"countries": [
				"MX"
			],
			"comments": "Central Time US - Coahuila, Nuevo León, Tamaulipas (US border)"
		},
		"America/Mazatlan": {
			"name": "America/Mazatlan",
			"lat": 23.2167,
			"long": - 105.5833,
			"countries": [
				"MX"
			],
			"comments": "Mountain Time - Baja California Sur, Nayarit, Sinaloa"
		},
		"America/Chihuahua": {
			"name": "America/Chihuahua",
			"lat": 28.6333,
			"long": - 105.9167,
			"countries": [
				"MX"
			],
			"comments": "Mountain Time - Chihuahua (most areas)"
		},
		"America/Ojinaga": {
			"name": "America/Ojinaga",
			"lat": 29.5667,
			"long": - 103.5833,
			"countries": [
				"MX"
			],
			"comments": "Mountain Time US - Chihuahua (US border)"
		},
		"America/Hermosillo": {
			"name": "America/Hermosillo",
			"lat": 29.0667,
			"long": - 109.0333,
			"countries": [
				"MX"
			],
			"comments": "Mountain Standard Time - Sonora"
		},
		"America/Tijuana": {
			"name": "America/Tijuana",
			"lat": 32.5333,
			"long": - 116.9833,
			"countries": [
				"MX"
			],
			"comments": "Pacific Time US - Baja California"
		},
		"America/Bahia_Banderas": {
			"name": "America/Bahia_Banderas",
			"lat": 20.8,
			"long": - 104.75,
			"countries": [
				"MX"
			],
			"comments": "Central Time - Bahía de Banderas"
		},
		"Asia/Kuala_Lumpur": {
			"name": "Asia/Kuala_Lumpur",
			"lat": 3.1667,
			"long": 101.7,
			"countries": [
				"MY"
			],
			"comments": "Malaysia (peninsula)"
		},
		"Asia/Kuching": {
			"name": "Asia/Kuching",
			"lat": 1.55,
			"long": 110.3333,
			"countries": [
				"MY"
			],
			"comments": "Sabah, Sarawak"
		},
		"Africa/Maputo": {
			"name": "Africa/Maputo",
			"lat": - 24.0333,
			"long": 32.5833,
			"countries": [
				"MZ",
				"BI",
				"BW",
				"CD",
				"MW",
				"RW",
				"ZM",
				"ZW"
			],
			"comments": "Central Africa Time"
		},
		"Africa/Windhoek": {
			"name": "Africa/Windhoek",
			"lat": - 21.4333,
			"long": 17.1,
			"countries": [
				"NA"
			],
			"comments": ""
		},
		"Pacific/Noumea": {
			"name": "Pacific/Noumea",
			"lat": - 21.7333,
			"long": 166.45,
			"countries": [
				"NC"
			],
			"comments": ""
		},
		"Pacific/Norfolk": {
			"name": "Pacific/Norfolk",
			"lat": - 28.95,
			"long": 167.9667,
			"countries": [
				"NF"
			],
			"comments": ""
		},
		"Africa/Lagos": {
			"name": "Africa/Lagos",
			"lat": 6.45,
			"long": 3.4,
			"countries": [
				"NG",
				"AO",
				"BJ",
				"CD",
				"CF",
				"CG",
				"CM",
				"GA",
				"GQ",
				"NE"
			],
			"comments": "West Africa Time"
		},
		"America/Managua": {
			"name": "America/Managua",
			"lat": 12.15,
			"long": - 85.7167,
			"countries": [
				"NI"
			],
			"comments": ""
		},
		"Europe/Amsterdam": {
			"name": "Europe/Amsterdam",
			"lat": 52.3667,
			"long": 4.9,
			"countries": [
				"NL"
			],
			"comments": ""
		},
		"Europe/Oslo": {
			"name": "Europe/Oslo",
			"lat": 59.9167,
			"long": 10.75,
			"countries": [
				"NO",
				"SJ"
			],
			"comments": ""
		},
		"Asia/Kathmandu": {
			"name": "Asia/Kathmandu",
			"lat": 27.7167,
			"long": 85.3167,
			"countries": [
				"NP"
			],
			"comments": ""
		},
		"Pacific/Nauru": {
			"name": "Pacific/Nauru",
			"lat": 0.5167,
			"long": 166.9167,
			"countries": [
				"NR"
			],
			"comments": ""
		},
		"Pacific/Niue": {
			"name": "Pacific/Niue",
			"lat": - 18.9833,
			"long": - 168.0833,
			"countries": [
				"NU"
			],
			"comments": ""
		},
		"Pacific/Auckland": {
			"name": "Pacific/Auckland",
			"lat": - 35.1333,
			"long": 174.7667,
			"countries": [
				"NZ",
				"AQ"
			],
			"comments": "New Zealand time"
		},
		"Pacific/Chatham": {
			"name": "Pacific/Chatham",
			"lat": - 42.05,
			"long": - 175.45,
			"countries": [
				"NZ"
			],
			"comments": "Chatham Islands"
		},
		"America/Panama": {
			"name": "America/Panama",
			"lat": 8.9667,
			"long": - 78.4667,
			"countries": [
				"PA",
				"KY"
			],
			"comments": ""
		},
		"America/Lima": {
			"name": "America/Lima",
			"lat": - 11.95,
			"long": - 76.95,
			"countries": [
				"PE"
			],
			"comments": ""
		},
		"Pacific/Tahiti": {
			"name": "Pacific/Tahiti",
			"lat": - 16.4667,
			"long": - 148.4333,
			"countries": [
				"PF"
			],
			"comments": "Society Islands"
		},
		"Pacific/Marquesas": {
			"name": "Pacific/Marquesas",
			"lat": - 9,
			"long": - 138.5,
			"countries": [
				"PF"
			],
			"comments": "Marquesas Islands"
		},
		"Pacific/Gambier": {
			"name": "Pacific/Gambier",
			"lat": - 22.8667,
			"long": - 133.05,
			"countries": [
				"PF"
			],
			"comments": "Gambier Islands"
		},
		"Pacific/Port_Moresby": {
			"name": "Pacific/Port_Moresby",
			"lat": - 8.5,
			"long": 147.1667,
			"countries": [
				"PG"
			],
			"comments": "Papua New Guinea (most areas)"
		},
		"Pacific/Bougainville": {
			"name": "Pacific/Bougainville",
			"lat": - 5.7833,
			"long": 155.5667,
			"countries": [
				"PG"
			],
			"comments": "Bougainville"
		},
		"Asia/Manila": {
			"name": "Asia/Manila",
			"lat": 14.5833,
			"long": 121,
			"countries": [
				"PH"
			],
			"comments": ""
		},
		"Asia/Karachi": {
			"name": "Asia/Karachi",
			"lat": 24.8667,
			"long": 67.05,
			"countries": [
				"PK"
			],
			"comments": ""
		},
		"Europe/Warsaw": {
			"name": "Europe/Warsaw",
			"lat": 52.25,
			"long": 21,
			"countries": [
				"PL"
			],
			"comments": ""
		},
		"America/Miquelon": {
			"name": "America/Miquelon",
			"lat": 47.05,
			"long": - 55.6667,
			"countries": [
				"PM"
			],
			"comments": ""
		},
		"Pacific/Pitcairn": {
			"name": "Pacific/Pitcairn",
			"lat": - 24.9333,
			"long": - 129.9167,
			"countries": [
				"PN"
			],
			"comments": ""
		},
		"America/Puerto_Rico": {
			"name": "America/Puerto_Rico",
			"lat": 18.4683,
			"long": - 65.8939,
			"countries": [
				"PR"
			],
			"comments": ""
		},
		"Asia/Gaza": {
			"name": "Asia/Gaza",
			"lat": 31.5,
			"long": 34.4667,
			"countries": [
				"PS"
			],
			"comments": "Gaza Strip"
		},
		"Asia/Hebron": {
			"name": "Asia/Hebron",
			"lat": 31.5333,
			"long": 35.095,
			"countries": [
				"PS"
			],
			"comments": "West Bank"
		},
		"Europe/Lisbon": {
			"name": "Europe/Lisbon",
			"lat": 38.7167,
			"long": - 8.8667,
			"countries": [
				"PT"
			],
			"comments": "Portugal (mainland)"
		},
		"Atlantic/Madeira": {
			"name": "Atlantic/Madeira",
			"lat": 32.6333,
			"long": - 15.1,
			"countries": [
				"PT"
			],
			"comments": "Madeira Islands"
		},
		"Atlantic/Azores": {
			"name": "Atlantic/Azores",
			"lat": 37.7333,
			"long": - 24.3333,
			"countries": [
				"PT"
			],
			"comments": "Azores"
		},
		"Pacific/Palau": {
			"name": "Pacific/Palau",
			"lat": 7.3333,
			"long": 134.4833,
			"countries": [
				"PW"
			],
			"comments": ""
		},
		"America/Asuncion": {
			"name": "America/Asuncion",
			"lat": - 24.7333,
			"long": - 56.3333,
			"countries": [
				"PY"
			],
			"comments": ""
		},
		"Asia/Qatar": {
			"name": "Asia/Qatar",
			"lat": 25.2833,
			"long": 51.5333,
			"countries": [
				"QA",
				"BH"
			],
			"comments": ""
		},
		"Indian/Reunion": {
			"name": "Indian/Reunion",
			"lat": - 19.1333,
			"long": 55.4667,
			"countries": [
				"RE",
				"TF"
			],
			"comments": "Réunion, Crozet, Scattered Islands"
		},
		"Europe/Bucharest": {
			"name": "Europe/Bucharest",
			"lat": 44.4333,
			"long": 26.1,
			"countries": [
				"RO"
			],
			"comments": ""
		},
		"Europe/Belgrade": {
			"name": "Europe/Belgrade",
			"lat": 44.8333,
			"long": 20.5,
			"countries": [
				"RS",
				"BA",
				"HR",
				"ME",
				"MK",
				"SI"
			],
			"comments": ""
		},
		"Europe/Kaliningrad": {
			"name": "Europe/Kaliningrad",
			"lat": 54.7167,
			"long": 20.5,
			"countries": [
				"RU"
			],
			"comments": "MSK-01 - Kaliningrad"
		},
		"Europe/Moscow": {
			"name": "Europe/Moscow",
			"lat": 55.7558,
			"long": 37.6178,
			"countries": [
				"RU"
			],
			"comments": "MSK+00 - Moscow area"
		},
		"Europe/Simferopol": {
			"name": "Europe/Simferopol",
			"lat": 44.95,
			"long": 34.1,
			"countries": [
				"RU"
			],
			"comments": "MSK+00 - Crimea"
		},
		"Europe/Volgograd": {
			"name": "Europe/Volgograd",
			"lat": 48.7333,
			"long": 44.4167,
			"countries": [
				"RU"
			],
			"comments": "MSK+00 - Volgograd, Saratov"
		},
		"Europe/Kirov": {
			"name": "Europe/Kirov",
			"lat": 58.6,
			"long": 49.65,
			"countries": [
				"RU"
			],
			"comments": "MSK+00 - Kirov"
		},
		"Europe/Astrakhan": {
			"name": "Europe/Astrakhan",
			"lat": 46.35,
			"long": 48.05,
			"countries": [
				"RU"
			],
			"comments": "MSK+01 - Astrakhan"
		},
		"Europe/Samara": {
			"name": "Europe/Samara",
			"lat": 53.2,
			"long": 50.15,
			"countries": [
				"RU"
			],
			"comments": "MSK+01 - Samara, Udmurtia"
		},
		"Europe/Ulyanovsk": {
			"name": "Europe/Ulyanovsk",
			"lat": 54.3333,
			"long": 48.4,
			"countries": [
				"RU"
			],
			"comments": "MSK+01 - Ulyanovsk"
		},
		"Asia/Yekaterinburg": {
			"name": "Asia/Yekaterinburg",
			"lat": 56.85,
			"long": 60.6,
			"countries": [
				"RU"
			],
			"comments": "MSK+02 - Urals"
		},
		"Asia/Omsk": {
			"name": "Asia/Omsk",
			"lat": 55,
			"long": 73.4,
			"countries": [
				"RU"
			],
			"comments": "MSK+03 - Omsk"
		},
		"Asia/Novosibirsk": {
			"name": "Asia/Novosibirsk",
			"lat": 55.0333,
			"long": 82.9167,
			"countries": [
				"RU"
			],
			"comments": "MSK+03 - Novosibirsk"
		},
		"Asia/Barnaul": {
			"name": "Asia/Barnaul",
			"lat": 53.3667,
			"long": 83.75,
			"countries": [
				"RU"
			],
			"comments": "MSK+04 - Altai"
		},
		"Asia/Tomsk": {
			"name": "Asia/Tomsk",
			"lat": 56.5,
			"long": 84.9667,
			"countries": [
				"RU"
			],
			"comments": "MSK+04 - Tomsk"
		},
		"Asia/Novokuznetsk": {
			"name": "Asia/Novokuznetsk",
			"lat": 53.75,
			"long": 87.1167,
			"countries": [
				"RU"
			],
			"comments": "MSK+04 - Kemerovo"
		},
		"Asia/Krasnoyarsk": {
			"name": "Asia/Krasnoyarsk",
			"lat": 56.0167,
			"long": 92.8333,
			"countries": [
				"RU"
			],
			"comments": "MSK+04 - Krasnoyarsk area"
		},
		"Asia/Irkutsk": {
			"name": "Asia/Irkutsk",
			"lat": 52.2667,
			"long": 104.3333,
			"countries": [
				"RU"
			],
			"comments": "MSK+05 - Irkutsk, Buryatia"
		},
		"Asia/Chita": {
			"name": "Asia/Chita",
			"lat": 52.05,
			"long": 113.4667,
			"countries": [
				"RU"
			],
			"comments": "MSK+06 - Zabaykalsky"
		},
		"Asia/Yakutsk": {
			"name": "Asia/Yakutsk",
			"lat": 62,
			"long": 129.6667,
			"countries": [
				"RU"
			],
			"comments": "MSK+06 - Lena River"
		},
		"Asia/Khandyga": {
			"name": "Asia/Khandyga",
			"lat": 62.6564,
			"long": 135.5539,
			"countries": [
				"RU"
			],
			"comments": "MSK+06 - Tomponsky, Ust-Maysky"
		},
		"Asia/Vladivostok": {
			"name": "Asia/Vladivostok",
			"lat": 43.1667,
			"long": 131.9333,
			"countries": [
				"RU"
			],
			"comments": "MSK+07 - Amur River"
		},
		"Asia/Ust-Nera": {
			"name": "Asia/Ust-Nera",
			"lat": 64.5603,
			"long": 143.2267,
			"countries": [
				"RU"
			],
			"comments": "MSK+07 - Oymyakonsky"
		},
		"Asia/Magadan": {
			"name": "Asia/Magadan",
			"lat": 59.5667,
			"long": 150.8,
			"countries": [
				"RU"
			],
			"comments": "MSK+08 - Magadan"
		},
		"Asia/Sakhalin": {
			"name": "Asia/Sakhalin",
			"lat": 46.9667,
			"long": 142.7,
			"countries": [
				"RU"
			],
			"comments": "MSK+08 - Sakhalin Island"
		},
		"Asia/Srednekolymsk": {
			"name": "Asia/Srednekolymsk",
			"lat": 67.4667,
			"long": 153.7167,
			"countries": [
				"RU"
			],
			"comments": "MSK+08 - Sakha (E); North Kuril Is"
		},
		"Asia/Kamchatka": {
			"name": "Asia/Kamchatka",
			"lat": 53.0167,
			"long": 158.65,
			"countries": [
				"RU"
			],
			"comments": "MSK+09 - Kamchatka"
		},
		"Asia/Anadyr": {
			"name": "Asia/Anadyr",
			"lat": 64.75,
			"long": 177.4833,
			"countries": [
				"RU"
			],
			"comments": "MSK+09 - Bering Sea"
		},
		"Asia/Riyadh": {
			"name": "Asia/Riyadh",
			"lat": 24.6333,
			"long": 46.7167,
			"countries": [
				"SA",
				"KW",
				"YE"
			],
			"comments": ""
		},
		"Pacific/Guadalcanal": {
			"name": "Pacific/Guadalcanal",
			"lat": - 8.4667,
			"long": 160.2,
			"countries": [
				"SB"
			],
			"comments": ""
		},
		"Indian/Mahe": {
			"name": "Indian/Mahe",
			"lat": - 3.3333,
			"long": 55.4667,
			"countries": [
				"SC"
			],
			"comments": ""
		},
		"Africa/Khartoum": {
			"name": "Africa/Khartoum",
			"lat": 15.6,
			"long": 32.5333,
			"countries": [
				"SD",
				"SS"
			],
			"comments": ""
		},
		"Europe/Stockholm": {
			"name": "Europe/Stockholm",
			"lat": 59.3333,
			"long": 18.05,
			"countries": [
				"SE"
			],
			"comments": ""
		},
		"Asia/Singapore": {
			"name": "Asia/Singapore",
			"lat": 1.2833,
			"long": 103.85,
			"countries": [
				"SG"
			],
			"comments": ""
		},
		"America/Paramaribo": {
			"name": "America/Paramaribo",
			"lat": 5.8333,
			"long": - 54.8333,
			"countries": [
				"SR"
			],
			"comments": ""
		},
		"America/El_Salvador": {
			"name": "America/El_Salvador",
			"lat": 13.7,
			"long": - 88.8,
			"countries": [
				"SV"
			],
			"comments": ""
		},
		"Asia/Damascus": {
			"name": "Asia/Damascus",
			"lat": 33.5,
			"long": 36.3,
			"countries": [
				"SY"
			],
			"comments": ""
		},
		"America/Grand_Turk": {
			"name": "America/Grand_Turk",
			"lat": 21.4667,
			"long": - 70.8667,
			"countries": [
				"TC"
			],
			"comments": ""
		},
		"Africa/Ndjamena": {
			"name": "Africa/Ndjamena",
			"lat": 12.1167,
			"long": 15.05,
			"countries": [
				"TD"
			],
			"comments": ""
		},
		"Indian/Kerguelen": {
			"name": "Indian/Kerguelen",
			"lat": - 48.6472,
			"long": 70.2175,
			"countries": [
				"TF"
			],
			"comments": "Kerguelen, St Paul Island, Amsterdam Island"
		},
		"Asia/Bangkok": {
			"name": "Asia/Bangkok",
			"lat": 13.75,
			"long": 100.5167,
			"countries": [
				"TH",
				"KH",
				"LA",
				"VN"
			],
			"comments": "Indochina (most areas)"
		},
		"Asia/Dushanbe": {
			"name": "Asia/Dushanbe",
			"lat": 38.5833,
			"long": 68.8,
			"countries": [
				"TJ"
			],
			"comments": ""
		},
		"Pacific/Fakaofo": {
			"name": "Pacific/Fakaofo",
			"lat": - 8.6333,
			"long": - 170.7667,
			"countries": [
				"TK"
			],
			"comments": ""
		},
		"Asia/Dili": {
			"name": "Asia/Dili",
			"lat": - 7.45,
			"long": 125.5833,
			"countries": [
				"TL"
			],
			"comments": ""
		},
		"Asia/Ashgabat": {
			"name": "Asia/Ashgabat",
			"lat": 37.95,
			"long": 58.3833,
			"countries": [
				"TM"
			],
			"comments": ""
		},
		"Africa/Tunis": {
			"name": "Africa/Tunis",
			"lat": 36.8,
			"long": 10.1833,
			"countries": [
				"TN"
			],
			"comments": ""
		},
		"Pacific/Tongatapu": {
			"name": "Pacific/Tongatapu",
			"lat": - 20.8333,
			"long": - 174.8333,
			"countries": [
				"TO"
			],
			"comments": ""
		},
		"Europe/Istanbul": {
			"name": "Europe/Istanbul",
			"lat": 41.0167,
			"long": 28.9667,
			"countries": [
				"TR"
			],
			"comments": ""
		},
		"America/Port_of_Spain": {
			"name": "America/Port_of_Spain",
			"lat": 10.65,
			"long": - 60.4833,
			"countries": [
				"TT",
				"AG",
				"AI",
				"BL",
				"DM",
				"GD",
				"GP",
				"KN",
				"LC",
				"MF",
				"MS",
				"VC",
				"VG",
				"VI"
			],
			"comments": ""
		},
		"Pacific/Funafuti": {
			"name": "Pacific/Funafuti",
			"lat": - 7.4833,
			"long": 179.2167,
			"countries": [
				"TV"
			],
			"comments": ""
		},
		"Asia/Taipei": {
			"name": "Asia/Taipei",
			"lat": 25.05,
			"long": 121.5,
			"countries": [
				"TW"
			],
			"comments": ""
		},
		"Europe/Kiev": {
			"name": "Europe/Kiev",
			"lat": 50.4333,
			"long": 30.5167,
			"countries": [
				"UA"
			],
			"comments": "Ukraine (most areas)"
		},
		"Europe/Uzhgorod": {
			"name": "Europe/Uzhgorod",
			"lat": 48.6167,
			"long": 22.3,
			"countries": [
				"UA"
			],
			"comments": "Ruthenia"
		},
		"Europe/Zaporozhye": {
			"name": "Europe/Zaporozhye",
			"lat": 47.8333,
			"long": 35.1667,
			"countries": [
				"UA"
			],
			"comments": "Zaporozh'ye/Zaporizhia; Lugansk/Luhansk (east)"
		},
		"Pacific/Wake": {
			"name": "Pacific/Wake",
			"lat": 19.2833,
			"long": 166.6167,
			"countries": [
				"UM"
			],
			"comments": "Wake Island"
		},
		"America/New_York": {
			"name": "America/New_York",
			"lat": 40.7142,
			"long": - 73.9936,
			"countries": [
				"US"
			],
			"comments": "Eastern (most areas)"
		},
		"America/Detroit": {
			"name": "America/Detroit",
			"lat": 42.3314,
			"long": - 82.9542,
			"countries": [
				"US"
			],
			"comments": "Eastern - MI (most areas)"
		},
		"America/Kentucky/Louisville": {
			"name": "America/Kentucky/Louisville",
			"lat": 38.2542,
			"long": - 84.2406,
			"countries": [
				"US"
			],
			"comments": "Eastern - KY (Louisville area)"
		},
		"America/Kentucky/Monticello": {
			"name": "America/Kentucky/Monticello",
			"lat": 36.8297,
			"long": - 83.1508,
			"countries": [
				"US"
			],
			"comments": "Eastern - KY (Wayne)"
		},
		"America/Indiana/Indianapolis": {
			"name": "America/Indiana/Indianapolis",
			"lat": 39.7683,
			"long": - 85.8419,
			"countries": [
				"US"
			],
			"comments": "Eastern - IN (most areas)"
		},
		"America/Indiana/Vincennes": {
			"name": "America/Indiana/Vincennes",
			"lat": 38.6772,
			"long": - 86.4714,
			"countries": [
				"US"
			],
			"comments": "Eastern - IN (Da, Du, K, Mn)"
		},
		"America/Indiana/Winamac": {
			"name": "America/Indiana/Winamac",
			"lat": 41.0514,
			"long": - 85.3969,
			"countries": [
				"US"
			],
			"comments": "Eastern - IN (Pulaski)"
		},
		"America/Indiana/Marengo": {
			"name": "America/Indiana/Marengo",
			"lat": 38.3756,
			"long": - 85.6553,
			"countries": [
				"US"
			],
			"comments": "Eastern - IN (Crawford)"
		},
		"America/Indiana/Petersburg": {
			"name": "America/Indiana/Petersburg",
			"lat": 38.4919,
			"long": - 86.7214,
			"countries": [
				"US"
			],
			"comments": "Eastern - IN (Pike)"
		},
		"America/Indiana/Vevay": {
			"name": "America/Indiana/Vevay",
			"lat": 38.7478,
			"long": - 84.9328,
			"countries": [
				"US"
			],
			"comments": "Eastern - IN (Switzerland)"
		},
		"America/Chicago": {
			"name": "America/Chicago",
			"lat": 41.85,
			"long": - 86.35,
			"countries": [
				"US"
			],
			"comments": "Central (most areas)"
		},
		"America/Indiana/Tell_City": {
			"name": "America/Indiana/Tell_City",
			"lat": 37.9531,
			"long": - 85.2386,
			"countries": [
				"US"
			],
			"comments": "Central - IN (Perry)"
		},
		"America/Indiana/Knox": {
			"name": "America/Indiana/Knox",
			"lat": 41.2958,
			"long": - 85.375,
			"countries": [
				"US"
			],
			"comments": "Central - IN (Starke)"
		},
		"America/Menominee": {
			"name": "America/Menominee",
			"lat": 45.1078,
			"long": - 86.3858,
			"countries": [
				"US"
			],
			"comments": "Central - MI (Wisconsin border)"
		},
		"America/North_Dakota/Center": {
			"name": "America/North_Dakota/Center",
			"lat": 47.1164,
			"long": - 100.7008,
			"countries": [
				"US"
			],
			"comments": "Central - ND (Oliver)"
		},
		"America/North_Dakota/New_Salem": {
			"name": "America/North_Dakota/New_Salem",
			"lat": 46.845,
			"long": - 100.5892,
			"countries": [
				"US"
			],
			"comments": "Central - ND (Morton rural)"
		},
		"America/North_Dakota/Beulah": {
			"name": "America/North_Dakota/Beulah",
			"lat": 47.2642,
			"long": - 100.2222,
			"countries": [
				"US"
			],
			"comments": "Central - ND (Mercer)"
		},
		"America/Denver": {
			"name": "America/Denver",
			"lat": 39.7392,
			"long": - 103.0158,
			"countries": [
				"US"
			],
			"comments": "Mountain (most areas)"
		},
		"America/Boise": {
			"name": "America/Boise",
			"lat": 43.6136,
			"long": - 115.7975,
			"countries": [
				"US"
			],
			"comments": "Mountain - ID (south); OR (east)"
		},
		"America/Phoenix": {
			"name": "America/Phoenix",
			"lat": 33.4483,
			"long": - 111.9267,
			"countries": [
				"US"
			],
			"comments": "MST - Arizona (except Navajo)"
		},
		"America/Los_Angeles": {
			"name": "America/Los_Angeles",
			"lat": 34.0522,
			"long": - 117.7572,
			"countries": [
				"US"
			],
			"comments": "Pacific"
		},
		"America/Anchorage": {
			"name": "America/Anchorage",
			"lat": 61.2181,
			"long": - 148.0997,
			"countries": [
				"US"
			],
			"comments": "Alaska (most areas)"
		},
		"America/Juneau": {
			"name": "America/Juneau",
			"lat": 58.3019,
			"long": - 133.5803,
			"countries": [
				"US"
			],
			"comments": "Alaska - Juneau area"
		},
		"America/Sitka": {
			"name": "America/Sitka",
			"lat": 57.1764,
			"long": - 134.6981,
			"countries": [
				"US"
			],
			"comments": "Alaska - Sitka area"
		},
		"America/Metlakatla": {
			"name": "America/Metlakatla",
			"lat": 55.1269,
			"long": - 130.4236,
			"countries": [
				"US"
			],
			"comments": "Alaska - Annette Island"
		},
		"America/Yakutat": {
			"name": "America/Yakutat",
			"lat": 59.5469,
			"long": - 138.2728,
			"countries": [
				"US"
			],
			"comments": "Alaska - Yakutat"
		},
		"America/Nome": {
			"name": "America/Nome",
			"lat": 64.5011,
			"long": - 164.5936,
			"countries": [
				"US"
			],
			"comments": "Alaska (west)"
		},
		"America/Adak": {
			"name": "America/Adak",
			"lat": 51.88,
			"long": - 175.3419,
			"countries": [
				"US"
			],
			"comments": "Aleutian Islands"
		},
		"Pacific/Honolulu": {
			"name": "Pacific/Honolulu",
			"lat": 21.3069,
			"long": - 156.1417,
			"countries": [
				"US",
				"UM"
			],
			"comments": "Hawaii"
		},
		"America/Montevideo": {
			"name": "America/Montevideo",
			"lat": - 33.1167,
			"long": - 55.8167,
			"countries": [
				"UY"
			],
			"comments": ""
		},
		"Asia/Samarkand": {
			"name": "Asia/Samarkand",
			"lat": 39.6667,
			"long": 66.8,
			"countries": [
				"UZ"
			],
			"comments": "Uzbekistan (west)"
		},
		"Asia/Tashkent": {
			"name": "Asia/Tashkent",
			"lat": 41.3333,
			"long": 69.3,
			"countries": [
				"UZ"
			],
			"comments": "Uzbekistan (east)"
		},
		"America/Caracas": {
			"name": "America/Caracas",
			"lat": 10.5,
			"long": - 65.0667,
			"countries": [
				"VE"
			],
			"comments": ""
		},
		"Asia/Ho_Chi_Minh": {
			"name": "Asia/Ho_Chi_Minh",
			"lat": 10.75,
			"long": 106.6667,
			"countries": [
				"VN"
			],
			"comments": "Vietnam (south)"
		},
		"Pacific/Efate": {
			"name": "Pacific/Efate",
			"lat": - 16.3333,
			"long": 168.4167,
			"countries": [
				"VU"
			],
			"comments": ""
		},
		"Pacific/Wallis": {
			"name": "Pacific/Wallis",
			"lat": - 12.7,
			"long": - 175.8333,
			"countries": [
				"WF"
			],
			"comments": ""
		},
		"Pacific/Apia": {
			"name": "Pacific/Apia",
			"lat": - 12.1667,
			"long": - 170.2667,
			"countries": [
				"WS"
			],
			"comments": ""
		},
		"Africa/Johannesburg": {
			"name": "Africa/Johannesburg",
			"lat": - 25.75,
			"long": 28,
			"countries": [
				"ZA",
				"LS",
				"SZ"
			],
			"comments": ""
		}
	}
};

//! moment.js
//! version : 2.14.1
//! authors : Tim Wood, Iskren Chernev, Moment.js contributors
//! license : MIT
//! momentjs.com
!function(a,b){"object"==typeof exports&&"undefined"!=typeof module?module.exports=b():"function"==typeof define&&define.amd?define(b):a.moment=b()}(this,function(){"use strict";function a(){return je.apply(null,arguments)}
// This is done to register the method called with moment()
// without creating circular dependencies.
function b(a){je=a}function c(a){return a instanceof Array||"[object Array]"===Object.prototype.toString.call(a)}function d(a){return"[object Object]"===Object.prototype.toString.call(a)}function e(a){var b;for(b in a)
// even if its not own property I'd still call it non-empty
return!1;return!0}function f(a){return a instanceof Date||"[object Date]"===Object.prototype.toString.call(a)}function g(a,b){var c,d=[];for(c=0;c<a.length;++c)d.push(b(a[c],c));return d}function h(a,b){return Object.prototype.hasOwnProperty.call(a,b)}function i(a,b){for(var c in b)h(b,c)&&(a[c]=b[c]);return h(b,"toString")&&(a.toString=b.toString),h(b,"valueOf")&&(a.valueOf=b.valueOf),a}function j(a,b,c,d){return qb(a,b,c,d,!0).utc()}function k(){
// We need to deep clone this object.
return{empty:!1,unusedTokens:[],unusedInput:[],overflow:-2,charsLeftOver:0,nullInput:!1,invalidMonth:null,invalidFormat:!1,userInvalidated:!1,iso:!1,parsedDateParts:[],meridiem:null}}function l(a){return null==a._pf&&(a._pf=k()),a._pf}function m(a){if(null==a._isValid){var b=l(a),c=ke.call(b.parsedDateParts,function(a){return null!=a});a._isValid=!isNaN(a._d.getTime())&&b.overflow<0&&!b.empty&&!b.invalidMonth&&!b.invalidWeekday&&!b.nullInput&&!b.invalidFormat&&!b.userInvalidated&&(!b.meridiem||b.meridiem&&c),a._strict&&(a._isValid=a._isValid&&0===b.charsLeftOver&&0===b.unusedTokens.length&&void 0===b.bigHour)}return a._isValid}function n(a){var b=j(NaN);return null!=a?i(l(b),a):l(b).userInvalidated=!0,b}function o(a){return void 0===a}function p(a,b){var c,d,e;if(o(b._isAMomentObject)||(a._isAMomentObject=b._isAMomentObject),o(b._i)||(a._i=b._i),o(b._f)||(a._f=b._f),o(b._l)||(a._l=b._l),o(b._strict)||(a._strict=b._strict),o(b._tzm)||(a._tzm=b._tzm),o(b._isUTC)||(a._isUTC=b._isUTC),o(b._offset)||(a._offset=b._offset),o(b._pf)||(a._pf=l(b)),o(b._locale)||(a._locale=b._locale),le.length>0)for(c in le)d=le[c],e=b[d],o(e)||(a[d]=e);return a}
// Moment prototype object
function q(b){p(this,b),this._d=new Date(null!=b._d?b._d.getTime():NaN),me===!1&&(me=!0,a.updateOffset(this),me=!1)}function r(a){return a instanceof q||null!=a&&null!=a._isAMomentObject}function s(a){return 0>a?Math.ceil(a)||0:Math.floor(a)}function t(a){var b=+a,c=0;return 0!==b&&isFinite(b)&&(c=s(b)),c}
// compare two arrays, return the number of differences
function u(a,b,c){var d,e=Math.min(a.length,b.length),f=Math.abs(a.length-b.length),g=0;for(d=0;e>d;d++)(c&&a[d]!==b[d]||!c&&t(a[d])!==t(b[d]))&&g++;return g+f}function v(b){a.suppressDeprecationWarnings===!1&&"undefined"!=typeof console&&console.warn&&console.warn("Deprecation warning: "+b)}function w(b,c){var d=!0;return i(function(){return null!=a.deprecationHandler&&a.deprecationHandler(null,b),d&&(v(b+"\nArguments: "+Array.prototype.slice.call(arguments).join(", ")+"\n"+(new Error).stack),d=!1),c.apply(this,arguments)},c)}function x(b,c){null!=a.deprecationHandler&&a.deprecationHandler(b,c),ne[b]||(v(c),ne[b]=!0)}function y(a){return a instanceof Function||"[object Function]"===Object.prototype.toString.call(a)}function z(a){var b,c;for(c in a)b=a[c],y(b)?this[c]=b:this["_"+c]=b;this._config=a,
// Lenient ordinal parsing accepts just a number in addition to
// number + (possibly) stuff coming from _ordinalParseLenient.
this._ordinalParseLenient=new RegExp(this._ordinalParse.source+"|"+/\d{1,2}/.source)}function A(a,b){var c,e=i({},a);for(c in b)h(b,c)&&(d(a[c])&&d(b[c])?(e[c]={},i(e[c],a[c]),i(e[c],b[c])):null!=b[c]?e[c]=b[c]:delete e[c]);for(c in a)h(a,c)&&!h(b,c)&&d(a[c])&&(
// make sure changes to properties don't modify parent config
e[c]=i({},e[c]));return e}function B(a){null!=a&&this.set(a)}function C(a,b,c){var d=this._calendar[a]||this._calendar.sameElse;return y(d)?d.call(b,c):d}function D(a){var b=this._longDateFormat[a],c=this._longDateFormat[a.toUpperCase()];return b||!c?b:(this._longDateFormat[a]=c.replace(/MMMM|MM|DD|dddd/g,function(a){return a.slice(1)}),this._longDateFormat[a])}function E(){return this._invalidDate}function F(a){return this._ordinal.replace("%d",a)}function G(a,b,c,d){var e=this._relativeTime[c];return y(e)?e(a,b,c,d):e.replace(/%d/i,a)}function H(a,b){var c=this._relativeTime[a>0?"future":"past"];return y(c)?c(b):c.replace(/%s/i,b)}function I(a,b){var c=a.toLowerCase();we[c]=we[c+"s"]=we[b]=a}function J(a){return"string"==typeof a?we[a]||we[a.toLowerCase()]:void 0}function K(a){var b,c,d={};for(c in a)h(a,c)&&(b=J(c),b&&(d[b]=a[c]));return d}function L(a,b){xe[a]=b}function M(a){var b=[];for(var c in a)b.push({unit:c,priority:xe[c]});return b.sort(function(a,b){return a.priority-b.priority}),b}function N(b,c){return function(d){return null!=d?(P(this,b,d),a.updateOffset(this,c),this):O(this,b)}}function O(a,b){return a.isValid()?a._d["get"+(a._isUTC?"UTC":"")+b]():NaN}function P(a,b,c){a.isValid()&&a._d["set"+(a._isUTC?"UTC":"")+b](c)}
// MOMENTS
function Q(a){return a=J(a),y(this[a])?this[a]():this}function R(a,b){if("object"==typeof a){a=K(a);for(var c=M(a),d=0;d<c.length;d++)this[c[d].unit](a[c[d].unit])}else if(a=J(a),y(this[a]))return this[a](b);return this}function S(a,b,c){var d=""+Math.abs(a),e=b-d.length,f=a>=0;return(f?c?"+":"":"-")+Math.pow(10,Math.max(0,e)).toString().substr(1)+d}
// token:    'M'
// padded:   ['MM', 2]
// ordinal:  'Mo'
// callback: function () { this.month() + 1 }
function T(a,b,c,d){var e=d;"string"==typeof d&&(e=function(){return this[d]()}),a&&(Be[a]=e),b&&(Be[b[0]]=function(){return S(e.apply(this,arguments),b[1],b[2])}),c&&(Be[c]=function(){return this.localeData().ordinal(e.apply(this,arguments),a)})}function U(a){return a.match(/\[[\s\S]/)?a.replace(/^\[|\]$/g,""):a.replace(/\\/g,"")}function V(a){var b,c,d=a.match(ye);for(b=0,c=d.length;c>b;b++)Be[d[b]]?d[b]=Be[d[b]]:d[b]=U(d[b]);return function(b){var e,f="";for(e=0;c>e;e++)f+=d[e]instanceof Function?d[e].call(b,a):d[e];return f}}
// format date using native date object
function W(a,b){return a.isValid()?(b=X(b,a.localeData()),Ae[b]=Ae[b]||V(b),Ae[b](a)):a.localeData().invalidDate()}function X(a,b){function c(a){return b.longDateFormat(a)||a}var d=5;for(ze.lastIndex=0;d>=0&&ze.test(a);)a=a.replace(ze,c),ze.lastIndex=0,d-=1;return a}function Y(a,b,c){Te[a]=y(b)?b:function(a,d){return a&&c?c:b}}function Z(a,b){return h(Te,a)?Te[a](b._strict,b._locale):new RegExp($(a))}
// Code from http://stackoverflow.com/questions/3561493/is-there-a-regexp-escape-function-in-javascript
function $(a){return _(a.replace("\\","").replace(/\\(\[)|\\(\])|\[([^\]\[]*)\]|\\(.)/g,function(a,b,c,d,e){return b||c||d||e}))}function _(a){return a.replace(/[-\/\\^$*+?.()|[\]{}]/g,"\\$&")}function aa(a,b){var c,d=b;for("string"==typeof a&&(a=[a]),"number"==typeof b&&(d=function(a,c){c[b]=t(a)}),c=0;c<a.length;c++)Ue[a[c]]=d}function ba(a,b){aa(a,function(a,c,d,e){d._w=d._w||{},b(a,d._w,d,e)})}function ca(a,b,c){null!=b&&h(Ue,a)&&Ue[a](b,c._a,c,a)}function da(a,b){return new Date(Date.UTC(a,b+1,0)).getUTCDate()}function ea(a,b){return c(this._months)?this._months[a.month()]:this._months[(this._months.isFormat||cf).test(b)?"format":"standalone"][a.month()]}function fa(a,b){return c(this._monthsShort)?this._monthsShort[a.month()]:this._monthsShort[cf.test(b)?"format":"standalone"][a.month()]}function ga(a,b,c){var d,e,f,g=a.toLocaleLowerCase();if(!this._monthsParse)for(
// this is not used
this._monthsParse=[],this._longMonthsParse=[],this._shortMonthsParse=[],d=0;12>d;++d)f=j([2e3,d]),this._shortMonthsParse[d]=this.monthsShort(f,"").toLocaleLowerCase(),this._longMonthsParse[d]=this.months(f,"").toLocaleLowerCase();return c?"MMM"===b?(e=pe.call(this._shortMonthsParse,g),-1!==e?e:null):(e=pe.call(this._longMonthsParse,g),-1!==e?e:null):"MMM"===b?(e=pe.call(this._shortMonthsParse,g),-1!==e?e:(e=pe.call(this._longMonthsParse,g),-1!==e?e:null)):(e=pe.call(this._longMonthsParse,g),-1!==e?e:(e=pe.call(this._shortMonthsParse,g),-1!==e?e:null))}function ha(a,b,c){var d,e,f;if(this._monthsParseExact)return ga.call(this,a,b,c);
// TODO: add sorting
// Sorting makes sure if one month (or abbr) is a prefix of another
// see sorting in computeMonthsParse
for(this._monthsParse||(this._monthsParse=[],this._longMonthsParse=[],this._shortMonthsParse=[]),d=0;12>d;d++){
// test the regex
if(e=j([2e3,d]),c&&!this._longMonthsParse[d]&&(this._longMonthsParse[d]=new RegExp("^"+this.months(e,"").replace(".","")+"$","i"),this._shortMonthsParse[d]=new RegExp("^"+this.monthsShort(e,"").replace(".","")+"$","i")),c||this._monthsParse[d]||(f="^"+this.months(e,"")+"|^"+this.monthsShort(e,""),this._monthsParse[d]=new RegExp(f.replace(".",""),"i")),c&&"MMMM"===b&&this._longMonthsParse[d].test(a))return d;if(c&&"MMM"===b&&this._shortMonthsParse[d].test(a))return d;if(!c&&this._monthsParse[d].test(a))return d}}
// MOMENTS
function ia(a,b){var c;if(!a.isValid())
// No op
return a;if("string"==typeof b)if(/^\d+$/.test(b))b=t(b);else
// TODO: Another silent failure?
if(b=a.localeData().monthsParse(b),"number"!=typeof b)return a;return c=Math.min(a.date(),da(a.year(),b)),a._d["set"+(a._isUTC?"UTC":"")+"Month"](b,c),a}function ja(b){return null!=b?(ia(this,b),a.updateOffset(this,!0),this):O(this,"Month")}function ka(){return da(this.year(),this.month())}function la(a){return this._monthsParseExact?(h(this,"_monthsRegex")||na.call(this),a?this._monthsShortStrictRegex:this._monthsShortRegex):(h(this,"_monthsShortRegex")||(this._monthsShortRegex=ff),this._monthsShortStrictRegex&&a?this._monthsShortStrictRegex:this._monthsShortRegex)}function ma(a){return this._monthsParseExact?(h(this,"_monthsRegex")||na.call(this),a?this._monthsStrictRegex:this._monthsRegex):(h(this,"_monthsRegex")||(this._monthsRegex=gf),this._monthsStrictRegex&&a?this._monthsStrictRegex:this._monthsRegex)}function na(){function a(a,b){return b.length-a.length}var b,c,d=[],e=[],f=[];for(b=0;12>b;b++)c=j([2e3,b]),d.push(this.monthsShort(c,"")),e.push(this.months(c,"")),f.push(this.months(c,"")),f.push(this.monthsShort(c,""));for(
// Sorting makes sure if one month (or abbr) is a prefix of another it
// will match the longer piece.
d.sort(a),e.sort(a),f.sort(a),b=0;12>b;b++)d[b]=_(d[b]),e[b]=_(e[b]);for(b=0;24>b;b++)f[b]=_(f[b]);this._monthsRegex=new RegExp("^("+f.join("|")+")","i"),this._monthsShortRegex=this._monthsRegex,this._monthsStrictRegex=new RegExp("^("+e.join("|")+")","i"),this._monthsShortStrictRegex=new RegExp("^("+d.join("|")+")","i")}
// HELPERS
function oa(a){return pa(a)?366:365}function pa(a){return a%4===0&&a%100!==0||a%400===0}function qa(){return pa(this.year())}function ra(a,b,c,d,e,f,g){
//can't just apply() to create a date:
//http://stackoverflow.com/questions/181348/instantiating-a-javascript-object-by-calling-prototype-constructor-apply
var h=new Date(a,b,c,d,e,f,g);
//the date constructor remaps years 0-99 to 1900-1999
return 100>a&&a>=0&&isFinite(h.getFullYear())&&h.setFullYear(a),h}function sa(a){var b=new Date(Date.UTC.apply(null,arguments));
//the Date.UTC function remaps years 0-99 to 1900-1999
return 100>a&&a>=0&&isFinite(b.getUTCFullYear())&&b.setUTCFullYear(a),b}
// start-of-first-week - start-of-year
function ta(a,b,c){var// first-week day -- which january is always in the first week (4 for iso, 1 for other)
d=7+b-c,
// first-week day local weekday -- which local weekday is fwd
e=(7+sa(a,0,d).getUTCDay()-b)%7;return-e+d-1}
//http://en.wikipedia.org/wiki/ISO_week_date#Calculating_a_date_given_the_year.2C_week_number_and_weekday
function ua(a,b,c,d,e){var f,g,h=(7+c-d)%7,i=ta(a,d,e),j=1+7*(b-1)+h+i;return 0>=j?(f=a-1,g=oa(f)+j):j>oa(a)?(f=a+1,g=j-oa(a)):(f=a,g=j),{year:f,dayOfYear:g}}function va(a,b,c){var d,e,f=ta(a.year(),b,c),g=Math.floor((a.dayOfYear()-f-1)/7)+1;return 1>g?(e=a.year()-1,d=g+wa(e,b,c)):g>wa(a.year(),b,c)?(d=g-wa(a.year(),b,c),e=a.year()+1):(e=a.year(),d=g),{week:d,year:e}}function wa(a,b,c){var d=ta(a,b,c),e=ta(a+1,b,c);return(oa(a)-d+e)/7}
// HELPERS
// LOCALES
function xa(a){return va(a,this._week.dow,this._week.doy).week}function ya(){return this._week.dow}function za(){return this._week.doy}
// MOMENTS
function Aa(a){var b=this.localeData().week(this);return null==a?b:this.add(7*(a-b),"d")}function Ba(a){var b=va(this,1,4).week;return null==a?b:this.add(7*(a-b),"d")}
// HELPERS
function Ca(a,b){return"string"!=typeof a?a:isNaN(a)?(a=b.weekdaysParse(a),"number"==typeof a?a:null):parseInt(a,10)}function Da(a,b){return"string"==typeof a?b.weekdaysParse(a)%7||7:isNaN(a)?null:a}function Ea(a,b){return c(this._weekdays)?this._weekdays[a.day()]:this._weekdays[this._weekdays.isFormat.test(b)?"format":"standalone"][a.day()]}function Fa(a){return this._weekdaysShort[a.day()]}function Ga(a){return this._weekdaysMin[a.day()]}function Ha(a,b,c){var d,e,f,g=a.toLocaleLowerCase();if(!this._weekdaysParse)for(this._weekdaysParse=[],this._shortWeekdaysParse=[],this._minWeekdaysParse=[],d=0;7>d;++d)f=j([2e3,1]).day(d),this._minWeekdaysParse[d]=this.weekdaysMin(f,"").toLocaleLowerCase(),this._shortWeekdaysParse[d]=this.weekdaysShort(f,"").toLocaleLowerCase(),this._weekdaysParse[d]=this.weekdays(f,"").toLocaleLowerCase();return c?"dddd"===b?(e=pe.call(this._weekdaysParse,g),-1!==e?e:null):"ddd"===b?(e=pe.call(this._shortWeekdaysParse,g),-1!==e?e:null):(e=pe.call(this._minWeekdaysParse,g),-1!==e?e:null):"dddd"===b?(e=pe.call(this._weekdaysParse,g),-1!==e?e:(e=pe.call(this._shortWeekdaysParse,g),-1!==e?e:(e=pe.call(this._minWeekdaysParse,g),-1!==e?e:null))):"ddd"===b?(e=pe.call(this._shortWeekdaysParse,g),-1!==e?e:(e=pe.call(this._weekdaysParse,g),-1!==e?e:(e=pe.call(this._minWeekdaysParse,g),-1!==e?e:null))):(e=pe.call(this._minWeekdaysParse,g),-1!==e?e:(e=pe.call(this._weekdaysParse,g),-1!==e?e:(e=pe.call(this._shortWeekdaysParse,g),-1!==e?e:null)))}function Ia(a,b,c){var d,e,f;if(this._weekdaysParseExact)return Ha.call(this,a,b,c);for(this._weekdaysParse||(this._weekdaysParse=[],this._minWeekdaysParse=[],this._shortWeekdaysParse=[],this._fullWeekdaysParse=[]),d=0;7>d;d++){
// test the regex
if(e=j([2e3,1]).day(d),c&&!this._fullWeekdaysParse[d]&&(this._fullWeekdaysParse[d]=new RegExp("^"+this.weekdays(e,"").replace(".",".?")+"$","i"),this._shortWeekdaysParse[d]=new RegExp("^"+this.weekdaysShort(e,"").replace(".",".?")+"$","i"),this._minWeekdaysParse[d]=new RegExp("^"+this.weekdaysMin(e,"").replace(".",".?")+"$","i")),this._weekdaysParse[d]||(f="^"+this.weekdays(e,"")+"|^"+this.weekdaysShort(e,"")+"|^"+this.weekdaysMin(e,""),this._weekdaysParse[d]=new RegExp(f.replace(".",""),"i")),c&&"dddd"===b&&this._fullWeekdaysParse[d].test(a))return d;if(c&&"ddd"===b&&this._shortWeekdaysParse[d].test(a))return d;if(c&&"dd"===b&&this._minWeekdaysParse[d].test(a))return d;if(!c&&this._weekdaysParse[d].test(a))return d}}
// MOMENTS
function Ja(a){if(!this.isValid())return null!=a?this:NaN;var b=this._isUTC?this._d.getUTCDay():this._d.getDay();return null!=a?(a=Ca(a,this.localeData()),this.add(a-b,"d")):b}function Ka(a){if(!this.isValid())return null!=a?this:NaN;var b=(this.day()+7-this.localeData()._week.dow)%7;return null==a?b:this.add(a-b,"d")}function La(a){if(!this.isValid())return null!=a?this:NaN;
// behaves the same as moment#day except
// as a getter, returns 7 instead of 0 (1-7 range instead of 0-6)
// as a setter, sunday should belong to the previous week.
if(null!=a){var b=Da(a,this.localeData());return this.day(this.day()%7?b:b-7)}return this.day()||7}function Ma(a){return this._weekdaysParseExact?(h(this,"_weekdaysRegex")||Pa.call(this),a?this._weekdaysStrictRegex:this._weekdaysRegex):(h(this,"_weekdaysRegex")||(this._weekdaysRegex=nf),this._weekdaysStrictRegex&&a?this._weekdaysStrictRegex:this._weekdaysRegex)}function Na(a){return this._weekdaysParseExact?(h(this,"_weekdaysRegex")||Pa.call(this),a?this._weekdaysShortStrictRegex:this._weekdaysShortRegex):(h(this,"_weekdaysShortRegex")||(this._weekdaysShortRegex=of),this._weekdaysShortStrictRegex&&a?this._weekdaysShortStrictRegex:this._weekdaysShortRegex)}function Oa(a){return this._weekdaysParseExact?(h(this,"_weekdaysRegex")||Pa.call(this),a?this._weekdaysMinStrictRegex:this._weekdaysMinRegex):(h(this,"_weekdaysMinRegex")||(this._weekdaysMinRegex=pf),this._weekdaysMinStrictRegex&&a?this._weekdaysMinStrictRegex:this._weekdaysMinRegex)}function Pa(){function a(a,b){return b.length-a.length}var b,c,d,e,f,g=[],h=[],i=[],k=[];for(b=0;7>b;b++)c=j([2e3,1]).day(b),d=this.weekdaysMin(c,""),e=this.weekdaysShort(c,""),f=this.weekdays(c,""),g.push(d),h.push(e),i.push(f),k.push(d),k.push(e),k.push(f);for(
// Sorting makes sure if one weekday (or abbr) is a prefix of another it
// will match the longer piece.
g.sort(a),h.sort(a),i.sort(a),k.sort(a),b=0;7>b;b++)h[b]=_(h[b]),i[b]=_(i[b]),k[b]=_(k[b]);this._weekdaysRegex=new RegExp("^("+k.join("|")+")","i"),this._weekdaysShortRegex=this._weekdaysRegex,this._weekdaysMinRegex=this._weekdaysRegex,this._weekdaysStrictRegex=new RegExp("^("+i.join("|")+")","i"),this._weekdaysShortStrictRegex=new RegExp("^("+h.join("|")+")","i"),this._weekdaysMinStrictRegex=new RegExp("^("+g.join("|")+")","i")}
// FORMATTING
function Qa(){return this.hours()%12||12}function Ra(){return this.hours()||24}function Sa(a,b){T(a,0,0,function(){return this.localeData().meridiem(this.hours(),this.minutes(),b)})}
// PARSING
function Ta(a,b){return b._meridiemParse}
// LOCALES
function Ua(a){
// IE8 Quirks Mode & IE7 Standards Mode do not allow accessing strings like arrays
// Using charAt should be more compatible.
return"p"===(a+"").toLowerCase().charAt(0)}function Va(a,b,c){return a>11?c?"pm":"PM":c?"am":"AM"}function Wa(a){return a?a.toLowerCase().replace("_","-"):a}
// pick the locale from the array
// try ['en-au', 'en-gb'] as 'en-au', 'en-gb', 'en', as in move through the list trying each
// substring from most specific to least, but move to the next array item if it's a more specific variant than the current root
function Xa(a){for(var b,c,d,e,f=0;f<a.length;){for(e=Wa(a[f]).split("-"),b=e.length,c=Wa(a[f+1]),c=c?c.split("-"):null;b>0;){if(d=Ya(e.slice(0,b).join("-")))return d;if(c&&c.length>=b&&u(e,c,!0)>=b-1)
//the next array item is better than a shallower substring of this one
break;b--}f++}return null}function Ya(a){var b=null;
// TODO: Find a better way to register and load all the locales in Node
if(!uf[a]&&"undefined"!=typeof module&&module&&module.exports)try{b=qf._abbr,require("./locale/"+a),
// because defineLocale currently also sets the global locale, we
// want to undo that for lazy loaded locales
Za(b)}catch(c){}return uf[a]}
// This function will load locale and then set the global locale.  If
// no arguments are passed in, it will simply return the current global
// locale key.
function Za(a,b){var c;
// moment.duration._locale = moment._locale = data;
return a&&(c=o(b)?ab(a):$a(a,b),c&&(qf=c)),qf._abbr}function $a(a,b){if(null!==b){var c=tf;
// treat as if there is no base config
// backwards compat for now: also set the locale
return b.abbr=a,null!=uf[a]?(x("defineLocaleOverride","use moment.updateLocale(localeName, config) to change an existing locale. moment.defineLocale(localeName, config) should only be used for creating a new locale See http://momentjs.com/guides/#/warnings/define-locale/ for more info."),c=uf[a]._config):null!=b.parentLocale&&(null!=uf[b.parentLocale]?c=uf[b.parentLocale]._config:x("parentLocaleUndefined","specified parentLocale is not defined yet. See http://momentjs.com/guides/#/warnings/parent-locale/")),uf[a]=new B(A(c,b)),Za(a),uf[a]}
// useful for testing
return delete uf[a],null}function _a(a,b){if(null!=b){var c,d=tf;
// MERGE
null!=uf[a]&&(d=uf[a]._config),b=A(d,b),c=new B(b),c.parentLocale=uf[a],uf[a]=c,
// backwards compat for now: also set the locale
Za(a)}else
// pass null for config to unupdate, useful for tests
null!=uf[a]&&(null!=uf[a].parentLocale?uf[a]=uf[a].parentLocale:null!=uf[a]&&delete uf[a]);return uf[a]}
// returns locale data
function ab(a){var b;if(a&&a._locale&&a._locale._abbr&&(a=a._locale._abbr),!a)return qf;if(!c(a)){if(b=Ya(a))return b;a=[a]}return Xa(a)}function bb(){return oe(uf)}function cb(a){var b,c=a._a;return c&&-2===l(a).overflow&&(b=c[We]<0||c[We]>11?We:c[Xe]<1||c[Xe]>da(c[Ve],c[We])?Xe:c[Ye]<0||c[Ye]>24||24===c[Ye]&&(0!==c[Ze]||0!==c[$e]||0!==c[_e])?Ye:c[Ze]<0||c[Ze]>59?Ze:c[$e]<0||c[$e]>59?$e:c[_e]<0||c[_e]>999?_e:-1,l(a)._overflowDayOfYear&&(Ve>b||b>Xe)&&(b=Xe),l(a)._overflowWeeks&&-1===b&&(b=af),l(a)._overflowWeekday&&-1===b&&(b=bf),l(a).overflow=b),a}
// date from iso format
function db(a){var b,c,d,e,f,g,h=a._i,i=vf.exec(h)||wf.exec(h);if(i){for(l(a).iso=!0,b=0,c=yf.length;c>b;b++)if(yf[b][1].exec(i[1])){e=yf[b][0],d=yf[b][2]!==!1;break}if(null==e)return void(a._isValid=!1);if(i[3]){for(b=0,c=zf.length;c>b;b++)if(zf[b][1].exec(i[3])){
// match[2] should be 'T' or space
f=(i[2]||" ")+zf[b][0];break}if(null==f)return void(a._isValid=!1)}if(!d&&null!=f)return void(a._isValid=!1);if(i[4]){if(!xf.exec(i[4]))return void(a._isValid=!1);g="Z"}a._f=e+(f||"")+(g||""),jb(a)}else a._isValid=!1}
// date from iso format or fallback
function eb(b){var c=Af.exec(b._i);return null!==c?void(b._d=new Date(+c[1])):(db(b),void(b._isValid===!1&&(delete b._isValid,a.createFromInputFallback(b))))}
// Pick the first defined of two or three arguments.
function fb(a,b,c){return null!=a?a:null!=b?b:c}function gb(b){
// hooks is actually the exported moment object
var c=new Date(a.now());return b._useUTC?[c.getUTCFullYear(),c.getUTCMonth(),c.getUTCDate()]:[c.getFullYear(),c.getMonth(),c.getDate()]}
// convert an array to a date.
// the array should mirror the parameters below
// note: all values past the year are optional and will default to the lowest possible value.
// [year, month, day , hour, minute, second, millisecond]
function hb(a){var b,c,d,e,f=[];if(!a._d){
// Default to current date.
// * if no year, month, day of month are given, default to today
// * if day of month is given, default month and year
// * if month is given, default only year
// * if year is given, don't default anything
for(d=gb(a),a._w&&null==a._a[Xe]&&null==a._a[We]&&ib(a),a._dayOfYear&&(e=fb(a._a[Ve],d[Ve]),a._dayOfYear>oa(e)&&(l(a)._overflowDayOfYear=!0),c=sa(e,0,a._dayOfYear),a._a[We]=c.getUTCMonth(),a._a[Xe]=c.getUTCDate()),b=0;3>b&&null==a._a[b];++b)a._a[b]=f[b]=d[b];
// Zero out whatever was not defaulted, including time
for(;7>b;b++)a._a[b]=f[b]=null==a._a[b]?2===b?1:0:a._a[b];
// Check for 24:00:00.000
24===a._a[Ye]&&0===a._a[Ze]&&0===a._a[$e]&&0===a._a[_e]&&(a._nextDay=!0,a._a[Ye]=0),a._d=(a._useUTC?sa:ra).apply(null,f),
// Apply timezone offset from input. The actual utcOffset can be changed
// with parseZone.
null!=a._tzm&&a._d.setUTCMinutes(a._d.getUTCMinutes()-a._tzm),a._nextDay&&(a._a[Ye]=24)}}function ib(a){var b,c,d,e,f,g,h,i;b=a._w,null!=b.GG||null!=b.W||null!=b.E?(f=1,g=4,c=fb(b.GG,a._a[Ve],va(rb(),1,4).year),d=fb(b.W,1),e=fb(b.E,1),(1>e||e>7)&&(i=!0)):(f=a._locale._week.dow,g=a._locale._week.doy,c=fb(b.gg,a._a[Ve],va(rb(),f,g).year),d=fb(b.w,1),null!=b.d?(e=b.d,(0>e||e>6)&&(i=!0)):null!=b.e?(e=b.e+f,(b.e<0||b.e>6)&&(i=!0)):e=f),1>d||d>wa(c,f,g)?l(a)._overflowWeeks=!0:null!=i?l(a)._overflowWeekday=!0:(h=ua(c,d,e,f,g),a._a[Ve]=h.year,a._dayOfYear=h.dayOfYear)}
// date from string and format string
function jb(b){
// TODO: Move this to another part of the creation flow to prevent circular deps
if(b._f===a.ISO_8601)return void db(b);b._a=[],l(b).empty=!0;
// This array is used to make a Date, either with `new Date` or `Date.UTC`
var c,d,e,f,g,h=""+b._i,i=h.length,j=0;for(e=X(b._f,b._locale).match(ye)||[],c=0;c<e.length;c++)f=e[c],d=(h.match(Z(f,b))||[])[0],d&&(g=h.substr(0,h.indexOf(d)),g.length>0&&l(b).unusedInput.push(g),h=h.slice(h.indexOf(d)+d.length),j+=d.length),Be[f]?(d?l(b).empty=!1:l(b).unusedTokens.push(f),ca(f,d,b)):b._strict&&!d&&l(b).unusedTokens.push(f);
// add remaining unparsed input length to the string
l(b).charsLeftOver=i-j,h.length>0&&l(b).unusedInput.push(h),
// clear _12h flag if hour is <= 12
b._a[Ye]<=12&&l(b).bigHour===!0&&b._a[Ye]>0&&(l(b).bigHour=void 0),l(b).parsedDateParts=b._a.slice(0),l(b).meridiem=b._meridiem,
// handle meridiem
b._a[Ye]=kb(b._locale,b._a[Ye],b._meridiem),hb(b),cb(b)}function kb(a,b,c){var d;
// Fallback
return null==c?b:null!=a.meridiemHour?a.meridiemHour(b,c):null!=a.isPM?(d=a.isPM(c),d&&12>b&&(b+=12),d||12!==b||(b=0),b):b}
// date from string and array of format strings
function lb(a){var b,c,d,e,f;if(0===a._f.length)return l(a).invalidFormat=!0,void(a._d=new Date(NaN));for(e=0;e<a._f.length;e++)f=0,b=p({},a),null!=a._useUTC&&(b._useUTC=a._useUTC),b._f=a._f[e],jb(b),m(b)&&(f+=l(b).charsLeftOver,f+=10*l(b).unusedTokens.length,l(b).score=f,(null==d||d>f)&&(d=f,c=b));i(a,c||b)}function mb(a){if(!a._d){var b=K(a._i);a._a=g([b.year,b.month,b.day||b.date,b.hour,b.minute,b.second,b.millisecond],function(a){return a&&parseInt(a,10)}),hb(a)}}function nb(a){var b=new q(cb(ob(a)));
// Adding is smart enough around DST
return b._nextDay&&(b.add(1,"d"),b._nextDay=void 0),b}function ob(a){var b=a._i,d=a._f;return a._locale=a._locale||ab(a._l),null===b||void 0===d&&""===b?n({nullInput:!0}):("string"==typeof b&&(a._i=b=a._locale.preparse(b)),r(b)?new q(cb(b)):(c(d)?lb(a):f(b)?a._d=b:d?jb(a):pb(a),m(a)||(a._d=null),a))}function pb(b){var d=b._i;void 0===d?b._d=new Date(a.now()):f(d)?b._d=new Date(d.valueOf()):"string"==typeof d?eb(b):c(d)?(b._a=g(d.slice(0),function(a){return parseInt(a,10)}),hb(b)):"object"==typeof d?mb(b):"number"==typeof d?
// from milliseconds
b._d=new Date(d):a.createFromInputFallback(b)}function qb(a,b,f,g,h){var i={};
// object construction must be done this way.
// https://github.com/moment/moment/issues/1423
return"boolean"==typeof f&&(g=f,f=void 0),(d(a)&&e(a)||c(a)&&0===a.length)&&(a=void 0),i._isAMomentObject=!0,i._useUTC=i._isUTC=h,i._l=f,i._i=a,i._f=b,i._strict=g,nb(i)}function rb(a,b,c,d){return qb(a,b,c,d,!1)}
// Pick a moment m from moments so that m[fn](other) is true for all
// other. This relies on the function fn to be transitive.
//
// moments should either be an array of moment objects or an array, whose
// first element is an array of moment objects.
function sb(a,b){var d,e;if(1===b.length&&c(b[0])&&(b=b[0]),!b.length)return rb();for(d=b[0],e=1;e<b.length;++e)b[e].isValid()&&!b[e][a](d)||(d=b[e]);return d}
// TODO: Use [].sort instead?
function tb(){var a=[].slice.call(arguments,0);return sb("isBefore",a)}function ub(){var a=[].slice.call(arguments,0);return sb("isAfter",a)}function vb(a){var b=K(a),c=b.year||0,d=b.quarter||0,e=b.month||0,f=b.week||0,g=b.day||0,h=b.hour||0,i=b.minute||0,j=b.second||0,k=b.millisecond||0;
// representation for dateAddRemove
this._milliseconds=+k+1e3*j+// 1000
6e4*i+// 1000 * 60
1e3*h*60*60,//using 1000 * 60 * 60 instead of 36e5 to avoid floating point rounding errors https://github.com/moment/moment/issues/2978
// Because of dateAddRemove treats 24 hours as different from a
// day when working around DST, we need to store them separately
this._days=+g+7*f,
// It is impossible translate months into days without knowing
// which months you are are talking about, so we have to store
// it separately.
this._months=+e+3*d+12*c,this._data={},this._locale=ab(),this._bubble()}function wb(a){return a instanceof vb}
// FORMATTING
function xb(a,b){T(a,0,0,function(){var a=this.utcOffset(),c="+";return 0>a&&(a=-a,c="-"),c+S(~~(a/60),2)+b+S(~~a%60,2)})}function yb(a,b){var c=(b||"").match(a)||[],d=c[c.length-1]||[],e=(d+"").match(Ef)||["-",0,0],f=+(60*e[1])+t(e[2]);return"+"===e[0]?f:-f}
// Return a moment from input, that is local/utc/zone equivalent to model.
function zb(b,c){var d,e;
// Use low-level api, because this fn is low-level api.
return c._isUTC?(d=c.clone(),e=(r(b)||f(b)?b.valueOf():rb(b).valueOf())-d.valueOf(),d._d.setTime(d._d.valueOf()+e),a.updateOffset(d,!1),d):rb(b).local()}function Ab(a){
// On Firefox.24 Date#getTimezoneOffset returns a floating point.
// https://github.com/moment/moment/pull/1871
return 15*-Math.round(a._d.getTimezoneOffset()/15)}
// MOMENTS
// keepLocalTime = true means only change the timezone, without
// affecting the local hour. So 5:31:26 +0300 --[utcOffset(2, true)]-->
// 5:31:26 +0200 It is possible that 5:31:26 doesn't exist with offset
// +0200, so we adjust the time as needed, to be valid.
//
// Keeping the time actually adds/subtracts (one hour)
// from the actual represented time. That is why we call updateOffset
// a second time. In case it wants us to change the offset again
// _changeInProgress == true case, then we have to adjust, because
// there is no such time in the given timezone.
function Bb(b,c){var d,e=this._offset||0;return this.isValid()?null!=b?("string"==typeof b?b=yb(Qe,b):Math.abs(b)<16&&(b=60*b),!this._isUTC&&c&&(d=Ab(this)),this._offset=b,this._isUTC=!0,null!=d&&this.add(d,"m"),e!==b&&(!c||this._changeInProgress?Sb(this,Mb(b-e,"m"),1,!1):this._changeInProgress||(this._changeInProgress=!0,a.updateOffset(this,!0),this._changeInProgress=null)),this):this._isUTC?e:Ab(this):null!=b?this:NaN}function Cb(a,b){return null!=a?("string"!=typeof a&&(a=-a),this.utcOffset(a,b),this):-this.utcOffset()}function Db(a){return this.utcOffset(0,a)}function Eb(a){return this._isUTC&&(this.utcOffset(0,a),this._isUTC=!1,a&&this.subtract(Ab(this),"m")),this}function Fb(){return this._tzm?this.utcOffset(this._tzm):"string"==typeof this._i&&this.utcOffset(yb(Pe,this._i)),this}function Gb(a){return this.isValid()?(a=a?rb(a).utcOffset():0,(this.utcOffset()-a)%60===0):!1}function Hb(){return this.utcOffset()>this.clone().month(0).utcOffset()||this.utcOffset()>this.clone().month(5).utcOffset()}function Ib(){if(!o(this._isDSTShifted))return this._isDSTShifted;var a={};if(p(a,this),a=ob(a),a._a){var b=a._isUTC?j(a._a):rb(a._a);this._isDSTShifted=this.isValid()&&u(a._a,b.toArray())>0}else this._isDSTShifted=!1;return this._isDSTShifted}function Jb(){return this.isValid()?!this._isUTC:!1}function Kb(){return this.isValid()?this._isUTC:!1}function Lb(){return this.isValid()?this._isUTC&&0===this._offset:!1}function Mb(a,b){var c,d,e,f=a,
// matching against regexp is expensive, do it on demand
g=null;// checks for null or undefined
return wb(a)?f={ms:a._milliseconds,d:a._days,M:a._months}:"number"==typeof a?(f={},b?f[b]=a:f.milliseconds=a):(g=Ff.exec(a))?(c="-"===g[1]?-1:1,f={y:0,d:t(g[Xe])*c,h:t(g[Ye])*c,m:t(g[Ze])*c,s:t(g[$e])*c,ms:t(g[_e])*c}):(g=Gf.exec(a))?(c="-"===g[1]?-1:1,f={y:Nb(g[2],c),M:Nb(g[3],c),w:Nb(g[4],c),d:Nb(g[5],c),h:Nb(g[6],c),m:Nb(g[7],c),s:Nb(g[8],c)}):null==f?f={}:"object"==typeof f&&("from"in f||"to"in f)&&(e=Pb(rb(f.from),rb(f.to)),f={},f.ms=e.milliseconds,f.M=e.months),d=new vb(f),wb(a)&&h(a,"_locale")&&(d._locale=a._locale),d}function Nb(a,b){
// We'd normally use ~~inp for this, but unfortunately it also
// converts floats to ints.
// inp may be undefined, so careful calling replace on it.
var c=a&&parseFloat(a.replace(",","."));
// apply sign while we're at it
return(isNaN(c)?0:c)*b}function Ob(a,b){var c={milliseconds:0,months:0};return c.months=b.month()-a.month()+12*(b.year()-a.year()),a.clone().add(c.months,"M").isAfter(b)&&--c.months,c.milliseconds=+b-+a.clone().add(c.months,"M"),c}function Pb(a,b){var c;return a.isValid()&&b.isValid()?(b=zb(b,a),a.isBefore(b)?c=Ob(a,b):(c=Ob(b,a),c.milliseconds=-c.milliseconds,c.months=-c.months),c):{milliseconds:0,months:0}}function Qb(a){return 0>a?-1*Math.round(-1*a):Math.round(a)}
// TODO: remove 'name' arg after deprecation is removed
function Rb(a,b){return function(c,d){var e,f;
//invert the arguments, but complain about it
return null===d||isNaN(+d)||(x(b,"moment()."+b+"(period, number) is deprecated. Please use moment()."+b+"(number, period). See http://momentjs.com/guides/#/warnings/add-inverted-param/ for more info."),f=c,c=d,d=f),c="string"==typeof c?+c:c,e=Mb(c,d),Sb(this,e,a),this}}function Sb(b,c,d,e){var f=c._milliseconds,g=Qb(c._days),h=Qb(c._months);b.isValid()&&(e=null==e?!0:e,f&&b._d.setTime(b._d.valueOf()+f*d),g&&P(b,"Date",O(b,"Date")+g*d),h&&ia(b,O(b,"Month")+h*d),e&&a.updateOffset(b,g||h))}function Tb(a,b){var c=a.diff(b,"days",!0);return-6>c?"sameElse":-1>c?"lastWeek":0>c?"lastDay":1>c?"sameDay":2>c?"nextDay":7>c?"nextWeek":"sameElse"}function Ub(b,c){
// We want to compare the start of today, vs this.
// Getting start-of-today depends on whether we're local/utc/offset or not.
var d=b||rb(),e=zb(d,this).startOf("day"),f=a.calendarFormat(this,e)||"sameElse",g=c&&(y(c[f])?c[f].call(this,d):c[f]);return this.format(g||this.localeData().calendar(f,this,rb(d)))}function Vb(){return new q(this)}function Wb(a,b){var c=r(a)?a:rb(a);return this.isValid()&&c.isValid()?(b=J(o(b)?"millisecond":b),"millisecond"===b?this.valueOf()>c.valueOf():c.valueOf()<this.clone().startOf(b).valueOf()):!1}function Xb(a,b){var c=r(a)?a:rb(a);return this.isValid()&&c.isValid()?(b=J(o(b)?"millisecond":b),"millisecond"===b?this.valueOf()<c.valueOf():this.clone().endOf(b).valueOf()<c.valueOf()):!1}function Yb(a,b,c,d){return d=d||"()",("("===d[0]?this.isAfter(a,c):!this.isBefore(a,c))&&(")"===d[1]?this.isBefore(b,c):!this.isAfter(b,c))}function Zb(a,b){var c,d=r(a)?a:rb(a);return this.isValid()&&d.isValid()?(b=J(b||"millisecond"),"millisecond"===b?this.valueOf()===d.valueOf():(c=d.valueOf(),this.clone().startOf(b).valueOf()<=c&&c<=this.clone().endOf(b).valueOf())):!1}function $b(a,b){return this.isSame(a,b)||this.isAfter(a,b)}function _b(a,b){return this.isSame(a,b)||this.isBefore(a,b)}function ac(a,b,c){var d,e,f,g;// 1000
// 1000 * 60
// 1000 * 60 * 60
// 1000 * 60 * 60 * 24, negate dst
// 1000 * 60 * 60 * 24 * 7, negate dst
return this.isValid()?(d=zb(a,this),d.isValid()?(e=6e4*(d.utcOffset()-this.utcOffset()),b=J(b),"year"===b||"month"===b||"quarter"===b?(g=bc(this,d),"quarter"===b?g/=3:"year"===b&&(g/=12)):(f=this-d,g="second"===b?f/1e3:"minute"===b?f/6e4:"hour"===b?f/36e5:"day"===b?(f-e)/864e5:"week"===b?(f-e)/6048e5:f),c?g:s(g)):NaN):NaN}function bc(a,b){
// difference in months
var c,d,e=12*(b.year()-a.year())+(b.month()-a.month()),
// b is in (anchor - 1 month, anchor + 1 month)
f=a.clone().add(e,"months");
//check for negative zero, return zero if negative zero
// linear across the month
// linear across the month
return 0>b-f?(c=a.clone().add(e-1,"months"),d=(b-f)/(f-c)):(c=a.clone().add(e+1,"months"),d=(b-f)/(c-f)),-(e+d)||0}function cc(){return this.clone().locale("en").format("ddd MMM DD YYYY HH:mm:ss [GMT]ZZ")}function dc(){var a=this.clone().utc();return 0<a.year()&&a.year()<=9999?y(Date.prototype.toISOString)?this.toDate().toISOString():W(a,"YYYY-MM-DD[T]HH:mm:ss.SSS[Z]"):W(a,"YYYYYY-MM-DD[T]HH:mm:ss.SSS[Z]")}function ec(b){b||(b=this.isUtc()?a.defaultFormatUtc:a.defaultFormat);var c=W(this,b);return this.localeData().postformat(c)}function fc(a,b){return this.isValid()&&(r(a)&&a.isValid()||rb(a).isValid())?Mb({to:this,from:a}).locale(this.locale()).humanize(!b):this.localeData().invalidDate()}function gc(a){return this.from(rb(),a)}function hc(a,b){return this.isValid()&&(r(a)&&a.isValid()||rb(a).isValid())?Mb({from:this,to:a}).locale(this.locale()).humanize(!b):this.localeData().invalidDate()}function ic(a){return this.to(rb(),a)}
// If passed a locale key, it will set the locale for this
// instance.  Otherwise, it will return the locale configuration
// variables for this instance.
function jc(a){var b;return void 0===a?this._locale._abbr:(b=ab(a),null!=b&&(this._locale=b),this)}function kc(){return this._locale}function lc(a){
// the following switch intentionally omits break keywords
// to utilize falling through the cases.
switch(a=J(a)){case"year":this.month(0);/* falls through */
case"quarter":case"month":this.date(1);/* falls through */
case"week":case"isoWeek":case"day":case"date":this.hours(0);/* falls through */
case"hour":this.minutes(0);/* falls through */
case"minute":this.seconds(0);/* falls through */
case"second":this.milliseconds(0)}
// weeks are a special case
// quarters are also special
return"week"===a&&this.weekday(0),"isoWeek"===a&&this.isoWeekday(1),"quarter"===a&&this.month(3*Math.floor(this.month()/3)),this}function mc(a){
// 'date' is an alias for 'day', so it should be considered as such.
return a=J(a),void 0===a||"millisecond"===a?this:("date"===a&&(a="day"),this.startOf(a).add(1,"isoWeek"===a?"week":a).subtract(1,"ms"))}function nc(){return this._d.valueOf()-6e4*(this._offset||0)}function oc(){return Math.floor(this.valueOf()/1e3)}function pc(){return new Date(this.valueOf())}function qc(){var a=this;return[a.year(),a.month(),a.date(),a.hour(),a.minute(),a.second(),a.millisecond()]}function rc(){var a=this;return{years:a.year(),months:a.month(),date:a.date(),hours:a.hours(),minutes:a.minutes(),seconds:a.seconds(),milliseconds:a.milliseconds()}}function sc(){
// new Date(NaN).toJSON() === null
return this.isValid()?this.toISOString():null}function tc(){return m(this)}function uc(){return i({},l(this))}function vc(){return l(this).overflow}function wc(){return{input:this._i,format:this._f,locale:this._locale,isUTC:this._isUTC,strict:this._strict}}function xc(a,b){T(0,[a,a.length],0,b)}
// MOMENTS
function yc(a){return Cc.call(this,a,this.week(),this.weekday(),this.localeData()._week.dow,this.localeData()._week.doy)}function zc(a){return Cc.call(this,a,this.isoWeek(),this.isoWeekday(),1,4)}function Ac(){return wa(this.year(),1,4)}function Bc(){var a=this.localeData()._week;return wa(this.year(),a.dow,a.doy)}function Cc(a,b,c,d,e){var f;return null==a?va(this,d,e).year:(f=wa(a,d,e),b>f&&(b=f),Dc.call(this,a,b,c,d,e))}function Dc(a,b,c,d,e){var f=ua(a,b,c,d,e),g=sa(f.year,0,f.dayOfYear);return this.year(g.getUTCFullYear()),this.month(g.getUTCMonth()),this.date(g.getUTCDate()),this}
// MOMENTS
function Ec(a){return null==a?Math.ceil((this.month()+1)/3):this.month(3*(a-1)+this.month()%3)}
// HELPERS
// MOMENTS
function Fc(a){var b=Math.round((this.clone().startOf("day")-this.clone().startOf("year"))/864e5)+1;return null==a?b:this.add(a-b,"d")}function Gc(a,b){b[_e]=t(1e3*("0."+a))}
// MOMENTS
function Hc(){return this._isUTC?"UTC":""}function Ic(){return this._isUTC?"Coordinated Universal Time":""}function Jc(a){return rb(1e3*a)}function Kc(){return rb.apply(null,arguments).parseZone()}function Lc(a){return a}function Mc(a,b,c,d){var e=ab(),f=j().set(d,b);return e[c](f,a)}function Nc(a,b,c){if("number"==typeof a&&(b=a,a=void 0),a=a||"",null!=b)return Mc(a,b,c,"month");var d,e=[];for(d=0;12>d;d++)e[d]=Mc(a,d,c,"month");return e}
// ()
// (5)
// (fmt, 5)
// (fmt)
// (true)
// (true, 5)
// (true, fmt, 5)
// (true, fmt)
function Oc(a,b,c,d){"boolean"==typeof a?("number"==typeof b&&(c=b,b=void 0),b=b||""):(b=a,c=b,a=!1,"number"==typeof b&&(c=b,b=void 0),b=b||"");var e=ab(),f=a?e._week.dow:0;if(null!=c)return Mc(b,(c+f)%7,d,"day");var g,h=[];for(g=0;7>g;g++)h[g]=Mc(b,(g+f)%7,d,"day");return h}function Pc(a,b){return Nc(a,b,"months")}function Qc(a,b){return Nc(a,b,"monthsShort")}function Rc(a,b,c){return Oc(a,b,c,"weekdays")}function Sc(a,b,c){return Oc(a,b,c,"weekdaysShort")}function Tc(a,b,c){return Oc(a,b,c,"weekdaysMin")}function Uc(){var a=this._data;return this._milliseconds=Sf(this._milliseconds),this._days=Sf(this._days),this._months=Sf(this._months),a.milliseconds=Sf(a.milliseconds),a.seconds=Sf(a.seconds),a.minutes=Sf(a.minutes),a.hours=Sf(a.hours),a.months=Sf(a.months),a.years=Sf(a.years),this}function Vc(a,b,c,d){var e=Mb(b,c);return a._milliseconds+=d*e._milliseconds,a._days+=d*e._days,a._months+=d*e._months,a._bubble()}
// supports only 2.0-style add(1, 's') or add(duration)
function Wc(a,b){return Vc(this,a,b,1)}
// supports only 2.0-style subtract(1, 's') or subtract(duration)
function Xc(a,b){return Vc(this,a,b,-1)}function Yc(a){return 0>a?Math.floor(a):Math.ceil(a)}function Zc(){var a,b,c,d,e,f=this._milliseconds,g=this._days,h=this._months,i=this._data;
// if we have a mix of positive and negative values, bubble down first
// check: https://github.com/moment/moment/issues/2166
// The following code bubbles up values, see the tests for
// examples of what that means.
// convert days to months
// 12 months -> 1 year
return f>=0&&g>=0&&h>=0||0>=f&&0>=g&&0>=h||(f+=864e5*Yc(_c(h)+g),g=0,h=0),i.milliseconds=f%1e3,a=s(f/1e3),i.seconds=a%60,b=s(a/60),i.minutes=b%60,c=s(b/60),i.hours=c%24,g+=s(c/24),e=s($c(g)),h+=e,g-=Yc(_c(e)),d=s(h/12),h%=12,i.days=g,i.months=h,i.years=d,this}function $c(a){
// 400 years have 146097 days (taking into account leap year rules)
// 400 years have 12 months === 4800
return 4800*a/146097}function _c(a){
// the reverse of daysToMonths
return 146097*a/4800}function ad(a){var b,c,d=this._milliseconds;if(a=J(a),"month"===a||"year"===a)return b=this._days+d/864e5,c=this._months+$c(b),"month"===a?c:c/12;switch(b=this._days+Math.round(_c(this._months)),a){case"week":return b/7+d/6048e5;case"day":return b+d/864e5;case"hour":return 24*b+d/36e5;case"minute":return 1440*b+d/6e4;case"second":return 86400*b+d/1e3;
// Math.floor prevents floating point math errors here
case"millisecond":return Math.floor(864e5*b)+d;default:throw new Error("Unknown unit "+a)}}
// TODO: Use this.as('ms')?
function bd(){return this._milliseconds+864e5*this._days+this._months%12*2592e6+31536e6*t(this._months/12)}function cd(a){return function(){return this.as(a)}}function dd(a){return a=J(a),this[a+"s"]()}function ed(a){return function(){return this._data[a]}}function fd(){return s(this.days()/7)}
// helper function for moment.fn.from, moment.fn.fromNow, and moment.duration.fn.humanize
function gd(a,b,c,d,e){return e.relativeTime(b||1,!!c,a,d)}function hd(a,b,c){var d=Mb(a).abs(),e=gg(d.as("s")),f=gg(d.as("m")),g=gg(d.as("h")),h=gg(d.as("d")),i=gg(d.as("M")),j=gg(d.as("y")),k=e<hg.s&&["s",e]||1>=f&&["m"]||f<hg.m&&["mm",f]||1>=g&&["h"]||g<hg.h&&["hh",g]||1>=h&&["d"]||h<hg.d&&["dd",h]||1>=i&&["M"]||i<hg.M&&["MM",i]||1>=j&&["y"]||["yy",j];return k[2]=b,k[3]=+a>0,k[4]=c,gd.apply(null,k)}
// This function allows you to set the rounding function for relative time strings
function id(a){return void 0===a?gg:"function"==typeof a?(gg=a,!0):!1}
// This function allows you to set a threshold for relative time strings
function jd(a,b){return void 0===hg[a]?!1:void 0===b?hg[a]:(hg[a]=b,!0)}function kd(a){var b=this.localeData(),c=hd(this,!a,b);return a&&(c=b.pastFuture(+this,c)),b.postformat(c)}function ld(){
// for ISO strings we do not use the normal bubbling rules:
//  * milliseconds bubble up until they become hours
//  * days do not bubble at all
//  * months bubble up until they become years
// This is because there is no context-free conversion between hours and days
// (think of clock changes)
// and also not between days and months (28-31 days per month)
var a,b,c,d=ig(this._milliseconds)/1e3,e=ig(this._days),f=ig(this._months);a=s(d/60),b=s(a/60),d%=60,a%=60,c=s(f/12),f%=12;
// inspired by https://github.com/dordille/moment-isoduration/blob/master/moment.isoduration.js
var g=c,h=f,i=e,j=b,k=a,l=d,m=this.asSeconds();return m?(0>m?"-":"")+"P"+(g?g+"Y":"")+(h?h+"M":"")+(i?i+"D":"")+(j||k||l?"T":"")+(j?j+"H":"")+(k?k+"M":"")+(l?l+"S":""):"P0D"}function md(a,b){var c=a.split("_");return b%10===1&&b%100!==11?c[0]:b%10>=2&&4>=b%10&&(10>b%100||b%100>=20)?c[1]:c[2]}function nd(a,b,c){var d={mm:b?"хвіліна_хвіліны_хвілін":"хвіліну_хвіліны_хвілін",hh:b?"гадзіна_гадзіны_гадзін":"гадзіну_гадзіны_гадзін",dd:"дзень_дні_дзён",MM:"месяц_месяцы_месяцаў",yy:"год_гады_гадоў"};return"m"===c?b?"хвіліна":"хвіліну":"h"===c?b?"гадзіна":"гадзіну":a+" "+md(d[c],+a)}function od(a,b,c){var d={mm:"munutenn",MM:"miz",dd:"devezh"};return a+" "+rd(d[c],a)}function pd(a){switch(qd(a)){case 1:case 3:case 4:case 5:case 9:return a+" bloaz";default:return a+" vloaz"}}function qd(a){return a>9?qd(a%10):a}function rd(a,b){return 2===b?sd(a):a}function sd(a){var b={m:"v",b:"v",d:"z"};return void 0===b[a.charAt(0)]?a:b[a.charAt(0)]+a.substring(1)}function td(a,b,c){var d=a+" ";switch(c){case"m":return b?"jedna minuta":"jedne minute";case"mm":return d+=1===a?"minuta":2===a||3===a||4===a?"minute":"minuta";case"h":return b?"jedan sat":"jednog sata";case"hh":return d+=1===a?"sat":2===a||3===a||4===a?"sata":"sati";case"dd":return d+=1===a?"dan":"dana";case"MM":return d+=1===a?"mjesec":2===a||3===a||4===a?"mjeseca":"mjeseci";case"yy":return d+=1===a?"godina":2===a||3===a||4===a?"godine":"godina"}}function ud(a){return a>1&&5>a&&1!==~~(a/10)}function vd(a,b,c,d){var e=a+" ";switch(c){case"s":// a few seconds / in a few seconds / a few seconds ago
return b||d?"pár sekund":"pár sekundami";case"m":// a minute / in a minute / a minute ago
return b?"minuta":d?"minutu":"minutou";case"mm":// 9 minutes / in 9 minutes / 9 minutes ago
// 9 minutes / in 9 minutes / 9 minutes ago
return b||d?e+(ud(a)?"minuty":"minut"):e+"minutami";break;case"h":// an hour / in an hour / an hour ago
return b?"hodina":d?"hodinu":"hodinou";case"hh":// 9 hours / in 9 hours / 9 hours ago
// 9 hours / in 9 hours / 9 hours ago
return b||d?e+(ud(a)?"hodiny":"hodin"):e+"hodinami";break;case"d":// a day / in a day / a day ago
return b||d?"den":"dnem";case"dd":// 9 days / in 9 days / 9 days ago
// 9 days / in 9 days / 9 days ago
return b||d?e+(ud(a)?"dny":"dní"):e+"dny";break;case"M":// a month / in a month / a month ago
return b||d?"měsíc":"měsícem";case"MM":// 9 months / in 9 months / 9 months ago
// 9 months / in 9 months / 9 months ago
return b||d?e+(ud(a)?"měsíce":"měsíců"):e+"měsíci";break;case"y":// a year / in a year / a year ago
return b||d?"rok":"rokem";case"yy":// 9 years / in 9 years / 9 years ago
// 9 years / in 9 years / 9 years ago
return b||d?e+(ud(a)?"roky":"let"):e+"lety"}}function wd(a,b,c,d){var e={m:["eine Minute","einer Minute"],h:["eine Stunde","einer Stunde"],d:["ein Tag","einem Tag"],dd:[a+" Tage",a+" Tagen"],M:["ein Monat","einem Monat"],MM:[a+" Monate",a+" Monaten"],y:["ein Jahr","einem Jahr"],yy:[a+" Jahre",a+" Jahren"]};return b?e[c][0]:e[c][1]}function xd(a,b,c,d){var e={m:["eine Minute","einer Minute"],h:["eine Stunde","einer Stunde"],d:["ein Tag","einem Tag"],dd:[a+" Tage",a+" Tagen"],M:["ein Monat","einem Monat"],MM:[a+" Monate",a+" Monaten"],y:["ein Jahr","einem Jahr"],yy:[a+" Jahre",a+" Jahren"]};return b?e[c][0]:e[c][1]}function yd(a,b,c,d){var e={s:["mõne sekundi","mõni sekund","paar sekundit"],m:["ühe minuti","üks minut"],mm:[a+" minuti",a+" minutit"],h:["ühe tunni","tund aega","üks tund"],hh:[a+" tunni",a+" tundi"],d:["ühe päeva","üks päev"],M:["kuu aja","kuu aega","üks kuu"],MM:[a+" kuu",a+" kuud"],y:["ühe aasta","aasta","üks aasta"],yy:[a+" aasta",a+" aastat"]};return b?e[c][2]?e[c][2]:e[c][1]:d?e[c][0]:e[c][1]}function zd(a,b,c,d){var e="";switch(c){case"s":return d?"muutaman sekunnin":"muutama sekunti";case"m":return d?"minuutin":"minuutti";case"mm":e=d?"minuutin":"minuuttia";break;case"h":return d?"tunnin":"tunti";case"hh":e=d?"tunnin":"tuntia";break;case"d":return d?"päivän":"päivä";case"dd":e=d?"päivän":"päivää";break;case"M":return d?"kuukauden":"kuukausi";case"MM":e=d?"kuukauden":"kuukautta";break;case"y":return d?"vuoden":"vuosi";case"yy":e=d?"vuoden":"vuotta"}return e=Ad(a,d)+" "+e}function Ad(a,b){return 10>a?b?Jg[a]:Ig[a]:a}function Bd(a,b,c){var d=a+" ";switch(c){case"m":return b?"jedna minuta":"jedne minute";case"mm":return d+=1===a?"minuta":2===a||3===a||4===a?"minute":"minuta";case"h":return b?"jedan sat":"jednog sata";case"hh":return d+=1===a?"sat":2===a||3===a||4===a?"sata":"sati";case"dd":return d+=1===a?"dan":"dana";case"MM":return d+=1===a?"mjesec":2===a||3===a||4===a?"mjeseca":"mjeseci";case"yy":return d+=1===a?"godina":2===a||3===a||4===a?"godine":"godina"}}function Cd(a,b,c,d){var e=a;switch(c){case"s":return d||b?"néhány másodperc":"néhány másodperce";case"m":return"egy"+(d||b?" perc":" perce");case"mm":return e+(d||b?" perc":" perce");case"h":return"egy"+(d||b?" óra":" órája");case"hh":return e+(d||b?" óra":" órája");case"d":return"egy"+(d||b?" nap":" napja");case"dd":return e+(d||b?" nap":" napja");case"M":return"egy"+(d||b?" hónap":" hónapja");case"MM":return e+(d||b?" hónap":" hónapja");case"y":return"egy"+(d||b?" év":" éve");case"yy":return e+(d||b?" év":" éve")}return""}function Dd(a){return(a?"":"[múlt] ")+"["+Tg[this.day()]+"] LT[-kor]"}function Ed(a){return a%100===11?!0:a%10!==1}function Fd(a,b,c,d){var e=a+" ";switch(c){case"s":return b||d?"nokkrar sekúndur":"nokkrum sekúndum";case"m":return b?"mínúta":"mínútu";case"mm":return Ed(a)?e+(b||d?"mínútur":"mínútum"):b?e+"mínúta":e+"mínútu";case"hh":return Ed(a)?e+(b||d?"klukkustundir":"klukkustundum"):e+"klukkustund";case"d":return b?"dagur":d?"dag":"degi";case"dd":return Ed(a)?b?e+"dagar":e+(d?"daga":"dögum"):b?e+"dagur":e+(d?"dag":"degi");case"M":return b?"mánuður":d?"mánuð":"mánuði";case"MM":return Ed(a)?b?e+"mánuðir":e+(d?"mánuði":"mánuðum"):b?e+"mánuður":e+(d?"mánuð":"mánuði");case"y":return b||d?"ár":"ári";case"yy":return Ed(a)?e+(b||d?"ár":"árum"):e+(b||d?"ár":"ári")}}function Gd(a,b,c,d){var e={m:["eng Minutt","enger Minutt"],h:["eng Stonn","enger Stonn"],d:["een Dag","engem Dag"],M:["ee Mount","engem Mount"],y:["ee Joer","engem Joer"]};return b?e[c][0]:e[c][1]}function Hd(a){var b=a.substr(0,a.indexOf(" "));return Jd(b)?"a "+a:"an "+a}function Id(a){var b=a.substr(0,a.indexOf(" "));return Jd(b)?"viru "+a:"virun "+a}/**
     * Returns true if the word before the given number loses the '-n' ending.
     * e.g. 'an 10 Deeg' but 'a 5 Deeg'
     *
     * @param number {integer}
     * @returns {boolean}
     */
function Jd(a){if(a=parseInt(a,10),isNaN(a))return!1;if(0>a)
// Negative Number --> always true
return!0;if(10>a)
// Only 1 digit
return a>=4&&7>=a;if(100>a){
// 2 digits
var b=a%10,c=a/10;return Jd(0===b?c:b)}if(1e4>a){
// 3 or 4 digits --> recursively check first digit
for(;a>=10;)a/=10;return Jd(a)}
// Anything larger than 4 digits: recursively check first n-3 digits
return a/=1e3,Jd(a)}function Kd(a,b,c,d){return b?"kelios sekundės":d?"kelių sekundžių":"kelias sekundes"}function Ld(a,b,c,d){return b?Nd(c)[0]:d?Nd(c)[1]:Nd(c)[2]}function Md(a){return a%10===0||a>10&&20>a}function Nd(a){return Wg[a].split("_")}function Od(a,b,c,d){var e=a+" ";return 1===a?e+Ld(a,b,c[0],d):b?e+(Md(a)?Nd(c)[1]:Nd(c)[0]):d?e+Nd(c)[1]:e+(Md(a)?Nd(c)[1]:Nd(c)[2])}/**
     * @param withoutSuffix boolean true = a length of time; false = before/after a period of time.
     */
function Pd(a,b,c){return c?b%10===1&&b%100!==11?a[2]:a[3]:b%10===1&&b%100!==11?a[0]:a[1]}function Qd(a,b,c){return a+" "+Pd(Xg[c],a,b)}function Rd(a,b,c){return Pd(Xg[c],a,b)}function Sd(a,b){return b?"dažas sekundes":"dažām sekundēm"}function Td(a,b,c,d){var e="";if(b)switch(c){case"s":e="काही सेकंद";break;case"m":e="एक मिनिट";break;case"mm":e="%d मिनिटे";break;case"h":e="एक तास";break;case"hh":e="%d तास";break;case"d":e="एक दिवस";break;case"dd":e="%d दिवस";break;case"M":e="एक महिना";break;case"MM":e="%d महिने";break;case"y":e="एक वर्ष";break;case"yy":e="%d वर्षे"}else switch(c){case"s":e="काही सेकंदां";break;case"m":e="एका मिनिटा";break;case"mm":e="%d मिनिटां";break;case"h":e="एका तासा";break;case"hh":e="%d तासां";break;case"d":e="एका दिवसा";break;case"dd":e="%d दिवसां";break;case"M":e="एका महिन्या";break;case"MM":e="%d महिन्यां";break;case"y":e="एका वर्षा";break;case"yy":e="%d वर्षां"}return e.replace(/%d/i,a)}function Ud(a){return 5>a%10&&a%10>1&&~~(a/10)%10!==1}function Vd(a,b,c){var d=a+" ";switch(c){case"m":return b?"minuta":"minutę";case"mm":return d+(Ud(a)?"minuty":"minut");case"h":return b?"godzina":"godzinę";case"hh":return d+(Ud(a)?"godziny":"godzin");case"MM":return d+(Ud(a)?"miesiące":"miesięcy");case"yy":return d+(Ud(a)?"lata":"lat")}}function Wd(a,b,c){var d={mm:"minute",hh:"ore",dd:"zile",MM:"luni",yy:"ani"},e=" ";return(a%100>=20||a>=100&&a%100===0)&&(e=" de "),a+e+d[c]}function Xd(a,b){var c=a.split("_");return b%10===1&&b%100!==11?c[0]:b%10>=2&&4>=b%10&&(10>b%100||b%100>=20)?c[1]:c[2]}function Yd(a,b,c){var d={mm:b?"минута_минуты_минут":"минуту_минуты_минут",hh:"час_часа_часов",dd:"день_дня_дней",MM:"месяц_месяца_месяцев",yy:"год_года_лет"};return"m"===c?b?"минута":"минуту":a+" "+Xd(d[c],+a)}function Zd(a){return a>1&&5>a}function $d(a,b,c,d){var e=a+" ";switch(c){case"s":// a few seconds / in a few seconds / a few seconds ago
return b||d?"pár sekúnd":"pár sekundami";case"m":// a minute / in a minute / a minute ago
return b?"minúta":d?"minútu":"minútou";case"mm":// 9 minutes / in 9 minutes / 9 minutes ago
// 9 minutes / in 9 minutes / 9 minutes ago
return b||d?e+(Zd(a)?"minúty":"minút"):e+"minútami";break;case"h":// an hour / in an hour / an hour ago
return b?"hodina":d?"hodinu":"hodinou";case"hh":// 9 hours / in 9 hours / 9 hours ago
// 9 hours / in 9 hours / 9 hours ago
return b||d?e+(Zd(a)?"hodiny":"hodín"):e+"hodinami";break;case"d":// a day / in a day / a day ago
return b||d?"deň":"dňom";case"dd":// 9 days / in 9 days / 9 days ago
// 9 days / in 9 days / 9 days ago
return b||d?e+(Zd(a)?"dni":"dní"):e+"dňami";break;case"M":// a month / in a month / a month ago
return b||d?"mesiac":"mesiacom";case"MM":// 9 months / in 9 months / 9 months ago
// 9 months / in 9 months / 9 months ago
return b||d?e+(Zd(a)?"mesiace":"mesiacov"):e+"mesiacmi";break;case"y":// a year / in a year / a year ago
return b||d?"rok":"rokom";case"yy":// 9 years / in 9 years / 9 years ago
// 9 years / in 9 years / 9 years ago
return b||d?e+(Zd(a)?"roky":"rokov"):e+"rokmi"}}function _d(a,b,c,d){var e=a+" ";switch(c){case"s":return b||d?"nekaj sekund":"nekaj sekundami";case"m":return b?"ena minuta":"eno minuto";case"mm":return e+=1===a?b?"minuta":"minuto":2===a?b||d?"minuti":"minutama":5>a?b||d?"minute":"minutami":b||d?"minut":"minutami";case"h":return b?"ena ura":"eno uro";case"hh":return e+=1===a?b?"ura":"uro":2===a?b||d?"uri":"urama":5>a?b||d?"ure":"urami":b||d?"ur":"urami";case"d":return b||d?"en dan":"enim dnem";case"dd":return e+=1===a?b||d?"dan":"dnem":2===a?b||d?"dni":"dnevoma":b||d?"dni":"dnevi";case"M":return b||d?"en mesec":"enim mesecem";case"MM":return e+=1===a?b||d?"mesec":"mesecem":2===a?b||d?"meseca":"mesecema":5>a?b||d?"mesece":"meseci":b||d?"mesecev":"meseci";case"y":return b||d?"eno leto":"enim letom";case"yy":return e+=1===a?b||d?"leto":"letom":2===a?b||d?"leti":"letoma":5>a?b||d?"leta":"leti":b||d?"let":"leti"}}function ae(a){var b=a;return b=-1!==a.indexOf("jaj")?b.slice(0,-3)+"leS":-1!==a.indexOf("jar")?b.slice(0,-3)+"waQ":-1!==a.indexOf("DIS")?b.slice(0,-3)+"nem":b+" pIq"}function be(a){var b=a;return b=-1!==a.indexOf("jaj")?b.slice(0,-3)+"Hu’":-1!==a.indexOf("jar")?b.slice(0,-3)+"wen":-1!==a.indexOf("DIS")?b.slice(0,-3)+"ben":b+" ret"}function ce(a,b,c,d){var e=de(a);switch(c){case"mm":return e+" tup";case"hh":return e+" rep";case"dd":return e+" jaj";case"MM":return e+" jar";case"yy":return e+" DIS"}}function de(a){var b=Math.floor(a%1e3/100),c=Math.floor(a%100/10),d=a%10,e="";return b>0&&(e+=qh[b]+"vatlh"),c>0&&(e+=(""!==e?" ":"")+qh[c]+"maH"),d>0&&(e+=(""!==e?" ":"")+qh[d]),""===e?"pagh":e}function ee(a,b,c,d){var e={s:["viensas secunds","'iensas secunds"],m:["'n míut","'iens míut"],mm:[a+" míuts",""+a+" míuts"],h:["'n þora","'iensa þora"],hh:[a+" þoras",""+a+" þoras"],d:["'n ziua","'iensa ziua"],dd:[a+" ziuas",""+a+" ziuas"],M:["'n mes","'iens mes"],MM:[a+" mesen",""+a+" mesen"],y:["'n ar","'iens ar"],yy:[a+" ars",""+a+" ars"]};return d?e[c][0]:b?e[c][0]:e[c][1]}function fe(a,b){var c=a.split("_");return b%10===1&&b%100!==11?c[0]:b%10>=2&&4>=b%10&&(10>b%100||b%100>=20)?c[1]:c[2]}function ge(a,b,c){var d={mm:b?"хвилина_хвилини_хвилин":"хвилину_хвилини_хвилин",hh:b?"година_години_годин":"годину_години_годин",dd:"день_дні_днів",MM:"місяць_місяці_місяців",yy:"рік_роки_років"};return"m"===c?b?"хвилина":"хвилину":"h"===c?b?"година":"годину":a+" "+fe(d[c],+a)}function he(a,b){var c={nominative:"неділя_понеділок_вівторок_середа_четвер_п’ятниця_субота".split("_"),accusative:"неділю_понеділок_вівторок_середу_четвер_п’ятницю_суботу".split("_"),genitive:"неділі_понеділка_вівторка_середи_четверга_п’ятниці_суботи".split("_")},d=/(\[[ВвУу]\]) ?dddd/.test(b)?"accusative":/\[?(?:минулої|наступної)? ?\] ?dddd/.test(b)?"genitive":"nominative";return c[d][a.day()]}function ie(a){return function(){return a+"о"+(11===this.hours()?"б":"")+"] LT"}}var je,ke;ke=Array.prototype.some?Array.prototype.some:function(a){for(var b=Object(this),c=b.length>>>0,d=0;c>d;d++)if(d in b&&a.call(this,b[d],d,b))return!0;return!1};
// Plugins that add properties should also add the key here (null value),
// so we can properly clone ourselves.
var le=a.momentProperties=[],me=!1,ne={};a.suppressDeprecationWarnings=!1,a.deprecationHandler=null;var oe;oe=Object.keys?Object.keys:function(a){var b,c=[];for(b in a)h(a,b)&&c.push(b);return c};var pe,qe={sameDay:"[Today at] LT",nextDay:"[Tomorrow at] LT",nextWeek:"dddd [at] LT",lastDay:"[Yesterday at] LT",lastWeek:"[Last] dddd [at] LT",sameElse:"L"},re={LTS:"h:mm:ss A",LT:"h:mm A",L:"MM/DD/YYYY",LL:"MMMM D, YYYY",LLL:"MMMM D, YYYY h:mm A",LLLL:"dddd, MMMM D, YYYY h:mm A"},se="Invalid date",te="%d",ue=/\d{1,2}/,ve={future:"in %s",past:"%s ago",s:"a few seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},we={},xe={},ye=/(\[[^\[]*\])|(\\)?([Hh]mm(ss)?|Mo|MM?M?M?|Do|DDDo|DD?D?D?|ddd?d?|do?|w[o|w]?|W[o|W]?|Qo?|YYYYYY|YYYYY|YYYY|YY|gg(ggg?)?|GG(GGG?)?|e|E|a|A|hh?|HH?|kk?|mm?|ss?|S{1,9}|x|X|zz?|ZZ?|.)/g,ze=/(\[[^\[]*\])|(\\)?(LTS|LT|LL?L?L?|l{1,4})/g,Ae={},Be={},Ce=/\d/,De=/\d\d/,Ee=/\d{3}/,Fe=/\d{4}/,Ge=/[+-]?\d{6}/,He=/\d\d?/,Ie=/\d\d\d\d?/,Je=/\d\d\d\d\d\d?/,Ke=/\d{1,3}/,Le=/\d{1,4}/,Me=/[+-]?\d{1,6}/,Ne=/\d+/,Oe=/[+-]?\d+/,Pe=/Z|[+-]\d\d:?\d\d/gi,Qe=/Z|[+-]\d\d(?::?\d\d)?/gi,Re=/[+-]?\d+(\.\d{1,3})?/,Se=/[0-9]*['a-z\u00A0-\u05FF\u0700-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+|[\u0600-\u06FF\/]+(\s*?[\u0600-\u06FF]+){1,2}/i,Te={},Ue={},Ve=0,We=1,Xe=2,Ye=3,Ze=4,$e=5,_e=6,af=7,bf=8;pe=Array.prototype.indexOf?Array.prototype.indexOf:function(a){
// I know
var b;for(b=0;b<this.length;++b)if(this[b]===a)return b;return-1},T("M",["MM",2],"Mo",function(){return this.month()+1}),T("MMM",0,0,function(a){return this.localeData().monthsShort(this,a)}),T("MMMM",0,0,function(a){return this.localeData().months(this,a)}),I("month","M"),L("month",8),Y("M",He),Y("MM",He,De),Y("MMM",function(a,b){return b.monthsShortRegex(a)}),Y("MMMM",function(a,b){return b.monthsRegex(a)}),aa(["M","MM"],function(a,b){b[We]=t(a)-1}),aa(["MMM","MMMM"],function(a,b,c,d){var e=c._locale.monthsParse(a,d,c._strict);null!=e?b[We]=e:l(c).invalidMonth=a});
// LOCALES
var cf=/D[oD]?(\[[^\[\]]*\]|\s+)+MMMM?/,df="January_February_March_April_May_June_July_August_September_October_November_December".split("_"),ef="Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),ff=Se,gf=Se;
// FORMATTING
T("Y",0,0,function(){var a=this.year();return 9999>=a?""+a:"+"+a}),T(0,["YY",2],0,function(){return this.year()%100}),T(0,["YYYY",4],0,"year"),T(0,["YYYYY",5],0,"year"),T(0,["YYYYYY",6,!0],0,"year"),
// ALIASES
I("year","y"),
// PRIORITIES
L("year",1),
// PARSING
Y("Y",Oe),Y("YY",He,De),Y("YYYY",Le,Fe),Y("YYYYY",Me,Ge),Y("YYYYYY",Me,Ge),aa(["YYYYY","YYYYYY"],Ve),aa("YYYY",function(b,c){c[Ve]=2===b.length?a.parseTwoDigitYear(b):t(b)}),aa("YY",function(b,c){c[Ve]=a.parseTwoDigitYear(b)}),aa("Y",function(a,b){b[Ve]=parseInt(a,10)}),
// HOOKS
a.parseTwoDigitYear=function(a){return t(a)+(t(a)>68?1900:2e3)};
// MOMENTS
var hf=N("FullYear",!0);
// FORMATTING
T("w",["ww",2],"wo","week"),T("W",["WW",2],"Wo","isoWeek"),
// ALIASES
I("week","w"),I("isoWeek","W"),
// PRIORITIES
L("week",5),L("isoWeek",5),
// PARSING
Y("w",He),Y("ww",He,De),Y("W",He),Y("WW",He,De),ba(["w","ww","W","WW"],function(a,b,c,d){b[d.substr(0,1)]=t(a)});var jf={dow:0,// Sunday is the first day of the week.
doy:6};
// FORMATTING
T("d",0,"do","day"),T("dd",0,0,function(a){return this.localeData().weekdaysMin(this,a)}),T("ddd",0,0,function(a){return this.localeData().weekdaysShort(this,a)}),T("dddd",0,0,function(a){return this.localeData().weekdays(this,a)}),T("e",0,0,"weekday"),T("E",0,0,"isoWeekday"),
// ALIASES
I("day","d"),I("weekday","e"),I("isoWeekday","E"),
// PRIORITY
L("day",11),L("weekday",11),L("isoWeekday",11),
// PARSING
Y("d",He),Y("e",He),Y("E",He),Y("dd",function(a,b){return b.weekdaysMinRegex(a)}),Y("ddd",function(a,b){return b.weekdaysShortRegex(a)}),Y("dddd",function(a,b){return b.weekdaysRegex(a)}),ba(["dd","ddd","dddd"],function(a,b,c,d){var e=c._locale.weekdaysParse(a,d,c._strict);
// if we didn't get a weekday name, mark the date as invalid
null!=e?b.d=e:l(c).invalidWeekday=a}),ba(["d","e","E"],function(a,b,c,d){b[d]=t(a)});
// LOCALES
var kf="Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),lf="Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),mf="Su_Mo_Tu_We_Th_Fr_Sa".split("_"),nf=Se,of=Se,pf=Se;T("H",["HH",2],0,"hour"),T("h",["hh",2],0,Qa),T("k",["kk",2],0,Ra),T("hmm",0,0,function(){return""+Qa.apply(this)+S(this.minutes(),2)}),T("hmmss",0,0,function(){return""+Qa.apply(this)+S(this.minutes(),2)+S(this.seconds(),2)}),T("Hmm",0,0,function(){return""+this.hours()+S(this.minutes(),2)}),T("Hmmss",0,0,function(){return""+this.hours()+S(this.minutes(),2)+S(this.seconds(),2)}),Sa("a",!0),Sa("A",!1),
// ALIASES
I("hour","h"),
// PRIORITY
L("hour",13),Y("a",Ta),Y("A",Ta),Y("H",He),Y("h",He),Y("HH",He,De),Y("hh",He,De),Y("hmm",Ie),Y("hmmss",Je),Y("Hmm",Ie),Y("Hmmss",Je),aa(["H","HH"],Ye),aa(["a","A"],function(a,b,c){c._isPm=c._locale.isPM(a),c._meridiem=a}),aa(["h","hh"],function(a,b,c){b[Ye]=t(a),l(c).bigHour=!0}),aa("hmm",function(a,b,c){var d=a.length-2;b[Ye]=t(a.substr(0,d)),b[Ze]=t(a.substr(d)),l(c).bigHour=!0}),aa("hmmss",function(a,b,c){var d=a.length-4,e=a.length-2;b[Ye]=t(a.substr(0,d)),b[Ze]=t(a.substr(d,2)),b[$e]=t(a.substr(e)),l(c).bigHour=!0}),aa("Hmm",function(a,b,c){var d=a.length-2;b[Ye]=t(a.substr(0,d)),b[Ze]=t(a.substr(d))}),aa("Hmmss",function(a,b,c){var d=a.length-4,e=a.length-2;b[Ye]=t(a.substr(0,d)),b[Ze]=t(a.substr(d,2)),b[$e]=t(a.substr(e))});var qf,rf=/[ap]\.?m?\.?/i,sf=N("Hours",!0),tf={calendar:qe,longDateFormat:re,invalidDate:se,ordinal:te,ordinalParse:ue,relativeTime:ve,months:df,monthsShort:ef,week:jf,weekdays:kf,weekdaysMin:mf,weekdaysShort:lf,meridiemParse:rf},uf={},vf=/^\s*((?:[+-]\d{6}|\d{4})-(?:\d\d-\d\d|W\d\d-\d|W\d\d|\d\d\d|\d\d))(?:(T| )(\d\d(?::\d\d(?::\d\d(?:[.,]\d+)?)?)?)([\+\-]\d\d(?::?\d\d)?|\s*Z)?)?/,wf=/^\s*((?:[+-]\d{6}|\d{4})(?:\d\d\d\d|W\d\d\d|W\d\d|\d\d\d|\d\d))(?:(T| )(\d\d(?:\d\d(?:\d\d(?:[.,]\d+)?)?)?)([\+\-]\d\d(?::?\d\d)?|\s*Z)?)?/,xf=/Z|[+-]\d\d(?::?\d\d)?/,yf=[["YYYYYY-MM-DD",/[+-]\d{6}-\d\d-\d\d/],["YYYY-MM-DD",/\d{4}-\d\d-\d\d/],["GGGG-[W]WW-E",/\d{4}-W\d\d-\d/],["GGGG-[W]WW",/\d{4}-W\d\d/,!1],["YYYY-DDD",/\d{4}-\d{3}/],["YYYY-MM",/\d{4}-\d\d/,!1],["YYYYYYMMDD",/[+-]\d{10}/],["YYYYMMDD",/\d{8}/],
// YYYYMM is NOT allowed by the standard
["GGGG[W]WWE",/\d{4}W\d{3}/],["GGGG[W]WW",/\d{4}W\d{2}/,!1],["YYYYDDD",/\d{7}/]],zf=[["HH:mm:ss.SSSS",/\d\d:\d\d:\d\d\.\d+/],["HH:mm:ss,SSSS",/\d\d:\d\d:\d\d,\d+/],["HH:mm:ss",/\d\d:\d\d:\d\d/],["HH:mm",/\d\d:\d\d/],["HHmmss.SSSS",/\d\d\d\d\d\d\.\d+/],["HHmmss,SSSS",/\d\d\d\d\d\d,\d+/],["HHmmss",/\d\d\d\d\d\d/],["HHmm",/\d\d\d\d/],["HH",/\d\d/]],Af=/^\/?Date\((\-?\d+)/i;a.createFromInputFallback=w("moment construction falls back to js Date. This is discouraged and will be removed in upcoming major release. Please refer to http://momentjs.com/guides/#/warnings/js-date/ for more info.",function(a){a._d=new Date(a._i+(a._useUTC?" UTC":""))}),
// constant that refers to the ISO standard
a.ISO_8601=function(){};var Bf=w("moment().min is deprecated, use moment.max instead. http://momentjs.com/guides/#/warnings/min-max/",function(){var a=rb.apply(null,arguments);return this.isValid()&&a.isValid()?this>a?this:a:n()}),Cf=w("moment().max is deprecated, use moment.min instead. http://momentjs.com/guides/#/warnings/min-max/",function(){var a=rb.apply(null,arguments);return this.isValid()&&a.isValid()?a>this?this:a:n()}),Df=function(){return Date.now?Date.now():+new Date};xb("Z",":"),xb("ZZ",""),
// PARSING
Y("Z",Qe),Y("ZZ",Qe),aa(["Z","ZZ"],function(a,b,c){c._useUTC=!0,c._tzm=yb(Qe,a)});
// HELPERS
// timezone chunker
// '+10:00' > ['10',  '00']
// '-1530'  > ['-15', '30']
var Ef=/([\+\-]|\d\d)/gi;
// HOOKS
// This function will be called whenever a moment is mutated.
// It is intended to keep the offset in sync with the timezone.
a.updateOffset=function(){};
// ASP.NET json date format regex
var Ff=/^(\-)?(?:(\d*)[. ])?(\d+)\:(\d+)(?:\:(\d+)\.?(\d{3})?\d*)?$/,Gf=/^(-)?P(?:(-?[0-9,.]*)Y)?(?:(-?[0-9,.]*)M)?(?:(-?[0-9,.]*)W)?(?:(-?[0-9,.]*)D)?(?:T(?:(-?[0-9,.]*)H)?(?:(-?[0-9,.]*)M)?(?:(-?[0-9,.]*)S)?)?$/;Mb.fn=vb.prototype;var Hf=Rb(1,"add"),If=Rb(-1,"subtract");a.defaultFormat="YYYY-MM-DDTHH:mm:ssZ",a.defaultFormatUtc="YYYY-MM-DDTHH:mm:ss[Z]";var Jf=w("moment().lang() is deprecated. Instead, use moment().localeData() to get the language configuration. Use moment().locale() to change languages.",function(a){return void 0===a?this.localeData():this.locale(a)});
// FORMATTING
T(0,["gg",2],0,function(){return this.weekYear()%100}),T(0,["GG",2],0,function(){return this.isoWeekYear()%100}),xc("gggg","weekYear"),xc("ggggg","weekYear"),xc("GGGG","isoWeekYear"),xc("GGGGG","isoWeekYear"),
// ALIASES
I("weekYear","gg"),I("isoWeekYear","GG"),
// PRIORITY
L("weekYear",1),L("isoWeekYear",1),
// PARSING
Y("G",Oe),Y("g",Oe),Y("GG",He,De),Y("gg",He,De),Y("GGGG",Le,Fe),Y("gggg",Le,Fe),Y("GGGGG",Me,Ge),Y("ggggg",Me,Ge),ba(["gggg","ggggg","GGGG","GGGGG"],function(a,b,c,d){b[d.substr(0,2)]=t(a)}),ba(["gg","GG"],function(b,c,d,e){c[e]=a.parseTwoDigitYear(b)}),
// FORMATTING
T("Q",0,"Qo","quarter"),
// ALIASES
I("quarter","Q"),
// PRIORITY
L("quarter",7),
// PARSING
Y("Q",Ce),aa("Q",function(a,b){b[We]=3*(t(a)-1)}),
// FORMATTING
T("D",["DD",2],"Do","date"),
// ALIASES
I("date","D"),
// PRIOROITY
L("date",9),
// PARSING
Y("D",He),Y("DD",He,De),Y("Do",function(a,b){return a?b._ordinalParse:b._ordinalParseLenient}),aa(["D","DD"],Xe),aa("Do",function(a,b){b[Xe]=t(a.match(He)[0],10)});
// MOMENTS
var Kf=N("Date",!0);
// FORMATTING
T("DDD",["DDDD",3],"DDDo","dayOfYear"),
// ALIASES
I("dayOfYear","DDD"),
// PRIORITY
L("dayOfYear",4),
// PARSING
Y("DDD",Ke),Y("DDDD",Ee),aa(["DDD","DDDD"],function(a,b,c){c._dayOfYear=t(a)}),
// FORMATTING
T("m",["mm",2],0,"minute"),
// ALIASES
I("minute","m"),
// PRIORITY
L("minute",14),
// PARSING
Y("m",He),Y("mm",He,De),aa(["m","mm"],Ze);
// MOMENTS
var Lf=N("Minutes",!1);
// FORMATTING
T("s",["ss",2],0,"second"),
// ALIASES
I("second","s"),
// PRIORITY
L("second",15),
// PARSING
Y("s",He),Y("ss",He,De),aa(["s","ss"],$e);
// MOMENTS
var Mf=N("Seconds",!1);
// FORMATTING
T("S",0,0,function(){return~~(this.millisecond()/100)}),T(0,["SS",2],0,function(){return~~(this.millisecond()/10)}),T(0,["SSS",3],0,"millisecond"),T(0,["SSSS",4],0,function(){return 10*this.millisecond()}),T(0,["SSSSS",5],0,function(){return 100*this.millisecond()}),T(0,["SSSSSS",6],0,function(){return 1e3*this.millisecond()}),T(0,["SSSSSSS",7],0,function(){return 1e4*this.millisecond()}),T(0,["SSSSSSSS",8],0,function(){return 1e5*this.millisecond()}),T(0,["SSSSSSSSS",9],0,function(){return 1e6*this.millisecond()}),
// ALIASES
I("millisecond","ms"),
// PRIORITY
L("millisecond",16),
// PARSING
Y("S",Ke,Ce),Y("SS",Ke,De),Y("SSS",Ke,Ee);var Nf;for(Nf="SSSS";Nf.length<=9;Nf+="S")Y(Nf,Ne);for(Nf="S";Nf.length<=9;Nf+="S")aa(Nf,Gc);
// MOMENTS
var Of=N("Milliseconds",!1);
// FORMATTING
T("z",0,0,"zoneAbbr"),T("zz",0,0,"zoneName");var Pf=q.prototype;Pf.add=Hf,Pf.calendar=Ub,Pf.clone=Vb,Pf.diff=ac,Pf.endOf=mc,Pf.format=ec,Pf.from=fc,Pf.fromNow=gc,Pf.to=hc,Pf.toNow=ic,Pf.get=Q,Pf.invalidAt=vc,Pf.isAfter=Wb,Pf.isBefore=Xb,Pf.isBetween=Yb,Pf.isSame=Zb,Pf.isSameOrAfter=$b,Pf.isSameOrBefore=_b,Pf.isValid=tc,Pf.lang=Jf,Pf.locale=jc,Pf.localeData=kc,Pf.max=Cf,Pf.min=Bf,Pf.parsingFlags=uc,Pf.set=R,Pf.startOf=lc,Pf.subtract=If,Pf.toArray=qc,Pf.toObject=rc,Pf.toDate=pc,Pf.toISOString=dc,Pf.toJSON=sc,Pf.toString=cc,Pf.unix=oc,Pf.valueOf=nc,Pf.creationData=wc,
// Year
Pf.year=hf,Pf.isLeapYear=qa,
// Week Year
Pf.weekYear=yc,Pf.isoWeekYear=zc,
// Quarter
Pf.quarter=Pf.quarters=Ec,
// Month
Pf.month=ja,Pf.daysInMonth=ka,
// Week
Pf.week=Pf.weeks=Aa,Pf.isoWeek=Pf.isoWeeks=Ba,Pf.weeksInYear=Bc,Pf.isoWeeksInYear=Ac,
// Day
Pf.date=Kf,Pf.day=Pf.days=Ja,Pf.weekday=Ka,Pf.isoWeekday=La,Pf.dayOfYear=Fc,
// Hour
Pf.hour=Pf.hours=sf,
// Minute
Pf.minute=Pf.minutes=Lf,
// Second
Pf.second=Pf.seconds=Mf,
// Millisecond
Pf.millisecond=Pf.milliseconds=Of,
// Offset
Pf.utcOffset=Bb,Pf.utc=Db,Pf.local=Eb,Pf.parseZone=Fb,Pf.hasAlignedHourOffset=Gb,Pf.isDST=Hb,Pf.isLocal=Jb,Pf.isUtcOffset=Kb,Pf.isUtc=Lb,Pf.isUTC=Lb,
// Timezone
Pf.zoneAbbr=Hc,Pf.zoneName=Ic,
// Deprecations
Pf.dates=w("dates accessor is deprecated. Use date instead.",Kf),Pf.months=w("months accessor is deprecated. Use month instead",ja),Pf.years=w("years accessor is deprecated. Use year instead",hf),Pf.zone=w("moment().zone is deprecated, use moment().utcOffset instead. http://momentjs.com/guides/#/warnings/zone/",Cb),Pf.isDSTShifted=w("isDSTShifted is deprecated. See http://momentjs.com/guides/#/warnings/dst-shifted/ for more information",Ib);var Qf=Pf,Rf=B.prototype;Rf.calendar=C,Rf.longDateFormat=D,Rf.invalidDate=E,Rf.ordinal=F,Rf.preparse=Lc,Rf.postformat=Lc,Rf.relativeTime=G,Rf.pastFuture=H,Rf.set=z,
// Month
Rf.months=ea,Rf.monthsShort=fa,Rf.monthsParse=ha,Rf.monthsRegex=ma,Rf.monthsShortRegex=la,
// Week
Rf.week=xa,Rf.firstDayOfYear=za,Rf.firstDayOfWeek=ya,
// Day of Week
Rf.weekdays=Ea,Rf.weekdaysMin=Ga,Rf.weekdaysShort=Fa,Rf.weekdaysParse=Ia,Rf.weekdaysRegex=Ma,Rf.weekdaysShortRegex=Na,Rf.weekdaysMinRegex=Oa,
// Hours
Rf.isPM=Ua,Rf.meridiem=Va,Za("en",{ordinalParse:/\d{1,2}(th|st|nd|rd)/,ordinal:function(a){var b=a%10,c=1===t(a%100/10)?"th":1===b?"st":2===b?"nd":3===b?"rd":"th";return a+c}}),
// Side effect imports
a.lang=w("moment.lang is deprecated. Use moment.locale instead.",Za),a.langData=w("moment.langData is deprecated. Use moment.localeData instead.",ab);var Sf=Math.abs,Tf=cd("ms"),Uf=cd("s"),Vf=cd("m"),Wf=cd("h"),Xf=cd("d"),Yf=cd("w"),Zf=cd("M"),$f=cd("y"),_f=ed("milliseconds"),ag=ed("seconds"),bg=ed("minutes"),cg=ed("hours"),dg=ed("days"),eg=ed("months"),fg=ed("years"),gg=Math.round,hg={s:45,// seconds to minute
m:45,// minutes to hour
h:22,// hours to day
d:26,// days to month
M:11},ig=Math.abs,jg=vb.prototype;jg.abs=Uc,jg.add=Wc,jg.subtract=Xc,jg.as=ad,jg.asMilliseconds=Tf,jg.asSeconds=Uf,jg.asMinutes=Vf,jg.asHours=Wf,jg.asDays=Xf,jg.asWeeks=Yf,jg.asMonths=Zf,jg.asYears=$f,jg.valueOf=bd,jg._bubble=Zc,jg.get=dd,jg.milliseconds=_f,jg.seconds=ag,jg.minutes=bg,jg.hours=cg,jg.days=dg,jg.weeks=fd,jg.months=eg,jg.years=fg,jg.humanize=kd,jg.toISOString=ld,jg.toString=ld,jg.toJSON=ld,jg.locale=jc,jg.localeData=kc,
// Deprecations
jg.toIsoString=w("toIsoString() is deprecated. Please use toISOString() instead (notice the capitals)",ld),jg.lang=Jf,
// Side effect imports
// FORMATTING
T("X",0,0,"unix"),T("x",0,0,"valueOf"),
// PARSING
Y("x",Oe),Y("X",Re),aa("X",function(a,b,c){c._d=new Date(1e3*parseFloat(a,10))}),aa("x",function(a,b,c){c._d=new Date(t(a))}),a.version="2.14.1",b(rb),a.fn=Qf,a.min=tb,a.max=ub,a.now=Df,a.utc=j,a.unix=Jc,a.months=Pc,a.isDate=f,a.locale=Za,a.invalid=n,a.duration=Mb,a.isMoment=r,a.weekdays=Rc,a.parseZone=Kc,a.localeData=ab,a.isDuration=wb,a.monthsShort=Qc,a.weekdaysMin=Tc,a.defineLocale=$a,a.updateLocale=_a,a.locales=bb,a.weekdaysShort=Sc,a.normalizeUnits=J,a.relativeTimeRounding=id,a.relativeTimeThreshold=jd,a.calendarFormat=Tb,a.prototype=Qf;var kg=a,lg=(kg.defineLocale("af",{months:"Januarie_Februarie_Maart_April_Mei_Junie_Julie_Augustus_September_Oktober_November_Desember".split("_"),monthsShort:"Jan_Feb_Mrt_Apr_Mei_Jun_Jul_Aug_Sep_Okt_Nov_Des".split("_"),weekdays:"Sondag_Maandag_Dinsdag_Woensdag_Donderdag_Vrydag_Saterdag".split("_"),weekdaysShort:"Son_Maa_Din_Woe_Don_Vry_Sat".split("_"),weekdaysMin:"So_Ma_Di_Wo_Do_Vr_Sa".split("_"),meridiemParse:/vm|nm/i,isPM:function(a){return/^nm$/i.test(a)},meridiem:function(a,b,c){return 12>a?c?"vm":"VM":c?"nm":"NM"},longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Vandag om] LT",nextDay:"[Môre om] LT",nextWeek:"dddd [om] LT",lastDay:"[Gister om] LT",lastWeek:"[Laas] dddd [om] LT",sameElse:"L"},relativeTime:{future:"oor %s",past:"%s gelede",s:"'n paar sekondes",m:"'n minuut",mm:"%d minute",h:"'n uur",hh:"%d ure",d:"'n dag",dd:"%d dae",M:"'n maand",MM:"%d maande",y:"'n jaar",yy:"%d jaar"},ordinalParse:/\d{1,2}(ste|de)/,ordinal:function(a){return a+(1===a||8===a||a>=20?"ste":"de")},week:{dow:1,// Maandag is die eerste dag van die week.
doy:4}}),kg.defineLocale("ar-ma",{months:"يناير_فبراير_مارس_أبريل_ماي_يونيو_يوليوز_غشت_شتنبر_أكتوبر_نونبر_دجنبر".split("_"),monthsShort:"يناير_فبراير_مارس_أبريل_ماي_يونيو_يوليوز_غشت_شتنبر_أكتوبر_نونبر_دجنبر".split("_"),weekdays:"الأحد_الإتنين_الثلاثاء_الأربعاء_الخميس_الجمعة_السبت".split("_"),weekdaysShort:"احد_اتنين_ثلاثاء_اربعاء_خميس_جمعة_سبت".split("_"),weekdaysMin:"ح_ن_ث_ر_خ_ج_س".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[اليوم على الساعة] LT",nextDay:"[غدا على الساعة] LT",nextWeek:"dddd [على الساعة] LT",lastDay:"[أمس على الساعة] LT",lastWeek:"dddd [على الساعة] LT",sameElse:"L"},relativeTime:{future:"في %s",past:"منذ %s",s:"ثوان",m:"دقيقة",mm:"%d دقائق",h:"ساعة",hh:"%d ساعات",d:"يوم",dd:"%d أيام",M:"شهر",MM:"%d أشهر",y:"سنة",yy:"%d سنوات"},week:{dow:6,// Saturday is the first day of the week.
doy:12}}),{1:"١",2:"٢",3:"٣",4:"٤",5:"٥",6:"٦",7:"٧",8:"٨",9:"٩",0:"٠"}),mg={"١":"1","٢":"2","٣":"3","٤":"4","٥":"5","٦":"6","٧":"7","٨":"8","٩":"9","٠":"0"},ng=(kg.defineLocale("ar-sa",{months:"يناير_فبراير_مارس_أبريل_مايو_يونيو_يوليو_أغسطس_سبتمبر_أكتوبر_نوفمبر_ديسمبر".split("_"),monthsShort:"يناير_فبراير_مارس_أبريل_مايو_يونيو_يوليو_أغسطس_سبتمبر_أكتوبر_نوفمبر_ديسمبر".split("_"),weekdays:"الأحد_الإثنين_الثلاثاء_الأربعاء_الخميس_الجمعة_السبت".split("_"),weekdaysShort:"أحد_إثنين_ثلاثاء_أربعاء_خميس_جمعة_سبت".split("_"),weekdaysMin:"ح_ن_ث_ر_خ_ج_س".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},meridiemParse:/ص|م/,isPM:function(a){return"م"===a},meridiem:function(a,b,c){return 12>a?"ص":"م"},calendar:{sameDay:"[اليوم على الساعة] LT",nextDay:"[غدا على الساعة] LT",nextWeek:"dddd [على الساعة] LT",lastDay:"[أمس على الساعة] LT",lastWeek:"dddd [على الساعة] LT",sameElse:"L"},relativeTime:{future:"في %s",past:"منذ %s",s:"ثوان",m:"دقيقة",mm:"%d دقائق",h:"ساعة",hh:"%d ساعات",d:"يوم",dd:"%d أيام",M:"شهر",MM:"%d أشهر",y:"سنة",yy:"%d سنوات"},preparse:function(a){return a.replace(/[١٢٣٤٥٦٧٨٩٠]/g,function(a){return mg[a]}).replace(/،/g,",")},postformat:function(a){return a.replace(/\d/g,function(a){return lg[a]}).replace(/,/g,"،")},week:{dow:6,// Saturday is the first day of the week.
doy:12}}),kg.defineLocale("ar-tn",{months:"جانفي_فيفري_مارس_أفريل_ماي_جوان_جويلية_أوت_سبتمبر_أكتوبر_نوفمبر_ديسمبر".split("_"),monthsShort:"جانفي_فيفري_مارس_أفريل_ماي_جوان_جويلية_أوت_سبتمبر_أكتوبر_نوفمبر_ديسمبر".split("_"),weekdays:"الأحد_الإثنين_الثلاثاء_الأربعاء_الخميس_الجمعة_السبت".split("_"),weekdaysShort:"أحد_إثنين_ثلاثاء_أربعاء_خميس_جمعة_سبت".split("_"),weekdaysMin:"ح_ن_ث_ر_خ_ج_س".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[اليوم على الساعة] LT",nextDay:"[غدا على الساعة] LT",nextWeek:"dddd [على الساعة] LT",lastDay:"[أمس على الساعة] LT",lastWeek:"dddd [على الساعة] LT",sameElse:"L"},relativeTime:{future:"في %s",past:"منذ %s",s:"ثوان",m:"دقيقة",mm:"%d دقائق",h:"ساعة",hh:"%d ساعات",d:"يوم",dd:"%d أيام",M:"شهر",MM:"%d أشهر",y:"سنة",yy:"%d سنوات"},week:{dow:1,// Monday is the first day of the week.
doy:4}}),{1:"١",2:"٢",3:"٣",4:"٤",5:"٥",6:"٦",7:"٧",8:"٨",9:"٩",0:"٠"}),og={"١":"1","٢":"2","٣":"3","٤":"4","٥":"5","٦":"6","٧":"7","٨":"8","٩":"9","٠":"0"},pg=function(a){return 0===a?0:1===a?1:2===a?2:a%100>=3&&10>=a%100?3:a%100>=11?4:5},qg={s:["أقل من ثانية","ثانية واحدة",["ثانيتان","ثانيتين"],"%d ثوان","%d ثانية","%d ثانية"],m:["أقل من دقيقة","دقيقة واحدة",["دقيقتان","دقيقتين"],"%d دقائق","%d دقيقة","%d دقيقة"],h:["أقل من ساعة","ساعة واحدة",["ساعتان","ساعتين"],"%d ساعات","%d ساعة","%d ساعة"],d:["أقل من يوم","يوم واحد",["يومان","يومين"],"%d أيام","%d يومًا","%d يوم"],M:["أقل من شهر","شهر واحد",["شهران","شهرين"],"%d أشهر","%d شهرا","%d شهر"],y:["أقل من عام","عام واحد",["عامان","عامين"],"%d أعوام","%d عامًا","%d عام"]},rg=function(a){return function(b,c,d,e){var f=pg(b),g=qg[a][pg(b)];return 2===f&&(g=g[c?0:1]),g.replace(/%d/i,b)}},sg=["كانون الثاني يناير","شباط فبراير","آذار مارس","نيسان أبريل","أيار مايو","حزيران يونيو","تموز يوليو","آب أغسطس","أيلول سبتمبر","تشرين الأول أكتوبر","تشرين الثاني نوفمبر","كانون الأول ديسمبر"],tg=(kg.defineLocale("ar",{months:sg,monthsShort:sg,weekdays:"الأحد_الإثنين_الثلاثاء_الأربعاء_الخميس_الجمعة_السبت".split("_"),weekdaysShort:"أحد_إثنين_ثلاثاء_أربعاء_خميس_جمعة_سبت".split("_"),weekdaysMin:"ح_ن_ث_ر_خ_ج_س".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"D/‏M/‏YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},meridiemParse:/ص|م/,isPM:function(a){return"م"===a},meridiem:function(a,b,c){return 12>a?"ص":"م"},calendar:{sameDay:"[اليوم عند الساعة] LT",nextDay:"[غدًا عند الساعة] LT",nextWeek:"dddd [عند الساعة] LT",lastDay:"[أمس عند الساعة] LT",lastWeek:"dddd [عند الساعة] LT",sameElse:"L"},relativeTime:{future:"بعد %s",past:"منذ %s",s:rg("s"),m:rg("m"),mm:rg("m"),h:rg("h"),hh:rg("h"),d:rg("d"),dd:rg("d"),M:rg("M"),MM:rg("M"),y:rg("y"),yy:rg("y")},preparse:function(a){return a.replace(/\u200f/g,"").replace(/[١٢٣٤٥٦٧٨٩٠]/g,function(a){return og[a]}).replace(/،/g,",")},postformat:function(a){return a.replace(/\d/g,function(a){return ng[a]}).replace(/,/g,"،")},week:{dow:6,// Saturday is the first day of the week.
doy:12}}),{1:"-inci",5:"-inci",8:"-inci",70:"-inci",80:"-inci",2:"-nci",7:"-nci",20:"-nci",50:"-nci",3:"-üncü",4:"-üncü",100:"-üncü",6:"-ncı",9:"-uncu",10:"-uncu",30:"-uncu",60:"-ıncı",90:"-ıncı"}),ug=(kg.defineLocale("az",{months:"yanvar_fevral_mart_aprel_may_iyun_iyul_avqust_sentyabr_oktyabr_noyabr_dekabr".split("_"),monthsShort:"yan_fev_mar_apr_may_iyn_iyl_avq_sen_okt_noy_dek".split("_"),weekdays:"Bazar_Bazar ertəsi_Çərşənbə axşamı_Çərşənbə_Cümə axşamı_Cümə_Şənbə".split("_"),weekdaysShort:"Baz_BzE_ÇAx_Çər_CAx_Cüm_Şən".split("_"),weekdaysMin:"Bz_BE_ÇA_Çə_CA_Cü_Şə".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[bugün saat] LT",nextDay:"[sabah saat] LT",nextWeek:"[gələn həftə] dddd [saat] LT",lastDay:"[dünən] LT",lastWeek:"[keçən həftə] dddd [saat] LT",sameElse:"L"},relativeTime:{future:"%s sonra",past:"%s əvvəl",s:"birneçə saniyyə",m:"bir dəqiqə",mm:"%d dəqiqə",h:"bir saat",hh:"%d saat",d:"bir gün",dd:"%d gün",M:"bir ay",MM:"%d ay",y:"bir il",yy:"%d il"},meridiemParse:/gecə|səhər|gündüz|axşam/,isPM:function(a){return/^(gündüz|axşam)$/.test(a)},meridiem:function(a,b,c){return 4>a?"gecə":12>a?"səhər":17>a?"gündüz":"axşam"},ordinalParse:/\d{1,2}-(ıncı|inci|nci|üncü|ncı|uncu)/,ordinal:function(a){if(0===a)// special case for zero
return a+"-ıncı";var b=a%10,c=a%100-b,d=a>=100?100:null;return a+(tg[b]||tg[c]||tg[d])},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("be",{months:{format:"студзеня_лютага_сакавіка_красавіка_траўня_чэрвеня_ліпеня_жніўня_верасня_кастрычніка_лістапада_снежня".split("_"),standalone:"студзень_люты_сакавік_красавік_травень_чэрвень_ліпень_жнівень_верасень_кастрычнік_лістапад_снежань".split("_")},monthsShort:"студ_лют_сак_крас_трав_чэрв_ліп_жнів_вер_каст_ліст_снеж".split("_"),weekdays:{format:"нядзелю_панядзелак_аўторак_сераду_чацвер_пятніцу_суботу".split("_"),standalone:"нядзеля_панядзелак_аўторак_серада_чацвер_пятніца_субота".split("_"),isFormat:/\[ ?[Вв] ?(?:мінулую|наступную)? ?\] ?dddd/},weekdaysShort:"нд_пн_ат_ср_чц_пт_сб".split("_"),weekdaysMin:"нд_пн_ат_ср_чц_пт_сб".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY г.",LLL:"D MMMM YYYY г., HH:mm",LLLL:"dddd, D MMMM YYYY г., HH:mm"},calendar:{sameDay:"[Сёння ў] LT",nextDay:"[Заўтра ў] LT",lastDay:"[Учора ў] LT",nextWeek:function(){return"[У] dddd [ў] LT"},lastWeek:function(){switch(this.day()){case 0:case 3:case 5:case 6:return"[У мінулую] dddd [ў] LT";case 1:case 2:case 4:return"[У мінулы] dddd [ў] LT"}},sameElse:"L"},relativeTime:{future:"праз %s",past:"%s таму",s:"некалькі секунд",m:nd,mm:nd,h:nd,hh:nd,d:"дзень",dd:nd,M:"месяц",MM:nd,y:"год",yy:nd},meridiemParse:/ночы|раніцы|дня|вечара/,isPM:function(a){return/^(дня|вечара)$/.test(a)},meridiem:function(a,b,c){return 4>a?"ночы":12>a?"раніцы":17>a?"дня":"вечара"},ordinalParse:/\d{1,2}-(і|ы|га)/,ordinal:function(a,b){switch(b){case"M":case"d":case"DDD":case"w":case"W":return a%10!==2&&a%10!==3||a%100===12||a%100===13?a+"-ы":a+"-і";case"D":return a+"-га";default:return a}},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("bg",{months:"януари_февруари_март_април_май_юни_юли_август_септември_октомври_ноември_декември".split("_"),monthsShort:"янр_фев_мар_апр_май_юни_юли_авг_сеп_окт_ное_дек".split("_"),weekdays:"неделя_понеделник_вторник_сряда_четвъртък_петък_събота".split("_"),weekdaysShort:"нед_пон_вто_сря_чет_пет_съб".split("_"),weekdaysMin:"нд_пн_вт_ср_чт_пт_сб".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"D.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY H:mm",LLLL:"dddd, D MMMM YYYY H:mm"},calendar:{sameDay:"[Днес в] LT",nextDay:"[Утре в] LT",nextWeek:"dddd [в] LT",lastDay:"[Вчера в] LT",lastWeek:function(){switch(this.day()){case 0:case 3:case 6:return"[В изминалата] dddd [в] LT";case 1:case 2:case 4:case 5:return"[В изминалия] dddd [в] LT"}},sameElse:"L"},relativeTime:{future:"след %s",past:"преди %s",s:"няколко секунди",m:"минута",mm:"%d минути",h:"час",hh:"%d часа",d:"ден",dd:"%d дни",M:"месец",MM:"%d месеца",y:"година",yy:"%d години"},ordinalParse:/\d{1,2}-(ев|ен|ти|ви|ри|ми)/,ordinal:function(a){var b=a%10,c=a%100;return 0===a?a+"-ев":0===c?a+"-ен":c>10&&20>c?a+"-ти":1===b?a+"-ви":2===b?a+"-ри":7===b||8===b?a+"-ми":a+"-ти"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),{1:"১",2:"২",3:"৩",4:"৪",5:"৫",6:"৬",7:"৭",8:"৮",9:"৯",0:"০"}),vg={"১":"1","২":"2","৩":"3","৪":"4","৫":"5","৬":"6","৭":"7","৮":"8","৯":"9","০":"0"},wg=(kg.defineLocale("bn",{months:"জানুয়ারী_ফেবুয়ারী_মার্চ_এপ্রিল_মে_জুন_জুলাই_অগাস্ট_সেপ্টেম্বর_অক্টোবর_নভেম্বর_ডিসেম্বর".split("_"),monthsShort:"জানু_ফেব_মার্চ_এপর_মে_জুন_জুল_অগ_সেপ্ট_অক্টো_নভ_ডিসেম্".split("_"),weekdays:"রবিবার_সোমবার_মঙ্গলবার_বুধবার_বৃহস্পত্তিবার_শুক্রবার_শনিবার".split("_"),weekdaysShort:"রবি_সোম_মঙ্গল_বুধ_বৃহস্পত্তি_শুক্র_শনি".split("_"),weekdaysMin:"রব_সম_মঙ্গ_বু_ব্রিহ_শু_শনি".split("_"),longDateFormat:{LT:"A h:mm সময়",LTS:"A h:mm:ss সময়",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, A h:mm সময়",LLLL:"dddd, D MMMM YYYY, A h:mm সময়"},calendar:{sameDay:"[আজ] LT",nextDay:"[আগামীকাল] LT",nextWeek:"dddd, LT",lastDay:"[গতকাল] LT",lastWeek:"[গত] dddd, LT",sameElse:"L"},relativeTime:{future:"%s পরে",past:"%s আগে",s:"কয়েক সেকেন্ড",m:"এক মিনিট",mm:"%d মিনিট",h:"এক ঘন্টা",hh:"%d ঘন্টা",d:"এক দিন",dd:"%d দিন",M:"এক মাস",MM:"%d মাস",y:"এক বছর",yy:"%d বছর"},preparse:function(a){return a.replace(/[১২৩৪৫৬৭৮৯০]/g,function(a){return vg[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return ug[a]})},meridiemParse:/রাত|সকাল|দুপুর|বিকাল|রাত/,meridiemHour:function(a,b){return 12===a&&(a=0),"রাত"===b&&a>=4||"দুপুর"===b&&5>a||"বিকাল"===b?a+12:a},meridiem:function(a,b,c){return 4>a?"রাত":10>a?"সকাল":17>a?"দুপুর":20>a?"বিকাল":"রাত"},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),{1:"༡",2:"༢",3:"༣",4:"༤",5:"༥",6:"༦",7:"༧",8:"༨",9:"༩",0:"༠"}),xg={"༡":"1","༢":"2","༣":"3","༤":"4","༥":"5","༦":"6","༧":"7","༨":"8","༩":"9","༠":"0"},yg=(kg.defineLocale("bo",{months:"ཟླ་བ་དང་པོ_ཟླ་བ་གཉིས་པ_ཟླ་བ་གསུམ་པ_ཟླ་བ་བཞི་པ_ཟླ་བ་ལྔ་པ_ཟླ་བ་དྲུག་པ_ཟླ་བ་བདུན་པ_ཟླ་བ་བརྒྱད་པ_ཟླ་བ་དགུ་པ_ཟླ་བ་བཅུ་པ_ཟླ་བ་བཅུ་གཅིག་པ_ཟླ་བ་བཅུ་གཉིས་པ".split("_"),monthsShort:"ཟླ་བ་དང་པོ_ཟླ་བ་གཉིས་པ_ཟླ་བ་གསུམ་པ_ཟླ་བ་བཞི་པ_ཟླ་བ་ལྔ་པ_ཟླ་བ་དྲུག་པ_ཟླ་བ་བདུན་པ_ཟླ་བ་བརྒྱད་པ_ཟླ་བ་དགུ་པ_ཟླ་བ་བཅུ་པ_ཟླ་བ་བཅུ་གཅིག་པ_ཟླ་བ་བཅུ་གཉིས་པ".split("_"),weekdays:"གཟའ་ཉི་མ་_གཟའ་ཟླ་བ་_གཟའ་མིག་དམར་_གཟའ་ལྷག་པ་_གཟའ་ཕུར་བུ_གཟའ་པ་སངས་_གཟའ་སྤེན་པ་".split("_"),weekdaysShort:"ཉི་མ་_ཟླ་བ་_མིག་དམར་_ལྷག་པ་_ཕུར་བུ_པ་སངས་_སྤེན་པ་".split("_"),weekdaysMin:"ཉི་མ་_ཟླ་བ་_མིག་དམར་_ལྷག་པ་_ཕུར་བུ_པ་སངས་_སྤེན་པ་".split("_"),longDateFormat:{LT:"A h:mm",LTS:"A h:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, A h:mm",LLLL:"dddd, D MMMM YYYY, A h:mm"},calendar:{sameDay:"[དི་རིང] LT",nextDay:"[སང་ཉིན] LT",nextWeek:"[བདུན་ཕྲག་རྗེས་མ], LT",lastDay:"[ཁ་སང] LT",lastWeek:"[བདུན་ཕྲག་མཐའ་མ] dddd, LT",sameElse:"L"},relativeTime:{future:"%s ལ་",past:"%s སྔན་ལ",s:"ལམ་སང",m:"སྐར་མ་གཅིག",mm:"%d སྐར་མ",h:"ཆུ་ཚོད་གཅིག",hh:"%d ཆུ་ཚོད",d:"ཉིན་གཅིག",dd:"%d ཉིན་",M:"ཟླ་བ་གཅིག",MM:"%d ཟླ་བ",y:"ལོ་གཅིག",yy:"%d ལོ"},preparse:function(a){return a.replace(/[༡༢༣༤༥༦༧༨༩༠]/g,function(a){return xg[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return wg[a]})},meridiemParse:/མཚན་མོ|ཞོགས་ཀས|ཉིན་གུང|དགོང་དག|མཚན་མོ/,meridiemHour:function(a,b){return 12===a&&(a=0),"མཚན་མོ"===b&&a>=4||"ཉིན་གུང"===b&&5>a||"དགོང་དག"===b?a+12:a},meridiem:function(a,b,c){return 4>a?"མཚན་མོ":10>a?"ཞོགས་ཀས":17>a?"ཉིན་གུང":20>a?"དགོང་དག":"མཚན་མོ"},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),kg.defineLocale("br",{months:"Genver_C'hwevrer_Meurzh_Ebrel_Mae_Mezheven_Gouere_Eost_Gwengolo_Here_Du_Kerzu".split("_"),monthsShort:"Gen_C'hwe_Meu_Ebr_Mae_Eve_Gou_Eos_Gwe_Her_Du_Ker".split("_"),weekdays:"Sul_Lun_Meurzh_Merc'her_Yaou_Gwener_Sadorn".split("_"),weekdaysShort:"Sul_Lun_Meu_Mer_Yao_Gwe_Sad".split("_"),weekdaysMin:"Su_Lu_Me_Mer_Ya_Gw_Sa".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"h[e]mm A",LTS:"h[e]mm:ss A",L:"DD/MM/YYYY",LL:"D [a viz] MMMM YYYY",LLL:"D [a viz] MMMM YYYY h[e]mm A",LLLL:"dddd, D [a viz] MMMM YYYY h[e]mm A"},calendar:{sameDay:"[Hiziv da] LT",nextDay:"[Warc'hoazh da] LT",nextWeek:"dddd [da] LT",lastDay:"[Dec'h da] LT",lastWeek:"dddd [paset da] LT",sameElse:"L"},relativeTime:{future:"a-benn %s",past:"%s 'zo",s:"un nebeud segondennoù",m:"ur vunutenn",mm:od,h:"un eur",hh:"%d eur",d:"un devezh",dd:od,M:"ur miz",MM:od,y:"ur bloaz",yy:pd},ordinalParse:/\d{1,2}(añ|vet)/,ordinal:function(a){var b=1===a?"añ":"vet";return a+b},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("bs",{months:"januar_februar_mart_april_maj_juni_juli_august_septembar_oktobar_novembar_decembar".split("_"),monthsShort:"jan._feb._mar._apr._maj._jun._jul._aug._sep._okt._nov._dec.".split("_"),monthsParseExact:!0,weekdays:"nedjelja_ponedjeljak_utorak_srijeda_četvrtak_petak_subota".split("_"),weekdaysShort:"ned._pon._uto._sri._čet._pet._sub.".split("_"),weekdaysMin:"ne_po_ut_sr_če_pe_su".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD. MM. YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd, D. MMMM YYYY H:mm"},calendar:{sameDay:"[danas u] LT",nextDay:"[sutra u] LT",nextWeek:function(){switch(this.day()){case 0:return"[u] [nedjelju] [u] LT";case 3:return"[u] [srijedu] [u] LT";case 6:return"[u] [subotu] [u] LT";case 1:case 2:case 4:case 5:return"[u] dddd [u] LT"}},lastDay:"[jučer u] LT",lastWeek:function(){switch(this.day()){case 0:case 3:return"[prošlu] dddd [u] LT";case 6:return"[prošle] [subote] [u] LT";case 1:case 2:case 4:case 5:return"[prošli] dddd [u] LT"}},sameElse:"L"},relativeTime:{future:"za %s",past:"prije %s",s:"par sekundi",m:td,mm:td,h:td,hh:td,d:"dan",dd:td,M:"mjesec",MM:td,y:"godinu",yy:td},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("ca",{months:"gener_febrer_març_abril_maig_juny_juliol_agost_setembre_octubre_novembre_desembre".split("_"),monthsShort:"gen._febr._mar._abr._mai._jun._jul._ag._set._oct._nov._des.".split("_"),monthsParseExact:!0,weekdays:"diumenge_dilluns_dimarts_dimecres_dijous_divendres_dissabte".split("_"),weekdaysShort:"dg._dl._dt._dc._dj._dv._ds.".split("_"),weekdaysMin:"Dg_Dl_Dt_Dc_Dj_Dv_Ds".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY H:mm",LLLL:"dddd D MMMM YYYY H:mm"},calendar:{sameDay:function(){return"[avui a "+(1!==this.hours()?"les":"la")+"] LT"},nextDay:function(){return"[demà a "+(1!==this.hours()?"les":"la")+"] LT"},nextWeek:function(){return"dddd [a "+(1!==this.hours()?"les":"la")+"] LT"},lastDay:function(){return"[ahir a "+(1!==this.hours()?"les":"la")+"] LT"},lastWeek:function(){return"[el] dddd [passat a "+(1!==this.hours()?"les":"la")+"] LT"},sameElse:"L"},relativeTime:{future:"en %s",past:"fa %s",s:"uns segons",m:"un minut",mm:"%d minuts",h:"una hora",hh:"%d hores",d:"un dia",dd:"%d dies",M:"un mes",MM:"%d mesos",y:"un any",yy:"%d anys"},ordinalParse:/\d{1,2}(r|n|t|è|a)/,ordinal:function(a,b){var c=1===a?"r":2===a?"n":3===a?"r":4===a?"t":"è";return"w"!==b&&"W"!==b||(c="a"),a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),"leden_únor_březen_duben_květen_červen_červenec_srpen_září_říjen_listopad_prosinec".split("_")),zg="led_úno_bře_dub_kvě_čvn_čvc_srp_zář_říj_lis_pro".split("_"),Ag=(kg.defineLocale("cs",{months:yg,monthsShort:zg,monthsParse:function(a,b){var c,d=[];for(c=0;12>c;c++)
// use custom parser to solve problem with July (červenec)
d[c]=new RegExp("^"+a[c]+"$|^"+b[c]+"$","i");return d}(yg,zg),shortMonthsParse:function(a){var b,c=[];for(b=0;12>b;b++)c[b]=new RegExp("^"+a[b]+"$","i");return c}(zg),longMonthsParse:function(a){var b,c=[];for(b=0;12>b;b++)c[b]=new RegExp("^"+a[b]+"$","i");return c}(yg),weekdays:"neděle_pondělí_úterý_středa_čtvrtek_pátek_sobota".split("_"),weekdaysShort:"ne_po_út_st_čt_pá_so".split("_"),weekdaysMin:"ne_po_út_st_čt_pá_so".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd D. MMMM YYYY H:mm",l:"D. M. YYYY"},calendar:{sameDay:"[dnes v] LT",nextDay:"[zítra v] LT",nextWeek:function(){switch(this.day()){case 0:return"[v neděli v] LT";case 1:case 2:return"[v] dddd [v] LT";case 3:return"[ve středu v] LT";case 4:return"[ve čtvrtek v] LT";case 5:return"[v pátek v] LT";case 6:return"[v sobotu v] LT"}},lastDay:"[včera v] LT",lastWeek:function(){switch(this.day()){case 0:return"[minulou neděli v] LT";case 1:case 2:return"[minulé] dddd [v] LT";case 3:return"[minulou středu v] LT";case 4:case 5:return"[minulý] dddd [v] LT";case 6:return"[minulou sobotu v] LT"}},sameElse:"L"},relativeTime:{future:"za %s",past:"před %s",s:vd,m:vd,mm:vd,h:vd,hh:vd,d:vd,dd:vd,M:vd,MM:vd,y:vd,yy:vd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("cv",{months:"кӑрлач_нарӑс_пуш_ака_май_ҫӗртме_утӑ_ҫурла_авӑн_юпа_чӳк_раштав".split("_"),monthsShort:"кӑр_нар_пуш_ака_май_ҫӗр_утӑ_ҫур_авн_юпа_чӳк_раш".split("_"),weekdays:"вырсарникун_тунтикун_ытларикун_юнкун_кӗҫнерникун_эрнекун_шӑматкун".split("_"),weekdaysShort:"выр_тун_ытл_юн_кӗҫ_эрн_шӑм".split("_"),weekdaysMin:"вр_тн_ыт_юн_кҫ_эр_шм".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD-MM-YYYY",LL:"YYYY [ҫулхи] MMMM [уйӑхӗн] D[-мӗшӗ]",LLL:"YYYY [ҫулхи] MMMM [уйӑхӗн] D[-мӗшӗ], HH:mm",LLLL:"dddd, YYYY [ҫулхи] MMMM [уйӑхӗн] D[-мӗшӗ], HH:mm"},calendar:{sameDay:"[Паян] LT [сехетре]",nextDay:"[Ыран] LT [сехетре]",lastDay:"[Ӗнер] LT [сехетре]",nextWeek:"[Ҫитес] dddd LT [сехетре]",lastWeek:"[Иртнӗ] dddd LT [сехетре]",sameElse:"L"},relativeTime:{future:function(a){var b=/сехет$/i.exec(a)?"рен":/ҫул$/i.exec(a)?"тан":"ран";return a+b},past:"%s каялла",s:"пӗр-ик ҫеккунт",m:"пӗр минут",mm:"%d минут",h:"пӗр сехет",hh:"%d сехет",d:"пӗр кун",dd:"%d кун",M:"пӗр уйӑх",MM:"%d уйӑх",y:"пӗр ҫул",yy:"%d ҫул"},ordinalParse:/\d{1,2}-мӗш/,ordinal:"%d-мӗш",week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("cy",{months:"Ionawr_Chwefror_Mawrth_Ebrill_Mai_Mehefin_Gorffennaf_Awst_Medi_Hydref_Tachwedd_Rhagfyr".split("_"),monthsShort:"Ion_Chwe_Maw_Ebr_Mai_Meh_Gor_Aws_Med_Hyd_Tach_Rhag".split("_"),weekdays:"Dydd Sul_Dydd Llun_Dydd Mawrth_Dydd Mercher_Dydd Iau_Dydd Gwener_Dydd Sadwrn".split("_"),weekdaysShort:"Sul_Llun_Maw_Mer_Iau_Gwe_Sad".split("_"),weekdaysMin:"Su_Ll_Ma_Me_Ia_Gw_Sa".split("_"),weekdaysParseExact:!0,
// time formats are the same as en-gb
longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Heddiw am] LT",nextDay:"[Yfory am] LT",nextWeek:"dddd [am] LT",lastDay:"[Ddoe am] LT",lastWeek:"dddd [diwethaf am] LT",sameElse:"L"},relativeTime:{future:"mewn %s",past:"%s yn ôl",s:"ychydig eiliadau",m:"munud",mm:"%d munud",h:"awr",hh:"%d awr",d:"diwrnod",dd:"%d diwrnod",M:"mis",MM:"%d mis",y:"blwyddyn",yy:"%d flynedd"},ordinalParse:/\d{1,2}(fed|ain|af|il|ydd|ed|eg)/,
// traditional ordinal numbers above 31 are not commonly used in colloquial Welsh
ordinal:function(a){var b=a,c="",d=["","af","il","ydd","ydd","ed","ed","ed","fed","fed","fed",// 1af to 10fed
"eg","fed","eg","eg","fed","eg","eg","fed","eg","fed"];return b>20?c=40===b||50===b||60===b||80===b||100===b?"fed":"ain":b>0&&(c=d[b]),a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("da",{months:"januar_februar_marts_april_maj_juni_juli_august_september_oktober_november_december".split("_"),monthsShort:"jan_feb_mar_apr_maj_jun_jul_aug_sep_okt_nov_dec".split("_"),weekdays:"søndag_mandag_tirsdag_onsdag_torsdag_fredag_lørdag".split("_"),weekdaysShort:"søn_man_tir_ons_tor_fre_lør".split("_"),weekdaysMin:"sø_ma_ti_on_to_fr_lø".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY HH:mm",LLLL:"dddd [d.] D. MMMM YYYY HH:mm"},calendar:{sameDay:"[I dag kl.] LT",nextDay:"[I morgen kl.] LT",nextWeek:"dddd [kl.] LT",lastDay:"[I går kl.] LT",lastWeek:"[sidste] dddd [kl] LT",sameElse:"L"},relativeTime:{future:"om %s",past:"%s siden",s:"få sekunder",m:"et minut",mm:"%d minutter",h:"en time",hh:"%d timer",d:"en dag",dd:"%d dage",M:"en måned",MM:"%d måneder",y:"et år",yy:"%d år"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("de-at",{months:"Jänner_Februar_März_April_Mai_Juni_Juli_August_September_Oktober_November_Dezember".split("_"),monthsShort:"Jän._Febr._Mrz._Apr._Mai_Jun._Jul._Aug._Sept._Okt._Nov._Dez.".split("_"),monthsParseExact:!0,weekdays:"Sonntag_Montag_Dienstag_Mittwoch_Donnerstag_Freitag_Samstag".split("_"),weekdaysShort:"So._Mo._Di._Mi._Do._Fr._Sa.".split("_"),weekdaysMin:"So_Mo_Di_Mi_Do_Fr_Sa".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY HH:mm",LLLL:"dddd, D. MMMM YYYY HH:mm"},calendar:{sameDay:"[heute um] LT [Uhr]",sameElse:"L",nextDay:"[morgen um] LT [Uhr]",nextWeek:"dddd [um] LT [Uhr]",lastDay:"[gestern um] LT [Uhr]",lastWeek:"[letzten] dddd [um] LT [Uhr]"},relativeTime:{future:"in %s",past:"vor %s",s:"ein paar Sekunden",m:wd,mm:"%d Minuten",h:wd,hh:"%d Stunden",d:wd,dd:wd,M:wd,MM:wd,y:wd,yy:wd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("de",{months:"Januar_Februar_März_April_Mai_Juni_Juli_August_September_Oktober_November_Dezember".split("_"),monthsShort:"Jan._Febr._Mrz._Apr._Mai_Jun._Jul._Aug._Sept._Okt._Nov._Dez.".split("_"),monthsParseExact:!0,weekdays:"Sonntag_Montag_Dienstag_Mittwoch_Donnerstag_Freitag_Samstag".split("_"),weekdaysShort:"So._Mo._Di._Mi._Do._Fr._Sa.".split("_"),weekdaysMin:"So_Mo_Di_Mi_Do_Fr_Sa".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY HH:mm",LLLL:"dddd, D. MMMM YYYY HH:mm"},calendar:{sameDay:"[heute um] LT [Uhr]",sameElse:"L",nextDay:"[morgen um] LT [Uhr]",nextWeek:"dddd [um] LT [Uhr]",lastDay:"[gestern um] LT [Uhr]",lastWeek:"[letzten] dddd [um] LT [Uhr]"},relativeTime:{future:"in %s",past:"vor %s",s:"ein paar Sekunden",m:xd,mm:"%d Minuten",h:xd,hh:"%d Stunden",d:xd,dd:xd,M:xd,MM:xd,y:xd,yy:xd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),["ޖެނުއަރީ","ފެބްރުއަރީ","މާރިޗު","އޭޕްރީލު","މޭ","ޖޫން","ޖުލައި","އޯގަސްޓު","ސެޕްޓެމްބަރު","އޮކްޓޯބަރު","ނޮވެމްބަރު","ޑިސެމްބަރު"]),Bg=["އާދިއްތަ","ހޯމަ","އަންގާރަ","ބުދަ","ބުރާސްފަތި","ހުކުރު","ހޮނިހިރު"],Cg=(kg.defineLocale("dv",{months:Ag,monthsShort:Ag,weekdays:Bg,weekdaysShort:Bg,weekdaysMin:"އާދި_ހޯމަ_އަން_ބުދަ_ބުރާ_ހުކު_ހޮނި".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"D/M/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},meridiemParse:/މކ|މފ/,isPM:function(a){return"މފ"===a},meridiem:function(a,b,c){return 12>a?"މކ":"މފ"},calendar:{sameDay:"[މިއަދު] LT",nextDay:"[މާދަމާ] LT",nextWeek:"dddd LT",lastDay:"[އިއްޔެ] LT",lastWeek:"[ފާއިތުވި] dddd LT",sameElse:"L"},relativeTime:{future:"ތެރޭގައި %s",past:"ކުރިން %s",s:"ސިކުންތުކޮޅެއް",m:"މިނިޓެއް",mm:"މިނިޓު %d",h:"ގަޑިއިރެއް",hh:"ގަޑިއިރު %d",d:"ދުވަހެއް",dd:"ދުވަސް %d",M:"މަހެއް",MM:"މަސް %d",y:"އަހަރެއް",yy:"އަހަރު %d"},preparse:function(a){return a.replace(/،/g,",")},postformat:function(a){return a.replace(/,/g,"،")},week:{dow:7,// Sunday is the first day of the week.
doy:12}}),kg.defineLocale("el",{monthsNominativeEl:"Ιανουάριος_Φεβρουάριος_Μάρτιος_Απρίλιος_Μάιος_Ιούνιος_Ιούλιος_Αύγουστος_Σεπτέμβριος_Οκτώβριος_Νοέμβριος_Δεκέμβριος".split("_"),monthsGenitiveEl:"Ιανουαρίου_Φεβρουαρίου_Μαρτίου_Απριλίου_Μαΐου_Ιουνίου_Ιουλίου_Αυγούστου_Σεπτεμβρίου_Οκτωβρίου_Νοεμβρίου_Δεκεμβρίου".split("_"),months:function(a,b){return/D/.test(b.substring(0,b.indexOf("MMMM")))?this._monthsGenitiveEl[a.month()]:this._monthsNominativeEl[a.month()]},monthsShort:"Ιαν_Φεβ_Μαρ_Απρ_Μαϊ_Ιουν_Ιουλ_Αυγ_Σεπ_Οκτ_Νοε_Δεκ".split("_"),weekdays:"Κυριακή_Δευτέρα_Τρίτη_Τετάρτη_Πέμπτη_Παρασκευή_Σάββατο".split("_"),weekdaysShort:"Κυρ_Δευ_Τρι_Τετ_Πεμ_Παρ_Σαβ".split("_"),weekdaysMin:"Κυ_Δε_Τρ_Τε_Πε_Πα_Σα".split("_"),meridiem:function(a,b,c){return a>11?c?"μμ":"ΜΜ":c?"πμ":"ΠΜ"},isPM:function(a){return"μ"===(a+"").toLowerCase()[0]},meridiemParse:/[ΠΜ]\.?Μ?\.?/i,longDateFormat:{LT:"h:mm A",LTS:"h:mm:ss A",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY h:mm A",LLLL:"dddd, D MMMM YYYY h:mm A"},calendarEl:{sameDay:"[Σήμερα {}] LT",nextDay:"[Αύριο {}] LT",nextWeek:"dddd [{}] LT",lastDay:"[Χθες {}] LT",lastWeek:function(){switch(this.day()){case 6:return"[το προηγούμενο] dddd [{}] LT";default:return"[την προηγούμενη] dddd [{}] LT"}},sameElse:"L"},calendar:function(a,b){var c=this._calendarEl[a],d=b&&b.hours();return y(c)&&(c=c.apply(b)),c.replace("{}",d%12===1?"στη":"στις")},relativeTime:{future:"σε %s",past:"%s πριν",s:"λίγα δευτερόλεπτα",m:"ένα λεπτό",mm:"%d λεπτά",h:"μία ώρα",hh:"%d ώρες",d:"μία μέρα",dd:"%d μέρες",M:"ένας μήνας",MM:"%d μήνες",y:"ένας χρόνος",yy:"%d χρόνια"},ordinalParse:/\d{1,2}η/,ordinal:"%dη",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("en-au",{months:"January_February_March_April_May_June_July_August_September_October_November_December".split("_"),monthsShort:"Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),weekdays:"Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),weekdaysShort:"Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),weekdaysMin:"Su_Mo_Tu_We_Th_Fr_Sa".split("_"),longDateFormat:{LT:"h:mm A",LTS:"h:mm:ss A",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY h:mm A",LLLL:"dddd, D MMMM YYYY h:mm A"},calendar:{sameDay:"[Today at] LT",nextDay:"[Tomorrow at] LT",nextWeek:"dddd [at] LT",lastDay:"[Yesterday at] LT",lastWeek:"[Last] dddd [at] LT",sameElse:"L"},relativeTime:{future:"in %s",past:"%s ago",s:"a few seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},ordinalParse:/\d{1,2}(st|nd|rd|th)/,ordinal:function(a){var b=a%10,c=1===~~(a%100/10)?"th":1===b?"st":2===b?"nd":3===b?"rd":"th";return a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("en-ca",{months:"January_February_March_April_May_June_July_August_September_October_November_December".split("_"),monthsShort:"Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),weekdays:"Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),weekdaysShort:"Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),weekdaysMin:"Su_Mo_Tu_We_Th_Fr_Sa".split("_"),longDateFormat:{LT:"h:mm A",LTS:"h:mm:ss A",L:"YYYY-MM-DD",LL:"MMMM D, YYYY",LLL:"MMMM D, YYYY h:mm A",LLLL:"dddd, MMMM D, YYYY h:mm A"},calendar:{sameDay:"[Today at] LT",nextDay:"[Tomorrow at] LT",nextWeek:"dddd [at] LT",lastDay:"[Yesterday at] LT",lastWeek:"[Last] dddd [at] LT",sameElse:"L"},relativeTime:{future:"in %s",past:"%s ago",s:"a few seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},ordinalParse:/\d{1,2}(st|nd|rd|th)/,ordinal:function(a){var b=a%10,c=1===~~(a%100/10)?"th":1===b?"st":2===b?"nd":3===b?"rd":"th";return a+c}}),kg.defineLocale("en-gb",{months:"January_February_March_April_May_June_July_August_September_October_November_December".split("_"),monthsShort:"Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),weekdays:"Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),weekdaysShort:"Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),weekdaysMin:"Su_Mo_Tu_We_Th_Fr_Sa".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Today at] LT",nextDay:"[Tomorrow at] LT",nextWeek:"dddd [at] LT",lastDay:"[Yesterday at] LT",lastWeek:"[Last] dddd [at] LT",sameElse:"L"},relativeTime:{future:"in %s",past:"%s ago",s:"a few seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},ordinalParse:/\d{1,2}(st|nd|rd|th)/,ordinal:function(a){var b=a%10,c=1===~~(a%100/10)?"th":1===b?"st":2===b?"nd":3===b?"rd":"th";return a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("en-ie",{months:"January_February_March_April_May_June_July_August_September_October_November_December".split("_"),monthsShort:"Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),weekdays:"Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),weekdaysShort:"Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),weekdaysMin:"Su_Mo_Tu_We_Th_Fr_Sa".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD-MM-YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[Today at] LT",nextDay:"[Tomorrow at] LT",nextWeek:"dddd [at] LT",lastDay:"[Yesterday at] LT",lastWeek:"[Last] dddd [at] LT",sameElse:"L"},relativeTime:{future:"in %s",past:"%s ago",s:"a few seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},ordinalParse:/\d{1,2}(st|nd|rd|th)/,ordinal:function(a){var b=a%10,c=1===~~(a%100/10)?"th":1===b?"st":2===b?"nd":3===b?"rd":"th";return a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("en-nz",{months:"January_February_March_April_May_June_July_August_September_October_November_December".split("_"),monthsShort:"Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec".split("_"),weekdays:"Sunday_Monday_Tuesday_Wednesday_Thursday_Friday_Saturday".split("_"),weekdaysShort:"Sun_Mon_Tue_Wed_Thu_Fri_Sat".split("_"),weekdaysMin:"Su_Mo_Tu_We_Th_Fr_Sa".split("_"),longDateFormat:{LT:"h:mm A",LTS:"h:mm:ss A",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY h:mm A",LLLL:"dddd, D MMMM YYYY h:mm A"},calendar:{sameDay:"[Today at] LT",nextDay:"[Tomorrow at] LT",nextWeek:"dddd [at] LT",lastDay:"[Yesterday at] LT",lastWeek:"[Last] dddd [at] LT",sameElse:"L"},relativeTime:{future:"in %s",past:"%s ago",s:"a few seconds",m:"a minute",mm:"%d minutes",h:"an hour",hh:"%d hours",d:"a day",dd:"%d days",M:"a month",MM:"%d months",y:"a year",yy:"%d years"},ordinalParse:/\d{1,2}(st|nd|rd|th)/,ordinal:function(a){var b=a%10,c=1===~~(a%100/10)?"th":1===b?"st":2===b?"nd":3===b?"rd":"th";return a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("eo",{months:"januaro_februaro_marto_aprilo_majo_junio_julio_aŭgusto_septembro_oktobro_novembro_decembro".split("_"),monthsShort:"jan_feb_mar_apr_maj_jun_jul_aŭg_sep_okt_nov_dec".split("_"),weekdays:"Dimanĉo_Lundo_Mardo_Merkredo_Ĵaŭdo_Vendredo_Sabato".split("_"),weekdaysShort:"Dim_Lun_Mard_Merk_Ĵaŭ_Ven_Sab".split("_"),weekdaysMin:"Di_Lu_Ma_Me_Ĵa_Ve_Sa".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"YYYY-MM-DD",LL:"D[-an de] MMMM, YYYY",LLL:"D[-an de] MMMM, YYYY HH:mm",LLLL:"dddd, [la] D[-an de] MMMM, YYYY HH:mm"},meridiemParse:/[ap]\.t\.m/i,isPM:function(a){return"p"===a.charAt(0).toLowerCase()},meridiem:function(a,b,c){return a>11?c?"p.t.m.":"P.T.M.":c?"a.t.m.":"A.T.M."},calendar:{sameDay:"[Hodiaŭ je] LT",nextDay:"[Morgaŭ je] LT",nextWeek:"dddd [je] LT",lastDay:"[Hieraŭ je] LT",lastWeek:"[pasinta] dddd [je] LT",sameElse:"L"},relativeTime:{future:"je %s",past:"antaŭ %s",s:"sekundoj",m:"minuto",mm:"%d minutoj",h:"horo",hh:"%d horoj",d:"tago",//ne 'diurno', ĉar estas uzita por proksimumo
dd:"%d tagoj",M:"monato",MM:"%d monatoj",y:"jaro",yy:"%d jaroj"},ordinalParse:/\d{1,2}a/,ordinal:"%da",week:{dow:1,// Monday is the first day of the week.
doy:7}}),"ene._feb._mar._abr._may._jun._jul._ago._sep._oct._nov._dic.".split("_")),Dg="ene_feb_mar_abr_may_jun_jul_ago_sep_oct_nov_dic".split("_"),Eg=(kg.defineLocale("es-do",{months:"enero_febrero_marzo_abril_mayo_junio_julio_agosto_septiembre_octubre_noviembre_diciembre".split("_"),monthsShort:function(a,b){return/-MMM-/.test(b)?Dg[a.month()]:Cg[a.month()]},monthsParseExact:!0,weekdays:"domingo_lunes_martes_miércoles_jueves_viernes_sábado".split("_"),weekdaysShort:"dom._lun._mar._mié._jue._vie._sáb.".split("_"),weekdaysMin:"do_lu_ma_mi_ju_vi_sá".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"h:mm A",LTS:"h:mm:ss A",L:"DD/MM/YYYY",LL:"D [de] MMMM [de] YYYY",LLL:"D [de] MMMM [de] YYYY h:mm A",LLLL:"dddd, D [de] MMMM [de] YYYY h:mm A"},calendar:{sameDay:function(){return"[hoy a la"+(1!==this.hours()?"s":"")+"] LT"},nextDay:function(){return"[mañana a la"+(1!==this.hours()?"s":"")+"] LT"},nextWeek:function(){return"dddd [a la"+(1!==this.hours()?"s":"")+"] LT"},lastDay:function(){return"[ayer a la"+(1!==this.hours()?"s":"")+"] LT"},lastWeek:function(){return"[el] dddd [pasado a la"+(1!==this.hours()?"s":"")+"] LT"},sameElse:"L"},relativeTime:{future:"en %s",past:"hace %s",s:"unos segundos",m:"un minuto",mm:"%d minutos",h:"una hora",hh:"%d horas",d:"un día",dd:"%d días",M:"un mes",MM:"%d meses",y:"un año",yy:"%d años"},ordinalParse:/\d{1,2}º/,ordinal:"%dº",week:{dow:1,// Monday is the first day of the week.
doy:4}}),"ene._feb._mar._abr._may._jun._jul._ago._sep._oct._nov._dic.".split("_")),Fg="ene_feb_mar_abr_may_jun_jul_ago_sep_oct_nov_dic".split("_"),Gg=(kg.defineLocale("es",{months:"enero_febrero_marzo_abril_mayo_junio_julio_agosto_septiembre_octubre_noviembre_diciembre".split("_"),monthsShort:function(a,b){return/-MMM-/.test(b)?Fg[a.month()]:Eg[a.month()]},monthsParseExact:!0,weekdays:"domingo_lunes_martes_miércoles_jueves_viernes_sábado".split("_"),weekdaysShort:"dom._lun._mar._mié._jue._vie._sáb.".split("_"),weekdaysMin:"do_lu_ma_mi_ju_vi_sá".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD/MM/YYYY",LL:"D [de] MMMM [de] YYYY",LLL:"D [de] MMMM [de] YYYY H:mm",LLLL:"dddd, D [de] MMMM [de] YYYY H:mm"},calendar:{sameDay:function(){return"[hoy a la"+(1!==this.hours()?"s":"")+"] LT"},nextDay:function(){return"[mañana a la"+(1!==this.hours()?"s":"")+"] LT"},nextWeek:function(){return"dddd [a la"+(1!==this.hours()?"s":"")+"] LT"},lastDay:function(){return"[ayer a la"+(1!==this.hours()?"s":"")+"] LT"},lastWeek:function(){return"[el] dddd [pasado a la"+(1!==this.hours()?"s":"")+"] LT"},sameElse:"L"},relativeTime:{future:"en %s",past:"hace %s",s:"unos segundos",m:"un minuto",mm:"%d minutos",h:"una hora",hh:"%d horas",d:"un día",dd:"%d días",M:"un mes",MM:"%d meses",y:"un año",yy:"%d años"},ordinalParse:/\d{1,2}º/,ordinal:"%dº",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("et",{months:"jaanuar_veebruar_märts_aprill_mai_juuni_juuli_august_september_oktoober_november_detsember".split("_"),monthsShort:"jaan_veebr_märts_apr_mai_juuni_juuli_aug_sept_okt_nov_dets".split("_"),weekdays:"pühapäev_esmaspäev_teisipäev_kolmapäev_neljapäev_reede_laupäev".split("_"),weekdaysShort:"P_E_T_K_N_R_L".split("_"),weekdaysMin:"P_E_T_K_N_R_L".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd, D. MMMM YYYY H:mm"},calendar:{sameDay:"[Täna,] LT",nextDay:"[Homme,] LT",nextWeek:"[Järgmine] dddd LT",lastDay:"[Eile,] LT",lastWeek:"[Eelmine] dddd LT",sameElse:"L"},relativeTime:{future:"%s pärast",past:"%s tagasi",s:yd,m:yd,mm:yd,h:yd,hh:yd,d:yd,dd:"%d päeva",M:yd,MM:yd,y:yd,yy:yd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("eu",{months:"urtarrila_otsaila_martxoa_apirila_maiatza_ekaina_uztaila_abuztua_iraila_urria_azaroa_abendua".split("_"),monthsShort:"urt._ots._mar._api._mai._eka._uzt._abu._ira._urr._aza._abe.".split("_"),monthsParseExact:!0,weekdays:"igandea_astelehena_asteartea_asteazkena_osteguna_ostirala_larunbata".split("_"),weekdaysShort:"ig._al._ar._az._og._ol._lr.".split("_"),weekdaysMin:"ig_al_ar_az_og_ol_lr".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"YYYY-MM-DD",LL:"YYYY[ko] MMMM[ren] D[a]",LLL:"YYYY[ko] MMMM[ren] D[a] HH:mm",LLLL:"dddd, YYYY[ko] MMMM[ren] D[a] HH:mm",l:"YYYY-M-D",ll:"YYYY[ko] MMM D[a]",lll:"YYYY[ko] MMM D[a] HH:mm",llll:"ddd, YYYY[ko] MMM D[a] HH:mm"},calendar:{sameDay:"[gaur] LT[etan]",nextDay:"[bihar] LT[etan]",nextWeek:"dddd LT[etan]",lastDay:"[atzo] LT[etan]",lastWeek:"[aurreko] dddd LT[etan]",sameElse:"L"},relativeTime:{future:"%s barru",past:"duela %s",s:"segundo batzuk",m:"minutu bat",mm:"%d minutu",h:"ordu bat",hh:"%d ordu",d:"egun bat",dd:"%d egun",M:"hilabete bat",MM:"%d hilabete",y:"urte bat",yy:"%d urte"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),{1:"۱",2:"۲",3:"۳",4:"۴",5:"۵",6:"۶",7:"۷",8:"۸",9:"۹",0:"۰"}),Hg={"۱":"1","۲":"2","۳":"3","۴":"4","۵":"5","۶":"6","۷":"7","۸":"8","۹":"9","۰":"0"},Ig=(kg.defineLocale("fa",{months:"ژانویه_فوریه_مارس_آوریل_مه_ژوئن_ژوئیه_اوت_سپتامبر_اکتبر_نوامبر_دسامبر".split("_"),monthsShort:"ژانویه_فوریه_مارس_آوریل_مه_ژوئن_ژوئیه_اوت_سپتامبر_اکتبر_نوامبر_دسامبر".split("_"),weekdays:"یک‌شنبه_دوشنبه_سه‌شنبه_چهارشنبه_پنج‌شنبه_جمعه_شنبه".split("_"),weekdaysShort:"یک‌شنبه_دوشنبه_سه‌شنبه_چهارشنبه_پنج‌شنبه_جمعه_شنبه".split("_"),weekdaysMin:"ی_د_س_چ_پ_ج_ش".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},meridiemParse:/قبل از ظهر|بعد از ظهر/,isPM:function(a){return/بعد از ظهر/.test(a)},meridiem:function(a,b,c){return 12>a?"قبل از ظهر":"بعد از ظهر"},calendar:{sameDay:"[امروز ساعت] LT",nextDay:"[فردا ساعت] LT",nextWeek:"dddd [ساعت] LT",lastDay:"[دیروز ساعت] LT",lastWeek:"dddd [پیش] [ساعت] LT",sameElse:"L"},relativeTime:{future:"در %s",past:"%s پیش",s:"چندین ثانیه",m:"یک دقیقه",mm:"%d دقیقه",h:"یک ساعت",hh:"%d ساعت",d:"یک روز",dd:"%d روز",M:"یک ماه",MM:"%d ماه",y:"یک سال",yy:"%d سال"},preparse:function(a){return a.replace(/[۰-۹]/g,function(a){return Hg[a]}).replace(/،/g,",")},postformat:function(a){return a.replace(/\d/g,function(a){return Gg[a]}).replace(/,/g,"،")},ordinalParse:/\d{1,2}م/,ordinal:"%dم",week:{dow:6,// Saturday is the first day of the week.
doy:12}}),"nolla yksi kaksi kolme neljä viisi kuusi seitsemän kahdeksan yhdeksän".split(" ")),Jg=["nolla","yhden","kahden","kolmen","neljän","viiden","kuuden",Ig[7],Ig[8],Ig[9]],Kg=(kg.defineLocale("fi",{months:"tammikuu_helmikuu_maaliskuu_huhtikuu_toukokuu_kesäkuu_heinäkuu_elokuu_syyskuu_lokakuu_marraskuu_joulukuu".split("_"),monthsShort:"tammi_helmi_maalis_huhti_touko_kesä_heinä_elo_syys_loka_marras_joulu".split("_"),weekdays:"sunnuntai_maanantai_tiistai_keskiviikko_torstai_perjantai_lauantai".split("_"),weekdaysShort:"su_ma_ti_ke_to_pe_la".split("_"),weekdaysMin:"su_ma_ti_ke_to_pe_la".split("_"),longDateFormat:{LT:"HH.mm",LTS:"HH.mm.ss",L:"DD.MM.YYYY",LL:"Do MMMM[ta] YYYY",LLL:"Do MMMM[ta] YYYY, [klo] HH.mm",LLLL:"dddd, Do MMMM[ta] YYYY, [klo] HH.mm",l:"D.M.YYYY",ll:"Do MMM YYYY",lll:"Do MMM YYYY, [klo] HH.mm",llll:"ddd, Do MMM YYYY, [klo] HH.mm"},calendar:{sameDay:"[tänään] [klo] LT",nextDay:"[huomenna] [klo] LT",nextWeek:"dddd [klo] LT",lastDay:"[eilen] [klo] LT",lastWeek:"[viime] dddd[na] [klo] LT",sameElse:"L"},relativeTime:{future:"%s päästä",past:"%s sitten",s:zd,m:zd,mm:zd,h:zd,hh:zd,d:zd,dd:zd,M:zd,MM:zd,y:zd,yy:zd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("fo",{months:"januar_februar_mars_apríl_mai_juni_juli_august_september_oktober_november_desember".split("_"),monthsShort:"jan_feb_mar_apr_mai_jun_jul_aug_sep_okt_nov_des".split("_"),weekdays:"sunnudagur_mánadagur_týsdagur_mikudagur_hósdagur_fríggjadagur_leygardagur".split("_"),weekdaysShort:"sun_mán_týs_mik_hós_frí_ley".split("_"),weekdaysMin:"su_má_tý_mi_hó_fr_le".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D. MMMM, YYYY HH:mm"},calendar:{sameDay:"[Í dag kl.] LT",nextDay:"[Í morgin kl.] LT",nextWeek:"dddd [kl.] LT",lastDay:"[Í gjár kl.] LT",lastWeek:"[síðstu] dddd [kl] LT",sameElse:"L"},relativeTime:{future:"um %s",past:"%s síðani",s:"fá sekund",m:"ein minutt",mm:"%d minuttir",h:"ein tími",hh:"%d tímar",d:"ein dagur",dd:"%d dagar",M:"ein mánaði",MM:"%d mánaðir",y:"eitt ár",yy:"%d ár"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("fr-ca",{months:"janvier_février_mars_avril_mai_juin_juillet_août_septembre_octobre_novembre_décembre".split("_"),monthsShort:"janv._févr._mars_avr._mai_juin_juil._août_sept._oct._nov._déc.".split("_"),monthsParseExact:!0,weekdays:"dimanche_lundi_mardi_mercredi_jeudi_vendredi_samedi".split("_"),weekdaysShort:"dim._lun._mar._mer._jeu._ven._sam.".split("_"),weekdaysMin:"Di_Lu_Ma_Me_Je_Ve_Sa".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"YYYY-MM-DD",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[Aujourd'hui à] LT",nextDay:"[Demain à] LT",nextWeek:"dddd [à] LT",lastDay:"[Hier à] LT",lastWeek:"dddd [dernier à] LT",sameElse:"L"},relativeTime:{future:"dans %s",past:"il y a %s",s:"quelques secondes",m:"une minute",mm:"%d minutes",h:"une heure",hh:"%d heures",d:"un jour",dd:"%d jours",M:"un mois",MM:"%d mois",y:"un an",yy:"%d ans"},ordinalParse:/\d{1,2}(er|e)/,ordinal:function(a){return a+(1===a?"er":"e")}}),kg.defineLocale("fr-ch",{months:"janvier_février_mars_avril_mai_juin_juillet_août_septembre_octobre_novembre_décembre".split("_"),monthsShort:"janv._févr._mars_avr._mai_juin_juil._août_sept._oct._nov._déc.".split("_"),monthsParseExact:!0,weekdays:"dimanche_lundi_mardi_mercredi_jeudi_vendredi_samedi".split("_"),weekdaysShort:"dim._lun._mar._mer._jeu._ven._sam.".split("_"),weekdaysMin:"Di_Lu_Ma_Me_Je_Ve_Sa".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[Aujourd'hui à] LT",nextDay:"[Demain à] LT",nextWeek:"dddd [à] LT",lastDay:"[Hier à] LT",lastWeek:"dddd [dernier à] LT",sameElse:"L"},relativeTime:{future:"dans %s",past:"il y a %s",s:"quelques secondes",m:"une minute",mm:"%d minutes",h:"une heure",hh:"%d heures",d:"un jour",dd:"%d jours",M:"un mois",MM:"%d mois",y:"un an",yy:"%d ans"},ordinalParse:/\d{1,2}(er|e)/,ordinal:function(a){return a+(1===a?"er":"e")},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("fr",{months:"janvier_février_mars_avril_mai_juin_juillet_août_septembre_octobre_novembre_décembre".split("_"),monthsShort:"janv._févr._mars_avr._mai_juin_juil._août_sept._oct._nov._déc.".split("_"),monthsParseExact:!0,weekdays:"dimanche_lundi_mardi_mercredi_jeudi_vendredi_samedi".split("_"),weekdaysShort:"dim._lun._mar._mer._jeu._ven._sam.".split("_"),weekdaysMin:"Di_Lu_Ma_Me_Je_Ve_Sa".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[Aujourd'hui à] LT",nextDay:"[Demain à] LT",nextWeek:"dddd [à] LT",lastDay:"[Hier à] LT",lastWeek:"dddd [dernier à] LT",sameElse:"L"},relativeTime:{future:"dans %s",past:"il y a %s",s:"quelques secondes",m:"une minute",mm:"%d minutes",h:"une heure",hh:"%d heures",d:"un jour",dd:"%d jours",M:"un mois",MM:"%d mois",y:"un an",yy:"%d ans"},ordinalParse:/\d{1,2}(er|)/,ordinal:function(a){return a+(1===a?"er":"")},week:{dow:1,// Monday is the first day of the week.
doy:4}}),"jan._feb._mrt._apr._mai_jun._jul._aug._sep._okt._nov._des.".split("_")),Lg="jan_feb_mrt_apr_mai_jun_jul_aug_sep_okt_nov_des".split("_"),Mg=(kg.defineLocale("fy",{months:"jannewaris_febrewaris_maart_april_maaie_juny_july_augustus_septimber_oktober_novimber_desimber".split("_"),monthsShort:function(a,b){return/-MMM-/.test(b)?Lg[a.month()]:Kg[a.month()]},monthsParseExact:!0,weekdays:"snein_moandei_tiisdei_woansdei_tongersdei_freed_sneon".split("_"),weekdaysShort:"si._mo._ti._wo._to._fr._so.".split("_"),weekdaysMin:"Si_Mo_Ti_Wo_To_Fr_So".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD-MM-YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[hjoed om] LT",nextDay:"[moarn om] LT",nextWeek:"dddd [om] LT",lastDay:"[juster om] LT",lastWeek:"[ôfrûne] dddd [om] LT",sameElse:"L"},relativeTime:{future:"oer %s",past:"%s lyn",s:"in pear sekonden",m:"ien minút",mm:"%d minuten",h:"ien oere",hh:"%d oeren",d:"ien dei",dd:"%d dagen",M:"ien moanne",MM:"%d moannen",y:"ien jier",yy:"%d jierren"},ordinalParse:/\d{1,2}(ste|de)/,ordinal:function(a){return a+(1===a||8===a||a>=20?"ste":"de")},week:{dow:1,// Monday is the first day of the week.
doy:4}}),["Am Faoilleach","An Gearran","Am Màrt","An Giblean","An Cèitean","An t-Ògmhios","An t-Iuchar","An Lùnastal","An t-Sultain","An Dàmhair","An t-Samhain","An Dùbhlachd"]),Ng=["Faoi","Gear","Màrt","Gibl","Cèit","Ògmh","Iuch","Lùn","Sult","Dàmh","Samh","Dùbh"],Og=["Didòmhnaich","Diluain","Dimàirt","Diciadain","Diardaoin","Dihaoine","Disathairne"],Pg=["Did","Dil","Dim","Dic","Dia","Dih","Dis"],Qg=["Dò","Lu","Mà","Ci","Ar","Ha","Sa"],Rg=(kg.defineLocale("gd",{months:Mg,monthsShort:Ng,monthsParseExact:!0,weekdays:Og,weekdaysShort:Pg,weekdaysMin:Qg,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[An-diugh aig] LT",nextDay:"[A-màireach aig] LT",nextWeek:"dddd [aig] LT",lastDay:"[An-dè aig] LT",lastWeek:"dddd [seo chaidh] [aig] LT",sameElse:"L"},relativeTime:{future:"ann an %s",past:"bho chionn %s",s:"beagan diogan",m:"mionaid",mm:"%d mionaidean",h:"uair",hh:"%d uairean",d:"latha",dd:"%d latha",M:"mìos",MM:"%d mìosan",y:"bliadhna",yy:"%d bliadhna"},ordinalParse:/\d{1,2}(d|na|mh)/,ordinal:function(a){var b=1===a?"d":a%10===2?"na":"mh";return a+b},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("gl",{months:"Xaneiro_Febreiro_Marzo_Abril_Maio_Xuño_Xullo_Agosto_Setembro_Outubro_Novembro_Decembro".split("_"),monthsShort:"Xan._Feb._Mar._Abr._Mai._Xuñ._Xul._Ago._Set._Out._Nov._Dec.".split("_"),monthsParseExact:!0,weekdays:"Domingo_Luns_Martes_Mércores_Xoves_Venres_Sábado".split("_"),weekdaysShort:"Dom._Lun._Mar._Mér._Xov._Ven._Sáb.".split("_"),weekdaysMin:"Do_Lu_Ma_Mé_Xo_Ve_Sá".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY H:mm",LLLL:"dddd D MMMM YYYY H:mm"},calendar:{sameDay:function(){return"[hoxe "+(1!==this.hours()?"ás":"á")+"] LT"},nextDay:function(){return"[mañá "+(1!==this.hours()?"ás":"á")+"] LT"},nextWeek:function(){return"dddd ["+(1!==this.hours()?"ás":"a")+"] LT"},lastDay:function(){return"[onte "+(1!==this.hours()?"á":"a")+"] LT"},lastWeek:function(){return"[o] dddd [pasado "+(1!==this.hours()?"ás":"a")+"] LT"},sameElse:"L"},relativeTime:{future:function(a){return"uns segundos"===a?"nuns segundos":"en "+a},past:"hai %s",s:"uns segundos",m:"un minuto",mm:"%d minutos",h:"unha hora",hh:"%d horas",d:"un día",dd:"%d días",M:"un mes",MM:"%d meses",y:"un ano",yy:"%d anos"},ordinalParse:/\d{1,2}º/,ordinal:"%dº",week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("he",{months:"ינואר_פברואר_מרץ_אפריל_מאי_יוני_יולי_אוגוסט_ספטמבר_אוקטובר_נובמבר_דצמבר".split("_"),monthsShort:"ינו׳_פבר׳_מרץ_אפר׳_מאי_יוני_יולי_אוג׳_ספט׳_אוק׳_נוב׳_דצמ׳".split("_"),weekdays:"ראשון_שני_שלישי_רביעי_חמישי_שישי_שבת".split("_"),weekdaysShort:"א׳_ב׳_ג׳_ד׳_ה׳_ו׳_ש׳".split("_"),weekdaysMin:"א_ב_ג_ד_ה_ו_ש".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D [ב]MMMM YYYY",LLL:"D [ב]MMMM YYYY HH:mm",LLLL:"dddd, D [ב]MMMM YYYY HH:mm",l:"D/M/YYYY",ll:"D MMM YYYY",lll:"D MMM YYYY HH:mm",llll:"ddd, D MMM YYYY HH:mm"},calendar:{sameDay:"[היום ב־]LT",nextDay:"[מחר ב־]LT",nextWeek:"dddd [בשעה] LT",lastDay:"[אתמול ב־]LT",lastWeek:"[ביום] dddd [האחרון בשעה] LT",sameElse:"L"},relativeTime:{future:"בעוד %s",past:"לפני %s",s:"מספר שניות",m:"דקה",mm:"%d דקות",h:"שעה",hh:function(a){return 2===a?"שעתיים":a+" שעות"},d:"יום",dd:function(a){return 2===a?"יומיים":a+" ימים"},M:"חודש",MM:function(a){return 2===a?"חודשיים":a+" חודשים"},y:"שנה",yy:function(a){return 2===a?"שנתיים":a%10===0&&10!==a?a+" שנה":a+" שנים"}},meridiemParse:/אחה"צ|לפנה"צ|אחרי הצהריים|לפני הצהריים|לפנות בוקר|בבוקר|בערב/i,isPM:function(a){return/^(אחה"צ|אחרי הצהריים|בערב)$/.test(a)},meridiem:function(a,b,c){return 5>a?"לפנות בוקר":10>a?"בבוקר":12>a?c?'לפנה"צ':"לפני הצהריים":18>a?c?'אחה"צ':"אחרי הצהריים":"בערב"}}),{1:"१",2:"२",3:"३",4:"४",5:"५",6:"६",7:"७",8:"८",9:"९",0:"०"}),Sg={"१":"1","२":"2","३":"3","४":"4","५":"5","६":"6","७":"7","८":"8","९":"9","०":"0"},Tg=(kg.defineLocale("hi",{months:"जनवरी_फ़रवरी_मार्च_अप्रैल_मई_जून_जुलाई_अगस्त_सितम्बर_अक्टूबर_नवम्बर_दिसम्बर".split("_"),monthsShort:"जन._फ़र._मार्च_अप्रै._मई_जून_जुल._अग._सित._अक्टू._नव._दिस.".split("_"),monthsParseExact:!0,weekdays:"रविवार_सोमवार_मंगलवार_बुधवार_गुरूवार_शुक्रवार_शनिवार".split("_"),weekdaysShort:"रवि_सोम_मंगल_बुध_गुरू_शुक्र_शनि".split("_"),weekdaysMin:"र_सो_मं_बु_गु_शु_श".split("_"),longDateFormat:{LT:"A h:mm बजे",LTS:"A h:mm:ss बजे",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, A h:mm बजे",LLLL:"dddd, D MMMM YYYY, A h:mm बजे"},calendar:{sameDay:"[आज] LT",nextDay:"[कल] LT",nextWeek:"dddd, LT",lastDay:"[कल] LT",lastWeek:"[पिछले] dddd, LT",sameElse:"L"},relativeTime:{future:"%s में",past:"%s पहले",s:"कुछ ही क्षण",m:"एक मिनट",mm:"%d मिनट",h:"एक घंटा",hh:"%d घंटे",d:"एक दिन",dd:"%d दिन",M:"एक महीने",MM:"%d महीने",y:"एक वर्ष",yy:"%d वर्ष"},preparse:function(a){return a.replace(/[१२३४५६७८९०]/g,function(a){return Sg[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return Rg[a]})},
// Hindi notation for meridiems are quite fuzzy in practice. While there exists
// a rigid notion of a 'Pahar' it is not used as rigidly in modern Hindi.
meridiemParse:/रात|सुबह|दोपहर|शाम/,meridiemHour:function(a,b){return 12===a&&(a=0),"रात"===b?4>a?a:a+12:"सुबह"===b?a:"दोपहर"===b?a>=10?a:a+12:"शाम"===b?a+12:void 0},meridiem:function(a,b,c){return 4>a?"रात":10>a?"सुबह":17>a?"दोपहर":20>a?"शाम":"रात"},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),kg.defineLocale("hr",{months:{format:"siječnja_veljače_ožujka_travnja_svibnja_lipnja_srpnja_kolovoza_rujna_listopada_studenoga_prosinca".split("_"),standalone:"siječanj_veljača_ožujak_travanj_svibanj_lipanj_srpanj_kolovoz_rujan_listopad_studeni_prosinac".split("_")},monthsShort:"sij._velj._ožu._tra._svi._lip._srp._kol._ruj._lis._stu._pro.".split("_"),monthsParseExact:!0,weekdays:"nedjelja_ponedjeljak_utorak_srijeda_četvrtak_petak_subota".split("_"),weekdaysShort:"ned._pon._uto._sri._čet._pet._sub.".split("_"),weekdaysMin:"ne_po_ut_sr_če_pe_su".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD. MM. YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd, D. MMMM YYYY H:mm"},calendar:{sameDay:"[danas u] LT",nextDay:"[sutra u] LT",nextWeek:function(){switch(this.day()){case 0:return"[u] [nedjelju] [u] LT";case 3:return"[u] [srijedu] [u] LT";case 6:return"[u] [subotu] [u] LT";case 1:case 2:case 4:case 5:return"[u] dddd [u] LT"}},lastDay:"[jučer u] LT",lastWeek:function(){switch(this.day()){case 0:case 3:return"[prošlu] dddd [u] LT";case 6:return"[prošle] [subote] [u] LT";case 1:case 2:case 4:case 5:return"[prošli] dddd [u] LT"}},sameElse:"L"},relativeTime:{future:"za %s",past:"prije %s",s:"par sekundi",m:Bd,mm:Bd,h:Bd,hh:Bd,d:"dan",dd:Bd,M:"mjesec",MM:Bd,y:"godinu",yy:Bd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),"vasárnap hétfőn kedden szerdán csütörtökön pénteken szombaton".split(" ")),Ug=(kg.defineLocale("hu",{months:"január_február_március_április_május_június_július_augusztus_szeptember_október_november_december".split("_"),monthsShort:"jan_feb_márc_ápr_máj_jún_júl_aug_szept_okt_nov_dec".split("_"),weekdays:"vasárnap_hétfő_kedd_szerda_csütörtök_péntek_szombat".split("_"),weekdaysShort:"vas_hét_kedd_sze_csüt_pén_szo".split("_"),weekdaysMin:"v_h_k_sze_cs_p_szo".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"YYYY.MM.DD.",LL:"YYYY. MMMM D.",LLL:"YYYY. MMMM D. H:mm",LLLL:"YYYY. MMMM D., dddd H:mm"},meridiemParse:/de|du/i,isPM:function(a){return"u"===a.charAt(1).toLowerCase()},meridiem:function(a,b,c){return 12>a?c===!0?"de":"DE":c===!0?"du":"DU"},calendar:{sameDay:"[ma] LT[-kor]",nextDay:"[holnap] LT[-kor]",nextWeek:function(){return Dd.call(this,!0)},lastDay:"[tegnap] LT[-kor]",lastWeek:function(){return Dd.call(this,!1)},sameElse:"L"},relativeTime:{future:"%s múlva",past:"%s",s:Cd,m:Cd,mm:Cd,h:Cd,hh:Cd,d:Cd,dd:Cd,M:Cd,MM:Cd,y:Cd,yy:Cd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("hy-am",{months:{format:"հունվարի_փետրվարի_մարտի_ապրիլի_մայիսի_հունիսի_հուլիսի_օգոստոսի_սեպտեմբերի_հոկտեմբերի_նոյեմբերի_դեկտեմբերի".split("_"),standalone:"հունվար_փետրվար_մարտ_ապրիլ_մայիս_հունիս_հուլիս_օգոստոս_սեպտեմբեր_հոկտեմբեր_նոյեմբեր_դեկտեմբեր".split("_")},monthsShort:"հնվ_փտր_մրտ_ապր_մյս_հնս_հլս_օգս_սպտ_հկտ_նմբ_դկտ".split("_"),weekdays:"կիրակի_երկուշաբթի_երեքշաբթի_չորեքշաբթի_հինգշաբթի_ուրբաթ_շաբաթ".split("_"),weekdaysShort:"կրկ_երկ_երք_չրք_հնգ_ուրբ_շբթ".split("_"),weekdaysMin:"կրկ_երկ_երք_չրք_հնգ_ուրբ_շբթ".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY թ.",LLL:"D MMMM YYYY թ., HH:mm",LLLL:"dddd, D MMMM YYYY թ., HH:mm"},calendar:{sameDay:"[այսօր] LT",nextDay:"[վաղը] LT",lastDay:"[երեկ] LT",nextWeek:function(){return"dddd [օրը ժամը] LT"},lastWeek:function(){return"[անցած] dddd [օրը ժամը] LT"},sameElse:"L"},relativeTime:{future:"%s հետո",past:"%s առաջ",s:"մի քանի վայրկյան",m:"րոպե",mm:"%d րոպե",h:"ժամ",hh:"%d ժամ",d:"օր",dd:"%d օր",M:"ամիս",MM:"%d ամիս",y:"տարի",yy:"%d տարի"},meridiemParse:/գիշերվա|առավոտվա|ցերեկվա|երեկոյան/,isPM:function(a){return/^(ցերեկվա|երեկոյան)$/.test(a)},meridiem:function(a){return 4>a?"գիշերվա":12>a?"առավոտվա":17>a?"ցերեկվա":"երեկոյան"},ordinalParse:/\d{1,2}|\d{1,2}-(ին|րդ)/,ordinal:function(a,b){switch(b){case"DDD":case"w":case"W":case"DDDo":return 1===a?a+"-ին":a+"-րդ";default:return a}},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("id",{months:"Januari_Februari_Maret_April_Mei_Juni_Juli_Agustus_September_Oktober_November_Desember".split("_"),monthsShort:"Jan_Feb_Mar_Apr_Mei_Jun_Jul_Ags_Sep_Okt_Nov_Des".split("_"),weekdays:"Minggu_Senin_Selasa_Rabu_Kamis_Jumat_Sabtu".split("_"),weekdaysShort:"Min_Sen_Sel_Rab_Kam_Jum_Sab".split("_"),weekdaysMin:"Mg_Sn_Sl_Rb_Km_Jm_Sb".split("_"),longDateFormat:{LT:"HH.mm",LTS:"HH.mm.ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY [pukul] HH.mm",LLLL:"dddd, D MMMM YYYY [pukul] HH.mm"},meridiemParse:/pagi|siang|sore|malam/,meridiemHour:function(a,b){return 12===a&&(a=0),"pagi"===b?a:"siang"===b?a>=11?a:a+12:"sore"===b||"malam"===b?a+12:void 0},meridiem:function(a,b,c){return 11>a?"pagi":15>a?"siang":19>a?"sore":"malam"},calendar:{sameDay:"[Hari ini pukul] LT",nextDay:"[Besok pukul] LT",nextWeek:"dddd [pukul] LT",lastDay:"[Kemarin pukul] LT",lastWeek:"dddd [lalu pukul] LT",sameElse:"L"},relativeTime:{future:"dalam %s",past:"%s yang lalu",s:"beberapa detik",m:"semenit",mm:"%d menit",h:"sejam",hh:"%d jam",d:"sehari",dd:"%d hari",M:"sebulan",MM:"%d bulan",y:"setahun",yy:"%d tahun"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("is",{months:"janúar_febrúar_mars_apríl_maí_júní_júlí_ágúst_september_október_nóvember_desember".split("_"),monthsShort:"jan_feb_mar_apr_maí_jún_júl_ágú_sep_okt_nóv_des".split("_"),weekdays:"sunnudagur_mánudagur_þriðjudagur_miðvikudagur_fimmtudagur_föstudagur_laugardagur".split("_"),weekdaysShort:"sun_mán_þri_mið_fim_fös_lau".split("_"),weekdaysMin:"Su_Má_Þr_Mi_Fi_Fö_La".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY [kl.] H:mm",LLLL:"dddd, D. MMMM YYYY [kl.] H:mm"},calendar:{sameDay:"[í dag kl.] LT",nextDay:"[á morgun kl.] LT",nextWeek:"dddd [kl.] LT",lastDay:"[í gær kl.] LT",lastWeek:"[síðasta] dddd [kl.] LT",sameElse:"L"},relativeTime:{future:"eftir %s",past:"fyrir %s síðan",s:Fd,m:Fd,mm:Fd,h:"klukkustund",hh:Fd,d:Fd,dd:Fd,M:Fd,MM:Fd,y:Fd,yy:Fd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("it",{months:"gennaio_febbraio_marzo_aprile_maggio_giugno_luglio_agosto_settembre_ottobre_novembre_dicembre".split("_"),monthsShort:"gen_feb_mar_apr_mag_giu_lug_ago_set_ott_nov_dic".split("_"),weekdays:"Domenica_Lunedì_Martedì_Mercoledì_Giovedì_Venerdì_Sabato".split("_"),weekdaysShort:"Dom_Lun_Mar_Mer_Gio_Ven_Sab".split("_"),weekdaysMin:"Do_Lu_Ma_Me_Gi_Ve_Sa".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Oggi alle] LT",nextDay:"[Domani alle] LT",nextWeek:"dddd [alle] LT",lastDay:"[Ieri alle] LT",lastWeek:function(){switch(this.day()){case 0:return"[la scorsa] dddd [alle] LT";default:return"[lo scorso] dddd [alle] LT"}},sameElse:"L"},relativeTime:{future:function(a){return(/^[0-9].+$/.test(a)?"tra":"in")+" "+a},past:"%s fa",s:"alcuni secondi",m:"un minuto",mm:"%d minuti",h:"un'ora",hh:"%d ore",d:"un giorno",dd:"%d giorni",M:"un mese",MM:"%d mesi",y:"un anno",yy:"%d anni"},ordinalParse:/\d{1,2}º/,ordinal:"%dº",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("ja",{months:"1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),monthsShort:"1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),weekdays:"日曜日_月曜日_火曜日_水曜日_木曜日_金曜日_土曜日".split("_"),weekdaysShort:"日_月_火_水_木_金_土".split("_"),weekdaysMin:"日_月_火_水_木_金_土".split("_"),longDateFormat:{LT:"Ah時m分",LTS:"Ah時m分s秒",L:"YYYY/MM/DD",LL:"YYYY年M月D日",LLL:"YYYY年M月D日Ah時m分",LLLL:"YYYY年M月D日Ah時m分 dddd"},meridiemParse:/午前|午後/i,isPM:function(a){return"午後"===a},meridiem:function(a,b,c){return 12>a?"午前":"午後"},calendar:{sameDay:"[今日] LT",nextDay:"[明日] LT",nextWeek:"[来週]dddd LT",lastDay:"[昨日] LT",lastWeek:"[前週]dddd LT",sameElse:"L"},ordinalParse:/\d{1,2}日/,ordinal:function(a,b){switch(b){case"d":case"D":case"DDD":return a+"日";default:return a}},relativeTime:{future:"%s後",past:"%s前",s:"数秒",m:"1分",mm:"%d分",h:"1時間",hh:"%d時間",d:"1日",dd:"%d日",M:"1ヶ月",MM:"%dヶ月",y:"1年",yy:"%d年"}}),kg.defineLocale("jv",{months:"Januari_Februari_Maret_April_Mei_Juni_Juli_Agustus_September_Oktober_Nopember_Desember".split("_"),monthsShort:"Jan_Feb_Mar_Apr_Mei_Jun_Jul_Ags_Sep_Okt_Nop_Des".split("_"),weekdays:"Minggu_Senen_Seloso_Rebu_Kemis_Jemuwah_Septu".split("_"),weekdaysShort:"Min_Sen_Sel_Reb_Kem_Jem_Sep".split("_"),weekdaysMin:"Mg_Sn_Sl_Rb_Km_Jm_Sp".split("_"),longDateFormat:{LT:"HH.mm",LTS:"HH.mm.ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY [pukul] HH.mm",LLLL:"dddd, D MMMM YYYY [pukul] HH.mm"},meridiemParse:/enjing|siyang|sonten|ndalu/,meridiemHour:function(a,b){return 12===a&&(a=0),"enjing"===b?a:"siyang"===b?a>=11?a:a+12:"sonten"===b||"ndalu"===b?a+12:void 0},meridiem:function(a,b,c){return 11>a?"enjing":15>a?"siyang":19>a?"sonten":"ndalu"},calendar:{sameDay:"[Dinten puniko pukul] LT",nextDay:"[Mbenjang pukul] LT",nextWeek:"dddd [pukul] LT",lastDay:"[Kala wingi pukul] LT",lastWeek:"dddd [kepengker pukul] LT",sameElse:"L"},relativeTime:{future:"wonten ing %s",past:"%s ingkang kepengker",s:"sawetawis detik",m:"setunggal menit",mm:"%d menit",h:"setunggal jam",hh:"%d jam",d:"sedinten",dd:"%d dinten",M:"sewulan",MM:"%d wulan",y:"setaun",yy:"%d taun"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("ka",{months:{standalone:"იანვარი_თებერვალი_მარტი_აპრილი_მაისი_ივნისი_ივლისი_აგვისტო_სექტემბერი_ოქტომბერი_ნოემბერი_დეკემბერი".split("_"),format:"იანვარს_თებერვალს_მარტს_აპრილის_მაისს_ივნისს_ივლისს_აგვისტს_სექტემბერს_ოქტომბერს_ნოემბერს_დეკემბერს".split("_")},monthsShort:"იან_თებ_მარ_აპრ_მაი_ივნ_ივლ_აგვ_სექ_ოქტ_ნოე_დეკ".split("_"),weekdays:{standalone:"კვირა_ორშაბათი_სამშაბათი_ოთხშაბათი_ხუთშაბათი_პარასკევი_შაბათი".split("_"),format:"კვირას_ორშაბათს_სამშაბათს_ოთხშაბათს_ხუთშაბათს_პარასკევს_შაბათს".split("_"),isFormat:/(წინა|შემდეგ)/},weekdaysShort:"კვი_ორშ_სამ_ოთხ_ხუთ_პარ_შაბ".split("_"),weekdaysMin:"კვ_ორ_სა_ოთ_ხუ_პა_შა".split("_"),longDateFormat:{LT:"h:mm A",LTS:"h:mm:ss A",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY h:mm A",LLLL:"dddd, D MMMM YYYY h:mm A"},calendar:{sameDay:"[დღეს] LT[-ზე]",nextDay:"[ხვალ] LT[-ზე]",lastDay:"[გუშინ] LT[-ზე]",nextWeek:"[შემდეგ] dddd LT[-ზე]",lastWeek:"[წინა] dddd LT-ზე",sameElse:"L"},relativeTime:{future:function(a){return/(წამი|წუთი|საათი|წელი)/.test(a)?a.replace(/ი$/,"ში"):a+"ში"},past:function(a){return/(წამი|წუთი|საათი|დღე|თვე)/.test(a)?a.replace(/(ი|ე)$/,"ის წინ"):/წელი/.test(a)?a.replace(/წელი$/,"წლის წინ"):void 0},s:"რამდენიმე წამი",m:"წუთი",mm:"%d წუთი",h:"საათი",hh:"%d საათი",d:"დღე",dd:"%d დღე",M:"თვე",MM:"%d თვე",y:"წელი",yy:"%d წელი"},ordinalParse:/0|1-ლი|მე-\d{1,2}|\d{1,2}-ე/,ordinal:function(a){return 0===a?a:1===a?a+"-ლი":20>a||100>=a&&a%20===0||a%100===0?"მე-"+a:a+"-ე"},week:{dow:1,doy:7}}),{0:"-ші",1:"-ші",2:"-ші",3:"-ші",4:"-ші",5:"-ші",6:"-шы",7:"-ші",8:"-ші",9:"-шы",10:"-шы",20:"-шы",30:"-шы",40:"-шы",50:"-ші",60:"-шы",70:"-ші",80:"-ші",90:"-шы",100:"-ші"}),Vg=(kg.defineLocale("kk",{months:"қаңтар_ақпан_наурыз_сәуір_мамыр_маусым_шілде_тамыз_қыркүйек_қазан_қараша_желтоқсан".split("_"),monthsShort:"қаң_ақп_нау_сәу_мам_мау_шіл_там_қыр_қаз_қар_жел".split("_"),weekdays:"жексенбі_дүйсенбі_сейсенбі_сәрсенбі_бейсенбі_жұма_сенбі".split("_"),weekdaysShort:"жек_дүй_сей_сәр_бей_жұм_сен".split("_"),weekdaysMin:"жк_дй_сй_ср_бй_жм_сн".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Бүгін сағат] LT",nextDay:"[Ертең сағат] LT",nextWeek:"dddd [сағат] LT",lastDay:"[Кеше сағат] LT",lastWeek:"[Өткен аптаның] dddd [сағат] LT",sameElse:"L"},relativeTime:{future:"%s ішінде",past:"%s бұрын",s:"бірнеше секунд",m:"бір минут",mm:"%d минут",h:"бір сағат",hh:"%d сағат",d:"бір күн",dd:"%d күн",M:"бір ай",MM:"%d ай",y:"бір жыл",yy:"%d жыл"},ordinalParse:/\d{1,2}-(ші|шы)/,ordinal:function(a){var b=a%10,c=a>=100?100:null;return a+(Ug[a]||Ug[b]||Ug[c])},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("km",{months:"មករា_កុម្ភៈ_មីនា_មេសា_ឧសភា_មិថុនា_កក្កដា_សីហា_កញ្ញា_តុលា_វិច្ឆិកា_ធ្នូ".split("_"),monthsShort:"មករា_កុម្ភៈ_មីនា_មេសា_ឧសភា_មិថុនា_កក្កដា_សីហា_កញ្ញា_តុលា_វិច្ឆិកា_ធ្នូ".split("_"),weekdays:"អាទិត្យ_ច័ន្ទ_អង្គារ_ពុធ_ព្រហស្បតិ៍_សុក្រ_សៅរ៍".split("_"),weekdaysShort:"អាទិត្យ_ច័ន្ទ_អង្គារ_ពុធ_ព្រហស្បតិ៍_សុក្រ_សៅរ៍".split("_"),weekdaysMin:"អាទិត្យ_ច័ន្ទ_អង្គារ_ពុធ_ព្រហស្បតិ៍_សុក្រ_សៅរ៍".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[ថ្ងៃនេះ ម៉ោង] LT",nextDay:"[ស្អែក ម៉ោង] LT",nextWeek:"dddd [ម៉ោង] LT",lastDay:"[ម្សិលមិញ ម៉ោង] LT",lastWeek:"dddd [សប្តាហ៍មុន] [ម៉ោង] LT",sameElse:"L"},relativeTime:{future:"%sទៀត",past:"%sមុន",s:"ប៉ុន្មានវិនាទី",m:"មួយនាទី",mm:"%d នាទី",h:"មួយម៉ោង",hh:"%d ម៉ោង",d:"មួយថ្ងៃ",dd:"%d ថ្ងៃ",M:"មួយខែ",MM:"%d ខែ",y:"មួយឆ្នាំ",yy:"%d ឆ្នាំ"},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("ko",{months:"1월_2월_3월_4월_5월_6월_7월_8월_9월_10월_11월_12월".split("_"),monthsShort:"1월_2월_3월_4월_5월_6월_7월_8월_9월_10월_11월_12월".split("_"),weekdays:"일요일_월요일_화요일_수요일_목요일_금요일_토요일".split("_"),weekdaysShort:"일_월_화_수_목_금_토".split("_"),weekdaysMin:"일_월_화_수_목_금_토".split("_"),longDateFormat:{LT:"A h시 m분",LTS:"A h시 m분 s초",L:"YYYY.MM.DD",LL:"YYYY년 MMMM D일",LLL:"YYYY년 MMMM D일 A h시 m분",LLLL:"YYYY년 MMMM D일 dddd A h시 m분"},calendar:{sameDay:"오늘 LT",nextDay:"내일 LT",nextWeek:"dddd LT",lastDay:"어제 LT",lastWeek:"지난주 dddd LT",sameElse:"L"},relativeTime:{future:"%s 후",past:"%s 전",s:"몇 초",ss:"%d초",m:"일분",mm:"%d분",h:"한 시간",hh:"%d시간",d:"하루",dd:"%d일",M:"한 달",MM:"%d달",y:"일 년",yy:"%d년"},ordinalParse:/\d{1,2}일/,ordinal:"%d일",meridiemParse:/오전|오후/,isPM:function(a){return"오후"===a},meridiem:function(a,b,c){return 12>a?"오전":"오후"}}),{0:"-чү",1:"-чи",2:"-чи",3:"-чү",4:"-чү",5:"-чи",6:"-чы",7:"-чи",8:"-чи",9:"-чу",10:"-чу",20:"-чы",30:"-чу",40:"-чы",50:"-чү",60:"-чы",70:"-чи",80:"-чи",90:"-чу",100:"-чү"}),Wg=(kg.defineLocale("ky",{months:"январь_февраль_март_апрель_май_июнь_июль_август_сентябрь_октябрь_ноябрь_декабрь".split("_"),monthsShort:"янв_фев_март_апр_май_июнь_июль_авг_сен_окт_ноя_дек".split("_"),weekdays:"Жекшемби_Дүйшөмбү_Шейшемби_Шаршемби_Бейшемби_Жума_Ишемби".split("_"),weekdaysShort:"Жек_Дүй_Шей_Шар_Бей_Жум_Ише".split("_"),weekdaysMin:"Жк_Дй_Шй_Шр_Бй_Жм_Иш".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Бүгүн саат] LT",nextDay:"[Эртең саат] LT",nextWeek:"dddd [саат] LT",lastDay:"[Кече саат] LT",lastWeek:"[Өткен аптанын] dddd [күнү] [саат] LT",sameElse:"L"},relativeTime:{future:"%s ичинде",past:"%s мурун",s:"бирнече секунд",m:"бир мүнөт",mm:"%d мүнөт",h:"бир саат",hh:"%d саат",d:"бир күн",dd:"%d күн",M:"бир ай",MM:"%d ай",y:"бир жыл",yy:"%d жыл"},ordinalParse:/\d{1,2}-(чи|чы|чү|чу)/,ordinal:function(a){var b=a%10,c=a>=100?100:null;return a+(Vg[a]||Vg[b]||Vg[c])},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("lb",{months:"Januar_Februar_Mäerz_Abrëll_Mee_Juni_Juli_August_September_Oktober_November_Dezember".split("_"),monthsShort:"Jan._Febr._Mrz._Abr._Mee_Jun._Jul._Aug._Sept._Okt._Nov._Dez.".split("_"),monthsParseExact:!0,weekdays:"Sonndeg_Méindeg_Dënschdeg_Mëttwoch_Donneschdeg_Freideg_Samschdeg".split("_"),weekdaysShort:"So._Mé._Dë._Më._Do._Fr._Sa.".split("_"),weekdaysMin:"So_Mé_Dë_Më_Do_Fr_Sa".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm [Auer]",LTS:"H:mm:ss [Auer]",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm [Auer]",LLLL:"dddd, D. MMMM YYYY H:mm [Auer]"},calendar:{sameDay:"[Haut um] LT",sameElse:"L",nextDay:"[Muer um] LT",nextWeek:"dddd [um] LT",lastDay:"[Gëschter um] LT",lastWeek:function(){
// Different date string for 'Dënschdeg' (Tuesday) and 'Donneschdeg' (Thursday) due to phonological rule
switch(this.day()){case 2:case 4:return"[Leschten] dddd [um] LT";default:return"[Leschte] dddd [um] LT"}}},relativeTime:{future:Hd,past:Id,s:"e puer Sekonnen",m:Gd,mm:"%d Minutten",h:Gd,hh:"%d Stonnen",d:Gd,dd:"%d Deeg",M:Gd,MM:"%d Méint",y:Gd,yy:"%d Joer"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("lo",{months:"ມັງກອນ_ກຸມພາ_ມີນາ_ເມສາ_ພຶດສະພາ_ມິຖຸນາ_ກໍລະກົດ_ສິງຫາ_ກັນຍາ_ຕຸລາ_ພະຈິກ_ທັນວາ".split("_"),monthsShort:"ມັງກອນ_ກຸມພາ_ມີນາ_ເມສາ_ພຶດສະພາ_ມິຖຸນາ_ກໍລະກົດ_ສິງຫາ_ກັນຍາ_ຕຸລາ_ພະຈິກ_ທັນວາ".split("_"),weekdays:"ອາທິດ_ຈັນ_ອັງຄານ_ພຸດ_ພະຫັດ_ສຸກ_ເສົາ".split("_"),weekdaysShort:"ທິດ_ຈັນ_ອັງຄານ_ພຸດ_ພະຫັດ_ສຸກ_ເສົາ".split("_"),weekdaysMin:"ທ_ຈ_ອຄ_ພ_ພຫ_ສກ_ສ".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"ວັນdddd D MMMM YYYY HH:mm"},meridiemParse:/ຕອນເຊົ້າ|ຕອນແລງ/,isPM:function(a){return"ຕອນແລງ"===a},meridiem:function(a,b,c){return 12>a?"ຕອນເຊົ້າ":"ຕອນແລງ"},calendar:{sameDay:"[ມື້ນີ້ເວລາ] LT",nextDay:"[ມື້ອື່ນເວລາ] LT",nextWeek:"[ວັນ]dddd[ໜ້າເວລາ] LT",lastDay:"[ມື້ວານນີ້ເວລາ] LT",lastWeek:"[ວັນ]dddd[ແລ້ວນີ້ເວລາ] LT",sameElse:"L"},relativeTime:{future:"ອີກ %s",past:"%sຜ່ານມາ",s:"ບໍ່ເທົ່າໃດວິນາທີ",m:"1 ນາທີ",mm:"%d ນາທີ",h:"1 ຊົ່ວໂມງ",hh:"%d ຊົ່ວໂມງ",d:"1 ມື້",dd:"%d ມື້",M:"1 ເດືອນ",MM:"%d ເດືອນ",y:"1 ປີ",yy:"%d ປີ"},ordinalParse:/(ທີ່)\d{1,2}/,ordinal:function(a){return"ທີ່"+a}}),{m:"minutė_minutės_minutę",mm:"minutės_minučių_minutes",h:"valanda_valandos_valandą",hh:"valandos_valandų_valandas",d:"diena_dienos_dieną",dd:"dienos_dienų_dienas",M:"mėnuo_mėnesio_mėnesį",MM:"mėnesiai_mėnesių_mėnesius",y:"metai_metų_metus",yy:"metai_metų_metus"}),Xg=(kg.defineLocale("lt",{months:{format:"sausio_vasario_kovo_balandžio_gegužės_birželio_liepos_rugpjūčio_rugsėjo_spalio_lapkričio_gruodžio".split("_"),standalone:"sausis_vasaris_kovas_balandis_gegužė_birželis_liepa_rugpjūtis_rugsėjis_spalis_lapkritis_gruodis".split("_"),isFormat:/D[oD]?(\[[^\[\]]*\]|\s+)+MMMM?|MMMM?(\[[^\[\]]*\]|\s+)+D[oD]?/},monthsShort:"sau_vas_kov_bal_geg_bir_lie_rgp_rgs_spa_lap_grd".split("_"),weekdays:{format:"sekmadienį_pirmadienį_antradienį_trečiadienį_ketvirtadienį_penktadienį_šeštadienį".split("_"),standalone:"sekmadienis_pirmadienis_antradienis_trečiadienis_ketvirtadienis_penktadienis_šeštadienis".split("_"),isFormat:/dddd HH:mm/},weekdaysShort:"Sek_Pir_Ant_Tre_Ket_Pen_Šeš".split("_"),weekdaysMin:"S_P_A_T_K_Pn_Š".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"YYYY-MM-DD",LL:"YYYY [m.] MMMM D [d.]",LLL:"YYYY [m.] MMMM D [d.], HH:mm [val.]",LLLL:"YYYY [m.] MMMM D [d.], dddd, HH:mm [val.]",l:"YYYY-MM-DD",ll:"YYYY [m.] MMMM D [d.]",lll:"YYYY [m.] MMMM D [d.], HH:mm [val.]",llll:"YYYY [m.] MMMM D [d.], ddd, HH:mm [val.]"},calendar:{sameDay:"[Šiandien] LT",nextDay:"[Rytoj] LT",nextWeek:"dddd LT",lastDay:"[Vakar] LT",lastWeek:"[Praėjusį] dddd LT",sameElse:"L"},relativeTime:{future:"po %s",past:"prieš %s",s:Kd,m:Ld,mm:Od,h:Ld,hh:Od,d:Ld,dd:Od,M:Ld,MM:Od,y:Ld,yy:Od},ordinalParse:/\d{1,2}-oji/,ordinal:function(a){return a+"-oji"},week:{dow:1,// Monday is the first day of the week.
doy:4}}),{m:"minūtes_minūtēm_minūte_minūtes".split("_"),mm:"minūtes_minūtēm_minūte_minūtes".split("_"),h:"stundas_stundām_stunda_stundas".split("_"),hh:"stundas_stundām_stunda_stundas".split("_"),d:"dienas_dienām_diena_dienas".split("_"),dd:"dienas_dienām_diena_dienas".split("_"),M:"mēneša_mēnešiem_mēnesis_mēneši".split("_"),MM:"mēneša_mēnešiem_mēnesis_mēneši".split("_"),y:"gada_gadiem_gads_gadi".split("_"),yy:"gada_gadiem_gads_gadi".split("_")}),Yg=(kg.defineLocale("lv",{months:"janvāris_februāris_marts_aprīlis_maijs_jūnijs_jūlijs_augusts_septembris_oktobris_novembris_decembris".split("_"),monthsShort:"jan_feb_mar_apr_mai_jūn_jūl_aug_sep_okt_nov_dec".split("_"),weekdays:"svētdiena_pirmdiena_otrdiena_trešdiena_ceturtdiena_piektdiena_sestdiena".split("_"),weekdaysShort:"Sv_P_O_T_C_Pk_S".split("_"),weekdaysMin:"Sv_P_O_T_C_Pk_S".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY.",LL:"YYYY. [gada] D. MMMM",LLL:"YYYY. [gada] D. MMMM, HH:mm",LLLL:"YYYY. [gada] D. MMMM, dddd, HH:mm"},calendar:{sameDay:"[Šodien pulksten] LT",nextDay:"[Rīt pulksten] LT",nextWeek:"dddd [pulksten] LT",lastDay:"[Vakar pulksten] LT",lastWeek:"[Pagājušā] dddd [pulksten] LT",sameElse:"L"},relativeTime:{future:"pēc %s",past:"pirms %s",s:Sd,m:Rd,mm:Qd,h:Rd,hh:Qd,d:Rd,dd:Qd,M:Rd,MM:Qd,y:Rd,yy:Qd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),{words:{//Different grammatical cases
m:["jedan minut","jednog minuta"],mm:["minut","minuta","minuta"],h:["jedan sat","jednog sata"],hh:["sat","sata","sati"],dd:["dan","dana","dana"],MM:["mjesec","mjeseca","mjeseci"],yy:["godina","godine","godina"]},correctGrammaticalCase:function(a,b){return 1===a?b[0]:a>=2&&4>=a?b[1]:b[2]},translate:function(a,b,c){var d=Yg.words[c];return 1===c.length?b?d[0]:d[1]:a+" "+Yg.correctGrammaticalCase(a,d)}}),Zg=(kg.defineLocale("me",{months:"januar_februar_mart_april_maj_jun_jul_avgust_septembar_oktobar_novembar_decembar".split("_"),monthsShort:"jan._feb._mar._apr._maj_jun_jul_avg._sep._okt._nov._dec.".split("_"),monthsParseExact:!0,weekdays:"nedjelja_ponedjeljak_utorak_srijeda_četvrtak_petak_subota".split("_"),weekdaysShort:"ned._pon._uto._sri._čet._pet._sub.".split("_"),weekdaysMin:"ne_po_ut_sr_če_pe_su".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD. MM. YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd, D. MMMM YYYY H:mm"},calendar:{sameDay:"[danas u] LT",nextDay:"[sjutra u] LT",nextWeek:function(){switch(this.day()){case 0:return"[u] [nedjelju] [u] LT";case 3:return"[u] [srijedu] [u] LT";case 6:return"[u] [subotu] [u] LT";case 1:case 2:case 4:case 5:return"[u] dddd [u] LT"}},lastDay:"[juče u] LT",lastWeek:function(){var a=["[prošle] [nedjelje] [u] LT","[prošlog] [ponedjeljka] [u] LT","[prošlog] [utorka] [u] LT","[prošle] [srijede] [u] LT","[prošlog] [četvrtka] [u] LT","[prošlog] [petka] [u] LT","[prošle] [subote] [u] LT"];return a[this.day()]},sameElse:"L"},relativeTime:{future:"za %s",past:"prije %s",s:"nekoliko sekundi",m:Yg.translate,mm:Yg.translate,h:Yg.translate,hh:Yg.translate,d:"dan",dd:Yg.translate,M:"mjesec",MM:Yg.translate,y:"godinu",yy:Yg.translate},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("mk",{months:"јануари_февруари_март_април_мај_јуни_јули_август_септември_октомври_ноември_декември".split("_"),monthsShort:"јан_фев_мар_апр_мај_јун_јул_авг_сеп_окт_ное_дек".split("_"),weekdays:"недела_понеделник_вторник_среда_четврток_петок_сабота".split("_"),weekdaysShort:"нед_пон_вто_сре_чет_пет_саб".split("_"),weekdaysMin:"нe_пo_вт_ср_че_пе_сa".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"D.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY H:mm",LLLL:"dddd, D MMMM YYYY H:mm"},calendar:{sameDay:"[Денес во] LT",nextDay:"[Утре во] LT",nextWeek:"[Во] dddd [во] LT",lastDay:"[Вчера во] LT",lastWeek:function(){switch(this.day()){case 0:case 3:case 6:return"[Изминатата] dddd [во] LT";case 1:case 2:case 4:case 5:return"[Изминатиот] dddd [во] LT"}},sameElse:"L"},relativeTime:{future:"после %s",past:"пред %s",s:"неколку секунди",m:"минута",mm:"%d минути",h:"час",hh:"%d часа",d:"ден",dd:"%d дена",M:"месец",MM:"%d месеци",y:"година",yy:"%d години"},ordinalParse:/\d{1,2}-(ев|ен|ти|ви|ри|ми)/,ordinal:function(a){var b=a%10,c=a%100;return 0===a?a+"-ев":0===c?a+"-ен":c>10&&20>c?a+"-ти":1===b?a+"-ви":2===b?a+"-ри":7===b||8===b?a+"-ми":a+"-ти"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("ml",{months:"ജനുവരി_ഫെബ്രുവരി_മാർച്ച്_ഏപ്രിൽ_മേയ്_ജൂൺ_ജൂലൈ_ഓഗസ്റ്റ്_സെപ്റ്റംബർ_ഒക്ടോബർ_നവംബർ_ഡിസംബർ".split("_"),monthsShort:"ജനു._ഫെബ്രു._മാർ._ഏപ്രി._മേയ്_ജൂൺ_ജൂലൈ._ഓഗ._സെപ്റ്റ._ഒക്ടോ._നവം._ഡിസം.".split("_"),monthsParseExact:!0,weekdays:"ഞായറാഴ്ച_തിങ്കളാഴ്ച_ചൊവ്വാഴ്ച_ബുധനാഴ്ച_വ്യാഴാഴ്ച_വെള്ളിയാഴ്ച_ശനിയാഴ്ച".split("_"),weekdaysShort:"ഞായർ_തിങ്കൾ_ചൊവ്വ_ബുധൻ_വ്യാഴം_വെള്ളി_ശനി".split("_"),weekdaysMin:"ഞാ_തി_ചൊ_ബു_വ്യാ_വെ_ശ".split("_"),longDateFormat:{LT:"A h:mm -നു",LTS:"A h:mm:ss -നു",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, A h:mm -നു",LLLL:"dddd, D MMMM YYYY, A h:mm -നു"},calendar:{sameDay:"[ഇന്ന്] LT",nextDay:"[നാളെ] LT",nextWeek:"dddd, LT",lastDay:"[ഇന്നലെ] LT",lastWeek:"[കഴിഞ്ഞ] dddd, LT",sameElse:"L"},relativeTime:{future:"%s കഴിഞ്ഞ്",past:"%s മുൻപ്",s:"അൽപ നിമിഷങ്ങൾ",m:"ഒരു മിനിറ്റ്",mm:"%d മിനിറ്റ്",h:"ഒരു മണിക്കൂർ",hh:"%d മണിക്കൂർ",d:"ഒരു ദിവസം",dd:"%d ദിവസം",M:"ഒരു മാസം",MM:"%d മാസം",y:"ഒരു വർഷം",yy:"%d വർഷം"},meridiemParse:/രാത്രി|രാവിലെ|ഉച്ച കഴിഞ്ഞ്|വൈകുന്നേരം|രാത്രി/i,meridiemHour:function(a,b){return 12===a&&(a=0),"രാത്രി"===b&&a>=4||"ഉച്ച കഴിഞ്ഞ്"===b||"വൈകുന്നേരം"===b?a+12:a},meridiem:function(a,b,c){return 4>a?"രാത്രി":12>a?"രാവിലെ":17>a?"ഉച്ച കഴിഞ്ഞ്":20>a?"വൈകുന്നേരം":"രാത്രി"}}),{1:"१",2:"२",3:"३",4:"४",5:"५",6:"६",7:"७",8:"८",9:"९",0:"०"}),$g={"१":"1","२":"2","३":"3","४":"4","५":"5","६":"6","७":"7","८":"8","९":"9","०":"0"},_g=(kg.defineLocale("mr",{months:"जानेवारी_फेब्रुवारी_मार्च_एप्रिल_मे_जून_जुलै_ऑगस्ट_सप्टेंबर_ऑक्टोबर_नोव्हेंबर_डिसेंबर".split("_"),monthsShort:"जाने._फेब्रु._मार्च._एप्रि._मे._जून._जुलै._ऑग._सप्टें._ऑक्टो._नोव्हें._डिसें.".split("_"),monthsParseExact:!0,weekdays:"रविवार_सोमवार_मंगळवार_बुधवार_गुरूवार_शुक्रवार_शनिवार".split("_"),weekdaysShort:"रवि_सोम_मंगळ_बुध_गुरू_शुक्र_शनि".split("_"),weekdaysMin:"र_सो_मं_बु_गु_शु_श".split("_"),longDateFormat:{LT:"A h:mm वाजता",LTS:"A h:mm:ss वाजता",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, A h:mm वाजता",LLLL:"dddd, D MMMM YYYY, A h:mm वाजता"},calendar:{sameDay:"[आज] LT",nextDay:"[उद्या] LT",nextWeek:"dddd, LT",lastDay:"[काल] LT",lastWeek:"[मागील] dddd, LT",sameElse:"L"},relativeTime:{future:"%sमध्ये",past:"%sपूर्वी",s:Td,m:Td,mm:Td,h:Td,hh:Td,d:Td,dd:Td,M:Td,MM:Td,y:Td,yy:Td},preparse:function(a){return a.replace(/[१२३४५६७८९०]/g,function(a){return $g[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return Zg[a]})},meridiemParse:/रात्री|सकाळी|दुपारी|सायंकाळी/,meridiemHour:function(a,b){return 12===a&&(a=0),"रात्री"===b?4>a?a:a+12:"सकाळी"===b?a:"दुपारी"===b?a>=10?a:a+12:"सायंकाळी"===b?a+12:void 0},meridiem:function(a,b,c){return 4>a?"रात्री":10>a?"सकाळी":17>a?"दुपारी":20>a?"सायंकाळी":"रात्री"},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),kg.defineLocale("ms-my",{months:"Januari_Februari_Mac_April_Mei_Jun_Julai_Ogos_September_Oktober_November_Disember".split("_"),monthsShort:"Jan_Feb_Mac_Apr_Mei_Jun_Jul_Ogs_Sep_Okt_Nov_Dis".split("_"),weekdays:"Ahad_Isnin_Selasa_Rabu_Khamis_Jumaat_Sabtu".split("_"),weekdaysShort:"Ahd_Isn_Sel_Rab_Kha_Jum_Sab".split("_"),weekdaysMin:"Ah_Is_Sl_Rb_Km_Jm_Sb".split("_"),longDateFormat:{LT:"HH.mm",LTS:"HH.mm.ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY [pukul] HH.mm",LLLL:"dddd, D MMMM YYYY [pukul] HH.mm"},meridiemParse:/pagi|tengahari|petang|malam/,meridiemHour:function(a,b){return 12===a&&(a=0),"pagi"===b?a:"tengahari"===b?a>=11?a:a+12:"petang"===b||"malam"===b?a+12:void 0},meridiem:function(a,b,c){return 11>a?"pagi":15>a?"tengahari":19>a?"petang":"malam"},calendar:{sameDay:"[Hari ini pukul] LT",nextDay:"[Esok pukul] LT",nextWeek:"dddd [pukul] LT",lastDay:"[Kelmarin pukul] LT",lastWeek:"dddd [lepas pukul] LT",sameElse:"L"},relativeTime:{future:"dalam %s",past:"%s yang lepas",s:"beberapa saat",m:"seminit",mm:"%d minit",h:"sejam",hh:"%d jam",d:"sehari",dd:"%d hari",M:"sebulan",MM:"%d bulan",y:"setahun",yy:"%d tahun"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("ms",{months:"Januari_Februari_Mac_April_Mei_Jun_Julai_Ogos_September_Oktober_November_Disember".split("_"),monthsShort:"Jan_Feb_Mac_Apr_Mei_Jun_Jul_Ogs_Sep_Okt_Nov_Dis".split("_"),weekdays:"Ahad_Isnin_Selasa_Rabu_Khamis_Jumaat_Sabtu".split("_"),weekdaysShort:"Ahd_Isn_Sel_Rab_Kha_Jum_Sab".split("_"),weekdaysMin:"Ah_Is_Sl_Rb_Km_Jm_Sb".split("_"),longDateFormat:{LT:"HH.mm",LTS:"HH.mm.ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY [pukul] HH.mm",LLLL:"dddd, D MMMM YYYY [pukul] HH.mm"},meridiemParse:/pagi|tengahari|petang|malam/,meridiemHour:function(a,b){return 12===a&&(a=0),"pagi"===b?a:"tengahari"===b?a>=11?a:a+12:"petang"===b||"malam"===b?a+12:void 0},meridiem:function(a,b,c){return 11>a?"pagi":15>a?"tengahari":19>a?"petang":"malam"},calendar:{sameDay:"[Hari ini pukul] LT",nextDay:"[Esok pukul] LT",nextWeek:"dddd [pukul] LT",lastDay:"[Kelmarin pukul] LT",lastWeek:"dddd [lepas pukul] LT",sameElse:"L"},relativeTime:{future:"dalam %s",past:"%s yang lepas",s:"beberapa saat",m:"seminit",mm:"%d minit",h:"sejam",hh:"%d jam",d:"sehari",dd:"%d hari",M:"sebulan",MM:"%d bulan",y:"setahun",yy:"%d tahun"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),{1:"၁",2:"၂",3:"၃",4:"၄",5:"၅",6:"၆",7:"၇",8:"၈",9:"၉",0:"၀"}),ah={"၁":"1","၂":"2","၃":"3","၄":"4","၅":"5","၆":"6","၇":"7","၈":"8","၉":"9","၀":"0"},bh=(kg.defineLocale("my",{months:"ဇန်နဝါရီ_ဖေဖော်ဝါရီ_မတ်_ဧပြီ_မေ_ဇွန်_ဇူလိုင်_သြဂုတ်_စက်တင်ဘာ_အောက်တိုဘာ_နိုဝင်ဘာ_ဒီဇင်ဘာ".split("_"),monthsShort:"ဇန်_ဖေ_မတ်_ပြီ_မေ_ဇွန်_လိုင်_သြ_စက်_အောက်_နို_ဒီ".split("_"),weekdays:"တနင်္ဂနွေ_တနင်္လာ_အင်္ဂါ_ဗုဒ္ဓဟူး_ကြာသပတေး_သောကြာ_စနေ".split("_"),weekdaysShort:"နွေ_လာ_ဂါ_ဟူး_ကြာ_သော_နေ".split("_"),weekdaysMin:"နွေ_လာ_ဂါ_ဟူး_ကြာ_သော_နေ".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[ယနေ.] LT [မှာ]",nextDay:"[မနက်ဖြန်] LT [မှာ]",nextWeek:"dddd LT [မှာ]",lastDay:"[မနေ.က] LT [မှာ]",lastWeek:"[ပြီးခဲ့သော] dddd LT [မှာ]",sameElse:"L"},relativeTime:{future:"လာမည့် %s မှာ",past:"လွန်ခဲ့သော %s က",s:"စက္ကန်.အနည်းငယ်",m:"တစ်မိနစ်",mm:"%d မိနစ်",h:"တစ်နာရီ",hh:"%d နာရီ",d:"တစ်ရက်",dd:"%d ရက်",M:"တစ်လ",MM:"%d လ",y:"တစ်နှစ်",yy:"%d နှစ်"},preparse:function(a){return a.replace(/[၁၂၃၄၅၆၇၈၉၀]/g,function(a){return ah[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return _g[a]})},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("nb",{months:"januar_februar_mars_april_mai_juni_juli_august_september_oktober_november_desember".split("_"),monthsShort:"jan._feb._mars_april_mai_juni_juli_aug._sep._okt._nov._des.".split("_"),monthsParseExact:!0,weekdays:"søndag_mandag_tirsdag_onsdag_torsdag_fredag_lørdag".split("_"),weekdaysShort:"sø._ma._ti._on._to._fr._lø.".split("_"),weekdaysMin:"sø_ma_ti_on_to_fr_lø".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY [kl.] HH:mm",LLLL:"dddd D. MMMM YYYY [kl.] HH:mm"},calendar:{sameDay:"[i dag kl.] LT",nextDay:"[i morgen kl.] LT",nextWeek:"dddd [kl.] LT",lastDay:"[i går kl.] LT",lastWeek:"[forrige] dddd [kl.] LT",sameElse:"L"},relativeTime:{future:"om %s",past:"%s siden",s:"noen sekunder",m:"ett minutt",mm:"%d minutter",h:"en time",hh:"%d timer",d:"en dag",dd:"%d dager",M:"en måned",MM:"%d måneder",y:"ett år",yy:"%d år"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),{1:"१",2:"२",3:"३",4:"४",5:"५",6:"६",7:"७",8:"८",9:"९",0:"०"}),ch={"१":"1","२":"2","३":"3","४":"4","५":"5","६":"6","७":"7","८":"8","९":"9","०":"0"},dh=(kg.defineLocale("ne",{months:"जनवरी_फेब्रुवरी_मार्च_अप्रिल_मई_जुन_जुलाई_अगष्ट_सेप्टेम्बर_अक्टोबर_नोभेम्बर_डिसेम्बर".split("_"),monthsShort:"जन._फेब्रु._मार्च_अप्रि._मई_जुन_जुलाई._अग._सेप्ट._अक्टो._नोभे._डिसे.".split("_"),monthsParseExact:!0,weekdays:"आइतबार_सोमबार_मङ्गलबार_बुधबार_बिहिबार_शुक्रबार_शनिबार".split("_"),weekdaysShort:"आइत._सोम._मङ्गल._बुध._बिहि._शुक्र._शनि.".split("_"),weekdaysMin:"आ._सो._मं._बु._बि._शु._श.".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"Aको h:mm बजे",LTS:"Aको h:mm:ss बजे",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, Aको h:mm बजे",LLLL:"dddd, D MMMM YYYY, Aको h:mm बजे"},preparse:function(a){return a.replace(/[१२३४५६७८९०]/g,function(a){return ch[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return bh[a]})},meridiemParse:/राति|बिहान|दिउँसो|साँझ/,meridiemHour:function(a,b){return 12===a&&(a=0),"राति"===b?4>a?a:a+12:"बिहान"===b?a:"दिउँसो"===b?a>=10?a:a+12:"साँझ"===b?a+12:void 0},meridiem:function(a,b,c){return 3>a?"राति":12>a?"बिहान":16>a?"दिउँसो":20>a?"साँझ":"राति"},calendar:{sameDay:"[आज] LT",nextDay:"[भोलि] LT",nextWeek:"[आउँदो] dddd[,] LT",lastDay:"[हिजो] LT",lastWeek:"[गएको] dddd[,] LT",sameElse:"L"},relativeTime:{future:"%sमा",past:"%s अगाडि",s:"केही क्षण",m:"एक मिनेट",mm:"%d मिनेट",h:"एक घण्टा",hh:"%d घण्टा",d:"एक दिन",dd:"%d दिन",M:"एक महिना",MM:"%d महिना",y:"एक बर्ष",yy:"%d बर्ष"},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),"jan._feb._mrt._apr._mei_jun._jul._aug._sep._okt._nov._dec.".split("_")),eh="jan_feb_mrt_apr_mei_jun_jul_aug_sep_okt_nov_dec".split("_"),fh=(kg.defineLocale("nl",{months:"januari_februari_maart_april_mei_juni_juli_augustus_september_oktober_november_december".split("_"),monthsShort:function(a,b){return/-MMM-/.test(b)?eh[a.month()]:dh[a.month()]},monthsParseExact:!0,weekdays:"zondag_maandag_dinsdag_woensdag_donderdag_vrijdag_zaterdag".split("_"),weekdaysShort:"zo._ma._di._wo._do._vr._za.".split("_"),weekdaysMin:"Zo_Ma_Di_Wo_Do_Vr_Za".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD-MM-YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[vandaag om] LT",nextDay:"[morgen om] LT",nextWeek:"dddd [om] LT",lastDay:"[gisteren om] LT",lastWeek:"[afgelopen] dddd [om] LT",sameElse:"L"},relativeTime:{future:"over %s",past:"%s geleden",s:"een paar seconden",m:"één minuut",mm:"%d minuten",h:"één uur",hh:"%d uur",d:"één dag",dd:"%d dagen",M:"één maand",MM:"%d maanden",y:"één jaar",yy:"%d jaar"},ordinalParse:/\d{1,2}(ste|de)/,ordinal:function(a){return a+(1===a||8===a||a>=20?"ste":"de")},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("nn",{months:"januar_februar_mars_april_mai_juni_juli_august_september_oktober_november_desember".split("_"),monthsShort:"jan_feb_mar_apr_mai_jun_jul_aug_sep_okt_nov_des".split("_"),weekdays:"sundag_måndag_tysdag_onsdag_torsdag_fredag_laurdag".split("_"),weekdaysShort:"sun_mån_tys_ons_tor_fre_lau".split("_"),weekdaysMin:"su_må_ty_on_to_fr_lø".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY [kl.] H:mm",LLLL:"dddd D. MMMM YYYY [kl.] HH:mm"},calendar:{sameDay:"[I dag klokka] LT",nextDay:"[I morgon klokka] LT",nextWeek:"dddd [klokka] LT",lastDay:"[I går klokka] LT",lastWeek:"[Føregåande] dddd [klokka] LT",sameElse:"L"},relativeTime:{future:"om %s",past:"%s sidan",s:"nokre sekund",m:"eit minutt",mm:"%d minutt",h:"ein time",hh:"%d timar",d:"ein dag",dd:"%d dagar",M:"ein månad",MM:"%d månader",y:"eit år",yy:"%d år"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),{1:"੧",2:"੨",3:"੩",4:"੪",5:"੫",6:"੬",7:"੭",8:"੮",9:"੯",0:"੦"}),gh={"੧":"1","੨":"2","੩":"3","੪":"4","੫":"5","੬":"6","੭":"7","੮":"8","੯":"9","੦":"0"},hh=(kg.defineLocale("pa-in",{
// There are months name as per Nanakshahi Calender but they are not used as rigidly in modern Punjabi.
months:"ਜਨਵਰੀ_ਫ਼ਰਵਰੀ_ਮਾਰਚ_ਅਪ੍ਰੈਲ_ਮਈ_ਜੂਨ_ਜੁਲਾਈ_ਅਗਸਤ_ਸਤੰਬਰ_ਅਕਤੂਬਰ_ਨਵੰਬਰ_ਦਸੰਬਰ".split("_"),monthsShort:"ਜਨਵਰੀ_ਫ਼ਰਵਰੀ_ਮਾਰਚ_ਅਪ੍ਰੈਲ_ਮਈ_ਜੂਨ_ਜੁਲਾਈ_ਅਗਸਤ_ਸਤੰਬਰ_ਅਕਤੂਬਰ_ਨਵੰਬਰ_ਦਸੰਬਰ".split("_"),weekdays:"ਐਤਵਾਰ_ਸੋਮਵਾਰ_ਮੰਗਲਵਾਰ_ਬੁਧਵਾਰ_ਵੀਰਵਾਰ_ਸ਼ੁੱਕਰਵਾਰ_ਸ਼ਨੀਚਰਵਾਰ".split("_"),weekdaysShort:"ਐਤ_ਸੋਮ_ਮੰਗਲ_ਬੁਧ_ਵੀਰ_ਸ਼ੁਕਰ_ਸ਼ਨੀ".split("_"),weekdaysMin:"ਐਤ_ਸੋਮ_ਮੰਗਲ_ਬੁਧ_ਵੀਰ_ਸ਼ੁਕਰ_ਸ਼ਨੀ".split("_"),longDateFormat:{LT:"A h:mm ਵਜੇ",LTS:"A h:mm:ss ਵਜੇ",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, A h:mm ਵਜੇ",LLLL:"dddd, D MMMM YYYY, A h:mm ਵਜੇ"},calendar:{sameDay:"[ਅਜ] LT",nextDay:"[ਕਲ] LT",nextWeek:"dddd, LT",lastDay:"[ਕਲ] LT",lastWeek:"[ਪਿਛਲੇ] dddd, LT",sameElse:"L"},relativeTime:{future:"%s ਵਿੱਚ",past:"%s ਪਿਛਲੇ",s:"ਕੁਝ ਸਕਿੰਟ",m:"ਇਕ ਮਿੰਟ",mm:"%d ਮਿੰਟ",h:"ਇੱਕ ਘੰਟਾ",hh:"%d ਘੰਟੇ",d:"ਇੱਕ ਦਿਨ",dd:"%d ਦਿਨ",M:"ਇੱਕ ਮਹੀਨਾ",MM:"%d ਮਹੀਨੇ",y:"ਇੱਕ ਸਾਲ",yy:"%d ਸਾਲ"},preparse:function(a){return a.replace(/[੧੨੩੪੫੬੭੮੯੦]/g,function(a){return gh[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return fh[a]})},
// Punjabi notation for meridiems are quite fuzzy in practice. While there exists
// a rigid notion of a 'Pahar' it is not used as rigidly in modern Punjabi.
meridiemParse:/ਰਾਤ|ਸਵੇਰ|ਦੁਪਹਿਰ|ਸ਼ਾਮ/,meridiemHour:function(a,b){return 12===a&&(a=0),"ਰਾਤ"===b?4>a?a:a+12:"ਸਵੇਰ"===b?a:"ਦੁਪਹਿਰ"===b?a>=10?a:a+12:"ਸ਼ਾਮ"===b?a+12:void 0},meridiem:function(a,b,c){return 4>a?"ਰਾਤ":10>a?"ਸਵੇਰ":17>a?"ਦੁਪਹਿਰ":20>a?"ਸ਼ਾਮ":"ਰਾਤ"},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),"styczeń_luty_marzec_kwiecień_maj_czerwiec_lipiec_sierpień_wrzesień_październik_listopad_grudzień".split("_")),ih="stycznia_lutego_marca_kwietnia_maja_czerwca_lipca_sierpnia_września_października_listopada_grudnia".split("_"),jh=(kg.defineLocale("pl",{months:function(a,b){return""===b?"("+ih[a.month()]+"|"+hh[a.month()]+")":/D MMMM/.test(b)?ih[a.month()]:hh[a.month()]},monthsShort:"sty_lut_mar_kwi_maj_cze_lip_sie_wrz_paź_lis_gru".split("_"),weekdays:"niedziela_poniedziałek_wtorek_środa_czwartek_piątek_sobota".split("_"),weekdaysShort:"nie_pon_wt_śr_czw_pt_sb".split("_"),weekdaysMin:"Nd_Pn_Wt_Śr_Cz_Pt_So".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Dziś o] LT",nextDay:"[Jutro o] LT",nextWeek:"[W] dddd [o] LT",lastDay:"[Wczoraj o] LT",lastWeek:function(){switch(this.day()){case 0:return"[W zeszłą niedzielę o] LT";case 3:return"[W zeszłą środę o] LT";case 6:return"[W zeszłą sobotę o] LT";default:return"[W zeszły] dddd [o] LT"}},sameElse:"L"},relativeTime:{future:"za %s",past:"%s temu",s:"kilka sekund",m:Vd,mm:Vd,h:Vd,hh:Vd,d:"1 dzień",dd:"%d dni",M:"miesiąc",MM:Vd,y:"rok",yy:Vd},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("pt-br",{months:"Janeiro_Fevereiro_Março_Abril_Maio_Junho_Julho_Agosto_Setembro_Outubro_Novembro_Dezembro".split("_"),monthsShort:"Jan_Fev_Mar_Abr_Mai_Jun_Jul_Ago_Set_Out_Nov_Dez".split("_"),weekdays:"Domingo_Segunda-feira_Terça-feira_Quarta-feira_Quinta-feira_Sexta-feira_Sábado".split("_"),weekdaysShort:"Dom_Seg_Ter_Qua_Qui_Sex_Sáb".split("_"),weekdaysMin:"Dom_2ª_3ª_4ª_5ª_6ª_Sáb".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D [de] MMMM [de] YYYY",LLL:"D [de] MMMM [de] YYYY [às] HH:mm",LLLL:"dddd, D [de] MMMM [de] YYYY [às] HH:mm"},calendar:{sameDay:"[Hoje às] LT",nextDay:"[Amanhã às] LT",nextWeek:"dddd [às] LT",lastDay:"[Ontem às] LT",lastWeek:function(){// Saturday + Sunday
return 0===this.day()||6===this.day()?"[Último] dddd [às] LT":"[Última] dddd [às] LT"},sameElse:"L"},relativeTime:{future:"em %s",past:"%s atrás",s:"poucos segundos",m:"um minuto",mm:"%d minutos",h:"uma hora",hh:"%d horas",d:"um dia",dd:"%d dias",M:"um mês",MM:"%d meses",y:"um ano",yy:"%d anos"},ordinalParse:/\d{1,2}º/,ordinal:"%dº"}),kg.defineLocale("pt",{months:"Janeiro_Fevereiro_Março_Abril_Maio_Junho_Julho_Agosto_Setembro_Outubro_Novembro_Dezembro".split("_"),monthsShort:"Jan_Fev_Mar_Abr_Mai_Jun_Jul_Ago_Set_Out_Nov_Dez".split("_"),weekdays:"Domingo_Segunda-Feira_Terça-Feira_Quarta-Feira_Quinta-Feira_Sexta-Feira_Sábado".split("_"),weekdaysShort:"Dom_Seg_Ter_Qua_Qui_Sex_Sáb".split("_"),weekdaysMin:"Dom_2ª_3ª_4ª_5ª_6ª_Sáb".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D [de] MMMM [de] YYYY",LLL:"D [de] MMMM [de] YYYY HH:mm",LLLL:"dddd, D [de] MMMM [de] YYYY HH:mm"},calendar:{sameDay:"[Hoje às] LT",nextDay:"[Amanhã às] LT",nextWeek:"dddd [às] LT",lastDay:"[Ontem às] LT",lastWeek:function(){// Saturday + Sunday
return 0===this.day()||6===this.day()?"[Último] dddd [às] LT":"[Última] dddd [às] LT"},sameElse:"L"},relativeTime:{future:"em %s",past:"há %s",s:"segundos",m:"um minuto",mm:"%d minutos",h:"uma hora",hh:"%d horas",d:"um dia",dd:"%d dias",M:"um mês",MM:"%d meses",y:"um ano",yy:"%d anos"},ordinalParse:/\d{1,2}º/,ordinal:"%dº",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("ro",{months:"ianuarie_februarie_martie_aprilie_mai_iunie_iulie_august_septembrie_octombrie_noiembrie_decembrie".split("_"),monthsShort:"ian._febr._mart._apr._mai_iun._iul._aug._sept._oct._nov._dec.".split("_"),monthsParseExact:!0,weekdays:"duminică_luni_marți_miercuri_joi_vineri_sâmbătă".split("_"),weekdaysShort:"Dum_Lun_Mar_Mie_Joi_Vin_Sâm".split("_"),weekdaysMin:"Du_Lu_Ma_Mi_Jo_Vi_Sâ".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY H:mm",LLLL:"dddd, D MMMM YYYY H:mm"},calendar:{sameDay:"[azi la] LT",nextDay:"[mâine la] LT",nextWeek:"dddd [la] LT",lastDay:"[ieri la] LT",lastWeek:"[fosta] dddd [la] LT",sameElse:"L"},relativeTime:{future:"peste %s",past:"%s în urmă",s:"câteva secunde",m:"un minut",mm:Wd,h:"o oră",hh:Wd,d:"o zi",dd:Wd,M:"o lună",MM:Wd,y:"un an",yy:Wd},week:{dow:1,// Monday is the first day of the week.
doy:7}}),[/^янв/i,/^фев/i,/^мар/i,/^апр/i,/^ма[йя]/i,/^июн/i,/^июл/i,/^авг/i,/^сен/i,/^окт/i,/^ноя/i,/^дек/i]),kh=(kg.defineLocale("ru",{months:{format:"января_февраля_марта_апреля_мая_июня_июля_августа_сентября_октября_ноября_декабря".split("_"),standalone:"январь_февраль_март_апрель_май_июнь_июль_август_сентябрь_октябрь_ноябрь_декабрь".split("_")},monthsShort:{
// по CLDR именно "июл." и "июн.", но какой смысл менять букву на точку ?
format:"янв._февр._мар._апр._мая_июня_июля_авг._сент._окт._нояб._дек.".split("_"),standalone:"янв._февр._март_апр._май_июнь_июль_авг._сент._окт._нояб._дек.".split("_")},weekdays:{standalone:"воскресенье_понедельник_вторник_среда_четверг_пятница_суббота".split("_"),format:"воскресенье_понедельник_вторник_среду_четверг_пятницу_субботу".split("_"),isFormat:/\[ ?[Вв] ?(?:прошлую|следующую|эту)? ?\] ?dddd/},weekdaysShort:"вс_пн_вт_ср_чт_пт_сб".split("_"),weekdaysMin:"вс_пн_вт_ср_чт_пт_сб".split("_"),monthsParse:jh,longMonthsParse:jh,shortMonthsParse:jh,
// полные названия с падежами, по три буквы, для некоторых, по 4 буквы, сокращения с точкой и без точки
monthsRegex:/^(январ[ья]|янв\.?|феврал[ья]|февр?\.?|марта?|мар\.?|апрел[ья]|апр\.?|ма[йя]|июн[ья]|июн\.?|июл[ья]|июл\.?|августа?|авг\.?|сентябр[ья]|сент?\.?|октябр[ья]|окт\.?|ноябр[ья]|нояб?\.?|декабр[ья]|дек\.?)/i,
// копия предыдущего
monthsShortRegex:/^(январ[ья]|янв\.?|феврал[ья]|февр?\.?|марта?|мар\.?|апрел[ья]|апр\.?|ма[йя]|июн[ья]|июн\.?|июл[ья]|июл\.?|августа?|авг\.?|сентябр[ья]|сент?\.?|октябр[ья]|окт\.?|ноябр[ья]|нояб?\.?|декабр[ья]|дек\.?)/i,
// полные названия с падежами
monthsStrictRegex:/^(январ[яь]|феврал[яь]|марта?|апрел[яь]|ма[яй]|июн[яь]|июл[яь]|августа?|сентябр[яь]|октябр[яь]|ноябр[яь]|декабр[яь])/i,
// Выражение, которое соотвествует только сокращённым формам
monthsShortStrictRegex:/^(янв\.|февр?\.|мар[т.]|апр\.|ма[яй]|июн[ья.]|июл[ья.]|авг\.|сент?\.|окт\.|нояб?\.|дек\.)/i,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY г.",LLL:"D MMMM YYYY г., HH:mm",LLLL:"dddd, D MMMM YYYY г., HH:mm"},calendar:{sameDay:"[Сегодня в] LT",nextDay:"[Завтра в] LT",lastDay:"[Вчера в] LT",nextWeek:function(a){if(a.week()===this.week())return 2===this.day()?"[Во] dddd [в] LT":"[В] dddd [в] LT";switch(this.day()){case 0:return"[В следующее] dddd [в] LT";case 1:case 2:case 4:return"[В следующий] dddd [в] LT";case 3:case 5:case 6:return"[В следующую] dddd [в] LT"}},lastWeek:function(a){if(a.week()===this.week())return 2===this.day()?"[Во] dddd [в] LT":"[В] dddd [в] LT";switch(this.day()){case 0:return"[В прошлое] dddd [в] LT";case 1:case 2:case 4:return"[В прошлый] dddd [в] LT";case 3:case 5:case 6:return"[В прошлую] dddd [в] LT"}},sameElse:"L"},relativeTime:{future:"через %s",past:"%s назад",s:"несколько секунд",m:Yd,mm:Yd,h:"час",hh:Yd,d:"день",dd:Yd,M:"месяц",MM:Yd,y:"год",yy:Yd},meridiemParse:/ночи|утра|дня|вечера/i,isPM:function(a){return/^(дня|вечера)$/.test(a)},meridiem:function(a,b,c){return 4>a?"ночи":12>a?"утра":17>a?"дня":"вечера"},ordinalParse:/\d{1,2}-(й|го|я)/,ordinal:function(a,b){switch(b){case"M":case"d":case"DDD":return a+"-й";case"D":return a+"-го";case"w":case"W":return a+"-я";default:return a}},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("se",{months:"ođđajagemánnu_guovvamánnu_njukčamánnu_cuoŋománnu_miessemánnu_geassemánnu_suoidnemánnu_borgemánnu_čakčamánnu_golggotmánnu_skábmamánnu_juovlamánnu".split("_"),monthsShort:"ođđj_guov_njuk_cuo_mies_geas_suoi_borg_čakč_golg_skáb_juov".split("_"),weekdays:"sotnabeaivi_vuossárga_maŋŋebárga_gaskavahkku_duorastat_bearjadat_lávvardat".split("_"),weekdaysShort:"sotn_vuos_maŋ_gask_duor_bear_láv".split("_"),weekdaysMin:"s_v_m_g_d_b_L".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"MMMM D. [b.] YYYY",LLL:"MMMM D. [b.] YYYY [ti.] HH:mm",LLLL:"dddd, MMMM D. [b.] YYYY [ti.] HH:mm"},calendar:{sameDay:"[otne ti] LT",nextDay:"[ihttin ti] LT",nextWeek:"dddd [ti] LT",lastDay:"[ikte ti] LT",lastWeek:"[ovddit] dddd [ti] LT",sameElse:"L"},relativeTime:{future:"%s geažes",past:"maŋit %s",s:"moadde sekunddat",m:"okta minuhta",mm:"%d minuhtat",h:"okta diimmu",hh:"%d diimmut",d:"okta beaivi",dd:"%d beaivvit",M:"okta mánnu",MM:"%d mánut",y:"okta jahki",yy:"%d jagit"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("si",{months:"ජනවාරි_පෙබරවාරි_මාර්තු_අප්‍රේල්_මැයි_ජූනි_ජූලි_අගෝස්තු_සැප්තැම්බර්_ඔක්තෝබර්_නොවැම්බර්_දෙසැම්බර්".split("_"),monthsShort:"ජන_පෙබ_මාර්_අප්_මැයි_ජූනි_ජූලි_අගෝ_සැප්_ඔක්_නොවැ_දෙසැ".split("_"),weekdays:"ඉරිදා_සඳුදා_අඟහරුවාදා_බදාදා_බ්‍රහස්පතින්දා_සිකුරාදා_සෙනසුරාදා".split("_"),weekdaysShort:"ඉරි_සඳු_අඟ_බදා_බ්‍රහ_සිකු_සෙන".split("_"),weekdaysMin:"ඉ_ස_අ_බ_බ්‍ර_සි_සෙ".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"a h:mm",LTS:"a h:mm:ss",L:"YYYY/MM/DD",LL:"YYYY MMMM D",LLL:"YYYY MMMM D, a h:mm",LLLL:"YYYY MMMM D [වැනි] dddd, a h:mm:ss"},calendar:{sameDay:"[අද] LT[ට]",nextDay:"[හෙට] LT[ට]",nextWeek:"dddd LT[ට]",lastDay:"[ඊයේ] LT[ට]",lastWeek:"[පසුගිය] dddd LT[ට]",sameElse:"L"},relativeTime:{future:"%sකින්",past:"%sකට පෙර",s:"තත්පර කිහිපය",m:"මිනිත්තුව",mm:"මිනිත්තු %d",h:"පැය",hh:"පැය %d",d:"දිනය",dd:"දින %d",M:"මාසය",MM:"මාස %d",y:"වසර",yy:"වසර %d"},ordinalParse:/\d{1,2} වැනි/,ordinal:function(a){return a+" වැනි"},meridiemParse:/පෙර වරු|පස් වරු|පෙ.ව|ප.ව./,isPM:function(a){return"ප.ව."===a||"පස් වරු"===a},meridiem:function(a,b,c){return a>11?c?"ප.ව.":"පස් වරු":c?"පෙ.ව.":"පෙර වරු"}}),"január_február_marec_apríl_máj_jún_júl_august_september_október_november_december".split("_")),lh="jan_feb_mar_apr_máj_jún_júl_aug_sep_okt_nov_dec".split("_"),mh=(kg.defineLocale("sk",{months:kh,monthsShort:lh,weekdays:"nedeľa_pondelok_utorok_streda_štvrtok_piatok_sobota".split("_"),weekdaysShort:"ne_po_ut_st_št_pi_so".split("_"),weekdaysMin:"ne_po_ut_st_št_pi_so".split("_"),longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD.MM.YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd D. MMMM YYYY H:mm"},calendar:{sameDay:"[dnes o] LT",nextDay:"[zajtra o] LT",nextWeek:function(){switch(this.day()){case 0:return"[v nedeľu o] LT";case 1:case 2:return"[v] dddd [o] LT";case 3:return"[v stredu o] LT";case 4:return"[vo štvrtok o] LT";case 5:return"[v piatok o] LT";case 6:return"[v sobotu o] LT"}},lastDay:"[včera o] LT",lastWeek:function(){switch(this.day()){case 0:return"[minulú nedeľu o] LT";case 1:case 2:return"[minulý] dddd [o] LT";case 3:return"[minulú stredu o] LT";case 4:case 5:return"[minulý] dddd [o] LT";case 6:return"[minulú sobotu o] LT"}},sameElse:"L"},relativeTime:{future:"za %s",past:"pred %s",s:$d,m:$d,mm:$d,h:$d,hh:$d,d:$d,dd:$d,M:$d,MM:$d,y:$d,yy:$d},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("sl",{months:"januar_februar_marec_april_maj_junij_julij_avgust_september_oktober_november_december".split("_"),monthsShort:"jan._feb._mar._apr._maj._jun._jul._avg._sep._okt._nov._dec.".split("_"),monthsParseExact:!0,weekdays:"nedelja_ponedeljek_torek_sreda_četrtek_petek_sobota".split("_"),weekdaysShort:"ned._pon._tor._sre._čet._pet._sob.".split("_"),weekdaysMin:"ne_po_to_sr_če_pe_so".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD. MM. YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd, D. MMMM YYYY H:mm"},calendar:{sameDay:"[danes ob] LT",nextDay:"[jutri ob] LT",nextWeek:function(){switch(this.day()){case 0:return"[v] [nedeljo] [ob] LT";case 3:return"[v] [sredo] [ob] LT";case 6:return"[v] [soboto] [ob] LT";case 1:case 2:case 4:case 5:return"[v] dddd [ob] LT"}},lastDay:"[včeraj ob] LT",lastWeek:function(){switch(this.day()){case 0:return"[prejšnjo] [nedeljo] [ob] LT";case 3:return"[prejšnjo] [sredo] [ob] LT";case 6:return"[prejšnjo] [soboto] [ob] LT";case 1:case 2:case 4:case 5:return"[prejšnji] dddd [ob] LT"}},sameElse:"L"},relativeTime:{future:"čez %s",past:"pred %s",s:_d,m:_d,mm:_d,h:_d,hh:_d,d:_d,dd:_d,M:_d,MM:_d,y:_d,yy:_d},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("sq",{months:"Janar_Shkurt_Mars_Prill_Maj_Qershor_Korrik_Gusht_Shtator_Tetor_Nëntor_Dhjetor".split("_"),monthsShort:"Jan_Shk_Mar_Pri_Maj_Qer_Kor_Gus_Sht_Tet_Nën_Dhj".split("_"),weekdays:"E Diel_E Hënë_E Martë_E Mërkurë_E Enjte_E Premte_E Shtunë".split("_"),weekdaysShort:"Die_Hën_Mar_Mër_Enj_Pre_Sht".split("_"),weekdaysMin:"D_H_Ma_Më_E_P_Sh".split("_"),weekdaysParseExact:!0,meridiemParse:/PD|MD/,isPM:function(a){return"M"===a.charAt(0)},meridiem:function(a,b,c){return 12>a?"PD":"MD"},longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[Sot në] LT",nextDay:"[Nesër në] LT",nextWeek:"dddd [në] LT",lastDay:"[Dje në] LT",lastWeek:"dddd [e kaluar në] LT",sameElse:"L"},relativeTime:{future:"në %s",past:"%s më parë",s:"disa sekonda",m:"një minutë",mm:"%d minuta",h:"një orë",hh:"%d orë",d:"një ditë",dd:"%d ditë",M:"një muaj",MM:"%d muaj",y:"një vit",yy:"%d vite"},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),{words:{//Different grammatical cases
m:["један минут","једне минуте"],mm:["минут","минуте","минута"],h:["један сат","једног сата"],hh:["сат","сата","сати"],dd:["дан","дана","дана"],MM:["месец","месеца","месеци"],yy:["година","године","година"]},correctGrammaticalCase:function(a,b){return 1===a?b[0]:a>=2&&4>=a?b[1]:b[2]},translate:function(a,b,c){var d=mh.words[c];return 1===c.length?b?d[0]:d[1]:a+" "+mh.correctGrammaticalCase(a,d)}}),nh=(kg.defineLocale("sr-cyrl",{months:"јануар_фебруар_март_април_мај_јун_јул_август_септембар_октобар_новембар_децембар".split("_"),monthsShort:"јан._феб._мар._апр._мај_јун_јул_авг._сеп._окт._нов._дец.".split("_"),monthsParseExact:!0,weekdays:"недеља_понедељак_уторак_среда_четвртак_петак_субота".split("_"),weekdaysShort:"нед._пон._уто._сре._чет._пет._суб.".split("_"),weekdaysMin:"не_по_ут_ср_че_пе_су".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD. MM. YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd, D. MMMM YYYY H:mm"},calendar:{sameDay:"[данас у] LT",nextDay:"[сутра у] LT",nextWeek:function(){switch(this.day()){case 0:return"[у] [недељу] [у] LT";case 3:return"[у] [среду] [у] LT";case 6:return"[у] [суботу] [у] LT";case 1:case 2:case 4:case 5:return"[у] dddd [у] LT"}},lastDay:"[јуче у] LT",lastWeek:function(){var a=["[прошле] [недеље] [у] LT","[прошлог] [понедељка] [у] LT","[прошлог] [уторка] [у] LT","[прошле] [среде] [у] LT","[прошлог] [четвртка] [у] LT","[прошлог] [петка] [у] LT","[прошле] [суботе] [у] LT"];return a[this.day()]},sameElse:"L"},relativeTime:{future:"за %s",past:"пре %s",s:"неколико секунди",m:mh.translate,mm:mh.translate,h:mh.translate,hh:mh.translate,d:"дан",dd:mh.translate,M:"месец",MM:mh.translate,y:"годину",yy:mh.translate},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),{words:{//Different grammatical cases
m:["jedan minut","jedne minute"],mm:["minut","minute","minuta"],h:["jedan sat","jednog sata"],hh:["sat","sata","sati"],dd:["dan","dana","dana"],MM:["mesec","meseca","meseci"],yy:["godina","godine","godina"]},correctGrammaticalCase:function(a,b){return 1===a?b[0]:a>=2&&4>=a?b[1]:b[2]},translate:function(a,b,c){var d=nh.words[c];return 1===c.length?b?d[0]:d[1]:a+" "+nh.correctGrammaticalCase(a,d)}}),oh=(kg.defineLocale("sr",{months:"januar_februar_mart_april_maj_jun_jul_avgust_septembar_oktobar_novembar_decembar".split("_"),monthsShort:"jan._feb._mar._apr._maj_jun_jul_avg._sep._okt._nov._dec.".split("_"),monthsParseExact:!0,weekdays:"nedelja_ponedeljak_utorak_sreda_četvrtak_petak_subota".split("_"),weekdaysShort:"ned._pon._uto._sre._čet._pet._sub.".split("_"),weekdaysMin:"ne_po_ut_sr_če_pe_su".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H:mm",LTS:"H:mm:ss",L:"DD. MM. YYYY",LL:"D. MMMM YYYY",LLL:"D. MMMM YYYY H:mm",LLLL:"dddd, D. MMMM YYYY H:mm"},calendar:{sameDay:"[danas u] LT",nextDay:"[sutra u] LT",nextWeek:function(){switch(this.day()){case 0:return"[u] [nedelju] [u] LT";case 3:return"[u] [sredu] [u] LT";case 6:return"[u] [subotu] [u] LT";case 1:case 2:case 4:case 5:return"[u] dddd [u] LT"}},lastDay:"[juče u] LT",lastWeek:function(){var a=["[prošle] [nedelje] [u] LT","[prošlog] [ponedeljka] [u] LT","[prošlog] [utorka] [u] LT","[prošle] [srede] [u] LT","[prošlog] [četvrtka] [u] LT","[prošlog] [petka] [u] LT","[prošle] [subote] [u] LT"];return a[this.day()]},sameElse:"L"},relativeTime:{future:"za %s",past:"pre %s",s:"nekoliko sekundi",m:nh.translate,mm:nh.translate,h:nh.translate,hh:nh.translate,d:"dan",dd:nh.translate,M:"mesec",MM:nh.translate,y:"godinu",yy:nh.translate},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("ss",{months:"Bhimbidvwane_Indlovana_Indlov'lenkhulu_Mabasa_Inkhwekhweti_Inhlaba_Kholwane_Ingci_Inyoni_Imphala_Lweti_Ingongoni".split("_"),monthsShort:"Bhi_Ina_Inu_Mab_Ink_Inh_Kho_Igc_Iny_Imp_Lwe_Igo".split("_"),weekdays:"Lisontfo_Umsombuluko_Lesibili_Lesitsatfu_Lesine_Lesihlanu_Umgcibelo".split("_"),weekdaysShort:"Lis_Umb_Lsb_Les_Lsi_Lsh_Umg".split("_"),weekdaysMin:"Li_Us_Lb_Lt_Ls_Lh_Ug".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"h:mm A",LTS:"h:mm:ss A",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY h:mm A",LLLL:"dddd, D MMMM YYYY h:mm A"},calendar:{sameDay:"[Namuhla nga] LT",nextDay:"[Kusasa nga] LT",nextWeek:"dddd [nga] LT",lastDay:"[Itolo nga] LT",lastWeek:"dddd [leliphelile] [nga] LT",sameElse:"L"},relativeTime:{future:"nga %s",past:"wenteka nga %s",s:"emizuzwana lomcane",m:"umzuzu",mm:"%d emizuzu",h:"lihora",hh:"%d emahora",d:"lilanga",dd:"%d emalanga",M:"inyanga",MM:"%d tinyanga",y:"umnyaka",yy:"%d iminyaka"},meridiemParse:/ekuseni|emini|entsambama|ebusuku/,meridiem:function(a,b,c){return 11>a?"ekuseni":15>a?"emini":19>a?"entsambama":"ebusuku"},meridiemHour:function(a,b){return 12===a&&(a=0),"ekuseni"===b?a:"emini"===b?a>=11?a:a+12:"entsambama"===b||"ebusuku"===b?0===a?0:a+12:void 0},ordinalParse:/\d{1,2}/,ordinal:"%d",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("sv",{months:"januari_februari_mars_april_maj_juni_juli_augusti_september_oktober_november_december".split("_"),monthsShort:"jan_feb_mar_apr_maj_jun_jul_aug_sep_okt_nov_dec".split("_"),weekdays:"söndag_måndag_tisdag_onsdag_torsdag_fredag_lördag".split("_"),weekdaysShort:"sön_mån_tis_ons_tor_fre_lör".split("_"),weekdaysMin:"sö_må_ti_on_to_fr_lö".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"YYYY-MM-DD",LL:"D MMMM YYYY",LLL:"D MMMM YYYY [kl.] HH:mm",LLLL:"dddd D MMMM YYYY [kl.] HH:mm",lll:"D MMM YYYY HH:mm",llll:"ddd D MMM YYYY HH:mm"},calendar:{sameDay:"[Idag] LT",nextDay:"[Imorgon] LT",lastDay:"[Igår] LT",nextWeek:"[På] dddd LT",lastWeek:"[I] dddd[s] LT",sameElse:"L"},relativeTime:{future:"om %s",past:"för %s sedan",s:"några sekunder",m:"en minut",mm:"%d minuter",h:"en timme",hh:"%d timmar",d:"en dag",dd:"%d dagar",M:"en månad",MM:"%d månader",y:"ett år",yy:"%d år"},ordinalParse:/\d{1,2}(e|a)/,ordinal:function(a){var b=a%10,c=1===~~(a%100/10)?"e":1===b?"a":2===b?"a":"e";return a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("sw",{months:"Januari_Februari_Machi_Aprili_Mei_Juni_Julai_Agosti_Septemba_Oktoba_Novemba_Desemba".split("_"),monthsShort:"Jan_Feb_Mac_Apr_Mei_Jun_Jul_Ago_Sep_Okt_Nov_Des".split("_"),weekdays:"Jumapili_Jumatatu_Jumanne_Jumatano_Alhamisi_Ijumaa_Jumamosi".split("_"),weekdaysShort:"Jpl_Jtat_Jnne_Jtan_Alh_Ijm_Jmos".split("_"),weekdaysMin:"J2_J3_J4_J5_Al_Ij_J1".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[leo saa] LT",nextDay:"[kesho saa] LT",nextWeek:"[wiki ijayo] dddd [saat] LT",lastDay:"[jana] LT",lastWeek:"[wiki iliyopita] dddd [saat] LT",sameElse:"L"},relativeTime:{future:"%s baadaye",past:"tokea %s",s:"hivi punde",m:"dakika moja",mm:"dakika %d",h:"saa limoja",hh:"masaa %d",d:"siku moja",dd:"masiku %d",M:"mwezi mmoja",MM:"miezi %d",y:"mwaka mmoja",yy:"miaka %d"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),{1:"௧",2:"௨",3:"௩",4:"௪",5:"௫",6:"௬",7:"௭",8:"௮",9:"௯",0:"௦"}),ph={"௧":"1","௨":"2","௩":"3","௪":"4","௫":"5","௬":"6","௭":"7","௮":"8","௯":"9","௦":"0"},qh=(kg.defineLocale("ta",{months:"ஜனவரி_பிப்ரவரி_மார்ச்_ஏப்ரல்_மே_ஜூன்_ஜூலை_ஆகஸ்ட்_செப்டெம்பர்_அக்டோபர்_நவம்பர்_டிசம்பர்".split("_"),monthsShort:"ஜனவரி_பிப்ரவரி_மார்ச்_ஏப்ரல்_மே_ஜூன்_ஜூலை_ஆகஸ்ட்_செப்டெம்பர்_அக்டோபர்_நவம்பர்_டிசம்பர்".split("_"),weekdays:"ஞாயிற்றுக்கிழமை_திங்கட்கிழமை_செவ்வாய்கிழமை_புதன்கிழமை_வியாழக்கிழமை_வெள்ளிக்கிழமை_சனிக்கிழமை".split("_"),weekdaysShort:"ஞாயிறு_திங்கள்_செவ்வாய்_புதன்_வியாழன்_வெள்ளி_சனி".split("_"),weekdaysMin:"ஞா_தி_செ_பு_வி_வெ_ச".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, HH:mm",LLLL:"dddd, D MMMM YYYY, HH:mm"},calendar:{sameDay:"[இன்று] LT",nextDay:"[நாளை] LT",nextWeek:"dddd, LT",lastDay:"[நேற்று] LT",lastWeek:"[கடந்த வாரம்] dddd, LT",sameElse:"L"},relativeTime:{future:"%s இல்",past:"%s முன்",s:"ஒரு சில விநாடிகள்",m:"ஒரு நிமிடம்",mm:"%d நிமிடங்கள்",h:"ஒரு மணி நேரம்",hh:"%d மணி நேரம்",d:"ஒரு நாள்",dd:"%d நாட்கள்",M:"ஒரு மாதம்",MM:"%d மாதங்கள்",y:"ஒரு வருடம்",yy:"%d ஆண்டுகள்"},ordinalParse:/\d{1,2}வது/,ordinal:function(a){return a+"வது"},preparse:function(a){return a.replace(/[௧௨௩௪௫௬௭௮௯௦]/g,function(a){return ph[a]})},postformat:function(a){return a.replace(/\d/g,function(a){return oh[a]})},
// refer http://ta.wikipedia.org/s/1er1
meridiemParse:/யாமம்|வைகறை|காலை|நண்பகல்|எற்பாடு|மாலை/,meridiem:function(a,b,c){return 2>a?" யாமம்":6>a?" வைகறை":10>a?" காலை":14>a?" நண்பகல்":18>a?" எற்பாடு":22>a?" மாலை":" யாமம்"},meridiemHour:function(a,b){return 12===a&&(a=0),"யாமம்"===b?2>a?a:a+12:"வைகறை"===b||"காலை"===b?a:"நண்பகல்"===b&&a>=10?a:a+12},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),kg.defineLocale("te",{months:"జనవరి_ఫిబ్రవరి_మార్చి_ఏప్రిల్_మే_జూన్_జూలై_ఆగస్టు_సెప్టెంబర్_అక్టోబర్_నవంబర్_డిసెంబర్".split("_"),monthsShort:"జన._ఫిబ్ర._మార్చి_ఏప్రి._మే_జూన్_జూలై_ఆగ._సెప్._అక్టో._నవ._డిసె.".split("_"),monthsParseExact:!0,weekdays:"ఆదివారం_సోమవారం_మంగళవారం_బుధవారం_గురువారం_శుక్రవారం_శనివారం".split("_"),weekdaysShort:"ఆది_సోమ_మంగళ_బుధ_గురు_శుక్ర_శని".split("_"),weekdaysMin:"ఆ_సో_మం_బు_గు_శు_శ".split("_"),longDateFormat:{LT:"A h:mm",LTS:"A h:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY, A h:mm",LLLL:"dddd, D MMMM YYYY, A h:mm"},calendar:{sameDay:"[నేడు] LT",nextDay:"[రేపు] LT",nextWeek:"dddd, LT",lastDay:"[నిన్న] LT",lastWeek:"[గత] dddd, LT",sameElse:"L"},relativeTime:{future:"%s లో",past:"%s క్రితం",s:"కొన్ని క్షణాలు",m:"ఒక నిమిషం",mm:"%d నిమిషాలు",h:"ఒక గంట",hh:"%d గంటలు",d:"ఒక రోజు",dd:"%d రోజులు",M:"ఒక నెల",MM:"%d నెలలు",y:"ఒక సంవత్సరం",yy:"%d సంవత్సరాలు"},ordinalParse:/\d{1,2}వ/,ordinal:"%dవ",meridiemParse:/రాత్రి|ఉదయం|మధ్యాహ్నం|సాయంత్రం/,meridiemHour:function(a,b){return 12===a&&(a=0),"రాత్రి"===b?4>a?a:a+12:"ఉదయం"===b?a:"మధ్యాహ్నం"===b?a>=10?a:a+12:"సాయంత్రం"===b?a+12:void 0},meridiem:function(a,b,c){return 4>a?"రాత్రి":10>a?"ఉదయం":17>a?"మధ్యాహ్నం":20>a?"సాయంత్రం":"రాత్రి"},week:{dow:0,// Sunday is the first day of the week.
doy:6}}),kg.defineLocale("th",{months:"มกราคม_กุมภาพันธ์_มีนาคม_เมษายน_พฤษภาคม_มิถุนายน_กรกฎาคม_สิงหาคม_กันยายน_ตุลาคม_พฤศจิกายน_ธันวาคม".split("_"),monthsShort:"ม.ค._ก.พ._มี.ค._เม.ย._พ.ค._มิ.ย._ก.ค._ส.ค._ก.ย._ต.ค._พ.ย._ธ.ค.".split("_"),monthsParseExact:!0,weekdays:"อาทิตย์_จันทร์_อังคาร_พุธ_พฤหัสบดี_ศุกร์_เสาร์".split("_"),weekdaysShort:"อาทิตย์_จันทร์_อังคาร_พุธ_พฤหัส_ศุกร์_เสาร์".split("_"),// yes, three characters difference
weekdaysMin:"อา._จ._อ._พ._พฤ._ศ._ส.".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"H นาฬิกา m นาที",LTS:"H นาฬิกา m นาที s วินาที",L:"YYYY/MM/DD",LL:"D MMMM YYYY",LLL:"D MMMM YYYY เวลา H นาฬิกา m นาที",LLLL:"วันddddที่ D MMMM YYYY เวลา H นาฬิกา m นาที"},meridiemParse:/ก่อนเที่ยง|หลังเที่ยง/,isPM:function(a){return"หลังเที่ยง"===a},meridiem:function(a,b,c){return 12>a?"ก่อนเที่ยง":"หลังเที่ยง"},calendar:{sameDay:"[วันนี้ เวลา] LT",nextDay:"[พรุ่งนี้ เวลา] LT",nextWeek:"dddd[หน้า เวลา] LT",lastDay:"[เมื่อวานนี้ เวลา] LT",lastWeek:"[วัน]dddd[ที่แล้ว เวลา] LT",sameElse:"L"},relativeTime:{future:"อีก %s",past:"%sที่แล้ว",s:"ไม่กี่วินาที",m:"1 นาที",mm:"%d นาที",h:"1 ชั่วโมง",hh:"%d ชั่วโมง",d:"1 วัน",dd:"%d วัน",M:"1 เดือน",MM:"%d เดือน",y:"1 ปี",yy:"%d ปี"}}),kg.defineLocale("tl-ph",{months:"Enero_Pebrero_Marso_Abril_Mayo_Hunyo_Hulyo_Agosto_Setyembre_Oktubre_Nobyembre_Disyembre".split("_"),monthsShort:"Ene_Peb_Mar_Abr_May_Hun_Hul_Ago_Set_Okt_Nob_Dis".split("_"),weekdays:"Linggo_Lunes_Martes_Miyerkules_Huwebes_Biyernes_Sabado".split("_"),weekdaysShort:"Lin_Lun_Mar_Miy_Huw_Biy_Sab".split("_"),weekdaysMin:"Li_Lu_Ma_Mi_Hu_Bi_Sab".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"MM/D/YYYY",LL:"MMMM D, YYYY",LLL:"MMMM D, YYYY HH:mm",LLLL:"dddd, MMMM DD, YYYY HH:mm"},calendar:{sameDay:"[Ngayon sa] LT",nextDay:"[Bukas sa] LT",nextWeek:"dddd [sa] LT",lastDay:"[Kahapon sa] LT",lastWeek:"dddd [huling linggo] LT",sameElse:"L"},relativeTime:{future:"sa loob ng %s",past:"%s ang nakalipas",s:"ilang segundo",m:"isang minuto",mm:"%d minuto",h:"isang oras",hh:"%d oras",d:"isang araw",dd:"%d araw",M:"isang buwan",MM:"%d buwan",y:"isang taon",yy:"%d taon"},ordinalParse:/\d{1,2}/,ordinal:function(a){return a},week:{dow:1,// Monday is the first day of the week.
doy:4}}),"pagh_wa’_cha’_wej_loS_vagh_jav_Soch_chorgh_Hut".split("_")),rh=(kg.defineLocale("tlh",{months:"tera’ jar wa’_tera’ jar cha’_tera’ jar wej_tera’ jar loS_tera’ jar vagh_tera’ jar jav_tera’ jar Soch_tera’ jar chorgh_tera’ jar Hut_tera’ jar wa’maH_tera’ jar wa’maH wa’_tera’ jar wa’maH cha’".split("_"),monthsShort:"jar wa’_jar cha’_jar wej_jar loS_jar vagh_jar jav_jar Soch_jar chorgh_jar Hut_jar wa’maH_jar wa’maH wa’_jar wa’maH cha’".split("_"),monthsParseExact:!0,weekdays:"lojmItjaj_DaSjaj_povjaj_ghItlhjaj_loghjaj_buqjaj_ghInjaj".split("_"),weekdaysShort:"lojmItjaj_DaSjaj_povjaj_ghItlhjaj_loghjaj_buqjaj_ghInjaj".split("_"),weekdaysMin:"lojmItjaj_DaSjaj_povjaj_ghItlhjaj_loghjaj_buqjaj_ghInjaj".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[DaHjaj] LT",nextDay:"[wa’leS] LT",nextWeek:"LLL",lastDay:"[wa’Hu’] LT",lastWeek:"LLL",sameElse:"L"},relativeTime:{future:ae,past:be,s:"puS lup",m:"wa’ tup",mm:ce,h:"wa’ rep",hh:ce,d:"wa’ jaj",dd:ce,M:"wa’ jar",MM:ce,y:"wa’ DIS",yy:ce},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),{1:"'inci",5:"'inci",8:"'inci",70:"'inci",80:"'inci",2:"'nci",7:"'nci",20:"'nci",50:"'nci",3:"'üncü",4:"'üncü",100:"'üncü",6:"'ncı",9:"'uncu",10:"'uncu",30:"'uncu",60:"'ıncı",90:"'ıncı"}),sh=(kg.defineLocale("tr",{months:"Ocak_Şubat_Mart_Nisan_Mayıs_Haziran_Temmuz_Ağustos_Eylül_Ekim_Kasım_Aralık".split("_"),monthsShort:"Oca_Şub_Mar_Nis_May_Haz_Tem_Ağu_Eyl_Eki_Kas_Ara".split("_"),weekdays:"Pazar_Pazartesi_Salı_Çarşamba_Perşembe_Cuma_Cumartesi".split("_"),weekdaysShort:"Paz_Pts_Sal_Çar_Per_Cum_Cts".split("_"),weekdaysMin:"Pz_Pt_Sa_Ça_Pe_Cu_Ct".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[bugün saat] LT",nextDay:"[yarın saat] LT",nextWeek:"[haftaya] dddd [saat] LT",lastDay:"[dün] LT",lastWeek:"[geçen hafta] dddd [saat] LT",sameElse:"L"},relativeTime:{future:"%s sonra",past:"%s önce",s:"birkaç saniye",m:"bir dakika",mm:"%d dakika",h:"bir saat",hh:"%d saat",d:"bir gün",dd:"%d gün",M:"bir ay",MM:"%d ay",y:"bir yıl",yy:"%d yıl"},ordinalParse:/\d{1,2}'(inci|nci|üncü|ncı|uncu|ıncı)/,ordinal:function(a){if(0===a)// special case for zero
return a+"'ıncı";var b=a%10,c=a%100-b,d=a>=100?100:null;return a+(rh[b]||rh[c]||rh[d])},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("tzl",{months:"Januar_Fevraglh_Març_Avrïu_Mai_Gün_Julia_Guscht_Setemvar_Listopäts_Noemvar_Zecemvar".split("_"),monthsShort:"Jan_Fev_Mar_Avr_Mai_Gün_Jul_Gus_Set_Lis_Noe_Zec".split("_"),weekdays:"Súladi_Lúneçi_Maitzi_Márcuri_Xhúadi_Viénerçi_Sáturi".split("_"),weekdaysShort:"Súl_Lún_Mai_Már_Xhú_Vié_Sát".split("_"),weekdaysMin:"Sú_Lú_Ma_Má_Xh_Vi_Sá".split("_"),longDateFormat:{LT:"HH.mm",LTS:"HH.mm.ss",L:"DD.MM.YYYY",LL:"D. MMMM [dallas] YYYY",LLL:"D. MMMM [dallas] YYYY HH.mm",LLLL:"dddd, [li] D. MMMM [dallas] YYYY HH.mm"},meridiemParse:/d\'o|d\'a/i,isPM:function(a){return"d'o"===a.toLowerCase()},meridiem:function(a,b,c){return a>11?c?"d'o":"D'O":c?"d'a":"D'A"},calendar:{sameDay:"[oxhi à] LT",nextDay:"[demà à] LT",nextWeek:"dddd [à] LT",lastDay:"[ieiri à] LT",lastWeek:"[sür el] dddd [lasteu à] LT",sameElse:"L"},relativeTime:{future:"osprei %s",past:"ja%s",s:ee,m:ee,mm:ee,h:ee,hh:ee,d:ee,dd:ee,M:ee,MM:ee,y:ee,yy:ee},ordinalParse:/\d{1,2}\./,ordinal:"%d.",week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("tzm-latn",{months:"innayr_brˤayrˤ_marˤsˤ_ibrir_mayyw_ywnyw_ywlywz_ɣwšt_šwtanbir_ktˤwbrˤ_nwwanbir_dwjnbir".split("_"),monthsShort:"innayr_brˤayrˤ_marˤsˤ_ibrir_mayyw_ywnyw_ywlywz_ɣwšt_šwtanbir_ktˤwbrˤ_nwwanbir_dwjnbir".split("_"),weekdays:"asamas_aynas_asinas_akras_akwas_asimwas_asiḍyas".split("_"),weekdaysShort:"asamas_aynas_asinas_akras_akwas_asimwas_asiḍyas".split("_"),weekdaysMin:"asamas_aynas_asinas_akras_akwas_asimwas_asiḍyas".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[asdkh g] LT",nextDay:"[aska g] LT",nextWeek:"dddd [g] LT",lastDay:"[assant g] LT",lastWeek:"dddd [g] LT",sameElse:"L"},relativeTime:{future:"dadkh s yan %s",past:"yan %s",s:"imik",m:"minuḍ",mm:"%d minuḍ",h:"saɛa",hh:"%d tassaɛin",d:"ass",dd:"%d ossan",M:"ayowr",MM:"%d iyyirn",y:"asgas",yy:"%d isgasn"},week:{dow:6,// Saturday is the first day of the week.
doy:12}}),kg.defineLocale("tzm",{months:"ⵉⵏⵏⴰⵢⵔ_ⴱⵕⴰⵢⵕ_ⵎⴰⵕⵚ_ⵉⴱⵔⵉⵔ_ⵎⴰⵢⵢⵓ_ⵢⵓⵏⵢⵓ_ⵢⵓⵍⵢⵓⵣ_ⵖⵓⵛⵜ_ⵛⵓⵜⴰⵏⴱⵉⵔ_ⴽⵟⵓⴱⵕ_ⵏⵓⵡⴰⵏⴱⵉⵔ_ⴷⵓⵊⵏⴱⵉⵔ".split("_"),monthsShort:"ⵉⵏⵏⴰⵢⵔ_ⴱⵕⴰⵢⵕ_ⵎⴰⵕⵚ_ⵉⴱⵔⵉⵔ_ⵎⴰⵢⵢⵓ_ⵢⵓⵏⵢⵓ_ⵢⵓⵍⵢⵓⵣ_ⵖⵓⵛⵜ_ⵛⵓⵜⴰⵏⴱⵉⵔ_ⴽⵟⵓⴱⵕ_ⵏⵓⵡⴰⵏⴱⵉⵔ_ⴷⵓⵊⵏⴱⵉⵔ".split("_"),weekdays:"ⴰⵙⴰⵎⴰⵙ_ⴰⵢⵏⴰⵙ_ⴰⵙⵉⵏⴰⵙ_ⴰⴽⵔⴰⵙ_ⴰⴽⵡⴰⵙ_ⴰⵙⵉⵎⵡⴰⵙ_ⴰⵙⵉⴹⵢⴰⵙ".split("_"),weekdaysShort:"ⴰⵙⴰⵎⴰⵙ_ⴰⵢⵏⴰⵙ_ⴰⵙⵉⵏⴰⵙ_ⴰⴽⵔⴰⵙ_ⴰⴽⵡⴰⵙ_ⴰⵙⵉⵎⵡⴰⵙ_ⴰⵙⵉⴹⵢⴰⵙ".split("_"),weekdaysMin:"ⴰⵙⴰⵎⴰⵙ_ⴰⵢⵏⴰⵙ_ⴰⵙⵉⵏⴰⵙ_ⴰⴽⵔⴰⵙ_ⴰⴽⵡⴰⵙ_ⴰⵙⵉⵎⵡⴰⵙ_ⴰⵙⵉⴹⵢⴰⵙ".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd D MMMM YYYY HH:mm"},calendar:{sameDay:"[ⴰⵙⴷⵅ ⴴ] LT",nextDay:"[ⴰⵙⴽⴰ ⴴ] LT",nextWeek:"dddd [ⴴ] LT",lastDay:"[ⴰⵚⴰⵏⵜ ⴴ] LT",lastWeek:"dddd [ⴴ] LT",sameElse:"L"},relativeTime:{future:"ⴷⴰⴷⵅ ⵙ ⵢⴰⵏ %s",past:"ⵢⴰⵏ %s",s:"ⵉⵎⵉⴽ",m:"ⵎⵉⵏⵓⴺ",mm:"%d ⵎⵉⵏⵓⴺ",h:"ⵙⴰⵄⴰ",hh:"%d ⵜⴰⵙⵙⴰⵄⵉⵏ",d:"ⴰⵙⵙ",dd:"%d oⵙⵙⴰⵏ",M:"ⴰⵢoⵓⵔ",MM:"%d ⵉⵢⵢⵉⵔⵏ",y:"ⴰⵙⴳⴰⵙ",yy:"%d ⵉⵙⴳⴰⵙⵏ"},week:{dow:6,// Saturday is the first day of the week.
doy:12}}),kg.defineLocale("uk",{months:{format:"січня_лютого_березня_квітня_травня_червня_липня_серпня_вересня_жовтня_листопада_грудня".split("_"),standalone:"січень_лютий_березень_квітень_травень_червень_липень_серпень_вересень_жовтень_листопад_грудень".split("_")},monthsShort:"січ_лют_бер_квіт_трав_черв_лип_серп_вер_жовт_лист_груд".split("_"),weekdays:he,weekdaysShort:"нд_пн_вт_ср_чт_пт_сб".split("_"),weekdaysMin:"нд_пн_вт_ср_чт_пт_сб".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD.MM.YYYY",LL:"D MMMM YYYY р.",LLL:"D MMMM YYYY р., HH:mm",LLLL:"dddd, D MMMM YYYY р., HH:mm"},calendar:{sameDay:ie("[Сьогодні "),nextDay:ie("[Завтра "),lastDay:ie("[Вчора "),nextWeek:ie("[У] dddd ["),lastWeek:function(){switch(this.day()){case 0:case 3:case 5:case 6:return ie("[Минулої] dddd [").call(this);case 1:case 2:case 4:return ie("[Минулого] dddd [").call(this)}},sameElse:"L"},relativeTime:{future:"за %s",past:"%s тому",s:"декілька секунд",m:ge,mm:ge,h:"годину",hh:ge,d:"день",dd:ge,M:"місяць",MM:ge,y:"рік",yy:ge},
// M. E.: those two are virtually unused but a user might want to implement them for his/her website for some reason
meridiemParse:/ночі|ранку|дня|вечора/,isPM:function(a){return/^(дня|вечора)$/.test(a)},meridiem:function(a,b,c){return 4>a?"ночі":12>a?"ранку":17>a?"дня":"вечора"},ordinalParse:/\d{1,2}-(й|го)/,ordinal:function(a,b){switch(b){case"M":case"d":case"DDD":case"w":case"W":return a+"-й";case"D":return a+"-го";default:return a}},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("uz",{months:"январ_феврал_март_апрел_май_июн_июл_август_сентябр_октябр_ноябр_декабр".split("_"),monthsShort:"янв_фев_мар_апр_май_июн_июл_авг_сен_окт_ноя_дек".split("_"),weekdays:"Якшанба_Душанба_Сешанба_Чоршанба_Пайшанба_Жума_Шанба".split("_"),weekdaysShort:"Якш_Душ_Сеш_Чор_Пай_Жум_Шан".split("_"),weekdaysMin:"Як_Ду_Се_Чо_Па_Жу_Ша".split("_"),longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"D MMMM YYYY, dddd HH:mm"},calendar:{sameDay:"[Бугун соат] LT [да]",nextDay:"[Эртага] LT [да]",nextWeek:"dddd [куни соат] LT [да]",lastDay:"[Кеча соат] LT [да]",lastWeek:"[Утган] dddd [куни соат] LT [да]",sameElse:"L"},relativeTime:{future:"Якин %s ичида",past:"Бир неча %s олдин",s:"фурсат",m:"бир дакика",mm:"%d дакика",h:"бир соат",hh:"%d соат",d:"бир кун",dd:"%d кун",M:"бир ой",MM:"%d ой",y:"бир йил",yy:"%d йил"},week:{dow:1,// Monday is the first day of the week.
doy:7}}),kg.defineLocale("vi",{months:"tháng 1_tháng 2_tháng 3_tháng 4_tháng 5_tháng 6_tháng 7_tháng 8_tháng 9_tháng 10_tháng 11_tháng 12".split("_"),monthsShort:"Th01_Th02_Th03_Th04_Th05_Th06_Th07_Th08_Th09_Th10_Th11_Th12".split("_"),monthsParseExact:!0,weekdays:"chủ nhật_thứ hai_thứ ba_thứ tư_thứ năm_thứ sáu_thứ bảy".split("_"),weekdaysShort:"CN_T2_T3_T4_T5_T6_T7".split("_"),weekdaysMin:"CN_T2_T3_T4_T5_T6_T7".split("_"),weekdaysParseExact:!0,meridiemParse:/sa|ch/i,isPM:function(a){return/^ch$/i.test(a)},meridiem:function(a,b,c){return 12>a?c?"sa":"SA":c?"ch":"CH"},longDateFormat:{LT:"HH:mm",LTS:"HH:mm:ss",L:"DD/MM/YYYY",LL:"D MMMM [năm] YYYY",LLL:"D MMMM [năm] YYYY HH:mm",LLLL:"dddd, D MMMM [năm] YYYY HH:mm",l:"DD/M/YYYY",ll:"D MMM YYYY",lll:"D MMM YYYY HH:mm",llll:"ddd, D MMM YYYY HH:mm"},calendar:{sameDay:"[Hôm nay lúc] LT",nextDay:"[Ngày mai lúc] LT",nextWeek:"dddd [tuần tới lúc] LT",lastDay:"[Hôm qua lúc] LT",lastWeek:"dddd [tuần rồi lúc] LT",sameElse:"L"},relativeTime:{future:"%s tới",past:"%s trước",s:"vài giây",m:"một phút",mm:"%d phút",h:"một giờ",hh:"%d giờ",d:"một ngày",dd:"%d ngày",M:"một tháng",MM:"%d tháng",y:"một năm",yy:"%d năm"},ordinalParse:/\d{1,2}/,ordinal:function(a){return a},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("x-pseudo",{months:"J~áñúá~rý_F~ébrú~árý_~Márc~h_Áp~ríl_~Máý_~Júñé~_Júl~ý_Áú~gúst~_Sép~témb~ér_Ó~ctób~ér_Ñ~óvém~bér_~Décé~mbér".split("_"),monthsShort:"J~áñ_~Féb_~Már_~Ápr_~Máý_~Júñ_~Júl_~Áúg_~Sép_~Óct_~Ñóv_~Déc".split("_"),monthsParseExact:!0,weekdays:"S~úñdá~ý_Mó~ñdáý~_Túé~sdáý~_Wéd~ñésd~áý_T~húrs~dáý_~Fríd~áý_S~átúr~dáý".split("_"),weekdaysShort:"S~úñ_~Móñ_~Túé_~Wéd_~Thú_~Frí_~Sát".split("_"),weekdaysMin:"S~ú_Mó~_Tú_~Wé_T~h_Fr~_Sá".split("_"),weekdaysParseExact:!0,longDateFormat:{LT:"HH:mm",L:"DD/MM/YYYY",LL:"D MMMM YYYY",LLL:"D MMMM YYYY HH:mm",LLLL:"dddd, D MMMM YYYY HH:mm"},calendar:{sameDay:"[T~ódá~ý át] LT",nextDay:"[T~ómó~rró~w át] LT",nextWeek:"dddd [át] LT",lastDay:"[Ý~ést~érdá~ý át] LT",lastWeek:"[L~ást] dddd [át] LT",sameElse:"L"},relativeTime:{future:"í~ñ %s",past:"%s á~gó",s:"á ~féw ~sécó~ñds",m:"á ~míñ~úté",mm:"%d m~íñú~tés",h:"á~ñ hó~úr",hh:"%d h~óúrs",d:"á ~dáý",dd:"%d d~áýs",M:"á ~móñ~th",MM:"%d m~óñt~hs",y:"á ~ýéár",yy:"%d ý~éárs"},ordinalParse:/\d{1,2}(th|st|nd|rd)/,ordinal:function(a){var b=a%10,c=1===~~(a%100/10)?"th":1===b?"st":2===b?"nd":3===b?"rd":"th";return a+c},week:{dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("zh-cn",{months:"一月_二月_三月_四月_五月_六月_七月_八月_九月_十月_十一月_十二月".split("_"),monthsShort:"1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),weekdays:"星期日_星期一_星期二_星期三_星期四_星期五_星期六".split("_"),weekdaysShort:"周日_周一_周二_周三_周四_周五_周六".split("_"),weekdaysMin:"日_一_二_三_四_五_六".split("_"),longDateFormat:{LT:"Ah点mm分",LTS:"Ah点m分s秒",L:"YYYY-MM-DD",LL:"YYYY年MMMD日",LLL:"YYYY年MMMD日Ah点mm分",LLLL:"YYYY年MMMD日ddddAh点mm分",l:"YYYY-MM-DD",ll:"YYYY年MMMD日",lll:"YYYY年MMMD日Ah点mm分",llll:"YYYY年MMMD日ddddAh点mm分"},meridiemParse:/凌晨|早上|上午|中午|下午|晚上/,meridiemHour:function(a,b){return 12===a&&(a=0),"凌晨"===b||"早上"===b||"上午"===b?a:"下午"===b||"晚上"===b?a+12:a>=11?a:a+12},meridiem:function(a,b,c){var d=100*a+b;return 600>d?"凌晨":900>d?"早上":1130>d?"上午":1230>d?"中午":1800>d?"下午":"晚上"},calendar:{sameDay:function(){return 0===this.minutes()?"[今天]Ah[点整]":"[今天]LT"},nextDay:function(){return 0===this.minutes()?"[明天]Ah[点整]":"[明天]LT"},lastDay:function(){return 0===this.minutes()?"[昨天]Ah[点整]":"[昨天]LT"},nextWeek:function(){var a,b;return a=kg().startOf("week"),b=this.diff(a,"days")>=7?"[下]":"[本]",0===this.minutes()?b+"dddAh点整":b+"dddAh点mm"},lastWeek:function(){var a,b;return a=kg().startOf("week"),b=this.unix()<a.unix()?"[上]":"[本]",0===this.minutes()?b+"dddAh点整":b+"dddAh点mm"},sameElse:"LL"},ordinalParse:/\d{1,2}(日|月|周)/,ordinal:function(a,b){switch(b){case"d":case"D":case"DDD":return a+"日";case"M":return a+"月";case"w":case"W":return a+"周";default:return a}},relativeTime:{future:"%s内",past:"%s前",s:"几秒",m:"1 分钟",mm:"%d 分钟",h:"1 小时",hh:"%d 小时",d:"1 天",dd:"%d 天",M:"1 个月",MM:"%d 个月",y:"1 年",yy:"%d 年"},week:{
// GB/T 7408-1994《数据元和交换格式·信息交换·日期和时间表示法》与ISO 8601:1988等效
dow:1,// Monday is the first day of the week.
doy:4}}),kg.defineLocale("zh-tw",{months:"一月_二月_三月_四月_五月_六月_七月_八月_九月_十月_十一月_十二月".split("_"),monthsShort:"1月_2月_3月_4月_5月_6月_7月_8月_9月_10月_11月_12月".split("_"),weekdays:"星期日_星期一_星期二_星期三_星期四_星期五_星期六".split("_"),weekdaysShort:"週日_週一_週二_週三_週四_週五_週六".split("_"),weekdaysMin:"日_一_二_三_四_五_六".split("_"),longDateFormat:{LT:"Ah點mm分",LTS:"Ah點m分s秒",L:"YYYY年MMMD日",LL:"YYYY年MMMD日",LLL:"YYYY年MMMD日Ah點mm分",LLLL:"YYYY年MMMD日ddddAh點mm分",l:"YYYY年MMMD日",ll:"YYYY年MMMD日",lll:"YYYY年MMMD日Ah點mm分",llll:"YYYY年MMMD日ddddAh點mm分"},meridiemParse:/凌晨|早上|上午|中午|下午|晚上/,meridiemHour:function(a,b){return 12===a&&(a=0),"凌晨"===b||"早上"===b||"上午"===b?a:"中午"===b?a>=11?a:a+12:"下午"===b||"晚上"===b?a+12:void 0},meridiem:function(a,b,c){var d=100*a+b;return 600>d?"凌晨":900>d?"早上":1130>d?"上午":1230>d?"中午":1800>d?"下午":"晚上"},calendar:{sameDay:"[今天]LT",nextDay:"[明天]LT",nextWeek:"[下]ddddLT",lastDay:"[昨天]LT",lastWeek:"[上]ddddLT",sameElse:"L"},ordinalParse:/\d{1,2}(日|月|週)/,ordinal:function(a,b){switch(b){case"d":case"D":case"DDD":return a+"日";case"M":return a+"月";case"w":case"W":return a+"週";default:return a}},relativeTime:{future:"%s內",past:"%s前",s:"幾秒",m:"1 分鐘",mm:"%d 分鐘",h:"1 小時",hh:"%d 小時",d:"1 天",dd:"%d 天",M:"1 個月",MM:"%d 個月",y:"1 年",yy:"%d 年"}}),kg);return sh.locale("en"),sh});

//! moment-timezone.js
//! version : 0.5.5
//! author : Tim Wood
//! license : MIT
//! github.com/moment/moment-timezone
!function(a,b){"use strict";"function"==typeof define&&define.amd?define(["moment"],b):"object"==typeof module&&module.exports?module.exports=b(require("moment")):b(a.moment)}(this,function(a){"use strict";function b(a){return a>96?a-87:a>64?a-29:a-48}function c(a){var c,d=0,e=a.split("."),f=e[0],g=e[1]||"",h=1,i=0,j=1;for(45===a.charCodeAt(0)&&(d=1,j=-1),d;d<f.length;d++)c=b(f.charCodeAt(d)),i=60*i+c;for(d=0;d<g.length;d++)h/=60,c=b(g.charCodeAt(d)),i+=c*h;return i*j}function d(a){for(var b=0;b<a.length;b++)a[b]=c(a[b])}function e(a,b){for(var c=0;c<b;c++)a[c]=Math.round((a[c-1]||0)+6e4*a[c]);a[b-1]=1/0}function f(a,b){var c,d=[];for(c=0;c<b.length;c++)d[c]=a[b[c]];return d}function g(a){var b=a.split("|"),c=b[2].split(" "),g=b[3].split(""),h=b[4].split(" ");return d(c),d(g),d(h),e(h,g.length),{name:b[0],abbrs:f(b[1].split(" "),g),offsets:f(c,g),untils:h,population:0|b[5]}}function h(a){a&&this._set(g(a))}function i(a){var b=a.toTimeString(),c=b.match(/\([a-z ]+\)/i);c&&c[0]?(c=c[0].match(/[A-Z]/g),c=c?c.join(""):void 0):(c=b.match(/[A-Z]{3,5}/g),c=c?c[0]:void 0),"GMT"===c&&(c=void 0),this.at=+a,this.abbr=c,this.offset=a.getTimezoneOffset()}function j(a){this.zone=a,this.offsetScore=0,this.abbrScore=0}function k(a,b){for(var c,d;d=6e4*((b.at-a.at)/12e4|0);)c=new i(new Date(a.at+d)),c.offset===a.offset?a=c:b=c;return a}function l(){var a,b,c,d=(new Date).getFullYear()-2,e=new i(new Date(d,0,1)),f=[e];for(c=1;c<48;c++)b=new i(new Date(d,c,1)),b.offset!==e.offset&&(a=k(e,b),f.push(a),f.push(new i(new Date(a.at+6e4)))),e=b;for(c=0;c<4;c++)f.push(new i(new Date(d+c,0,1))),f.push(new i(new Date(d+c,6,1)));return f}function m(a,b){return a.offsetScore!==b.offsetScore?a.offsetScore-b.offsetScore:a.abbrScore!==b.abbrScore?a.abbrScore-b.abbrScore:b.zone.population-a.zone.population}function n(a,b){var c,e;for(d(b),c=0;c<b.length;c++)e=b[c],I[e]=I[e]||{},I[e][a]=!0}function o(a){var b,c,d,e=a.length,f={},g=[];for(b=0;b<e;b++){d=I[a[b].offset]||{};for(c in d)d.hasOwnProperty(c)&&(f[c]=!0)}for(b in f)f.hasOwnProperty(b)&&g.push(H[b]);return g}function p(){try{var a=Intl.DateTimeFormat().resolvedOptions().timeZone;if(a){var b=H[r(a)];if(b)return b;z("Moment Timezone found "+a+" from the Intl api, but did not have that data loaded.")}}catch(c){}var d,e,f,g=l(),h=g.length,i=o(g),k=[];for(e=0;e<i.length;e++){for(d=new j(t(i[e]),h),f=0;f<h;f++)d.scoreOffsetAt(g[f]);k.push(d)}return k.sort(m),k.length>0?k[0].zone.name:void 0}function q(a){return D&&!a||(D=p()),D}function r(a){return(a||"").toLowerCase().replace(/\//g,"_")}function s(a){var b,c,d,e;for("string"==typeof a&&(a=[a]),b=0;b<a.length;b++)d=a[b].split("|"),c=d[0],e=r(c),F[e]=a[b],H[e]=c,d[5]&&n(e,d[2].split(" "))}function t(a,b){a=r(a);var c,d=F[a];return d instanceof h?d:"string"==typeof d?(d=new h(d),F[a]=d,d):G[a]&&b!==t&&(c=t(G[a],t))?(d=F[a]=new h,d._set(c),d.name=H[a],d):null}function u(){var a,b=[];for(a in H)H.hasOwnProperty(a)&&(F[a]||F[G[a]])&&H[a]&&b.push(H[a]);return b.sort()}function v(a){var b,c,d,e;for("string"==typeof a&&(a=[a]),b=0;b<a.length;b++)c=a[b].split("|"),d=r(c[0]),e=r(c[1]),G[d]=e,H[d]=c[0],G[e]=d,H[e]=c[1]}function w(a){s(a.zones),v(a.links),A.dataVersion=a.version}function x(a){return x.didShowError||(x.didShowError=!0,z("moment.tz.zoneExists('"+a+"') has been deprecated in favor of !moment.tz.zone('"+a+"')")),!!t(a)}function y(a){return!(!a._a||void 0!==a._tzm)}function z(a){"undefined"!=typeof console&&"function"==typeof console.error&&console.error(a)}function A(b){var c=Array.prototype.slice.call(arguments,0,-1),d=arguments[arguments.length-1],e=t(d),f=a.utc.apply(null,c);return e&&!a.isMoment(b)&&y(f)&&f.add(e.parse(f),"minutes"),f.tz(d),f}function B(a){return function(){return this._z?this._z.abbr(this):a.call(this)}}function C(a){return function(){return this._z=null,a.apply(this,arguments)}}if(void 0!==a.tz)return z("Moment Timezone "+a.tz.version+" was already loaded "+(a.tz.dataVersion?"with data from ":"without any data")+a.tz.dataVersion),a;var D,E="0.5.5",F={},G={},H={},I={},J=a.version.split("."),K=+J[0],L=+J[1];(K<2||2===K&&L<6)&&z("Moment Timezone requires Moment.js >= 2.6.0. You are using Moment.js "+a.version+". See momentjs.com"),h.prototype={_set:function(a){this.name=a.name,this.abbrs=a.abbrs,this.untils=a.untils,this.offsets=a.offsets,this.population=a.population},_index:function(a){var b,c=+a,d=this.untils;for(b=0;b<d.length;b++)if(c<d[b])return b},parse:function(a){var b,c,d,e,f=+a,g=this.offsets,h=this.untils,i=h.length-1;for(e=0;e<i;e++)if(b=g[e],c=g[e+1],d=g[e?e-1:e],b<c&&A.moveAmbiguousForward?b=c:b>d&&A.moveInvalidForward&&(b=d),f<h[e]-6e4*b)return g[e];return g[i]},abbr:function(a){return this.abbrs[this._index(a)]},offset:function(a){return this.offsets[this._index(a)]}},j.prototype.scoreOffsetAt=function(a){this.offsetScore+=Math.abs(this.zone.offset(a.at)-a.offset),this.zone.abbr(a.at).replace(/[^A-Z]/g,"")!==a.abbr&&this.abbrScore++},A.version=E,A.dataVersion="",A._zones=F,A._links=G,A._names=H,A.add=s,A.link=v,A.load=w,A.zone=t,A.zoneExists=x,A.guess=q,A.names=u,A.Zone=h,A.unpack=g,A.unpackBase60=c,A.needsOffset=y,A.moveInvalidForward=!0,A.moveAmbiguousForward=!1;var M=a.fn;a.tz=A,a.defaultZone=null,a.updateOffset=function(b,c){var d,e=a.defaultZone;void 0===b._z&&(e&&y(b)&&!b._isUTC&&(b._d=a.utc(b._a)._d,b.utc().add(e.parse(b),"minutes")),b._z=e),b._z&&(d=b._z.offset(b),Math.abs(d)<16&&(d/=60),void 0!==b.utcOffset?b.utcOffset(-d,c):b.zone(d,c))},M.tz=function(b){return b?(this._z=t(b),this._z?a.updateOffset(this):z("Moment Timezone has no data for "+b+". See http://momentjs.com/timezone/docs/#/data-loading/."),this):this._z?this._z.name:void 0},M.zoneName=B(M.zoneName),M.zoneAbbr=B(M.zoneAbbr),M.utc=C(M.utc),a.tz.setDefault=function(b){return(K<2||2===K&&L<9)&&z("Moment Timezone setDefault() requires Moment.js >= 2.9.0. You are using Moment.js "+a.version+"."),a.defaultZone=b?t(b):null,a};var N=a.momentProperties;return"[object Array]"===Object.prototype.toString.call(N)?(N.push("_z"),N.push("_a")):N&&(N._z=null),w({version:"2016f",zones:["Africa/Abidjan|GMT|0|0||48e5","Africa/Khartoum|EAT|-30|0||51e5","Africa/Algiers|CET|-10|0||26e5","Africa/Lagos|WAT|-10|0||17e6","Africa/Maputo|CAT|-20|0||26e5","Africa/Cairo|EET EEST|-20 -30|010101010|1Cby0 Fb0 c10 8n0 8Nd0 gL0 e10 mn0|15e6","Africa/Casablanca|WET WEST|0 -10|01010101010101010101010101010101010101010|1Cco0 Db0 1zd0 Lz0 1Nf0 wM0 co0 go0 1o00 s00 dA0 vc0 11A0 A00 e00 y00 11A0 uM0 e00 Dc0 11A0 s00 e00 IM0 WM0 mo0 gM0 LA0 WM0 jA0 e00 Rc0 11A0 e00 e00 U00 11A0 8o0 e00 11A0|32e5","Europe/Paris|CET CEST|-10 -20|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|11e6","Africa/Johannesburg|SAST|-20|0||84e5","Africa/Tripoli|EET CET CEST|-20 -10 -20|0120|1IlA0 TA0 1o00|11e5","Africa/Windhoek|WAST WAT|-20 -10|01010101010101010101010|1C1c0 11B0 1nX0 11B0 1nX0 11B0 1qL0 WN0 1qL0 11B0 1nX0 11B0 1nX0 11B0 1nX0 11B0 1nX0 11B0 1qL0 WN0 1qL0 11B0|32e4","America/Adak|HST HDT|a0 90|01010101010101010101010|1BR00 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|326","America/Anchorage|AKST AKDT|90 80|01010101010101010101010|1BQX0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|30e4","America/Santo_Domingo|AST|40|0||29e5","America/Araguaina|BRT BRST|30 20|010|1IdD0 Lz0|14e4","America/Argentina/Buenos_Aires|ART|30|0|","America/Asuncion|PYST PYT|30 40|01010101010101010101010|1C430 1a10 1fz0 1a10 1fz0 1cN0 17b0 1ip0 17b0 1ip0 17b0 1ip0 19X0 1fB0 19X0 1fB0 19X0 1ip0 17b0 1ip0 17b0 1ip0|28e5","America/Panama|EST|50|0||15e5","America/Bahia|BRT BRST|30 20|010|1FJf0 Rb0|27e5","America/Bahia_Banderas|MST CDT CST|70 50 60|01212121212121212121212|1C1l0 1nW0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0|84e3","America/Fortaleza|BRT|30|0||34e5","America/Managua|CST|60|0||22e5","America/Manaus|AMT|40|0||19e5","America/Bogota|COT|50|0||90e5","America/Denver|MST MDT|70 60|01010101010101010101010|1BQV0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|26e5","America/Campo_Grande|AMST AMT|30 40|01010101010101010101010|1BIr0 1zd0 On0 1zd0 Rb0 1zd0 Lz0 1C10 Lz0 1C10 On0 1zd0 On0 1zd0 On0 1zd0 On0 1C10 Lz0 1C10 Lz0 1C10|77e4","America/Cancun|CST CDT EST|60 50 50|010101010102|1C1k0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 Dd0|63e4","America/Caracas|VET VET|4u 40|01|1QMT0|29e5","America/Cayenne|GFT|30|0||58e3","America/Chicago|CST CDT|60 50|01010101010101010101010|1BQU0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|92e5","America/Chihuahua|MST MDT|70 60|01010101010101010101010|1C1l0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0|81e4","America/Phoenix|MST|70|0||42e5","America/Los_Angeles|PST PDT|80 70|01010101010101010101010|1BQW0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|15e6","America/New_York|EST EDT|50 40|01010101010101010101010|1BQT0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|21e6","America/Rio_Branco|AMT ACT|40 50|01|1KLE0|31e4","America/Fort_Nelson|PST PDT MST|80 70 70|010101010102|1BQW0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0|39e2","America/Halifax|AST ADT|40 30|01010101010101010101010|1BQS0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|39e4","America/Godthab|WGT WGST|30 20|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|17e3","America/Goose_Bay|AST ADT|40 30|01010101010101010101010|1BQQ1 1zb0 Op0 1zcX Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|76e2","America/Grand_Turk|EST EDT AST|50 40 40|0101010101012|1BQT0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|37e2","America/Guayaquil|ECT|50|0||27e5","America/Guyana|GYT|40|0||80e4","America/Havana|CST CDT|50 40|01010101010101010101010|1BQR0 1wo0 U00 1zc0 U00 1qM0 Oo0 1zc0 Oo0 1zc0 Oo0 1zc0 Rc0 1zc0 Oo0 1zc0 Oo0 1zc0 Oo0 1zc0 Oo0 1zc0|21e5","America/La_Paz|BOT|40|0||19e5","America/Lima|PET|50|0||11e6","America/Mexico_City|CST CDT|60 50|01010101010101010101010|1C1k0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0 14p0 1lb0 14p0 1nX0 11B0 1nX0 11B0 1nX0 14p0 1lb0 14p0 1lb0|20e6","America/Metlakatla|PST AKST AKDT|80 90 80|012121212121|1PAa0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|14e2","America/Miquelon|PMST PMDT|30 20|01010101010101010101010|1BQR0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|61e2","America/Montevideo|UYST UYT|20 30|010101010101|1BQQ0 1ld0 14n0 1ld0 14n0 1o10 11z0 1o10 11z0 1o10 11z0|17e5","America/Noronha|FNT|20|0||30e2","America/North_Dakota/Beulah|MST MDT CST CDT|70 60 60 50|01232323232323232323232|1BQV0 1zb0 Oo0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0","America/Paramaribo|SRT|30|0||24e4","America/Port-au-Prince|EST EDT|50 40|010101010|1GI70 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|23e5","America/Santiago|CLST CLT|30 40|010101010101010101010|1C1f0 1fB0 1nX0 G10 1EL0 Op0 1zb0 Rd0 1wn0 Rd0 46n0 Ap0 1Nb0 Ap0 1Nb0 Ap0 1Nb0 Ap0 1Nb0 Ap0|62e5","America/Sao_Paulo|BRST BRT|20 30|01010101010101010101010|1BIq0 1zd0 On0 1zd0 Rb0 1zd0 Lz0 1C10 Lz0 1C10 On0 1zd0 On0 1zd0 On0 1zd0 On0 1C10 Lz0 1C10 Lz0 1C10|20e6","America/Scoresbysund|EGT EGST|10 0|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|452","America/St_Johns|NST NDT|3u 2u|01010101010101010101010|1BQPv 1zb0 Op0 1zcX Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Rd0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0 Op0 1zb0|11e4","Antarctica/Casey|CAST AWST|-b0 -80|0101|1BN30 40P0 KL0|10","Antarctica/Davis|DAVT DAVT|-50 -70|0101|1BPw0 3Wn0 KN0|70","Antarctica/DumontDUrville|DDUT|-a0|0||80","Antarctica/Macquarie|AEDT MIST|-b0 -b0|01|1C140|1","Antarctica/Mawson|MAWT|-50|0||60","Pacific/Auckland|NZDT NZST|-d0 -c0|01010101010101010101010|1C120 1a00 1fA0 1a00 1fA0 1cM0 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1cM0 1fA0 1a00 1fA0 1a00|14e5","Antarctica/Rothera|ROTT|30|0||130","Antarctica/Syowa|SYOT|-30|0||20","Antarctica/Troll|UTC CEST|0 -20|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|40","Antarctica/Vostok|VOST|-60|0||25","Asia/Baghdad|AST|-30|0||66e5","Asia/Almaty|+06|-60|0||15e5","Asia/Amman|EET EEST|-20 -30|010101010101010101010|1BVy0 1qM0 11A0 1o00 11A0 4bX0 Dd0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0|25e5","Asia/Anadyr|ANAT ANAST ANAT|-c0 -c0 -b0|0120|1BWe0 1qN0 WM0|13e3","Asia/Aqtobe|+05|-50|0||27e4","Asia/Ashgabat|TMT|-50|0||41e4","Asia/Baku|AZT AZST|-40 -50|0101010101010|1BWo0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00|27e5","Asia/Bangkok|ICT|-70|0||15e6","Asia/Barnaul|+06 +07|-60 -70|010101|1BWk0 1qM0 WM0 8Hz0 3rd0","Asia/Beirut|EET EEST|-20 -30|01010101010101010101010|1BWm0 1qL0 WN0 1qL0 WN0 1qL0 11B0 1nX0 11B0 1nX0 11B0 1nX0 11B0 1qL0 WN0 1qL0 WN0 1qL0 11B0 1nX0 11B0 1nX0|22e5","Asia/Bishkek|KGT|-60|0||87e4","Asia/Brunei|BNT|-80|0||42e4","Asia/Kolkata|IST|-5u|0||15e6","Asia/Chita|YAKT YAKST YAKT IRKT|-90 -a0 -a0 -80|010230|1BWh0 1qM0 WM0 8Hz0 3re0|33e4","Asia/Choibalsan|CHOT CHOST|-80 -90|0101010101010|1O8G0 1cJ0 1cP0 1cJ0 1cP0 1fx0 1cP0 1cJ0 1cP0 1cJ0 1cP0 1cJ0|38e3","Asia/Shanghai|CST|-80|0||23e6","Asia/Dhaka|BDT|-60|0||16e6","Asia/Damascus|EET EEST|-20 -30|01010101010101010101010|1C0m0 1nX0 11B0 1nX0 11B0 1nX0 11B0 1nX0 11B0 1qL0 WN0 1qL0 WN0 1qL0 11B0 1nX0 11B0 1nX0 11B0 1nX0 11B0 1qL0|26e5","Asia/Dili|TLT|-90|0||19e4","Asia/Dubai|GST|-40|0||39e5","Asia/Dushanbe|TJT|-50|0||76e4","Asia/Gaza|EET EEST|-20 -30|01010101010101010101010|1BVW1 SKX 1xd1 MKX 1AN0 1a00 1fA0 1cL0 1cN0 1nX0 1210 1nz0 1220 1ny0 1220 1qm0 1220 1ny0 1220 1ny0 1220 1ny0|18e5","Asia/Hebron|EET EEST|-20 -30|0101010101010101010101010|1BVy0 Tb0 1xd1 MKX bB0 cn0 1cN0 1a00 1fA0 1cL0 1cN0 1nX0 1210 1nz0 1220 1ny0 1220 1qm0 1220 1ny0 1220 1ny0 1220 1ny0|25e4","Asia/Hong_Kong|HKT|-80|0||73e5","Asia/Hovd|HOVT HOVST|-70 -80|0101010101010|1O8H0 1cJ0 1cP0 1cJ0 1cP0 1fx0 1cP0 1cJ0 1cP0 1cJ0 1cP0 1cJ0|81e3","Asia/Irkutsk|IRKT IRKST IRKT|-80 -90 -90|01020|1BWi0 1qM0 WM0 8Hz0|60e4","Europe/Istanbul|EET EEST|-20 -30|01010101010101010101010|1BWp0 1qM0 Xc0 1qo0 WM0 1qM0 11A0 1o00 1200 1nA0 11A0 1tA0 U00 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|13e6","Asia/Jakarta|WIB|-70|0||31e6","Asia/Jayapura|WIT|-90|0||26e4","Asia/Jerusalem|IST IDT|-20 -30|01010101010101010101010|1BVA0 17X0 1kp0 1dz0 1c10 1aL0 1eN0 1oL0 10N0 1oL0 10N0 1oL0 10N0 1rz0 W10 1rz0 W10 1rz0 10N0 1oL0 10N0 1oL0|81e4","Asia/Kabul|AFT|-4u|0||46e5","Asia/Kamchatka|PETT PETST PETT|-c0 -c0 -b0|0120|1BWe0 1qN0 WM0|18e4","Asia/Karachi|PKT|-50|0||24e6","Asia/Urumqi|XJT|-60|0||32e5","Asia/Kathmandu|NPT|-5J|0||12e5","Asia/Khandyga|VLAT VLAST VLAT YAKT YAKT|-a0 -b0 -b0 -a0 -90|010234|1BWg0 1qM0 WM0 17V0 7zD0|66e2","Asia/Krasnoyarsk|KRAT KRAST KRAT|-70 -80 -80|01020|1BWj0 1qM0 WM0 8Hz0|10e5","Asia/Kuala_Lumpur|MYT|-80|0||71e5","Asia/Magadan|MAGT MAGST MAGT MAGT|-b0 -c0 -c0 -a0|010230|1BWf0 1qM0 WM0 8Hz0 3Cq0|95e3","Asia/Makassar|WITA|-80|0||15e5","Asia/Manila|PHT|-80|0||24e6","Europe/Athens|EET EEST|-20 -30|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|35e5","Asia/Novokuznetsk|+07 +06|-70 -60|010|1Dp80 WM0|55e4","Asia/Novosibirsk|+06 +07|-60 -70|010101|1BWk0 1qM0 WM0 8Hz0 4eN0|15e5","Asia/Omsk|OMST OMSST OMST|-60 -70 -70|01020|1BWk0 1qM0 WM0 8Hz0|12e5","Asia/Pyongyang|KST KST|-90 -8u|01|1P4D0|29e5","Asia/Rangoon|MMT|-6u|0||48e5","Asia/Sakhalin|SAKT SAKST SAKT|-a0 -b0 -b0|010202|1BWg0 1qM0 WM0 8Hz0 3rd0|58e4","Asia/Tashkent|UZT|-50|0||23e5","Asia/Seoul|KST|-90|0||23e6","Asia/Singapore|SGT|-80|0||56e5","Asia/Srednekolymsk|MAGT MAGST MAGT SRET|-b0 -c0 -c0 -b0|01023|1BWf0 1qM0 WM0 8Hz0|35e2","Asia/Tbilisi|GET|-40|0||11e5","Asia/Tehran|IRST IRDT|-3u -4u|01010101010101010101010|1BTUu 1dz0 1cp0 1dz0 1cp0 1dz0 1cN0 1dz0 1cp0 1dz0 1cp0 1dz0 1cp0 1dz0 1cN0 1dz0 1cp0 1dz0 1cp0 1dz0 1cp0 1dz0|14e6","Asia/Thimphu|BTT|-60|0||79e3","Asia/Tokyo|JST|-90|0||38e6","Asia/Tomsk|+06 +07|-60 -70|010101|1BWk0 1qM0 WM0 8Hz0 3Qp0|10e5","Asia/Ulaanbaatar|ULAT ULAST|-80 -90|0101010101010|1O8G0 1cJ0 1cP0 1cJ0 1cP0 1fx0 1cP0 1cJ0 1cP0 1cJ0 1cP0 1cJ0|12e5","Asia/Ust-Nera|MAGT MAGST MAGT VLAT VLAT|-b0 -c0 -c0 -b0 -a0|010234|1BWf0 1qM0 WM0 17V0 7zD0|65e2","Asia/Vladivostok|VLAT VLAST VLAT|-a0 -b0 -b0|01020|1BWg0 1qM0 WM0 8Hz0|60e4","Asia/Yakutsk|YAKT YAKST YAKT|-90 -a0 -a0|01020|1BWh0 1qM0 WM0 8Hz0|28e4","Asia/Yekaterinburg|YEKT YEKST YEKT|-50 -60 -60|01020|1BWl0 1qM0 WM0 8Hz0|14e5","Asia/Yerevan|AMT AMST|-40 -50|01010|1BWm0 1qM0 WM0 1qM0|13e5","Atlantic/Azores|AZOT AZOST|10 0|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|25e4","Europe/Lisbon|WET WEST|0 -10|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|27e5","Atlantic/Cape_Verde|CVT|10|0||50e4","Atlantic/South_Georgia|GST|20|0||30","Atlantic/Stanley|FKST FKT|30 40|010|1C6R0 U10|21e2","Australia/Sydney|AEDT AEST|-b0 -a0|01010101010101010101010|1C140 1cM0 1cM0 1cM0 1cM0 1fA0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1cM0 1cM0 1cM0 1cM0|40e5","Australia/Adelaide|ACDT ACST|-au -9u|01010101010101010101010|1C14u 1cM0 1cM0 1cM0 1cM0 1fA0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1cM0 1fA0 1cM0 1cM0 1cM0 1cM0|11e5","Australia/Brisbane|AEST|-a0|0||20e5","Australia/Darwin|ACST|-9u|0||12e4","Australia/Eucla|ACWST|-8J|0||368","Australia/Lord_Howe|LHDT LHST|-b0 -au|01010101010101010101010|1C130 1cMu 1cLu 1cMu 1cLu 1fAu 1cLu 1cMu 1cLu 1cMu 1cLu 1cMu 1cLu 1cMu 1cLu 1cMu 1cLu 1fAu 1cLu 1cMu 1cLu 1cMu|347","Australia/Perth|AWST|-80|0||18e5","Pacific/Easter|EASST EAST|50 60|010101010101010101010|1C1f0 1fB0 1nX0 G10 1EL0 Op0 1zb0 Rd0 1wn0 Rd0 46n0 Ap0 1Nb0 Ap0 1Nb0 Ap0 1Nb0 Ap0 1Nb0 Ap0|30e2","Europe/Dublin|GMT IST|0 -10|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|12e5","Etc/GMT+1|GMT+1|10|0|","Etc/GMT+10|GMT+10|a0|0|","Etc/GMT+11|GMT+11|b0|0|","Etc/GMT+12|GMT+12|c0|0|","Etc/GMT+2|GMT+2|20|0|","Etc/GMT+3|GMT+3|30|0|","Etc/GMT+4|GMT+4|40|0|","Etc/GMT+5|GMT+5|50|0|","Etc/GMT+6|GMT+6|60|0|","Etc/GMT+7|GMT+7|70|0|","Etc/GMT+8|GMT+8|80|0|","Etc/GMT+9|GMT+9|90|0|","Etc/GMT-1|GMT-1|-10|0|","Etc/GMT-10|GMT-10|-a0|0|","Etc/GMT-11|GMT-11|-b0|0|","Etc/GMT-12|GMT-12|-c0|0|","Etc/GMT-13|GMT-13|-d0|0|","Etc/GMT-14|GMT-14|-e0|0|","Etc/GMT-2|GMT-2|-20|0|","Etc/GMT-3|GMT-3|-30|0|","Etc/GMT-4|GMT-4|-40|0|","Etc/GMT-5|GMT-5|-50|0|","Etc/GMT-6|GMT-6|-60|0|","Etc/GMT-7|GMT-7|-70|0|","Etc/GMT-8|GMT-8|-80|0|","Etc/GMT-9|GMT-9|-90|0|","Etc/UCT|UCT|0|0|","Etc/UTC|UTC|0|0|","Europe/Astrakhan|+03 +04|-30 -40|010101|1BWn0 1qM0 WM0 8Hz0 3rd0","Europe/London|GMT BST|0 -10|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|10e6","Europe/Chisinau|EET EEST|-20 -30|01010101010101010101010|1BWo0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00|67e4","Europe/Kaliningrad|EET EEST FET|-20 -30 -30|01020|1BWo0 1qM0 WM0 8Hz0|44e4","Europe/Kirov|+03 +04|-30 -40|01010|1BWn0 1qM0 WM0 8Hz0|48e4","Europe/Minsk|EET EEST FET MSK|-20 -30 -30 -30|01023|1BWo0 1qM0 WM0 8Hy0|19e5","Europe/Moscow|MSK MSD MSK|-30 -40 -40|01020|1BWn0 1qM0 WM0 8Hz0|16e6","Europe/Samara|SAMT SAMST SAMT|-40 -40 -30|0120|1BWm0 1qN0 WM0|12e5","Europe/Simferopol|EET EEST MSK MSK|-20 -30 -40 -30|01010101023|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11z0 1nW0|33e4","Pacific/Honolulu|HST|a0|0||37e4","Indian/Chagos|IOT|-60|0||30e2","Indian/Christmas|CXT|-70|0||21e2","Indian/Cocos|CCT|-6u|0||596","Indian/Kerguelen|TFT|-50|0||130","Indian/Mahe|SCT|-40|0||79e3","Indian/Maldives|MVT|-50|0||35e4","Indian/Mauritius|MUT|-40|0||15e4","Indian/Reunion|RET|-40|0||84e4","Pacific/Majuro|MHT|-c0|0||28e3","MET|MET MEST|-10 -20|01010101010101010101010|1BWp0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00 11A0 1o00 11A0 1qM0 WM0 1qM0 WM0 1qM0 11A0 1o00 11A0 1o00","Pacific/Chatham|CHADT CHAST|-dJ -cJ|01010101010101010101010|1C120 1a00 1fA0 1a00 1fA0 1cM0 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1cM0 1fA0 1a00 1fA0 1a00|600","Pacific/Apia|SST SDT WSDT WSST|b0 a0 -e0 -d0|01012323232323232323232|1Dbn0 1ff0 1a00 CI0 AQ0 1cM0 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1a00 1fA0 1cM0 1fA0 1a00 1fA0 1a00|37e3","Pacific/Bougainville|PGT BST|-a0 -b0|01|1NwE0|18e4","Pacific/Chuuk|CHUT|-a0|0||49e3","Pacific/Efate|VUT|-b0|0||66e3","Pacific/Enderbury|PHOT|-d0|0||1","Pacific/Fakaofo|TKT TKT|b0 -d0|01|1Gfn0|483","Pacific/Fiji|FJST FJT|-d0 -c0|01010101010101010101010|1BWe0 1o00 Rc0 1wo0 Ao0 1Nc0 Ao0 1Q00 xz0 1SN0 uM0 1SM0 uM0 1VA0 s00 1VA0 uM0 1SM0 uM0 1SM0 uM0 1SM0|88e4","Pacific/Funafuti|TVT|-c0|0||45e2","Pacific/Galapagos|GALT|60|0||25e3","Pacific/Gambier|GAMT|90|0||125","Pacific/Guadalcanal|SBT|-b0|0||11e4","Pacific/Guam|ChST|-a0|0||17e4","Pacific/Kiritimati|LINT|-e0|0||51e2","Pacific/Kosrae|KOST|-b0|0||66e2","Pacific/Marquesas|MART|9u|0||86e2","Pacific/Pago_Pago|SST|b0|0||37e2","Pacific/Nauru|NRT|-c0|0||10e3","Pacific/Niue|NUT|b0|0||12e2","Pacific/Norfolk|NFT NFT|-bu -b0|01|1PoCu|25e4","Pacific/Noumea|NCT|-b0|0||98e3","Pacific/Palau|PWT|-90|0||21e3","Pacific/Pitcairn|PST|80|0||56","Pacific/Pohnpei|PONT|-b0|0||34e3","Pacific/Port_Moresby|PGT|-a0|0||25e4","Pacific/Rarotonga|CKT|a0|0||13e3","Pacific/Tahiti|TAHT|a0|0||18e4","Pacific/Tarawa|GILT|-c0|0||29e3","Pacific/Tongatapu|TOT|-d0|0||75e3","Pacific/Wake|WAKT|-c0|0||16e3","Pacific/Wallis|WFT|-c0|0||94"],links:["Africa/Abidjan|Africa/Accra","Africa/Abidjan|Africa/Bamako","Africa/Abidjan|Africa/Banjul","Africa/Abidjan|Africa/Bissau","Africa/Abidjan|Africa/Conakry","Africa/Abidjan|Africa/Dakar","Africa/Abidjan|Africa/Freetown","Africa/Abidjan|Africa/Lome","Africa/Abidjan|Africa/Monrovia","Africa/Abidjan|Africa/Nouakchott","Africa/Abidjan|Africa/Ouagadougou","Africa/Abidjan|Africa/Sao_Tome","Africa/Abidjan|Africa/Timbuktu","Africa/Abidjan|America/Danmarkshavn","Africa/Abidjan|Atlantic/Reykjavik","Africa/Abidjan|Atlantic/St_Helena","Africa/Abidjan|Etc/GMT","Africa/Abidjan|Etc/GMT+0","Africa/Abidjan|Etc/GMT-0","Africa/Abidjan|Etc/GMT0","Africa/Abidjan|Etc/Greenwich","Africa/Abidjan|GMT","Africa/Abidjan|GMT+0","Africa/Abidjan|GMT-0","Africa/Abidjan|GMT0","Africa/Abidjan|Greenwich","Africa/Abidjan|Iceland","Africa/Algiers|Africa/Tunis","Africa/Cairo|Egypt","Africa/Casablanca|Africa/El_Aaiun","Africa/Johannesburg|Africa/Maseru","Africa/Johannesburg|Africa/Mbabane","Africa/Khartoum|Africa/Addis_Ababa","Africa/Khartoum|Africa/Asmara","Africa/Khartoum|Africa/Asmera","Africa/Khartoum|Africa/Dar_es_Salaam","Africa/Khartoum|Africa/Djibouti","Africa/Khartoum|Africa/Juba","Africa/Khartoum|Africa/Kampala","Africa/Khartoum|Africa/Mogadishu","Africa/Khartoum|Africa/Nairobi","Africa/Khartoum|Indian/Antananarivo","Africa/Khartoum|Indian/Comoro","Africa/Khartoum|Indian/Mayotte","Africa/Lagos|Africa/Bangui","Africa/Lagos|Africa/Brazzaville","Africa/Lagos|Africa/Douala","Africa/Lagos|Africa/Kinshasa","Africa/Lagos|Africa/Libreville","Africa/Lagos|Africa/Luanda","Africa/Lagos|Africa/Malabo","Africa/Lagos|Africa/Ndjamena","Africa/Lagos|Africa/Niamey","Africa/Lagos|Africa/Porto-Novo","Africa/Maputo|Africa/Blantyre","Africa/Maputo|Africa/Bujumbura","Africa/Maputo|Africa/Gaborone","Africa/Maputo|Africa/Harare","Africa/Maputo|Africa/Kigali","Africa/Maputo|Africa/Lubumbashi","Africa/Maputo|Africa/Lusaka","Africa/Tripoli|Libya","America/Adak|America/Atka","America/Adak|US/Aleutian","America/Anchorage|America/Juneau","America/Anchorage|America/Nome","America/Anchorage|America/Sitka","America/Anchorage|America/Yakutat","America/Anchorage|US/Alaska","America/Argentina/Buenos_Aires|America/Argentina/Catamarca","America/Argentina/Buenos_Aires|America/Argentina/ComodRivadavia","America/Argentina/Buenos_Aires|America/Argentina/Cordoba","America/Argentina/Buenos_Aires|America/Argentina/Jujuy","America/Argentina/Buenos_Aires|America/Argentina/La_Rioja","America/Argentina/Buenos_Aires|America/Argentina/Mendoza","America/Argentina/Buenos_Aires|America/Argentina/Rio_Gallegos","America/Argentina/Buenos_Aires|America/Argentina/Salta","America/Argentina/Buenos_Aires|America/Argentina/San_Juan","America/Argentina/Buenos_Aires|America/Argentina/San_Luis","America/Argentina/Buenos_Aires|America/Argentina/Tucuman","America/Argentina/Buenos_Aires|America/Argentina/Ushuaia","America/Argentina/Buenos_Aires|America/Buenos_Aires","America/Argentina/Buenos_Aires|America/Catamarca","America/Argentina/Buenos_Aires|America/Cordoba","America/Argentina/Buenos_Aires|America/Jujuy","America/Argentina/Buenos_Aires|America/Mendoza","America/Argentina/Buenos_Aires|America/Rosario","America/Campo_Grande|America/Cuiaba","America/Chicago|America/Indiana/Knox","America/Chicago|America/Indiana/Tell_City","America/Chicago|America/Knox_IN","America/Chicago|America/Matamoros","America/Chicago|America/Menominee","America/Chicago|America/North_Dakota/Center","America/Chicago|America/North_Dakota/New_Salem","America/Chicago|America/Rainy_River","America/Chicago|America/Rankin_Inlet","America/Chicago|America/Resolute","America/Chicago|America/Winnipeg","America/Chicago|CST6CDT","America/Chicago|Canada/Central","America/Chicago|US/Central","America/Chicago|US/Indiana-Starke","America/Chihuahua|America/Mazatlan","America/Chihuahua|Mexico/BajaSur","America/Denver|America/Boise","America/Denver|America/Cambridge_Bay","America/Denver|America/Edmonton","America/Denver|America/Inuvik","America/Denver|America/Ojinaga","America/Denver|America/Shiprock","America/Denver|America/Yellowknife","America/Denver|Canada/Mountain","America/Denver|MST7MDT","America/Denver|Navajo","America/Denver|US/Mountain","America/Fortaleza|America/Belem","America/Fortaleza|America/Maceio","America/Fortaleza|America/Recife","America/Fortaleza|America/Santarem","America/Halifax|America/Glace_Bay","America/Halifax|America/Moncton","America/Halifax|America/Thule","America/Halifax|Atlantic/Bermuda","America/Halifax|Canada/Atlantic","America/Havana|Cuba","America/Los_Angeles|America/Dawson","America/Los_Angeles|America/Ensenada","America/Los_Angeles|America/Santa_Isabel","America/Los_Angeles|America/Tijuana","America/Los_Angeles|America/Vancouver","America/Los_Angeles|America/Whitehorse","America/Los_Angeles|Canada/Pacific","America/Los_Angeles|Canada/Yukon","America/Los_Angeles|Mexico/BajaNorte","America/Los_Angeles|PST8PDT","America/Los_Angeles|US/Pacific","America/Los_Angeles|US/Pacific-New","America/Managua|America/Belize","America/Managua|America/Costa_Rica","America/Managua|America/El_Salvador","America/Managua|America/Guatemala","America/Managua|America/Regina","America/Managua|America/Swift_Current","America/Managua|America/Tegucigalpa","America/Managua|Canada/East-Saskatchewan","America/Managua|Canada/Saskatchewan","America/Manaus|America/Boa_Vista","America/Manaus|America/Porto_Velho","America/Manaus|Brazil/West","America/Mexico_City|America/Merida","America/Mexico_City|America/Monterrey","America/Mexico_City|Mexico/General","America/New_York|America/Detroit","America/New_York|America/Fort_Wayne","America/New_York|America/Indiana/Indianapolis","America/New_York|America/Indiana/Marengo","America/New_York|America/Indiana/Petersburg","America/New_York|America/Indiana/Vevay","America/New_York|America/Indiana/Vincennes","America/New_York|America/Indiana/Winamac","America/New_York|America/Indianapolis","America/New_York|America/Iqaluit","America/New_York|America/Kentucky/Louisville","America/New_York|America/Kentucky/Monticello","America/New_York|America/Louisville","America/New_York|America/Montreal","America/New_York|America/Nassau","America/New_York|America/Nipigon","America/New_York|America/Pangnirtung","America/New_York|America/Thunder_Bay","America/New_York|America/Toronto","America/New_York|Canada/Eastern","America/New_York|EST5EDT","America/New_York|US/East-Indiana","America/New_York|US/Eastern","America/New_York|US/Michigan","America/Noronha|Brazil/DeNoronha","America/Panama|America/Atikokan","America/Panama|America/Cayman","America/Panama|America/Coral_Harbour","America/Panama|America/Jamaica","America/Panama|EST","America/Panama|Jamaica","America/Phoenix|America/Creston","America/Phoenix|America/Dawson_Creek","America/Phoenix|America/Hermosillo","America/Phoenix|MST","America/Phoenix|US/Arizona","America/Rio_Branco|America/Eirunepe","America/Rio_Branco|America/Porto_Acre","America/Rio_Branco|Brazil/Acre","America/Santiago|Antarctica/Palmer","America/Santiago|Chile/Continental","America/Santo_Domingo|America/Anguilla","America/Santo_Domingo|America/Antigua","America/Santo_Domingo|America/Aruba","America/Santo_Domingo|America/Barbados","America/Santo_Domingo|America/Blanc-Sablon","America/Santo_Domingo|America/Curacao","America/Santo_Domingo|America/Dominica","America/Santo_Domingo|America/Grenada","America/Santo_Domingo|America/Guadeloupe","America/Santo_Domingo|America/Kralendijk","America/Santo_Domingo|America/Lower_Princes","America/Santo_Domingo|America/Marigot","America/Santo_Domingo|America/Martinique","America/Santo_Domingo|America/Montserrat","America/Santo_Domingo|America/Port_of_Spain","America/Santo_Domingo|America/Puerto_Rico","America/Santo_Domingo|America/St_Barthelemy","America/Santo_Domingo|America/St_Kitts","America/Santo_Domingo|America/St_Lucia","America/Santo_Domingo|America/St_Thomas","America/Santo_Domingo|America/St_Vincent","America/Santo_Domingo|America/Tortola","America/Santo_Domingo|America/Virgin","America/Sao_Paulo|Brazil/East","America/St_Johns|Canada/Newfoundland","Asia/Almaty|Asia/Qyzylorda","Asia/Aqtobe|Asia/Aqtau","Asia/Aqtobe|Asia/Oral","Asia/Ashgabat|Asia/Ashkhabad","Asia/Baghdad|Asia/Aden","Asia/Baghdad|Asia/Bahrain","Asia/Baghdad|Asia/Kuwait","Asia/Baghdad|Asia/Qatar","Asia/Baghdad|Asia/Riyadh","Asia/Bangkok|Asia/Ho_Chi_Minh","Asia/Bangkok|Asia/Phnom_Penh","Asia/Bangkok|Asia/Saigon","Asia/Bangkok|Asia/Vientiane","Asia/Dhaka|Asia/Dacca","Asia/Dubai|Asia/Muscat","Asia/Hong_Kong|Hongkong","Asia/Jakarta|Asia/Pontianak","Asia/Jerusalem|Asia/Tel_Aviv","Asia/Jerusalem|Israel","Asia/Kathmandu|Asia/Katmandu","Asia/Kolkata|Asia/Calcutta","Asia/Kolkata|Asia/Colombo","Asia/Kuala_Lumpur|Asia/Kuching","Asia/Makassar|Asia/Ujung_Pandang","Asia/Seoul|ROK","Asia/Shanghai|Asia/Chongqing","Asia/Shanghai|Asia/Chungking","Asia/Shanghai|Asia/Harbin","Asia/Shanghai|Asia/Macao","Asia/Shanghai|Asia/Macau","Asia/Shanghai|Asia/Taipei","Asia/Shanghai|PRC","Asia/Shanghai|ROC","Asia/Singapore|Singapore","Asia/Tashkent|Asia/Samarkand","Asia/Tehran|Iran","Asia/Thimphu|Asia/Thimbu","Asia/Tokyo|Japan","Asia/Ulaanbaatar|Asia/Ulan_Bator","Asia/Urumqi|Asia/Kashgar","Australia/Adelaide|Australia/Broken_Hill","Australia/Adelaide|Australia/South","Australia/Adelaide|Australia/Yancowinna","Australia/Brisbane|Australia/Lindeman","Australia/Brisbane|Australia/Queensland","Australia/Darwin|Australia/North","Australia/Lord_Howe|Australia/LHI","Australia/Perth|Australia/West","Australia/Sydney|Australia/ACT","Australia/Sydney|Australia/Canberra","Australia/Sydney|Australia/Currie","Australia/Sydney|Australia/Hobart","Australia/Sydney|Australia/Melbourne","Australia/Sydney|Australia/NSW","Australia/Sydney|Australia/Tasmania","Australia/Sydney|Australia/Victoria","Etc/UCT|UCT","Etc/UTC|Etc/Universal","Etc/UTC|Etc/Zulu","Etc/UTC|UTC","Etc/UTC|Universal","Etc/UTC|Zulu","Europe/Astrakhan|Europe/Ulyanovsk","Europe/Athens|Asia/Nicosia","Europe/Athens|EET","Europe/Athens|Europe/Bucharest","Europe/Athens|Europe/Helsinki","Europe/Athens|Europe/Kiev","Europe/Athens|Europe/Mariehamn","Europe/Athens|Europe/Nicosia","Europe/Athens|Europe/Riga","Europe/Athens|Europe/Sofia","Europe/Athens|Europe/Tallinn","Europe/Athens|Europe/Uzhgorod","Europe/Athens|Europe/Vilnius","Europe/Athens|Europe/Zaporozhye","Europe/Chisinau|Europe/Tiraspol","Europe/Dublin|Eire","Europe/Istanbul|Asia/Istanbul","Europe/Istanbul|Turkey","Europe/Lisbon|Atlantic/Canary","Europe/Lisbon|Atlantic/Faeroe","Europe/Lisbon|Atlantic/Faroe","Europe/Lisbon|Atlantic/Madeira","Europe/Lisbon|Portugal","Europe/Lisbon|WET","Europe/London|Europe/Belfast","Europe/London|Europe/Guernsey","Europe/London|Europe/Isle_of_Man","Europe/London|Europe/Jersey","Europe/London|GB","Europe/London|GB-Eire","Europe/Moscow|Europe/Volgograd","Europe/Moscow|W-SU","Europe/Paris|Africa/Ceuta","Europe/Paris|Arctic/Longyearbyen","Europe/Paris|Atlantic/Jan_Mayen","Europe/Paris|CET","Europe/Paris|Europe/Amsterdam","Europe/Paris|Europe/Andorra","Europe/Paris|Europe/Belgrade","Europe/Paris|Europe/Berlin","Europe/Paris|Europe/Bratislava","Europe/Paris|Europe/Brussels","Europe/Paris|Europe/Budapest","Europe/Paris|Europe/Busingen","Europe/Paris|Europe/Copenhagen","Europe/Paris|Europe/Gibraltar","Europe/Paris|Europe/Ljubljana","Europe/Paris|Europe/Luxembourg","Europe/Paris|Europe/Madrid","Europe/Paris|Europe/Malta","Europe/Paris|Europe/Monaco","Europe/Paris|Europe/Oslo","Europe/Paris|Europe/Podgorica","Europe/Paris|Europe/Prague","Europe/Paris|Europe/Rome","Europe/Paris|Europe/San_Marino","Europe/Paris|Europe/Sarajevo","Europe/Paris|Europe/Skopje","Europe/Paris|Europe/Stockholm","Europe/Paris|Europe/Tirane","Europe/Paris|Europe/Vaduz","Europe/Paris|Europe/Vatican","Europe/Paris|Europe/Vienna","Europe/Paris|Europe/Warsaw","Europe/Paris|Europe/Zagreb","Europe/Paris|Europe/Zurich","Europe/Paris|Poland","Pacific/Auckland|Antarctica/McMurdo","Pacific/Auckland|Antarctica/South_Pole","Pacific/Auckland|NZ","Pacific/Chatham|NZ-CHAT","Pacific/Chuuk|Pacific/Truk","Pacific/Chuuk|Pacific/Yap","Pacific/Easter|Chile/EasterIsland","Pacific/Guam|Pacific/Saipan","Pacific/Honolulu|HST","Pacific/Honolulu|Pacific/Johnston","Pacific/Honolulu|US/Hawaii","Pacific/Majuro|Kwajalein","Pacific/Majuro|Pacific/Kwajalein","Pacific/Pago_Pago|Pacific/Midway","Pacific/Pago_Pago|Pacific/Samoa","Pacific/Pago_Pago|US/Samoa","Pacific/Pohnpei|Pacific/Ponape"]
}),a});

/*
 * utils.js
 *
 * Copyright 2016 Antergos
 *
 * This file is part of Cnchi.
 *
 * Cnchi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Cnchi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * The following additional terms are in effect as per Section 7 of the license:
 *
 * The preservation of all legal notices and author attributions in
 * the material or in the Appropriate Legal Notices displayed
 * by works containing it is required.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';


/**
 * Capitalizes a string.
 *
 * @returns {string}
 */
String.prototype.capitalise = function() {
	return this.charAt( 0 ).toUpperCase() + this.slice( 1 );
};


/**
 * Animate an element and once animation ends call callback if one is provided.
 *
 * @arg {String}   animation_name CSS class name for the animation.
 * @arg {function} [callback]     Function to call after the animation completes.
 */
$.fn.animateCss = function( animation_name, callback ) {
	let animation_end = 'webkitAnimationEnd animationend';

	this.addClass( animation_name ).one( animation_end, () => {
		setTimeout( () => {
			this.removeClass( animation_name );
		}, 1000 );

		if ( callback ) {
			callback();
		}
	} );
};


/*
 * logger.js
 *
 * Copyright 2016 Antergos
 *
 * This file is part of Cnchi.
 *
 * Cnchi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Cnchi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * The following additional terms are in effect as per Section 7 of the license:
 *
 * The preservation of all legal notices and author attributions in
 * the material or in the Appropriate Legal Notices displayed
 * by works containing it is required.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';


/**
 * Sends log messages through the Python<->JS Bridge to our Python logging handler.
 *
 * @prop {String} log_prefix      A string that will be prepended to log messages.
 * @prop {String} _unknown_method A string used for the calling method name when one isn't
 *     provided.
 */
class CnchiLogger {

	/**
	 * Creates a new Logger instance.
	 *
	 * @arg {String} log_prefix {@link Logger.log_prefix}
	 */
	constructor( log_prefix ) {
		this.log_prefix = log_prefix;
		this._unknown_method = '@unknown@';
	}

	/**
	 * Determines and returns the caller name based on value of `caller` argument
	 *
	 * @arg {Function|String} caller
	 * @returns {String}
	 * @private
	 */
	_get_caller_name( caller ) {
		return ( '' !== caller ) ? caller.name : this._unknown_method;
	}

	/**
	 * Prepares a message to be sent to Python logging facility.
	 *
	 * @arg {String} msg    The message to be logged.
	 * @arg {String} caller The name of the caller or an empty string.
	 * @returns {string}
	 * @private
	 */
	_process_message( msg, caller ) {
		return `[${this.log_prefix}.${this._get_caller_name( caller )}]: ${msg}`;
	}

	/**
	 * Sends a message to the Python logging facility.
	 *
	 * @arg {String} msg   The message to be sent.
	 * @arg {String} level The logging level to use for the message.
	 * @private
	 */
	_write_log( msg, level ) {
		let esc_msg = msg.replace( /"/g, '\\"' );
		msg = `_BR::["do-log-message", "${level}", "${esc_msg}"]`;

		cnchi._bridge_message_queue.push( msg );
		console.log( msg );
	}

	/**
	 * Sends a message to Python logging facility where logging level == method name.
	 *
	 * @arg {String}          msg         The message to be logged.
	 * @arg {Function|String} [caller=''] The method calling this log method.
	 */
	info( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'info' );
	}

	/**
	 * @see Logger.info
	 */
	debug( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'debug' );
	}

	/**
	 * @see Logger.info
	 */
	warning( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'warning' );
	}

	/**
	 * @see Logger.info
	 */
	error( msg, caller = '' ) {
		msg = this._process_message( msg, caller );
		this._write_log( msg, 'error' );
	}
}


window.CnchiLogger = CnchiLogger;


/*
 * object.js
 *
 * Copyright 2016 Antergos
 *
 * This file is part of Cnchi.
 *
 * Cnchi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Cnchi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * The following additional terms are in effect as per Section 7 of the license:
 *
 * The preservation of all legal notices and author attributions in
 * the material or in the Appropriate Legal Notices displayed
 * by works containing it is required.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';


/**
 * A base object for all Cnchi* objects. It sets up the logger and
 * binds `this` to the class for all class methods.
 *
 * @prop {Logger} logger The logger object.
 */
class CnchiObject {

	constructor() {
		this.logger = new CnchiLogger( this.constructor.name );
		this._bind_this();
	}

	/**
	 * Binds `this` to the class for all class methods.
	 *
	 * @private
	 */
	_bind_this() {
		let excluded = ['constructor', '_bind_this', 'not_excluded'];

		function not_excluded( method, context ) {
			let _excluded = excluded.findIndex( excluded_method => method === excluded_method ) > - 1,
				is_method = 'function' === typeof context[method];

			return is_method && ! _excluded;
		}

		for ( let obj = this; obj; obj = Object.getPrototypeOf( obj ) ) {
			for ( let method of Object.getOwnPropertyNames( obj ) ) {
				if ( not_excluded( method, this ) ) {
					this[method] = this[method].bind( this );
				}
			}
		}
	}
}

window.CnchiObject = CnchiObject;


/*
 * cnchi_app.js
 *
 * Copyright 2016 Antergos
 *
 * This file is part of Cnchi.
 *
 * Cnchi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Cnchi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * The following additional terms are in effect as per Section 7 of the license:
 *
 * The preservation of all legal notices and author attributions in
 * the material or in the Appropriate Legal Notices displayed
 * by works containing it is required.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';

/**
 * Whether or not the {@link CnchiApp} object has been created.
 */
let _cnchi_exists = false;


/**
 * The main application object. It follows the Singleton pattern.
 *
 * @prop {jQuery}   $header  A jQuery object corresponding to the app's header in the DOM.
 * @prop {boolean}  loaded   Whether or not the `page-loaded` event has fired.
 * @prop {String[]} cmds     The commands the app will accept from Python -> JS Bridge.
 * @prop {String[]} signals  The signals the app will allow to be sent via JS Bridge -> Python.
 * @prop {boolean}  dragging Whether or not the window is currently being dragged.
 */
class CnchiApp extends CnchiObject {

	constructor() {
		if ( false !== _cnchi_exists ) {
			return cnchi;
		}

		super();

		this.loaded = false;
		this.cmds = ['trigger_event'];
		this.signals = ['window-dragging-start', 'window-dragging-stop'];
		this.dragging = false;
		this.$header = $( '.header' );
		this._logger = null;
		this._bridge_message_queue = [];
		this.bmq_worker = null;
		this.$top_navigation_buttons = $( '.header_bottom .navigation_buttons .tabs' );

		this.register_event_handlers();
		this._start_bridge_message_queue_worker();
		this._maybe_unlock_top_level_tabs();
	}

	_maybe_unlock_top_level_tabs() {
		this.$top_navigation_buttons.children().each( ( index, element ) => {
			let $tab_button = $( element );

			$tab_button.removeClass( 'locked' );

			if ( $tab_button.hasClass( 'active' ) ) {
				// This button is for the current page. Don't unlock anymore buttons.
				return false;
			}
		} );
	}

	_start_bridge_message_queue_worker() {
		this.bmq_worker = setInterval( () => {
			if ( this._bridge_message_queue.length === 0 ) {
				return;
			}

			document.title = this._bridge_message_queue.shift();
		}, 100 );
	}

	/**
	 * Sends an allowed signal and optional arguments to the backend via the Python<->JS Bridge.
	 *
	 * @arg {...String|Array|Object} args The first arg should always be the name of the signal.
	 *
	 * @example
	 * emit_signal( 'do-some-action' );
	 * emit_signal( 'do-some-action', arg1, arg2 );
	 */
	emit_signal( ...args ) {
		let msg = '[', _args = [];

		if ( $.inArray( args[0], this.signals ) < 0 ) {
			this.logger.error( `cmd: "${args[0]}" is not in the list of allowed signals!` );
			return;
		}

		// Convert any non-string args to JSON strings so that we have a single string to send.
		for ( let _arg of args ) {
			if ( Array === typeof _arg || _arg instanceof Object ) {
				_arg = JSON.stringify( _arg );
			} else if ( 'string' === typeof _arg ) {
				_arg = `"${_arg}"`;
			}

			msg = `${msg}${_arg}, `;
		}

		msg = msg.replace( /, $/, '' );
		msg = `${msg}]`;

		this.logger.debug( `Emitting signal: "${msg}" via python bridge...` );

		this._bridge_message_queue.push( `_BR::${msg}` );
	}


	/**
	 * Header `mousedown` event callback. Intended to be used to implement window dragging.
	 * There is no official api for our use-case. Still, it appears to be possible. However,
	 * it doesn't work at the moment (probably because of some bug in GTK).
	 *
	 * @arg {jQuery.Event} event
	 *
	 * @todo Find a way to make this work.
	 */
	header_mousedown_cb( event ) {
		let $target = event.target ? $( event.target ) : event.currentTarget ? $( event.currentTarget ) : null;

		if ( null === $target ) {
			this.logger.debug( 'no target!' );
			return;
		}

		if ( $target.closest( '.no-drag' ).length || true === cnchi._dragging ) {
			this.logger.debug( `mousedown returning! ${cnchi._dragging}` );
			return;
		}

		cnchi._dragging = true;
		cnchi.emit_signal( 'window-dragging-start', 'window-dragging-start' );
	}

	/**
	 * Header `mouseup` event callback.
	 *
	 * @see CnchiApp.header_mousedown_cb
	 */
	header_mouseup_cb( event ) {
		let $target = event.target ? $( event.target ) : event.currentTarget ? $( event.currentTarget ) : null;

		if ( null === $target ) {
			this.logger.debug( 'no target!' );
			return;
		}

		if ( $target.closest( '.no-drag' ).length || false === cnchi._dragging ) {
			this.logger.debug( `mouseup returning! ${cnchi._dragging}` );
			return;
		}

		cnchi._dragging = false;

		cnchi.emit_signal( 'window-dragging-stop', 'window-dragging-stop' );
	}

	/**
	 * Handles messages sent from the backend via the Python<->JS Bridge. Messages are
	 * injected into the global scope as an `Object` referenced by a unique variable. The
	 * variable name is then passed to this method as a string so it can access the message.
	 *
	 * @arg msg_obj_var_name
	 */
	js_bridge_handler( msg_obj_var_name ) {
		let data, cmd, args;

		args = window[msg_obj_var_name].args;
		cmd = window[msg_obj_var_name].cmd;

		if ( ! cmd.length ) {
			this.logger.error( '"cmd" is required!', this.js_bridge_handler );
			return;
		}

		if ( $.inArray( cmd, this.cmds ) < 0 ) {
			this.logger.error(
				`cmd: "${cmd}" is not in the list of allowed commands!`, this.js_bridge_handler
			);
			return;
		}

		if ( args.length === 1 ) {
			args = args.pop();
		}

		this.logger.debug( `Running command: ${cmd} with args: ${args}...`,
						   this.js_bridge_handler );

		this[cmd]( args );
	}

	page_loaded_handler( event, page ) {
		if ( false === cnchi.loaded ) {
			cnchi.loaded = true;
		}
	}

	register_event_handlers() {
		//$(window).on('page-loaded', (event) => this.page_loaded_handler(event));
		//this.$header.on('mousedown', '*', this.header_mousedown_cb);
		//this.$header.on('mouseup', '*', this.header_mouseup_cb);
	}

	/**
	 * Triggers an event for signal received from backend with optional arguments.
	 *
	 * @arg {String|Array} event Either the event name or an Array where the first item is
	 *                           the event name and remaining items are args to pass to callback.
	 */
	trigger_event( event ) {
		let args = [];

		if ( Array.isArray( event ) ) {
			args = event;
			event = args.shift();

			if ( args.length === 1 ) {
				args = args.pop();
			}
		}

		this.logger.debug( `triggering event: ${event} with args: ${args}`, this.trigger_event );

		$( window ).trigger( event, args );
	}

}


if ( false === _cnchi_exists ) {
	window.cnchi = new CnchiApp();
	_cnchi_exists = true;
}



/*
 * tab.js
 *
 * Copyright 2016 Antergos
 *
 * This file is part of Cnchi.
 *
 * Cnchi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Cnchi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * The following additional terms are in effect as per Section 7 of the license:
 *
 * The preservation of all legal notices and author attributions in
 * the material or in the Appropriate Legal Notices displayed
 * by works containing it is required.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';


/**
 * Manages a tab in the UI. Tabs make up pages. All pages contain at least one tab.
 *
 * @prop {jQuery}    $tab    A jQuery object for the tab's HTML element in the DOM.
 * @prop {string}    id      The CSS ID for the tab.
 * @prop {string}    name    A name for this tab. It will be used in the navigation tab buttons.
 * @prop {CnchiPage} parent  This tab's parent tab (the page this tab appears on).
 */
class CnchiTab extends CnchiObject {
	/**
	 * Creates a new {@link CnchiTab} object.
	 *
	 * @arg {jQuery}    $tab     {@link CnchiTab.$tab}
	 * @arg {string}    [name]     {@link CnchiTab.name}
	 * @arg {CnchiPage} [parent] {@link CnchiTab.parent}
	 */
	constructor( $tab, name, page ) {
		super();

		let result = this._check_args( $tab, name, page );

		if ( true !== result ) {
			this.logger.error( result, this.constructor );
		}

		this.$tab = ( $tab instanceof jQuery ) ? $tab : $( `#${name}` );
		this.$tab_button = this._get_tab_button();
		this.locked = true;
		this.loaded = false;
		this.lock_key = `unlocked_tabs::${this.id}`;
		this.name = name;
		this.next_tab = null;
		this.page = page;
		this.previous_tab = null;

		this._maybe_unlock();

	}

	_check_args( $tab, name, page ) {
		let result = true;

		if ( 'undefined' === typeof $tab && '' === name ) {
			result = 'One of [$tab, name] required!';

		} else if ( 'undefined' === typeof page ) {
			result = 'page is required to create a new CnchiTab!';
		}

		return result;
	}

	_get_tab_button() {
		let selector = `[href\$="${this.name}"]`,
			$container = $( '.main_content' );

		return $container.find( '.navigation_buttons' ).find( selector ).parent();
	}

	_hide() {
		return this.$tab.fadeOut().promise();
	}

	_load_and_show() {
		return this.page.reload_element( `#${this.name}` ).then( this.$tab.fadeIn().promise() )
	}

	_maybe_unlock() {
		let unlocked = ( null !== localStorage.getItem( this.lock_key ) );

		if ( true === unlocked ) {
			this._unlock();
		}
	}

	_show() {
		let deferred;

		if ( this.page.tabs[0] === this || this.loaded ) {
			deferred = this.$tab.fadeIn().promise();
		} else {
			deferred = this._load_and_show();
		}

		return deferred;
	}

	_unlock() {
		this.$tab_button.removeClass( 'locked' );
		this.$tab_button.on( 'click', this.page.tab_button_clicked_cb );
		localStorage.setItem( this.lock_key, 'true' );
	}

	prepare( prepare_to ) {}
}

window.CnchiTab = CnchiTab;


/*
 * page.js
 *
 * Copyright 2016 Antergos
 *
 * This file is part of Cnchi.
 *
 * Cnchi is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Cnchi is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * The following additional terms are in effect as per Section 7 of the license:
 *
 * The preservation of all legal notices and author attributions in
 * the material or in the Appropriate Legal Notices displayed
 * by works containing it is required.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';


/**
 * Manages a page in the installation process. A page contains one or more tabs. When
 * a page contains only one tab, the page-level tab buttons will not be shown.
 *
 * @extends CnchiObject
 *
 * @prop {CnchiTab}   current_tab The tab that is currently visible on the page.
 * @prop {boolean}    has_tabs    Whether or not this page has mulitple tabs.
 * @prop {string[]}   signals     Names of signals used by the page to communicate with backend.
 * @prop {CnchiTab[]} tabs        This page's tabs. One tab is always implied (the page itself).
 *
 */
class CnchiPage extends CnchiObject {

	constructor( id ) {
		super();

		this.signals = [];
		this.tabs = [];
		this.current_tab = null;
		this.$page = $( '.main_content' );
		this.next_tab_animation_interval = null;

		this._initialize()
			.then( _ => this._set_current_tab( 0 ) )
			.catch( err => this.logger.error( err ) );
	}

	_initialize() {
		return Promise.all(
			[this._prepare_tabs(), this._register_event_handlers()]
		);
	}

	_assign_next_and_previous_tab_props() {
		for ( let [index, value] of this.tabs.entries() ) {
			value.previous_tab = ( index > 0 ) ? this.tabs[index - 1] : null;
			value.next_tab = ( index < (this.tabs.length - 1) ) ? this.tabs[index + 1] : null;
		}
	}

	_hide_tab( tab ) {
		return ( 'undefined' === typeof tab ) ? new Promise().resolve() : tab.hide();
	}

	/**
	 * Locates the page's tabs in the DOM and creates `CnchiTab` objects for them. Also ensures
	 * that `this.tabs`, `this.current_tab`, and `this.<tab_name>_tab`(s) are properly set.
	 */
	_prepare_tabs() {
		let $page_tabs = $( '.page_tab' );

		$page_tabs.each( ( index, element ) => {
			let tab_name = $( element ).attr( 'id' ),
				property_name = `${tab_name}_tab`;

			this[property_name] = new CnchiTab( $( element ), tab_name, this );

			this.tabs.push( this[property_name] );

			if ( index === ( $page_tabs.length - 1 ) ) {
				this._assign_next_and_previous_tab_props();
			}
		} );
	}

	_prepare_to_hide_tab( tab ) {
		return ( 'undefined' === typeof tab ) ? new Promise().resolve() : tab.prepare( 'hide' );
	}

	/**
	 * Adds this page's signals to {@link CnchiApp.signals} array.
	 */
	_register_allowed_signals() {
		for ( let signal of this.signals ) {
			cnchi.signals.push( signal );
		}
	}

	_prepare_to_show_tab( tab ) {
		if ( 'undefined' === typeof tab ) {
			tab = this.current_tab;
		}

		return tab.prepare( 'show' );
	}

	_register_event_handlers() {

	}

	/**
	 * Sets the current tab to the tab represented by `identifier`.
	 *
	 * @arg {string|number} identifier Either the tab name or index position in `this.tabs`.
	 */
	_set_current_tab( identifier ) {
		let tab;

		if ( Number.isInteger( identifier ) ) {
			tab = this.tabs[identifier];
		} else {
			tab = this.get_tab_by_name( identifier );
		}

		this._prepare_to_hide_tab()
			.then( Promise.all( [this._hide_tab(), this._prepare_to_show_tab( tab )] ) )
			.then( this._show_tab( tab ) )
			.catch( err => this.logger.error( err ) );
	}

	_show_tab( tab ) {
		return ( 'undefined' === typeof tab ) ? new Promise().resolve() : tab.show();
	}

	_unlock_next_tab_animated() {
		let $tab_button = this._get_next_tab_button();

		if ( $tab_button.hasClass( 'locked' ) ) {
			$tab_button.on( 'click', this.tab_button_clicked_cb ).removeClass( 'locked' );
		}

		$tab_button.animateCss( 'animated tada' );
	}

	change_current_tab_cb( event, id ) {
		console.log( 'change current tab fired!' );
		this.logger.debug( 'change current tab fired!' );
		clearInterval( this.next_tab_animation_interval );
		this.reload_element( `#${id}`, this.show_tab );
	}

	get_tab_by_name( tab_name ) {
		let property_name = `${tab_name}_tab`;
		return this[property_name];
	}

	/**
	 * Reloads a single element on the page. The result is the same as if the entire page
	 * had been reloaded, except only that single element will actually change.
	 *
	 * @arg {String}   selector A CSS selector that matches only one element on the page.
	 * @arg {Function} callback An optional callback to be called after element is reloaded.
	 */
	reload_element( selector ) {
		let deferred = $.Deferred(),
			url = `cnchi://${this.name}`,
			$old_el = this.$page.find( selector ),
			$new_el;

		$old_el.hide( 0 )
			.promise()
			.then( $.get( url ) )
			.then( ( data ) => {
				$new_el = $( data ).find( selector );
				console.log( $new_el );

				$old_el.replaceWith( $new_el );

				return $new_el.show( 0 ).promise()
			} )
			.done( () => {
				deferred.resolve()
			} );

		return deferred.promise();
	}

	tab_button_clicked_cb( event ) {
		let $target = $( event.currentTarget ),
			$tab_button = $target.closest( '.tab' );

		event.preventDefault();

		if ( $tab_button.hasClass( 'locked' ) ) {
			this.logger.warning(
				'Tab cannot be shown because it is locked!',
				this.tab_button_clicked_cb
			);
		}

		this._set_current_tab( event.data );
	}

	unlock_next_tab() {
		this._unlock_next_tab_animated();
		this.next_tab_animation_interval = setInterval( () => {
			this._unlock_next_tab_animated();
		}, 4000 );
	}
}

window.CnchiPage = CnchiPage;

//# sourceMappingURL=bundle.js.map