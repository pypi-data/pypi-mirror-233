(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[7856],{27856:function(a){!/*! @license DOMPurify 2.4.5 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/2.4.5/LICENSE */ function(b,c){a.exports=c()}(this,function(){"use strict";function a(b){return(a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(a){return typeof a}:function(a){return a&&"function"==typeof Symbol&&a.constructor===Symbol&&a!==Symbol.prototype?"symbol":typeof a})(b)}function b(a,c){return(b=Object.setPrototypeOf||function(a,b){return a.__proto__=b,a})(a,c)}function c(a,d,e){return(c=!function(){if("undefined"==typeof Reflect||!Reflect.construct||Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],function(){})),!0}catch(a){return!1}}()?function(a,c,d){var e=[null];e.push.apply(e,c);var f=new(Function.bind.apply(a,e));return d&&b(f,d.prototype),f}:Reflect.construct).apply(null,arguments)}function d(a){return e(a)||f(a)||g(a)||i()}function e(a){if(Array.isArray(a))return h(a)}function f(a){if("undefined"!=typeof Symbol&&null!=a[Symbol.iterator]||null!=a["@@iterator"])return Array.from(a)}function g(a,b){if(a){if("string"==typeof a)return h(a,b);var c=Object.prototype.toString.call(a).slice(8,-1);if("Object"===c&&a.constructor&&(c=a.constructor.name),"Map"===c||"Set"===c)return Array.from(a);if("Arguments"===c||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(c))return h(a,b)}}function h(a,b){(null==b||b>a.length)&&(b=a.length);for(var c=0,d=Array(b);c<b;c++)d[c]=a[c];return d}function i(){throw TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var j,k=Object.hasOwnProperty,l=Object.setPrototypeOf,m=Object.isFrozen,n=Object.getPrototypeOf,o=Object.getOwnPropertyDescriptor,p=Object.freeze,q=Object.seal,r=Object.create,s="undefined"!=typeof Reflect&&Reflect,t=s.apply,u=s.construct;t||(t=function(a,b,c){return a.apply(b,c)}),p||(p=function(a){return a}),q||(q=function(a){return a}),u||(u=function(a,b){return c(a,d(b))});var v=G(Array.prototype.forEach),w=G(Array.prototype.pop),x=G(Array.prototype.push),y=G(String.prototype.toLowerCase),z=G(String.prototype.toString),A=G(String.prototype.match),B=G(String.prototype.replace),C=G(String.prototype.indexOf),D=G(String.prototype.trim),E=G(RegExp.prototype.test),F=(j=TypeError,function(){for(var a=arguments.length,b=Array(a),c=0;c<a;c++)b[c]=arguments[c];return u(j,b)});function G(a){return function(b){for(var c=arguments.length,d=Array(c>1?c-1:0),e=1;e<c;e++)d[e-1]=arguments[e];return t(a,b,d)}}function H(a,b,c){c=c||y,l&&l(a,null);for(var d=b.length;d--;){var e=b[d];if("string"==typeof e){var f=c(e);f!==e&&(m(b)||(b[d]=f),e=f)}a[e]=!0}return a}function I(a){var b,c=r(null);for(b in a)!0===t(k,a,[b])&&(c[b]=a[b]);return c}function J(a,b){for(;null!==a;){var c=o(a,b);if(c){if(c.get)return G(c.get);if("function"==typeof c.value)return G(c.value)}a=n(a)}return function(a){return console.warn("fallback value for",a),null}}var K=p(["a","abbr","acronym","address","area","article","aside","audio","b","bdi","bdo","big","blink","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","content","data","datalist","dd","decorator","del","details","dfn","dialog","dir","div","dl","dt","element","em","fieldset","figcaption","figure","font","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","img","input","ins","kbd","label","legend","li","main","map","mark","marquee","menu","menuitem","meter","nav","nobr","ol","optgroup","option","output","p","picture","pre","progress","q","rp","rt","ruby","s","samp","section","select","shadow","small","source","spacer","span","strike","strong","style","sub","summary","sup","table","tbody","td","template","textarea","tfoot","th","thead","time","tr","track","tt","u","ul","var","video","wbr"]),L=p(["svg","a","altglyph","altglyphdef","altglyphitem","animatecolor","animatemotion","animatetransform","circle","clippath","defs","desc","ellipse","filter","font","g","glyph","glyphref","hkern","image","line","lineargradient","marker","mask","metadata","mpath","path","pattern","polygon","polyline","radialgradient","rect","stop","style","switch","symbol","text","textpath","title","tref","tspan","view","vkern"]),M=p(["feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence"]),N=p(["animate","color-profile","cursor","discard","fedropshadow","font-face","font-face-format","font-face-name","font-face-src","font-face-uri","foreignobject","hatch","hatchpath","mesh","meshgradient","meshpatch","meshrow","missing-glyph","script","set","solidcolor","unknown","use"]),O=p(["math","menclose","merror","mfenced","mfrac","mglyph","mi","mlabeledtr","mmultiscripts","mn","mo","mover","mpadded","mphantom","mroot","mrow","ms","mspace","msqrt","mstyle","msub","msup","msubsup","mtable","mtd","mtext","mtr","munder","munderover"]),P=p(["maction","maligngroup","malignmark","mlongdiv","mscarries","mscarry","msgroup","mstack","msline","msrow","semantics","annotation","annotation-xml","mprescripts","none"]),Q=p(["#text"]),R=p(["accept","action","align","alt","autocapitalize","autocomplete","autopictureinpicture","autoplay","background","bgcolor","border","capture","cellpadding","cellspacing","checked","cite","class","clear","color","cols","colspan","controls","controlslist","coords","crossorigin","datetime","decoding","default","dir","disabled","disablepictureinpicture","disableremoteplayback","download","draggable","enctype","enterkeyhint","face","for","headers","height","hidden","high","href","hreflang","id","inputmode","integrity","ismap","kind","label","lang","list","loading","loop","low","max","maxlength","media","method","min","minlength","multiple","muted","name","nonce","noshade","novalidate","nowrap","open","optimum","pattern","placeholder","playsinline","poster","preload","pubdate","radiogroup","readonly","rel","required","rev","reversed","role","rows","rowspan","spellcheck","scope","selected","shape","size","sizes","span","srclang","start","src","srcset","step","style","summary","tabindex","title","translate","type","usemap","valign","value","width","xmlns","slot"]),S=p(["accent-height","accumulate","additive","alignment-baseline","ascent","attributename","attributetype","azimuth","basefrequency","baseline-shift","begin","bias","by","class","clip","clippathunits","clip-path","clip-rule","color","color-interpolation","color-interpolation-filters","color-profile","color-rendering","cx","cy","d","dx","dy","diffuseconstant","direction","display","divisor","dur","edgemode","elevation","end","fill","fill-opacity","fill-rule","filter","filterunits","flood-color","flood-opacity","font-family","font-size","font-size-adjust","font-stretch","font-style","font-variant","font-weight","fx","fy","g1","g2","glyph-name","glyphref","gradientunits","gradienttransform","height","href","id","image-rendering","in","in2","k","k1","k2","k3","k4","kerning","keypoints","keysplines","keytimes","lang","lengthadjust","letter-spacing","kernelmatrix","kernelunitlength","lighting-color","local","marker-end","marker-mid","marker-start","markerheight","markerunits","markerwidth","maskcontentunits","maskunits","max","mask","media","method","mode","min","name","numoctaves","offset","operator","opacity","order","orient","orientation","origin","overflow","paint-order","path","pathlength","patterncontentunits","patterntransform","patternunits","points","preservealpha","preserveaspectratio","primitiveunits","r","rx","ry","radius","refx","refy","repeatcount","repeatdur","restart","result","rotate","scale","seed","shape-rendering","specularconstant","specularexponent","spreadmethod","startoffset","stddeviation","stitchtiles","stop-color","stop-opacity","stroke-dasharray","stroke-dashoffset","stroke-linecap","stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke","stroke-width","style","surfacescale","systemlanguage","tabindex","targetx","targety","transform","transform-origin","text-anchor","text-decoration","text-rendering","textlength","type","u1","u2","unicode","values","viewbox","visibility","version","vert-adv-y","vert-origin-x","vert-origin-y","width","word-spacing","wrap","writing-mode","xchannelselector","ychannelselector","x","x1","x2","xmlns","y","y1","y2","z","zoomandpan"]),T=p(["accent","accentunder","align","bevelled","close","columnsalign","columnlines","columnspan","denomalign","depth","dir","display","displaystyle","encoding","fence","frame","height","href","id","largeop","length","linethickness","lspace","lquote","mathbackground","mathcolor","mathsize","mathvariant","maxsize","minsize","movablelimits","notation","numalign","open","rowalign","rowlines","rowspacing","rowspan","rspace","rquote","scriptlevel","scriptminsize","scriptsizemultiplier","selection","separator","separators","stretchy","subscriptshift","supscriptshift","symmetric","voffset","width","xmlns"]),U=p(["xlink:href","xml:id","xlink:title","xml:space","xmlns:xlink"]),V=q(/\{\{[\w\W]*|[\w\W]*\}\}/gm),W=q(/<%[\w\W]*|[\w\W]*%>/gm),X=q(/\${[\w\W]*}/gm),Y=q(/^data-[\-\w.\u00B7-\uFFFF]/),Z=q(/^aria-[\-\w]+$/),$=q(/^(?:(?:(?:f|ht)tps?|mailto|tel|callto|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i),_=q(/^(?:\w+script|data):/i),aa=q(/[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g),ab=q(/^html$/i),ac=function(b,c){if("object"!==a(b)||"function"!=typeof b.createPolicy)return null;var d=null,e="data-tt-policy-suffix";c.currentScript&&c.currentScript.hasAttribute(e)&&(d=c.currentScript.getAttribute(e));var f="dompurify"+(d?"#"+d:"");try{return b.createPolicy(f,{createHTML:function(a){return a},createScriptURL:function(a){return a}})}catch(g){return console.warn("TrustedTypes policy "+f+" could not be created."),null}};function ad(){var b,c,e=arguments.length>0&& void 0!==arguments[0]?arguments[0]:"undefined"==typeof window?null:window,f=function(a){return ad(a)};if(f.version="2.4.5",f.removed=[],!e||!e.document||9!==e.document.nodeType)return f.isSupported=!1,f;var g=e.document,h=e.document,i=e.DocumentFragment,j=e.HTMLTemplateElement,k=e.Node,l=e.Element,m=e.NodeFilter,n=e.NamedNodeMap,o=void 0===n?e.NamedNodeMap||e.MozNamedAttrMap:n,q=e.HTMLFormElement,r=e.DOMParser,s=e.trustedTypes,t=l.prototype,u=J(t,"cloneNode"),G=J(t,"nextSibling"),ae=J(t,"childNodes"),af=J(t,"parentNode");if("function"==typeof j){var ag=h.createElement("template");ag.content&&ag.content.ownerDocument&&(h=ag.content.ownerDocument)}var ah=ac(s,g),ai=ah?ah.createHTML(""):"",aj=h,ak=aj.implementation,al=aj.createNodeIterator,am=aj.createDocumentFragment,an=aj.getElementsByTagName,ao=g.importNode,ap={};try{ap=I(h).documentMode?h.documentMode:{}}catch(aq){}var ar={};f.isSupported="function"==typeof af&&ak&& void 0!==ak.createHTMLDocument&&9!==ap;var as=V,at=W,au=X,av=Y,aw=Z,ax=_,ay=aa,az=$,aA=null,aB=H({},[].concat(d(K),d(L),d(M),d(O),d(Q))),aC=null,aD=H({},[].concat(d(R),d(S),d(T),d(U))),aE=Object.seal(Object.create(null,{tagNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},attributeNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},allowCustomizedBuiltInElements:{writable:!0,configurable:!1,enumerable:!0,value:!1}})),aF=null,aG=null,aH=!0,aI=!0,aJ=!1,aK=!0,aL=!1,aM=!1,aN=!1,aO=!1,aP=!1,aQ=!1,aR=!1,aS=!0,aT=!1,aU=!0,aV=!1,aW={},aX=null,aY=H({},["annotation-xml","audio","colgroup","desc","foreignobject","head","iframe","math","mi","mn","mo","ms","mtext","noembed","noframes","noscript","plaintext","script","style","svg","template","thead","title","video","xmp"]),aZ=null,a$=H({},["audio","video","img","source","image","track"]),a_=null,a0=H({},["alt","class","for","id","label","name","pattern","placeholder","role","summary","title","value","style","xmlns"]),a1="http://www.w3.org/1998/Math/MathML",a2="http://www.w3.org/2000/svg",a3="http://www.w3.org/1999/xhtml",a4=a3,a5=!1,a6=null,a7=H({},[a1,a2,a3],z),a8=["application/xhtml+xml","text/html"],a9=null,ba=h.createElement("form"),bb=function(a){return a instanceof RegExp||a instanceof Function},bc=function(e){(!a9||a9!==e)&&(e&&"object"===a(e)||(e={}),e=I(e),c="application/xhtml+xml"===(b=b=-1===a8.indexOf(e.PARSER_MEDIA_TYPE)?"text/html":e.PARSER_MEDIA_TYPE)?z:y,aA="ALLOWED_TAGS"in e?H({},e.ALLOWED_TAGS,c):aB,aC="ALLOWED_ATTR"in e?H({},e.ALLOWED_ATTR,c):aD,a6="ALLOWED_NAMESPACES"in e?H({},e.ALLOWED_NAMESPACES,z):a7,a_="ADD_URI_SAFE_ATTR"in e?H(I(a0),e.ADD_URI_SAFE_ATTR,c):a0,aZ="ADD_DATA_URI_TAGS"in e?H(I(a$),e.ADD_DATA_URI_TAGS,c):a$,aX="FORBID_CONTENTS"in e?H({},e.FORBID_CONTENTS,c):aY,aF="FORBID_TAGS"in e?H({},e.FORBID_TAGS,c):{},aG="FORBID_ATTR"in e?H({},e.FORBID_ATTR,c):{},aW="USE_PROFILES"in e&&e.USE_PROFILES,aH=!1!==e.ALLOW_ARIA_ATTR,aI=!1!==e.ALLOW_DATA_ATTR,aJ=e.ALLOW_UNKNOWN_PROTOCOLS||!1,aK=!1!==e.ALLOW_SELF_CLOSE_IN_ATTR,aL=e.SAFE_FOR_TEMPLATES||!1,aM=e.WHOLE_DOCUMENT||!1,aP=e.RETURN_DOM||!1,aQ=e.RETURN_DOM_FRAGMENT||!1,aR=e.RETURN_TRUSTED_TYPE||!1,aO=e.FORCE_BODY||!1,aS=!1!==e.SANITIZE_DOM,aT=e.SANITIZE_NAMED_PROPS||!1,aU=!1!==e.KEEP_CONTENT,aV=e.IN_PLACE||!1,az=e.ALLOWED_URI_REGEXP||az,a4=e.NAMESPACE||a3,aE=e.CUSTOM_ELEMENT_HANDLING||{},e.CUSTOM_ELEMENT_HANDLING&&bb(e.CUSTOM_ELEMENT_HANDLING.tagNameCheck)&&(aE.tagNameCheck=e.CUSTOM_ELEMENT_HANDLING.tagNameCheck),e.CUSTOM_ELEMENT_HANDLING&&bb(e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck)&&(aE.attributeNameCheck=e.CUSTOM_ELEMENT_HANDLING.attributeNameCheck),e.CUSTOM_ELEMENT_HANDLING&&"boolean"==typeof e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements&&(aE.allowCustomizedBuiltInElements=e.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements),aL&&(aI=!1),aQ&&(aP=!0),aW&&(aA=H({},d(Q)),aC=[],!0===aW.html&&(H(aA,K),H(aC,R)),!0===aW.svg&&(H(aA,L),H(aC,S),H(aC,U)),!0===aW.svgFilters&&(H(aA,M),H(aC,S),H(aC,U)),!0===aW.mathMl&&(H(aA,O),H(aC,T),H(aC,U))),e.ADD_TAGS&&(aA===aB&&(aA=I(aA)),H(aA,e.ADD_TAGS,c)),e.ADD_ATTR&&(aC===aD&&(aC=I(aC)),H(aC,e.ADD_ATTR,c)),e.ADD_URI_SAFE_ATTR&&H(a_,e.ADD_URI_SAFE_ATTR,c),e.FORBID_CONTENTS&&(aX===aY&&(aX=I(aX)),H(aX,e.FORBID_CONTENTS,c)),aU&&(aA["#text"]=!0),aM&&H(aA,["html","head","body"]),aA.table&&(H(aA,["tbody"]),delete aF.tbody),p&&p(e),a9=e)},bd=H({},["mi","mo","mn","ms","mtext"]),be=H({},["foreignobject","desc","title","annotation-xml"]),bf=H({},["title","style","font","a","script"]),bg=H({},L);H(bg,M),H(bg,N);var bh=H({},O);H(bh,P);var bi=function(a){var c=af(a);c&&c.tagName||(c={namespaceURI:a4,tagName:"template"});var d=y(a.tagName),e=y(c.tagName);return!!a6[a.namespaceURI]&&(a.namespaceURI===a2?c.namespaceURI===a3?"svg"===d:c.namespaceURI===a1?"svg"===d&&("annotation-xml"===e||bd[e]):Boolean(bg[d]):a.namespaceURI===a1?c.namespaceURI===a3?"math"===d:c.namespaceURI===a2?"math"===d&&be[e]:Boolean(bh[d]):a.namespaceURI===a3?(c.namespaceURI!==a2||!!be[e])&&(c.namespaceURI!==a1||!!bd[e])&&!bh[d]&&(bf[d]||!bg[d]):"application/xhtml+xml"===b&&!!a6[a.namespaceURI])},bj=function(a){x(f.removed,{element:a});try{a.parentNode.removeChild(a)}catch(b){try{a.outerHTML=ai}catch(c){a.remove()}}},bk=function(a,b){try{x(f.removed,{attribute:b.getAttributeNode(a),from:b})}catch(c){x(f.removed,{attribute:null,from:b})}if(b.removeAttribute(a),"is"===a&&!aC[a]){if(aP||aQ)try{bj(b)}catch(d){}else try{b.setAttribute(a,"")}catch(e){}}},bl=function(a){if(aO)a="<remove></remove>"+a;else{var c,d,e=A(a,/^[\r\n\t ]+/);d=e&&e[0]}"application/xhtml+xml"===b&&a4===a3&&(a='<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>'+a+"</body></html>");var f=ah?ah.createHTML(a):a;if(a4===a3)try{c=new r().parseFromString(f,b)}catch(g){}if(!c||!c.documentElement){c=ak.createDocument(a4,"template",null);try{c.documentElement.innerHTML=a5?ai:f}catch(i){}}var j=c.body||c.documentElement;return(a&&d&&j.insertBefore(h.createTextNode(d),j.childNodes[0]||null),a4===a3)?an.call(c,aM?"html":"body")[0]:aM?c.documentElement:j},bm=function(a){return al.call(a.ownerDocument||a,a,m.SHOW_ELEMENT|m.SHOW_COMMENT|m.SHOW_TEXT,null,!1)},bn=function(b){return"object"===a(k)?b instanceof k:b&&"object"===a(b)&&"number"==typeof b.nodeType&&"string"==typeof b.nodeName},bo=function(a,b,c){ar[a]&&v(ar[a],function(a){a.call(f,b,c,a9)})},bp=function(a){if(bo("beforeSanitizeElements",a,null),(b=a)instanceof q&&("string"!=typeof b.nodeName||"string"!=typeof b.textContent||"function"!=typeof b.removeChild||!(b.attributes instanceof o)||"function"!=typeof b.removeAttribute||"function"!=typeof b.setAttribute||"string"!=typeof b.namespaceURI||"function"!=typeof b.insertBefore||"function"!=typeof b.hasChildNodes)||E(/[\u0080-\uFFFF]/,a.nodeName))return bj(a),!0;var b,d,e=c(a.nodeName);if(bo("uponSanitizeElement",a,{tagName:e,allowedTags:aA}),a.hasChildNodes()&&!bn(a.firstElementChild)&&(!bn(a.content)||!bn(a.content.firstElementChild))&&E(/<[/\w]/g,a.innerHTML)&&E(/<[/\w]/g,a.textContent)||"select"===e&&E(/<template/i,a.innerHTML))return bj(a),!0;if(!aA[e]||aF[e]){if(!aF[e]&&br(e)&&(aE.tagNameCheck instanceof RegExp&&E(aE.tagNameCheck,e)||aE.tagNameCheck instanceof Function&&aE.tagNameCheck(e)))return!1;if(aU&&!aX[e]){var g=af(a)||a.parentNode,h=ae(a)||a.childNodes;if(h&&g)for(var i=h.length,j=i-1;j>=0;--j)g.insertBefore(u(h[j],!0),G(a))}return bj(a),!0}return a instanceof l&&!bi(a)||("noscript"===e||"noembed"===e)&&E(/<\/no(script|embed)/i,a.innerHTML)?(bj(a),!0):(aL&&3===a.nodeType&&(d=B(d=a.textContent,as," "),d=B(d,at," "),d=B(d,au," "),a.textContent!==d&&(x(f.removed,{element:a.cloneNode()}),a.textContent=d)),bo("afterSanitizeElements",a,null),!1)},bq=function(a,b,c){if(aS&&("id"===b||"name"===b)&&(c in h||c in ba))return!1;if(aI&&!aG[b]&&E(av,b));else if(aH&&E(aw,b));else if(!aC[b]||aG[b]){if(!(br(a)&&(aE.tagNameCheck instanceof RegExp&&E(aE.tagNameCheck,a)||aE.tagNameCheck instanceof Function&&aE.tagNameCheck(a))&&(aE.attributeNameCheck instanceof RegExp&&E(aE.attributeNameCheck,b)||aE.attributeNameCheck instanceof Function&&aE.attributeNameCheck(b))||"is"===b&&aE.allowCustomizedBuiltInElements&&(aE.tagNameCheck instanceof RegExp&&E(aE.tagNameCheck,c)||aE.tagNameCheck instanceof Function&&aE.tagNameCheck(c))))return!1}else if(a_[b]);else if(E(az,B(c,ay,"")));else if(("src"===b||"xlink:href"===b||"href"===b)&&"script"!==a&&0===C(c,"data:")&&aZ[a]);else if(aJ&&!E(ax,B(c,ay,"")));else if(c)return!1;return!0},br=function(a){return a.indexOf("-")>0},bs=function(b){bo("beforeSanitizeAttributes",b,null);var d,e,g,h,i=b.attributes;if(i){var j={attrName:"",attrValue:"",keepAttr:!0,allowedAttributes:aC};for(h=i.length;h--;){var k=d=i[h],l=k.name,m=k.namespaceURI;if(e="value"===l?d.value:D(d.value),g=c(l),j.attrName=g,j.attrValue=e,j.keepAttr=!0,j.forceKeepAttr=void 0,bo("uponSanitizeAttribute",b,j),e=j.attrValue,!j.forceKeepAttr&&(bk(l,b),j.keepAttr)){if(!aK&&E(/\/>/i,e)){bk(l,b);continue}aL&&(e=B(e,as," "),e=B(e,at," "),e=B(e,au," "));var n=c(b.nodeName);if(bq(n,g,e)){if(aT&&("id"===g||"name"===g)&&(bk(l,b),e="user-content-"+e),ah&&"object"===a(s)&&"function"==typeof s.getAttributeType){if(m);else switch(s.getAttributeType(n,g)){case"TrustedHTML":e=ah.createHTML(e);break;case"TrustedScriptURL":e=ah.createScriptURL(e)}}try{m?b.setAttributeNS(m,l,e):b.setAttribute(l,e),w(f.removed)}catch(o){}}}}bo("afterSanitizeAttributes",b,null)}},bt=function a(b){var c,d=bm(b);for(bo("beforeSanitizeShadowDOM",b,null);c=d.nextNode();)bo("uponSanitizeShadowNode",c,null),!bp(c)&&(c.content instanceof i&&a(c.content),bs(c));bo("afterSanitizeShadowDOM",b,null)};return f.sanitize=function(b){var d,h,j,l,m,n=arguments.length>1&& void 0!==arguments[1]?arguments[1]:{};if((a5=!b)&&(b="<!-->"),"string"!=typeof b&&!bn(b)){if("function"!=typeof b.toString)throw F("toString is not a function");if("string"!=typeof(b=b.toString()))throw F("dirty is not a string, aborting")}if(!f.isSupported){if("object"===a(e.toStaticHTML)||"function"==typeof e.toStaticHTML){if("string"==typeof b)return e.toStaticHTML(b);if(bn(b))return e.toStaticHTML(b.outerHTML)}return b}if(aN||bc(n),f.removed=[],"string"==typeof b&&(aV=!1),aV){if(b.nodeName){var o=c(b.nodeName);if(!aA[o]||aF[o])throw F("root node is forbidden and cannot be sanitized in-place")}}else if(b instanceof k)1===(h=(d=bl("<!---->")).ownerDocument.importNode(b,!0)).nodeType&&"BODY"===h.nodeName?d=h:"HTML"===h.nodeName?d=h:d.appendChild(h);else{if(!aP&&!aL&&!aM&& -1===b.indexOf("<"))return ah&&aR?ah.createHTML(b):b;if(!(d=bl(b)))return aP?null:aR?ai:""}d&&aO&&bj(d.firstChild);for(var p=bm(aV?b:d);j=p.nextNode();)!(3===j.nodeType&&j===l||bp(j))&&(j.content instanceof i&&bt(j.content),bs(j),l=j);if(l=null,aV)return b;if(aP){if(aQ)for(m=am.call(d.ownerDocument);d.firstChild;)m.appendChild(d.firstChild);else m=d;return(aC.shadowroot||aC.shadowrootmod)&&(m=ao.call(g,m,!0)),m}var q=aM?d.outerHTML:d.innerHTML;return aM&&aA["!doctype"]&&d.ownerDocument&&d.ownerDocument.doctype&&d.ownerDocument.doctype.name&&E(ab,d.ownerDocument.doctype.name)&&(q="<!DOCTYPE "+d.ownerDocument.doctype.name+">\n"+q),aL&&(q=B(q,as," "),q=B(q,at," "),q=B(q,au," ")),ah&&aR?ah.createHTML(q):q},f.setConfig=function(a){bc(a),aN=!0},f.clearConfig=function(){a9=null,aN=!1},f.isValidAttribute=function(a,b,d){a9||bc({});var e=c(a),f=c(b);return bq(e,f,d)},f.addHook=function(a,b){"function"==typeof b&&(ar[a]=ar[a]||[],x(ar[a],b))},f.removeHook=function(a){if(ar[a])return w(ar[a])},f.removeHooks=function(a){ar[a]&&(ar[a]=[])},f.removeAllHooks=function(){ar={}},f}return ad()})}}])
//# sourceMappingURL=7856.afb48b20b078498e.js.map